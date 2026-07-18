"""PoliceBrain behavior pins (TODO M5-2; PRD_police_brain §5) — ⚑ police repo only.

Expectimax over the truncated belief + capture-commit + determinism. The brain reads
the belief through its public surface, proposes through the Decision seam, and every
knob arrives via options (data-table defaults, config overrides — AppFTable pattern).
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation, make_brain
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board(barriers: frozenset = frozenset()) -> Board:  # type: ignore[type-arg]
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def make_belief(board: Board, opponent_at: tuple[int, int]) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=opponent_at,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=4.0,
        hint_trust=1.0,
    )


def observation(
    board: Board,
    position: tuple[int, int],
    *,
    step: int = 1,
    barriers_used: int = 0,
    max_barriers: int = 14,
) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="police",
        step=step,
        barriers_used=barriers_used,
        max_barriers=max_barriers,
    )


def test_capture_commit_steps_onto_a_certain_adjacent_cell() -> None:
    board = make_board()
    belief = make_belief(board, (3, 4))  # certain: the thief is due east
    decision = PoliceBrain(seed=1).decide(observation(board, (3, 3)), belief)
    assert decision.barrier is None
    assert decision.move == "E"  # step onto the mass; the claim rides free (SQ2)


def test_closes_distance_toward_a_certain_far_target() -> None:
    board = make_board()
    belief = make_belief(board, (6, 6))
    decision = PoliceBrain(seed=1).decide(observation(board, (0, 0)), belief)
    assert decision.move in {"S", "E"}


def test_seals_a_pocket_entrance_instead_of_stepping() -> None:
    # The thief is believed deep in a one-wide pocket: row 6 sealed from row 5 except
    # the entrance at (5, 5) — walling the OPEN entrance cuts its whole region off.
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))  # far end of the pocket
    decision = PoliceBrain(seed=1).decide(
        observation(board, (4, 5), barriers_used=len(walls)), belief
    )
    assert decision.barrier == (5, 5)  # graph surgery: one wall seals the region


def test_never_walls_with_quota_spent() -> None:
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))
    decision = PoliceBrain(seed=1).decide(
        observation(board, (4, 5), barriers_used=14, max_barriers=14), belief
    )
    assert decision.barrier is None


def test_barrier_threshold_option_disables_surgery() -> None:
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))
    brain = PoliceBrain(seed=1, options={"barrier_gain_threshold": 1e9})
    decision = brain.decide(observation(board, (4, 5), barriers_used=len(walls)), belief)
    assert decision.barrier is None  # the config knob really governs the policy


def test_decisions_are_deterministic_and_always_legal() -> None:
    board = make_board(barriers=frozenset({(2, 3), (3, 2)}))
    belief = make_belief(board, (0, 6))
    for _ in range(2):
        first = PoliceBrain(seed=7).decide(observation(board, (3, 3)), belief)
        again = PoliceBrain(seed=7).decide(observation(board, (3, 3)), belief)
        assert first == again
    assert first.move in MOVE_SET


def test_factory_builds_the_dotted_spec() -> None:
    brain = make_brain("copthief_police.brain:PoliceBrain", seed=3)
    assert isinstance(brain, PoliceBrain)
