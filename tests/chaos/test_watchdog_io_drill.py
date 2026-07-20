"""Chaos drill — M7-7(1): a blocking transport must not self-terminate a live loop.

This is the drill the real-tunnel kill run should have had. A scripted transport blocks
an outbound push for longer than the loop-liveness budget (the shape of a Cloudflare
edge dying mid-turn), and the armed watchdog must stay quiet while the loop is alive —
then still fire on a loop that is genuinely wedged. Both directions in keyless CI,
real threads, real time, scaled down.
"""

from __future__ import annotations

import threading
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from copthief_core.peer.p2p import run_peer_game
from copthief_core.peer.session import PeerSession
from copthief_core.peer.transport import PeerTransport, queue_pair
from copthief_core.peer.watchdog import Watchdog, watched
from copthief_core.shared.config import load_all

CONSTITUTION, _SHIPPED, _LIMITS = load_all(Path("config"), counted=False)
PRIVATE = replace(_SHIPPED, police_class="random", thief_class="random")


def make_watchdog(tmp_path: Path, *, loop: float, io: float) -> tuple[Watchdog, list[str]]:
    stalls: list[str] = []
    dog = Watchdog(
        timeout_sec=loop,
        io_timeout_sec=io,
        snapshot=lambda: {"role": "police"},
        persist_path=tmp_path / "state_police.json",
        on_stall=stalls.append,
    )
    return dog, stalls


class BlockingSend:
    """A transport whose FIRST outbound push hangs — the dead-edge shape."""

    def __init__(self, inner: PeerTransport, *, block_for: float) -> None:
        self._inner = inner
        self._block_for = block_for
        self.blocked = False

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401 - transparent proxy
        return getattr(self._inner, name)

    def send_turn(self, message: dict[str, Any]) -> None:
        if not self.blocked:
            self.blocked = True
            time.sleep(self._block_for)
        self._inner.send_turn(message)


def test_drill_a_blocked_outbound_call_never_fires_the_watchdog(tmp_path: Path) -> None:
    """The pre-series blocker, proven closed: an outbound push blocked for 3x the loop
    budget costs nothing, because the loop declared the wait and is demonstrably alive."""
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=5)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=6)
    police_transport, thief_transport = queue_pair(wait_timeout=10.0)
    dog, stalls = make_watchdog(tmp_path, loop=0.2, io=5.0)

    def opponent() -> None:
        run_peer_game(thief, thief_transport, turn_timeout=10.0, poll_interval=0.05)

    runner = threading.Thread(target=opponent, name="thief")
    runner.start()
    dog.beat()
    dog.start(poll_interval=0.02)
    try:
        result = run_peer_game(
            police,
            watched(BlockingSend(police_transport, block_for=0.6), dog),
            turn_timeout=10.0,
            poll_interval=0.05,
            heartbeat=lambda _event: dog.beat(),
        )
    finally:
        dog.stop()
    runner.join(timeout=20)
    assert dog.fired is False  # THE assertion: no self-termination
    assert stalls == []
    assert not (tmp_path / "state_police.json").exists()
    assert result.outcome in ("cop_capture", "thief_survival")  # and the game FINISHED


def test_drill_a_genuinely_dead_loop_still_persists_and_shuts_down(tmp_path: Path) -> None:
    """The other half of the DoD: the I/O window is a window, not an off switch."""
    dog, stalls = make_watchdog(tmp_path, loop=0.15, io=3.0)
    dog.start(poll_interval=0.02)
    try:
        dog.beat()
        deadline = time.time() + 3.0
        while not dog.fired and time.time() < deadline:
            time.sleep(0.02)  # no beats, no I/O window: a wedge
    finally:
        dog.stop()
    assert dog.fired is True
    assert len(stalls) == 1
    assert "loop stall" in stalls[0]
    assert (tmp_path / "state_police.json").exists()


def test_drill_a_transport_that_never_returns_still_fires(tmp_path: Path) -> None:
    """The backstop: a declared I/O wait that outlasts the I/O budget is a wedge too."""
    dog, stalls = make_watchdog(tmp_path, loop=0.1, io=0.3)
    dog.start(poll_interval=0.02)
    try:
        dog.beat()
        dog.enter_io()
        deadline = time.time() + 3.0
        while not dog.fired and time.time() < deadline:
            time.sleep(0.02)
    finally:
        dog.stop()
    assert dog.fired is True
    assert "transport stall" in stalls[0]
