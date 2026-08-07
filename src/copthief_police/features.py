"""PoliceBrain evaluation features + option defaults (PRD_police_brain §5).

`DEFAULT_OPTIONS` is a data table, not logic — the AppFTable pattern: these are the
canonical knob values, and any `[strategy.police]` / arena `brain_options` key
overrides them (the M5-4 GA writes tuned values into config; code never changes).
Leaf value is the cop's view of a (board, cop, thief-branch) state: capture handled
by the search; here distance, thief mobility, and thief safe-region size trade off
under the configured weights.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.domain.rules import legal_moves
from copthief_core.strategy.region import region_size

__all__ = ["DEFAULT_OPTIONS", "leaf_value", "region_size", "resolve_options"]

DEFAULT_OPTIONS: dict[str, float] = {
    "search_top_k": 6.0,  # belief support truncation (renormalized)
    "search_depth": 2.0,  # our-move plies in the expectimax
    "p_commit": 0.5,  # neighbor mass that triggers the capture-commit step
    "barrier_gain_threshold": 2.0,  # belief-weighted region cut needed to spend a wall
    "lockout_mass_threshold": 0.9,  # belief mass that may NOT end up walled away from us
    "region_cap": 24.0,  # BFS early-exit: beyond this a region counts as "open"
    "w_capture": 100.0,  # value of a captured branch (plus earlier-is-better bonus)
    "w_distance": 3.0,  # per-cell Manhattan pressure toward the mass
    "w_mobility": 2.0,  # per-move penalty for thief freedom
    "w_region": 1.0,  # per-cell penalty for thief safe area (capped)
    "w_budget": 1.0,  # cost of spending one barrier from the quota
    "decision_budget_seconds": 5.0,  # generous per-decision ceiling (perf pin)
}


def resolve_options(options: Mapping[str, float]) -> dict[str, float]:
    """The defaults table with config overrides applied (unknown keys tolerated)."""
    return {**DEFAULT_OPTIONS, **options}


def leaf_value(
    board: Board,
    cop: Coord,
    thief: Coord,
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
    region_cache: dict[Coord, int],
) -> float:
    """The non-terminal leaf: pressure the mass, starve mobility, shrink the region."""
    distance = abs(cop[0] - thief[0]) + abs(cop[1] - thief[1])
    mobility = len(legal_moves(board, thief, move_set))
    region = region_size(board, thief, move_set, int(opts["region_cap"]), region_cache)
    return (
        -opts["w_distance"] * distance - opts["w_mobility"] * mobility - opts["w_region"] * region
    )
