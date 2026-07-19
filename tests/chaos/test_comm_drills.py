"""Chaos drills — communication surface (PLAN §10): dead peer, deadline edge.

The deadline defense is binary: a silent opponent past `turn_timeout` costs a
TECHNICAL_LOSS (timeout outcome, loud transition), while a slow-but-alive
opponent inside the budget costs NOTHING (no false technical loss).
"""

from __future__ import annotations

import threading
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.p2p import run_peer_game
from copthief_core.peer.session import PeerSession
from copthief_core.peer.transport import queue_pair
from copthief_core.shared.config import load_all

CONSTITUTION, _SHIPPED, _LIMITS = load_all(Path("config"), counted=False)
PRIVATE = replace(_SHIPPED, police_class="random", thief_class="random")


def test_drill_dead_peer_mid_game_is_a_clean_timeout_technical_loss() -> None:
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=1)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=2)
    police_transport, thief_transport = queue_pair(wait_timeout=2.0)
    events: list[dict[str, Any]] = []

    def dead_thief() -> None:
        # The thief handshakes, sends its first turn... then the tunnel "dies".
        theirs = thief_transport.exchange_agreement(thief.negotiate_payload())
        assert theirs is not None
        thief.handle_negotiate(theirs)
        thief_transport.send_turn(thief.take_turn(now=time.time()))
        # silence forever

    runner = threading.Thread(target=dead_thief, name="dead-thief")
    runner.start()
    result = run_peer_game(
        police,
        police_transport,
        turn_timeout=0.6,
        poll_interval=0.05,
        log=events.append,
    )
    runner.join(timeout=5)
    assert result.outcome == "timeout"
    assert police.machine.state is GameState.TECHNICAL_LOSS
    triggers = [
        e["payload"]["trigger"]
        for e in events
        if e.get("event") == "transition" and e["payload"]["to"] == "technical_loss"
    ]
    assert any("deadline" in t for t in triggers)  # the SPECIFIC defense, named


def test_drill_delay_to_the_deadline_edge_never_costs_a_false_loss() -> None:
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=3)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=3)
    police_transport, thief_transport = queue_pair(wait_timeout=5.0)

    class SlowFirstSend:
        """The thief's first turn arrives late — but inside the budget."""

        def __init__(self) -> None:
            self.delayed = False

        def __getattr__(self, name: str) -> Any:  # noqa: ANN401 - transparent proxy
            return getattr(thief_transport, name)

        def send_turn(self, message: dict[str, Any]) -> None:
            if not self.delayed:
                self.delayed = True
                time.sleep(0.4)  # edge of a 2.0s budget: slow, not dead
            thief_transport.send_turn(message)

    def slow_thief() -> None:
        run_peer_game(
            thief,
            SlowFirstSend(),
            turn_timeout=5.0,
            poll_interval=0.05,
        )

    runner = threading.Thread(target=slow_thief, name="slow-thief")
    runner.start()
    result = run_peer_game(police, police_transport, turn_timeout=2.0, poll_interval=0.05)
    runner.join(timeout=10)
    assert result.outcome in ("cop_capture", "thief_survival")  # the game FINISHED
    assert police.machine.state is GameState.GAME_OVER
