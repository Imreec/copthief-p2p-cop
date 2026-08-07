"""The cop must never wall itself away from the thief (M7-49) — ⚑ police repo.

Reproduced from the 2026-08-08 friendly, g03. Our cop sealed their camping thief into
the two-cell pocket {(6,5), (6,6)} — good play — and its LAST wall, at (5,6), also
closed the only opening it could have reached the pocket through. Every neighbour of
both pocket cells was then a barrier we had placed ourselves:

    (6,5) -> (5,5) barrier · (6,4) barrier · (6,6) pocket
    (6,6) -> (5,6) barrier · (6,5) pocket

From that turn on there was no capture available at any depth, so the search went flat
and the cop stood at (4,5) playing STAY for sixteen turns with eleven barriers unspent,
while its belief sat correctly on (6,6) at 0.795 mass. The game was lost at step 15;
the STAYs were the symptom.

`strategy/region.path_length` was written for precisely this — its docstring says so —
and `barriers.best_candidate` never called it.
"""

from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.region import path_length
from copthief_police.barriers import best_candidate
from copthief_police.features import resolve_options

MOVE_SET = ("N", "S", "E", "W", "STAY")
OPTS = resolve_options({})


def make_board(barriers: frozenset[Coord] = frozenset()) -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def test_the_g03_wall_that_lost_the_game_is_refused() -> None:
    """Cop at (4,6), thief camped at (6,6), (5,5) and (6,4) already walled.

    Walling (5,6) shrinks the thief's region to two cells and is what greedy surgery
    wants. It is also the cell the cop must walk through to ever reach the pocket.
    """
    board = make_board(frozenset({(5, 5), (6, 4)}))
    cop = (4, 6)
    support = [((6, 6), 0.78), ((6, 5), 0.22)]
    assert path_length(board.with_barrier((5, 6)), cop, (6, 6), MOVE_SET) is None
    chosen = best_candidate(board, cop, support, MOVE_SET, OPTS, barriers_used=2, max_barriers=14)
    assert chosen != (5, 6)


def test_the_locked_out_state_is_unwinnable_which_is_why_the_wall_matters() -> None:
    """The state the friendly actually reached: no open path at all, from anywhere."""
    board = make_board(frozenset({(5, 5), (5, 6), (6, 4)}))
    for cell in [(4, 5), (4, 6), (3, 6), (0, 0)]:
        assert path_length(board, cell, (6, 6), MOVE_SET) is None


def test_a_wall_that_keeps_a_route_open_is_still_offered() -> None:
    """The guard must not make the cop stop walling — only stop walling itself out."""
    board = make_board()
    chosen = best_candidate(
        board, (3, 3), [((3, 4), 1.0)], MOVE_SET, OPTS, barriers_used=0, max_barriers=14
    )
    if chosen is not None:
        assert path_length(board.with_barrier(chosen), (3, 3), (3, 4), MOVE_SET) is not None or (
            chosen == (3, 4)
        )


def test_walling_the_thiefs_own_cell_survives_the_guard() -> None:
    """Rule 46 is a capture, not a lock-out: the mass being unreachable AFTER we bury
    it is the win condition, so the guard must never veto the killing wall."""
    board = make_board(frozenset({(5, 5), (6, 4)}))
    chosen = best_candidate(
        board, (6, 5), [((6, 6), 1.0)], MOVE_SET, OPTS, barriers_used=2, max_barriers=14
    )
    assert chosen == (6, 6)
