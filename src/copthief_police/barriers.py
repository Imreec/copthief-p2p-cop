"""Barrier graph-surgery (PRD_police_brain §5): spend quota on cuts, never coin-flips.

A candidate wall is scored by the belief-weighted shrink it inflicts on the thief's
reachable region (capped BFS with vs. without the wall) plus the mass it would trap
directly (barrier-on-cell capture). Only the best candidate at or above the configured
gain threshold is offered to the search as a root action.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.domain.rules import is_legal_barrier
from copthief_police.features import region_size


def candidate_cells(
    board: Board, cop: Coord, *, barriers_used: int, max_barriers: int
) -> list[Coord]:
    """The barrier law's reach: our own cell + orthogonal neighbors, quota permitting."""
    cells = [cop, *board.neighbors(cop)]
    return [
        cell
        for cell in cells
        if is_legal_barrier(
            board, cop, cell, barriers_used=barriers_used, max_barriers=max_barriers
        )
    ]


def surgery_gain(
    board: Board,
    cell: Coord,
    support: list[tuple[Coord, float]],
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
) -> float:
    """Belief-weighted region shrink + directly trapped mass for walling `cell`."""
    cap = int(opts["region_cap"])
    walled = board.with_barrier(cell)
    before: dict[Coord, int] = {}
    after: dict[Coord, int] = {}
    gain = 0.0
    for spot, p in support:
        if spot == cell:  # the wall lands ON the mass: barrier-on-thief capture
            gain += p * opts["w_capture"]
            continue
        shrink = region_size(board, spot, move_set, cap, before) - region_size(
            walled, spot, move_set, cap, after
        )
        gain += p * shrink
    return gain


def best_candidate(
    board: Board,
    cop: Coord,
    support: list[tuple[Coord, float]],
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
    *,
    barriers_used: int,
    max_barriers: int,
) -> Coord | None:
    """The highest-gain wall at/above the threshold, or None (deterministic ties)."""
    best: tuple[float, Coord] | None = None
    for cell in candidate_cells(board, cop, barriers_used=barriers_used, max_barriers=max_barriers):
        gain = surgery_gain(board, cell, support, move_set, opts)
        if gain >= opts["barrier_gain_threshold"] and (best is None or gain > best[0]):
            best = (gain, cell)
    return best[1] if best is not None else None
