"""The forcing endgame solver (M9-1) — ⚑ police repo.

Born from the 30–90 counted loss (g02/g04/g06): with the belief sharp on a camping
thief, the 2-ply expectimax proves "no catch in two plies" everywhere, the value
surface goes flat, and the cop STAYs for twenty turns. The solver is the missing
converter: when the belief support is small it searches for a single first action
that forces capture within a bounded horizon against EVERY support cell and every
thief reply — barriers inside the search (rule 46/47 capture forms included).
Anything unforced defers to the heuristic unchanged.
"""

from copthief_core.domain.board import Board, Coord
from copthief_police.endgame import forced_action, sharp_support
from copthief_police.features import resolve_options

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board(barriers: frozenset[Coord] = frozenset()) -> Board:
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def opts_with(**overrides: float) -> dict[str, float]:
    return resolve_options({k: float(v) for k, v in overrides.items()})


def test_depth_one_imprisonment_wall_is_found() -> None:
    """Thief certain at (6,6), (5,6) already walled, cop adjacent to (6,5):
    walling (6,5) imprisons immediately (rule 47) — the depth-1 forcing action."""
    board = make_board(frozenset({(5, 6)}))
    action = forced_action(
        board, (6, 4), [(6, 6)], MOVE_SET, opts_with(), barriers_used=1, max_barriers=14
    )
    assert action == ("barrier", (6, 5))


def test_depth_two_corner_seal_is_forced() -> None:
    """Cop at (5,5), thief certain in the corner (6,6), open board: wall (5,6) first;
    every thief reply (STAY or (6,5)) is then ended by the second wall — the exact
    two-wall corner seal our counted-series thief died to, from the cop's side."""
    board = make_board()
    action = forced_action(
        board, (5, 5), [(6, 6)], MOVE_SET, opts_with(), barriers_used=0, max_barriers=14
    )
    assert action == ("barrier", (5, 6))


def test_no_forcing_line_returns_none() -> None:
    """Open board, thief far away: nothing forces within the horizon — defer."""
    board = make_board()
    action = forced_action(
        board, (0, 0), [(6, 6)], MOVE_SET, opts_with(), barriers_used=0, max_barriers=14
    )
    assert action is None


def test_two_cell_support_must_be_forced_against_both() -> None:
    """Support {(6,6), (0,0)}: the corner seal kills (6,6) but not (0,0) —
    no single action forces both, so the solver must return None."""
    board = make_board()
    action = forced_action(
        board, (5, 5), [(0, 0), (6, 6)], MOVE_SET, opts_with(), barriers_used=0, max_barriers=14
    )
    assert action is None


def test_node_cap_defers_instead_of_stalling() -> None:
    """A tiny node budget aborts the search cleanly (None), never raises."""
    board = make_board()
    action = forced_action(
        board,
        (5, 5),
        [(6, 6)],
        MOVE_SET,
        opts_with(endgame_node_cap=1),
        barriers_used=0,
        max_barriers=14,
    )
    assert action is None


def test_exhausted_quota_still_finds_move_only_forces() -> None:
    """No barriers left: thief self-cornered at (6,6) with both exits walled by
    earlier play is already captured — but an ALMOST-sealed thief at (6,6) with
    (5,6),(6,5) open cannot be forced by moves alone from (5,5) in 5 plies on an
    open 7x7 (it always has an exit). The solver must respect the quota."""
    board = make_board()
    action = forced_action(
        board, (5, 5), [(6, 6)], MOVE_SET, opts_with(), barriers_used=14, max_barriers=14
    )
    assert action is None


def test_a_cop_body_plug_is_not_a_forcing_line() -> None:
    """M13 wire-true (ADR-0016): the thief escapes THROUGH the cop.

    Thief certain at (0,0), (0,1) walled, quota spent, cop two south at (2,0). The
    old model proved a force: cop steps to (1,0), the thief's only reply is STAY
    (the cop's cell was excluded as suicide), cop lands. On the wire the thief
    legally steps onto (1,0) — co-location is not graded — and walks out behind
    the cop. No move-only force exists here.
    """
    board = make_board(frozenset({(0, 1)}))
    action = forced_action(
        board, (2, 0), [(0, 0)], MOVE_SET, opts_with(), barriers_used=14, max_barriers=14
    )
    assert action is None


def test_a_certain_adjacent_thief_is_still_a_depth_one_landing() -> None:
    """The landing transition survives M13: a real move onto the support cell is a
    graded claim conversion (the commit path's geometry), proven at depth 1."""
    board = make_board(frozenset({(0, 1)}))
    action = forced_action(
        board, (1, 0), [(0, 0)], MOVE_SET, opts_with(), barriers_used=14, max_barriers=14
    )
    assert action == ("move", "N")


def test_a_stay_onto_a_colocated_thief_is_not_a_landing() -> None:
    """M13 wire-true (ADR-0016): a STAY declares nothing (ClaimPolicy refuses it),
    so a co-located 'capture' by standing still must not be provable. Thief certain
    ON the cop's cell, quota spent: nothing forces — the cop must step off and
    re-land, and the thief moves first.
    """
    board = make_board()
    action = forced_action(
        board, (3, 3), [(3, 3)], MOVE_SET, opts_with(), barriers_used=14, max_barriers=14
    )
    assert action is None


def test_sharp_support_gates_on_mass_and_width() -> None:
    """The gate: cells at/above the mass threshold, only when 1..max_cells qualify."""
    probs = {(6, 6): 0.6, (6, 5): 0.3, (0, 0): 0.04}
    assert sharp_support(probs, mass_threshold=0.05, max_cells=3) == [(6, 5), (6, 6)]
    assert sharp_support(probs, mass_threshold=0.05, max_cells=1) is None
    assert sharp_support({}, mass_threshold=0.05, max_cells=3) is None


def test_shallowest_force_wins_over_deeper_ones() -> None:
    """Iterative deepening: when a depth-1 landing exists (thief adjacent, certain),
    the solver takes it rather than a deeper wall plan — earlier is strictly safer."""
    board = make_board(frozenset({(5, 6)}))
    action = forced_action(
        board, (6, 5), [(6, 6)], MOVE_SET, opts_with(), barriers_used=1, max_barriers=14
    )
    assert action == ("move", "E")
