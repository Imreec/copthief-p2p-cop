"""DoctrineEvaderBrain cage-escape (M11-1) — flee the ENCLOSURE, not the cop.

The M10 exposure this closes: police-m10 converts doctrine-m10 32/32 by investing
sub-threshold walls at tempo. Every wall costs the cop its whole move, and the
correct counter is tempo punishment — relocate while the cop builds (the flight
cap LIFTS on observed wall-turns) — plus a k-wall pocket forecast so a cage is
priced while its gap still exists, not one wall before it closes.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.doctrine_evader import DoctrineEvaderBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")

ARMED = {
    "room_first": 1.0,
    "cage_escape": 1.0,
    "forecast_walls": 3.0,
    "forecast_wall_reach": 2.0,
    "tempo_window": 2.0,
    "tempo_cap": 12.0,
}


def make_board(barriers: frozenset[Coord] = frozenset()) -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def make_belief(board: Board, cop_cell: Coord) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=cop_cell,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=0.0,
        hint_trust=0.0,
    )


def make_observation(board: Board, position: Coord, *, step: int = 7) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="thief",
        step=step,
        barriers_used=0,
        max_barriers=14,
        max_moves=35,
    )


def test_cage_escape_off_leaves_the_m10_stream_unchanged() -> None:
    """The knobs default OFF: on the same geometry the armed-and-disarmed brain and
    the plain M10 brain pick the same move (champion-gate comparability)."""
    board = make_board(frozenset({(3, 5)}))
    m10 = DoctrineEvaderBrain(seed=3, options={"room_first": 1.0})
    off = DoctrineEvaderBrain(seed=3, options={**ARMED, "cage_escape": 0.0})
    obs, belief = make_observation(board, (3, 3)), make_belief(board, (3, 1))
    assert m10.pick_move(obs, belief) == off.pick_move(obs, make_belief(board, (3, 1)))


def test_an_observed_wall_turn_lifts_the_flight_cap() -> None:
    """Cop known at (3,1), us at (3,3): while the cop builds (barrier count grew
    between our observations) the tempo lift makes max-flight rule — E, the
    across-the-board relocation the floor would otherwise cap away."""
    brain = DoctrineEvaderBrain(seed=3, options=ARMED)
    before = make_board(frozenset({(3, 5)}))
    brain.pick_move(make_observation(before, (3, 3), step=1), make_belief(before, (3, 1)))
    after = make_board(frozenset({(3, 5), (2, 1)}))
    move = brain.pick_move(make_observation(after, (3, 3), step=2), make_belief(after, (3, 1)))
    assert move == "E"


def test_the_tempo_lift_expires_after_the_window() -> None:
    """Two turns after the wall-turn the floor rules again: the same geometry goes
    back to the room-first choice (N or S — the four-escape destinations)."""
    brain = DoctrineEvaderBrain(seed=3, options=ARMED)
    before = make_board(frozenset({(3, 5)}))
    brain.pick_move(make_observation(before, (3, 3), step=1), make_belief(before, (3, 1)))
    after = make_board(frozenset({(3, 5), (2, 1)}))
    brain.pick_move(make_observation(after, (3, 3), step=2), make_belief(after, (3, 1)))
    brain.pick_move(make_observation(after, (3, 3), step=3), make_belief(after, (3, 1)))
    move = brain.pick_move(make_observation(after, (3, 3), step=4), make_belief(after, (3, 1)))
    assert move in {"N", "S"}


def test_without_a_wall_turn_the_floor_still_rules() -> None:
    """Same geometry, no barrier growth: the armed brain keeps the room-first
    choice — the lift must key on observed wall investment, not on being hunted."""
    brain = DoctrineEvaderBrain(seed=3, options=ARMED)
    board = make_board(frozenset({(3, 5)}))
    brain.pick_move(make_observation(board, (3, 3), step=1), make_belief(board, (3, 1)))
    move = brain.pick_move(make_observation(board, (3, 3), step=2), make_belief(board, (3, 1)))
    assert move in {"N", "S"}


def test_the_k_wall_forecast_holds_the_closing_gap() -> None:
    """A four-wall cut down column 3 with the gap at rows 4-6 and the builder at
    (6,3): the west side is three walls from sealed. The one-wall room terms
    prefer W (more escapes today); the k-wall forecast prices the pocket and takes
    E onto the gap column — through it while it exists."""
    board = make_board(frozenset({(0, 3), (1, 3), (2, 3), (3, 3)}))
    obs, belief = make_observation(board, (4, 2)), make_belief(board, (6, 3))
    m10 = DoctrineEvaderBrain(seed=3, options={"room_first": 1.0})
    armed = DoctrineEvaderBrain(seed=3, options=ARMED)
    assert m10.pick_move(obs, belief) == "W"
    assert armed.pick_move(obs, make_belief(board, (6, 3))) == "E"
