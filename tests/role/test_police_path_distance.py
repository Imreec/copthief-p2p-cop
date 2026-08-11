"""PoliceBrain wall-aware leaf distance (M11-C1) — the nis-yar1 g01 stall fix.

The 2026-08-11 friendly, game 1: tracking perfect (argmax == their cell 35/35),
our cop at (2,4) with its OWN wall at (1,4) between it and their thief camped
at (0,4) — and it STOOD STILL for 19 turns with 11 walls unspent, conceding the
game. Root cause: the expectimax leaf prices distance as MANHATTAN, so the wall
created a local minimum (every move increases Manhattan distance to the mass)
the 2-ply horizon cannot see over; containment refused (BFS gap 4 > range 3)
and the solver had no proof. `path_distance` re-prices the leaf with the real
wall-aware path length. Default OFF: the shipped stream is untouched until
config arms it.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.brains import Observation
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")
ARMED = {
    "path_distance": 1.0,
    "contain_enabled": 1.0,
    "contain_range": 4.0,
    "tie_epsilon": 0.0,
}
G01_WALLS = frozenset({(6, 3), (4, 3), (1, 4)})  # our three g01 placements


def make_board(barriers: frozenset[Coord] = frozenset()) -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def make_belief(board: Board, thief_cell: Coord) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=thief_cell,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=0.0,
        hint_trust=0.0,
    )


def make_observation(board: Board, position: Coord) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="police",
        step=16,
        barriers_used=3,
        max_barriers=14,
        max_moves=35,
    )


def test_manhattan_leaf_stalls_in_the_g01_local_minimum() -> None:
    """The bug, pinned: with the wall between cop and mass, every move increases
    Manhattan distance, so the shipped leaf freezes the cop on STAY."""
    board = make_board(G01_WALLS)
    brain = PoliceBrain(seed=1, options={"contain_enabled": 1.0, "tie_epsilon": 0.0})
    decision = brain.decide(make_observation(board, (2, 4)), make_belief(board, (0, 4)))
    assert decision.barrier is None
    assert decision.move == "STAY"


def test_contain_range_four_resumes_conversion_on_the_camper() -> None:
    """The measured g01 cure: the stall held because containment refused at BFS
    gap 4 > contain_range 3 (and the frozen expectimax had nothing better than
    STAY). At range 4 the investment resumes — the board keeps shrinking toward
    the camper until the solver can finish, instead of a 19-turn mutual freeze."""
    board = make_board(G01_WALLS)
    brain = PoliceBrain(seed=1, options=ARMED)
    decision = brain.decide(make_observation(board, (2, 4)), make_belief(board, (0, 4)))
    assert decision.barrier is not None


def test_path_distance_matches_manhattan_on_an_open_board() -> None:
    """On a wall-free board the geodesic IS Manhattan, so arming the knob must
    not change the open-board decision stream (champion comparability)."""
    board = make_board()
    plain = PoliceBrain(seed=1, options={"tie_epsilon": 0.0})
    armed = PoliceBrain(seed=1, options={"path_distance": 1.0, "tie_epsilon": 0.0})
    obs, belief = make_observation(board, (3, 2)), make_belief(board, (3, 5))
    assert plain.decide(obs, belief).move == armed.decide(obs, make_belief(board, (3, 5))).move
