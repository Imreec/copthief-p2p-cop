"""PoliceBrain containment walling (M10) — walls become tempo, not just surgery.

The 08-10 friendly's odd games: belief argmax == the thief's true cell 35/35,
cop adjacent from ~step 7 — and ZERO of 42 barriers placed, three survivals.
Root cause measured in-repo: one wall in open center shrinks the reachable
region by exactly 1, so the surgery gain threshold (4.79) can never fire and
the forcing solver cannot prove a 5-action capture on an open board. Containment
invests sub-threshold walls deliberately — close, tracked, quota-reserved,
throttled — so the region shrinks until the solver CAN finish. Default OFF:
the shipped M9 decision stream is untouched until config arms it.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.brains import Observation
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")
ARMED = {"contain_enabled": 1.0, "tie_epsilon": 0.0}


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


def make_observation(
    board: Board, position: Coord, *, step: int = 10, barriers_used: int = 0, max_barriers: int = 14
) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="police",
        step=step,
        barriers_used=barriers_used,
        max_barriers=max_barriers,
        max_moves=35,
    )


def test_a_tracked_central_evader_draws_a_wall() -> None:
    """The g01 stalemate geometry: cop beside the loop, belief exact and central,
    surgery silent (shrink 1 < threshold) — containment walls anyway."""
    board = make_board()
    brain = PoliceBrain(seed=1, options=ARMED)
    decision = brain.decide(make_observation(board, (3, 2)), make_belief(board, (3, 4)))
    assert decision.barrier is not None


def test_off_by_default_the_m9_stream_is_untouched() -> None:
    """Without the knob the same geometry still yields the M9 chase move — the
    exact live failure, pinned so arming it is a deliberate config act."""
    board = make_board()
    brain = PoliceBrain(seed=1, options={"tie_epsilon": 0.0})
    decision = brain.decide(make_observation(board, (3, 2)), make_belief(board, (3, 4)))
    assert decision.barrier is None


def test_the_cooldown_spaces_wall_investments() -> None:
    """Two adjacent steps never both wall: the second decision inside the cooldown
    window chases instead (walling every turn donates unlimited tempo)."""
    board = make_board()
    brain = PoliceBrain(seed=1, options=ARMED)
    first = brain.decide(make_observation(board, (3, 2), step=10), make_belief(board, (3, 4)))
    assert first.barrier is not None
    board = board.with_barrier(first.barrier)
    second = brain.decide(
        make_observation(board, (3, 2), step=11, barriers_used=1), make_belief(board, (3, 4))
    )
    assert second.barrier is None


def test_the_endgame_reserve_is_never_invested() -> None:
    """Containment stops with `contain_reserve` walls still in quota — the solver's
    finishing walls (rules 46/47) must never find an empty magazine."""
    board = make_board()
    brain = PoliceBrain(seed=1, options=ARMED)
    decision = brain.decide(
        make_observation(board, (3, 2), barriers_used=12), make_belief(board, (3, 4))
    )
    assert decision.barrier is None


def test_a_far_target_is_chased_not_walled() -> None:
    """Beyond `contain_range` the wall is pure waste — the cop keeps closing."""
    board = make_board()
    brain = PoliceBrain(seed=1, options=ARMED)
    decision = brain.decide(make_observation(board, (0, 0)), make_belief(board, (5, 5)))
    assert decision.barrier is None
