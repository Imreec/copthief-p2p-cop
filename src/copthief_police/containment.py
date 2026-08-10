"""Containment walling (M10) — sub-threshold walls as deliberate tempo investment.

The 08-10 friendly proved a structural gap between the two existing wall paths:
the surgery threshold (`barriers.best_candidate`) needs a gain one wall can only
show near existing structure — in open center a wall shrinks the reachable region
by exactly 1, so against a central oscillator the threshold NEVER fires (0 of 42
barriers placed across three perfectly-tracked games) — and the forcing solver
(`endgame.forced_action`) correctly proves nothing on an open board, because one
pursuer without walls cannot force capture. Containment closes the loop between
them: while the belief is sharp and the chase is close, invest one wall every few
turns on the reachable cell that most shrinks the believed region (uncapped —
the surgery cap saturates in open space), tie-broken toward anchored cells (board
edge or existing walls) so investments accrete into cuts instead of scattering
into pillars. The board monotonically shrinks until the solver can finish.

Gated OFF by default (`contain_enabled`): the shipped M9 stream is byte-identical
until config arms it. Pure geometry + options; no I/O, no RNG.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.region import path_length, region_size
from copthief_police.barriers import candidate_cells, locks_us_out

__all__ = ["containment_wall"]


def _anchored(board: Board, cell: Coord) -> bool:
    """True when a wall here accretes: on the board rim, or touching a barrier."""
    low = board.axis_start_index
    high = low + board.grid_size - 1
    if cell[0] in (low, high) or cell[1] in (low, high):
        return True
    return any(neighbor in board.barriers for neighbor in board.neighbors(cell))


def containment_wall(
    observation: Observation,
    support: list[tuple[Coord, float]],
    opts: Mapping[str, float],
    *,
    last_wall_step: int,
) -> Coord | None:
    """The containment investment for this turn, or None (chase on).

    Input:  the cop's observation, the truncated belief support (cell, mass),
            the option table and the wall-spacing state.
    Output: the wall to place — reachable, not on believed mass, not a lockout,
            shrinking the believed region by at least `contain_min_shrink` — or
            None when any gate refuses (disabled, quota at the endgame reserve,
            inside the cooldown, target unsharp or beyond `contain_range`).
    """
    board, cop, move_set = observation.board, observation.position, observation.move_set
    barriers_used, max_barriers = observation.barriers_used, observation.max_barriers
    if opts["contain_enabled"] <= 0.0 or not support:
        return None
    if max_barriers - barriers_used <= opts["contain_reserve"]:
        return None
    if observation.step - last_wall_step < opts["contain_cooldown"]:
        return None
    target, mass = max(support, key=lambda entry: (entry[1], entry[0]))
    if mass < opts["contain_mass"]:
        return None
    gap = path_length(board, cop, target, move_set)
    if gap is None or gap > opts["contain_range"]:
        return None
    cap = board.grid_size * board.grid_size  # uncapped: the surgery cap saturates here

    def believed_region(candidate: Board) -> float:
        cache: dict[Coord, int] = {}
        return sum(
            p * region_size(candidate, spot, move_set, cap, cache)
            for spot, p in support
            if not candidate.is_blocked(spot)
        )

    base = believed_region(board)
    best: tuple[float, int, Coord] | None = None
    occupied = {spot for spot, _ in support}
    for cell in candidate_cells(board, cop, barriers_used=barriers_used, max_barriers=max_barriers):
        if cell in occupied:  # capture attempts belong to the surgery/solver paths
            continue
        if locks_us_out(board, cop, cell, support, move_set, opts):
            continue
        after = believed_region(board.with_barrier(cell))
        if base - after < opts["contain_min_shrink"]:
            continue
        key = (after, 0 if _anchored(board, cell) else 1, cell)
        if best is None or key < best:
            best = key
    return best[2] if best is not None else None
