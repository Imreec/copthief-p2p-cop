"""Seeded tie-break variance (M9-5) — the determinism kill.

The counted 30–90 replayed byte-identical games three times: signed starts +
brains whose tie-breaks never consumed their seed = an opponent replays a
proven kill script after game one. The fix is seed-CONSUMING tie resolution:
`tie_epsilon` for the cop (seeded choice among near-equal expectimax values,
0.0 = the shipped deterministic pin) and seeded exact-tie shuffling for the
doctrine evader. Reproducibility is kept: same (config, seed) = same game;
different sub-game seeds = different games.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.doctrine_evader import DoctrineEvaderBrain
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


def make_observation(board: Board, position: tuple[int, int], role: str) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role=role,
        step=5,
        barriers_used=0,
        max_barriers=14,
        max_moves=35,
    )


def cop_move(seed: int, tie_epsilon: float) -> str:
    """A symmetric hunt: cop at (3,3), belief certain at (0,0) — N and W tie."""
    board = make_board()
    belief = make_belief(board, (0, 0))
    brain = PoliceBrain(seed=seed, options={"tie_epsilon": tie_epsilon, "endgame_enabled": 0.0})
    return brain.pick_move(make_observation(board, (3, 3), "police"), belief)


def test_cop_default_stays_deterministic() -> None:
    """tie_epsilon 0.0 (shipped): every seed answers identically."""
    assert len({cop_move(seed, 0.0) for seed in range(10)}) == 1


def test_cop_tie_epsilon_varies_by_seed_within_the_tie_set() -> None:
    """tie_epsilon on: seeds split the near-equal set {N, W} — and never leave it."""
    moves = {cop_move(seed, 0.25) for seed in range(10)}
    assert len(moves) > 1
    assert moves <= {"N", "W"}


def test_evader_exact_ties_vary_by_seed() -> None:
    """Symmetric flight (cop far, all destinations tuple-equal): the seeded
    shuffle resolves the tie differently across sub-game seeds."""
    board = make_board()

    def move_for(seed: int) -> str:
        belief = make_belief(board, (0, 0))
        brain = DoctrineEvaderBrain(seed=seed)
        return brain.pick_move(make_observation(board, (3, 3), "thief"), belief)

    assert len({move_for(seed) for seed in range(12)}) > 1


def test_evader_same_seed_is_reproducible() -> None:
    """Same (config, seed) = the same decision — replay evidence stays valid."""
    board = make_board()

    def move_for() -> str:
        belief = make_belief(board, (0, 0))
        brain = DoctrineEvaderBrain(seed=11)
        return brain.pick_move(make_observation(board, (3, 3), "thief"), belief)

    assert move_for() == move_for()
