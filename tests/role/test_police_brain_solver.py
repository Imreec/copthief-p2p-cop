"""PoliceBrain × the forcing solver (M9-1 integration) — ⚑ police repo.

The solver outranks the heuristic exactly when it has a proof; everything else
is unchanged. The counted-loss scenario is the pin: belief collapsed on the
camping corner thief, cop two diagonal steps away — the heuristic sees no
gainful wall (region shrink is capped flat) and would only shadow the corner,
the solver proves the two-wall seal and starts it.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board() -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0)


def make_belief(board: Board) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=(3, 3),
        center_intensity=0.9,
        decay=0.1,
        smell_trust=0.0,
        hint_trust=0.0,
    )


def make_observation(board: Board) -> Observation:
    return Observation(
        board=board,
        position=(5, 5),
        move_set=MOVE_SET,
        role="police",
        step=10,
        barriers_used=0,
        max_barriers=14,
        max_moves=35,
    )


def test_certain_corner_thief_triggers_the_forced_seal() -> None:
    """Belief certain at (6,6): the solver's depth-2 corner seal wins the turn."""
    board = make_board()
    belief = make_belief(board)
    belief.note_claim((6, 6))
    decision = PoliceBrain(seed=7).decide(make_observation(board), belief)
    assert decision.barrier == (5, 6)


def test_disabled_solver_restores_the_heuristic() -> None:
    """`endgame_enabled = 0` (the arena A/B toggle): no wall is offered here —
    the capped region makes surgery gainless, so the heuristic plays a move."""
    board = make_board()
    belief = make_belief(board)
    belief.note_claim((6, 6))
    brain = PoliceBrain(seed=7, options={"endgame_enabled": 0.0})
    decision = brain.decide(make_observation(board), belief)
    assert decision.barrier is None


def test_flat_belief_skips_the_solver() -> None:
    """A wide posterior fails the sharp-support gate: the heuristic decides."""
    board = make_board()
    belief = make_belief(board)
    for _ in range(6):  # spread the start mass far past the support-width gate
        belief.predict()
    decision = PoliceBrain(seed=7).decide(make_observation(board), belief)
    assert decision.move in MOVE_SET
