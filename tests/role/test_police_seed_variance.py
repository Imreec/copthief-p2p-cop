"""Cop-side seeded tie-break variance (M9-5) — ⚑ police repo.

Split out of the mirrored tests/unit/strategy/test_seed_variance.py: these two
pins import `copthief_police`, which exists only in this repo, and the mirror
carried that import into the thief repo's collection (the M9 sync surfaced it).
Role-package tests live in tests/role/, which stays per-repo — the M1-5 lesson,
relearned in the opposite direction.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board() -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0)


def make_belief(board: Board, cell: tuple[int, int]) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=cell,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=0.0,
        hint_trust=0.0,
    )


def cop_move(seed: int, tie_epsilon: float) -> str:
    """A symmetric hunt: cop at (3,3), belief certain at (0,0) — N and W tie."""
    board = make_board()
    belief = make_belief(board, (0, 0))
    brain = PoliceBrain(seed=seed, options={"tie_epsilon": tie_epsilon, "endgame_enabled": 0.0})
    observation = Observation(
        board=board,
        position=(3, 3),
        move_set=MOVE_SET,
        role="police",
        step=5,
        barriers_used=0,
        max_barriers=14,
        max_moves=35,
    )
    return brain.pick_move(observation, belief)


def test_cop_default_stays_deterministic() -> None:
    """tie_epsilon 0.0 (shipped): every seed answers identically."""
    assert len({cop_move(seed, 0.0) for seed in range(10)}) == 1


def test_cop_tie_epsilon_varies_by_seed_within_the_tie_set() -> None:
    """tie_epsilon on: seeds split the near-equal set {N, W} — and never leave it."""
    moves = {cop_move(seed, 0.25) for seed in range(10)}
    assert len(moves) > 1
    assert moves <= {"N", "W"}
