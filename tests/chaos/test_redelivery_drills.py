"""Chaos drills — at-least-once delivery (M7-8, PLAN §10): redelivery and reorder.

The threat both teams carry into the league: a push whose HTTP ack is lost is retried
and ARRIVES TWICE (our own M7-7 push fix retries to the full turn budget, so we are a
duplicate sender by design — the risk is symmetric). A receiver that calls a repeated
step a protocol violation turns a flaky tunnel into a technical loss for BOTH sides
(App E rule 35). These drills assert the transport-layer defenses fire — and that the
rules-layer wall behind them is untouched.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.session import PeerSession, ProtocolViolationError
from copthief_core.shared.config import load_all

CONSTITUTION, _SHIPPED, _LIMITS = load_all(Path("config"), counted=False)
PRIVATE = replace(_SHIPPED, police_class="random", thief_class="random")


def _pair() -> tuple[PeerSession, PeerSession]:
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=1)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=2)
    police.handle_negotiate(thief.negotiate_payload())
    thief.handle_negotiate(police.negotiate_payload())
    return police, thief


def test_drill_a_redelivered_turn_is_dropped_and_play_continues() -> None:
    """The lost-ack retry: identical bytes, twice. Nothing is processed twice."""
    police, thief = _pair()
    first = thief.take_turn(now=1.0)
    police.handle_receive_turn(first)
    belief_after_one = police.belief.probs()
    scent_after_one = police.known_field.snapshot()

    answer = police.handle_receive_turn(dict(first))  # the retry lands

    assert answer["disposition"] == "duplicate"
    assert police.machine.state is not GameState.TECHNICAL_LOSS
    assert len(police.inbound) == 1  # archived once
    assert police.belief.probs() == belief_after_one  # no second predict/update
    assert police.known_field.snapshot() == scent_after_one  # no second decay
    police.take_turn(now=2.0)  # play simply continues


def _thief_stream(count: int) -> list[dict]:
    """`count` consecutive honest thief turns, recorded off a real paired session."""
    police, thief = _pair()
    stream = []
    for step in range(1, count + 1):
        message = thief.take_turn(now=float(step))
        stream.append(message)
        police.handle_receive_turn(message)
        thief.handle_receive_turn(police.take_turn(now=step + 0.1))
    return stream


def test_drill_b_an_early_turn_is_buffered_then_released_in_order() -> None:
    """A retry can split a message pair across a flap, so a later step can land while
    an earlier one is still in flight: hold the early one, play the expected one, then
    replay what was held — bounded, in order, never refused."""
    first, second, third = _thief_stream(3)
    police, _ = _pair()
    police.handle_receive_turn(first)
    police.take_turn(now=1.1)

    held = police.handle_receive_turn(third)  # step 3 overtakes step 2

    assert held["disposition"] == "buffered"
    assert len(police.inbound) == 1  # not archived, not applied
    assert police.machine.state is not GameState.TECHNICAL_LOSS
    assert police.release_buffered() is None  # not due while step 2 is missing

    assert police.handle_receive_turn(second)["disposition"] == "accepted"
    due = police.release_buffered()
    assert due is not None
    police.take_turn(now=2.1)
    assert police.handle_receive_turn(due)["disposition"] == "accepted"
    assert [m.step for m in police.inbound] == [1, 2, 3]


def test_drill_c_equivocation_at_a_played_step_still_collapses() -> None:
    """Dedup is transport tolerance, NOT rules tolerance: a second, DIFFERENT commit
    for a step already played is the exact fraud the commit scheme exists to catch."""
    police, thief = _pair()
    first = thief.take_turn(now=1.0)
    police.handle_receive_turn(first)
    police.take_turn(now=1.1)
    forged = dict(first)
    forged["commit"] = "f" * 64  # same step, different sealed move

    with pytest.raises(ProtocolViolationError, match="discontinuity"):
        police.handle_receive_turn(forged)
    assert police.machine.state is GameState.TECHNICAL_LOSS


def test_drill_d_a_flood_of_early_turns_is_refused_at_the_window() -> None:
    """Bounded tolerance: an opponent that never sends the awaited step cannot make us
    hold an unbounded queue for it. The buffer window is the flood rule."""
    police, thief = _pair()
    first = thief.take_turn(now=1.0)
    police.handle_receive_turn(first)
    police.take_turn(now=1.1)
    limit = PRIVATE.inbound_buffer_limit
    expected = 2
    for offset in range(limit):  # the whole window fills, none of it refused
        early = dict(first)
        early["step"], early["commit"] = expected + 1 + offset, f"{offset:064d}"
        assert police.handle_receive_turn(early)["disposition"] == "buffered"

    flood = dict(first)
    flood["step"], flood["commit"] = expected + 1 + limit, "e" * 64
    with pytest.raises(ProtocolViolationError, match="window"):
        police.handle_receive_turn(flood)
    assert police.machine.state is GameState.TECHNICAL_LOSS
