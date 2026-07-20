"""M7-7(4): replay must read the LIVE log shape, and must never pass vacuously.

A live peer log emits `peer_result` (peer/settlement) — `result` is the *local*
two-sided match event (peer/match). `replay_from_log` only ever read `result`, so every
real game — every friendly, every tunnel run, the mandatory README screenshot — rendered
`steps 0 / outcome unknown / game_uid ""` while the verdict underneath was computed
correctly. The live shape carries no `game_uid` in its result payload either: it is
established at the handshake, so the `negotiated` event is the source.

Rider (the more dangerous half): `verified = not problems` is TRUE when nothing was
checked, so a truncated or empty log printed "Verified OK". A replay that verified zero
records now says TAMPERED — fail-closed, like every other rule-19 surface.
"""

from __future__ import annotations

import json
from pathlib import Path

from copthief_core.peer.replay import (
    VERDICT_OK,
    VERDICT_TAMPERED,
    replay_from_log,
    verdict_for,
)

# The committed M5 friendly: our tuned cop captured the reference thief in 13 steps.
M5_FRIENDLY = Path("docs/evidence/m5-friendly-g3.jsonl")


def test_a_live_peer_log_populates_the_banner() -> None:
    summary = replay_from_log(M5_FRIENDLY)
    assert verdict_for(summary) == VERDICT_OK
    assert summary.steps == 13
    assert summary.outcome == "cop_capture"
    assert len(summary.game_uid) > 0  # from the handshake, not from the result payload


def test_the_live_game_uid_is_the_negotiated_one() -> None:
    events = [json.loads(line) for line in M5_FRIENDLY.read_text(encoding="utf-8").splitlines()]
    negotiated = next(e for e in events if e["event"] == "negotiated")
    assert replay_from_log(M5_FRIENDLY).game_uid == negotiated["game_uid"]


def test_the_verdict_still_rests_on_real_re_hashing() -> None:
    """The M5 evidence claim was always sound — the display was the bug. Pin the work
    the verdict actually did so a future 'fix' cannot hollow it out."""
    summary = replay_from_log(M5_FRIENDLY)
    assert summary.records_verified >= 1
    assert summary.problems == []
    assert set(summary.moves) == {"police", "thief"}


def test_an_empty_log_is_tampered_not_vacuously_verified(tmp_path: Path) -> None:
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    summary = replay_from_log(empty)
    assert summary.records_verified == 0
    assert verdict_for(summary) == VERDICT_TAMPERED


def test_a_log_truncated_before_the_audit_is_tampered(tmp_path: Path) -> None:
    """The aborted-game shape (kept fail-closed and disclosed): turns traveled, no
    record was ever revealed, so there is nothing to verify and nothing to trust."""
    lines = M5_FRIENDLY.read_text(encoding="utf-8").splitlines()
    kept = [
        line
        for line in lines
        if json.loads(line)["event"] not in ("audit", "audit_answer", "audit_received")
    ]
    truncated = tmp_path / "truncated.jsonl"
    truncated.write_text("\n".join(kept) + "\n", encoding="utf-8")
    summary = replay_from_log(truncated)
    assert summary.records_verified == 0
    assert verdict_for(summary) == VERDICT_TAMPERED
