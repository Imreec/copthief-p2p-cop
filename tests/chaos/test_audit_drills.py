"""Chaos drills — audit surface (PLAN §10): tampered record, fabricated scent.

Rule 19 (tamper) is existential: one flipped field in a revealed record fails the
whole audit. The scent-physics rider (FR-11, D2) is evidence-grade by design:
a fabricated grid produces a LOUD event and changes nothing else (SQ3 stance).
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.audit_flow import build_audit
from copthief_core.peer.session import PeerSession
from copthief_core.peer.settlement import settle, validate_opponent_audit
from copthief_core.shared.config import load_all

CONSTITUTION, _SHIPPED, _LIMITS = load_all(Path("config"), counted=False)
PRIVATE = replace(_SHIPPED, police_class="random", thief_class="random")


def _short_game() -> tuple[PeerSession, PeerSession]:
    """A few honest turns, then both sessions forced to GAME_OVER for settlement."""
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=1)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=2)
    police.handle_negotiate(thief.negotiate_payload())
    thief.handle_negotiate(police.negotiate_payload())
    for turn in range(3):
        police.handle_receive_turn(thief.take_turn(now=float(turn)))
        thief.handle_receive_turn(police.take_turn(now=float(turn) + 0.5))
    for session in (police, thief):
        session.outcome = "thief_survival"
        while session.machine.state is not GameState.GAME_OVER:
            session.machine.advance(
                GameState.VERIFYING
                if session.machine.state is not GameState.VERIFYING
                else GameState.GAME_OVER
            )
    return police, thief


def test_drill_one_tampered_revealed_field_fails_the_whole_audit() -> None:
    police, thief = _short_game()
    audit = build_audit("thief", thief.records, "survival")
    audit["records"][1]["payload"]["move"] = "MOVE:N"  # history rewritten
    claim, problems = validate_opponent_audit(
        audit, survival_threshold=CONSTITUTION.movement.survival_threshold
    )
    assert claim == "survival"
    assert any("tamper" in p for p in problems)  # the SPECIFIC defense, named


def test_drill_fabricated_scent_grid_raises_the_evidence_event_and_nothing_else() -> None:
    police, thief = _short_game()
    # The thief's grids arrived doctored: overwrite what we archived (wire truth).
    for message in police.inbound:
        message.smell_grid.clear()
        message.smell_grid["0,6"] = 0.9  # a planted trail far from the real walk

    sent: list[dict[str, Any]] = []

    class _Answer:
        def exchange_audit(self, ours: dict[str, Any]) -> dict[str, Any]:
            sent.append(ours)
            return build_audit("thief", thief.records, "survival")

    emitted: list[dict[str, Any]] = []
    result = settle(police, _Answer(), emitted.append)  # type: ignore[arg-type]
    mismatch_events = [e for e in emitted if e.get("event") == "scent_physics_mismatch"]
    assert len(mismatch_events) == 1
    assert mismatch_events[0]["payload"]["mismatches"]  # loud, per-step evidence
    # Evidence-grade ONLY (SQ3): the audit verdict and result are untouched.
    assert result.audit_ok is True


def test_drill_honest_grids_raise_no_event() -> None:
    police, thief = _short_game()

    class _Answer:
        def exchange_audit(self, ours: dict[str, Any]) -> dict[str, Any]:
            return build_audit("thief", thief.records, "survival")

    emitted: list[dict[str, Any]] = []
    settle(police, _Answer(), emitted.append)  # type: ignore[arg-type]
    assert [e for e in emitted if e.get("event") == "scent_physics_mismatch"] == []
