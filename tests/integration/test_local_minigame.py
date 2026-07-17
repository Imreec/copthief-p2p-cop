"""PLAN §13 M1 exit evidence (in-process half): full mini-game, sealing, self-audit pass.

Two symmetric peer loops play a complete mini-game through the in-process queue
transports — the reference's push/inbox convention (M2 F1) with zero network — ending in
survival, with both directions' audits re-hashed clean. The two-process localhost form of
the same run lives in tests/integration/test_p2p_live.py (excluded from keyless CI).
"""

from pathlib import Path

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.match import run_local_minigame

CONFIG_DIR = Path("config")


def test_full_minigame_over_queue_transports_self_audits_clean() -> None:
    result = run_local_minigame(CONFIG_DIR, police_seed=11, thief_seed=22)
    assert result.outcome == "thief_survival"
    assert result.audit_ok_police_side
    assert result.audit_ok_thief_side
    assert result.steps == result.survival_threshold  # the thief's survival turn count
    assert result.game_uid  # both peers derived the same shared id
    assert result.police_state is GameState.GAME_OVER
    assert result.thief_state is GameState.GAME_OVER
    assert result.scores == (result.survival_cop_points, result.survival_thief_points)


def test_minigame_is_reproducible_for_fixed_seeds() -> None:
    a = run_local_minigame(CONFIG_DIR, police_seed=7, thief_seed=13)
    b = run_local_minigame(CONFIG_DIR, police_seed=7, thief_seed=13)
    assert a.police_moves == b.police_moves
    assert a.thief_moves == b.thief_moves
