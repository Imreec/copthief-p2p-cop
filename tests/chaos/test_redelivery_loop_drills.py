"""Chaos drills — at-least-once delivery at the LOOP level (M7-8, PLAN §10).

Two properties the session-level drills cannot show: (1) one clock per EXPECTED
message — redelivered junk never renews our turn deadline, so a stall attempt burns
the sender's budget and not ours; (2) a whole mini-game survives a tunnel that
duplicates every single push, in both directions, with the mutual audit still clean.
"""

from __future__ import annotations

import threading
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.p2p import PeerGameResult, run_peer_game
from copthief_core.peer.session import PeerSession
from copthief_core.peer.transport import queue_pair
from copthief_core.shared.config import load_all

CONSTITUTION, _SHIPPED, _LIMITS = load_all(Path("config"), counted=False)
PRIVATE = replace(_SHIPPED, police_class="random", thief_class="random")


class _StuckTunnel:
    """A tunnel that delivers ONE real turn, then redelivers it forever.

    The at-least-once pathology taken to its limit: every ack is lost, so the same
    bytes keep arriving. Our loop must accept the first copy and let the deadline run
    on the copies — the opponent owes us step 2 and never sends it.
    """

    def __init__(self, agreement: dict[str, Any], turn: dict[str, Any]) -> None:
        self._agreement = agreement
        self._turn = turn
        self.sent: list[dict[str, Any]] = []

    def exchange_agreement(self, signed: dict[str, Any]) -> dict[str, Any]:
        self.sent.append(signed)
        return self._agreement

    def send_turn(self, message: dict[str, Any]) -> None:
        self.sent.append(message)

    def poll_turn(self, timeout: float) -> dict[str, Any]:
        time.sleep(timeout)  # pace like a real inbox drain
        return dict(self._turn)

    def exchange_audit(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        self.sent.append(payload)
        return None


def test_drill_e_redelivered_junk_never_renews_our_turn_deadline() -> None:
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=2)
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=1)
    thief.handle_negotiate(police.negotiate_payload())
    tunnel = _StuckTunnel(thief.negotiate_payload(), thief.take_turn(now=1.0))
    events: list[dict[str, Any]] = []

    started = time.time()
    result = run_peer_game(police, tunnel, turn_timeout=0.6, poll_interval=0.05, log=events.append)
    elapsed = time.time() - started

    assert result.outcome == "timeout"
    assert police.machine.state is GameState.TECHNICAL_LOSS
    triggers = [
        e["payload"]["trigger"]
        for e in events
        if e.get("event") == "transition" and e["payload"]["to"] == "technical_loss"
    ]
    assert any("deadline" in t for t in triggers)  # lost by RULE, on our own clock
    assert elapsed < 3.0  # the duplicates did not keep the clock alive
    # The first copy was played (we replied once); every later copy was tolerated.
    assert len(police.inbound) == 1
    assert sum(1 for e in events if e.get("event") == "inbound_tolerated") >= 1


class _DuplicatingTunnel:
    """A transparent proxy that pushes every message TWICE (lost-ack retry, always)."""

    def __init__(self, inner: Any) -> None:  # noqa: ANN401 - PeerTransport Protocol
        self._inner = inner

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401 - transparent proxy
        return getattr(self._inner, name)

    def send_turn(self, message: dict[str, Any]) -> None:
        self._inner.send_turn(message)
        self._inner.send_turn(dict(message))


def test_drill_f_a_full_game_survives_a_tunnel_that_duplicates_every_push() -> None:
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=1)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=2)
    police_t, thief_t = queue_pair(wait_timeout=PRIVATE.connect_timeout_seconds)
    results: dict[str, PeerGameResult] = {}

    def play(session: PeerSession, transport: Any) -> None:  # noqa: ANN401 - Protocol
        results[session.role] = run_peer_game(
            session, _DuplicatingTunnel(transport), turn_timeout=10.0, poll_interval=0.02
        )

    threads = [
        threading.Thread(target=play, args=(police, police_t), name="police"),
        threading.Thread(target=play, args=(thief, thief_t), name="thief"),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)

    assert results["thief"].outcome == "thief_survival"
    assert results["police"].outcome == "thief_survival"
    assert results["police"].audit_ok
    assert results["thief"].audit_ok
    assert results["police"].problems == ()
    assert results["thief"].problems == ()
    assert results["police"].game_uid == results["thief"].game_uid != ""
