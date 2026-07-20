"""Cop-only pin of the M5 friendly's replay banner (M7-7(4); M8 README screenshot).

The mirrored `tests/integration/test_replay_live_shape.py` proves the banner is populated
for whatever live-peer log a repo carries; this one pins the COP's exact committed
numbers, so a regression in that specific evidence file is caught. It lives under
`tests/role/` (never mirrored) precisely because it names a role-specific file — the
portable-pin lesson (PR #29).
"""

from __future__ import annotations

from pathlib import Path

from copthief_core.peer.replay import VERDICT_OK, replay_from_log, verdict_for

M5_FRIENDLY = Path("docs/evidence/m5-friendly-g3.jsonl")


def test_the_m5_friendly_banner_is_exactly_as_committed() -> None:
    summary = replay_from_log(M5_FRIENDLY)
    assert verdict_for(summary) == VERDICT_OK
    assert summary.steps == 13
    assert summary.outcome == "cop_capture"
    assert summary.records_verified == 28  # 26 traveled turns + step-0 both sides, re-hashed
    assert set(summary.moves) == {"police", "thief"}
