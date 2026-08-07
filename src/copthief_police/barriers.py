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
from copthief_core.strategy.region import path_length
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


def locks_us_out(
    board: Board,
    cop: Coord,
    cell: Coord,
    support: list[tuple[Coord, float]],
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
) -> bool:
    """True if walling `cell` would leave the cop no open route to the believed thief.

    The failure this exists to stop (M7-49, friendly g03): greedy area-shrinking will
    happily place the wall that completes a pocket AND closes the only opening the cop
    could have entered it through. After that there is no capture at any depth, the
    search goes flat, and the cop stands still until the clock runs out — which is
    exactly what happened, for sixteen turns with eleven barriers unspent.

    A wall landing ON the mass is exempt: that is the rule-46 capture, and the mass
    being unreachable afterwards is the win, not the bug. `path_length` returns None
    precisely for this test — its docstring has said so since M7-14.

    The test is MASS-WEIGHTED, not "any support cell": the truncated support carries
    cells at 1e-5, and vetoing a good cut because a near-zero tail cell went behind it
    costs real captures (measured: a flat any-cell veto dropped the police DoD 30/32 ->
    29/32). Only when `lockout_mass_threshold` of the belief ends up walled away from
    us is the cut a stalemate rather than surgery.
    """
    walled = board.with_barrier(cell)
    stranded = sum(
        p
        for spot, p in support
        if spot != cell and path_length(walled, cop, spot, move_set) is None
    )
    total = sum(p for spot, p in support if spot != cell)
    if total <= 0.0:
        return False
    return stranded / total >= opts["lockout_mass_threshold"]


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
    """The highest-gain wall at/above the threshold, or None (deterministic ties).

    Candidates that would seal the cop away from the mass are dropped before scoring:
    a cut we cannot walk through is not surgery, it is a stalemate we built ourselves.
    """
    best: tuple[float, Coord] | None = None
    for cell in candidate_cells(board, cop, barriers_used=barriers_used, max_barriers=max_barriers):
        if locks_us_out(board, cop, cell, support, move_set, opts):
            continue
        gain = surgery_gain(board, cell, support, move_set, opts)
        if gain >= opts["barrier_gain_threshold"] and (best is None or gain > best[0]):
            best = (gain, cell)
    return best[1] if best is not None else None
