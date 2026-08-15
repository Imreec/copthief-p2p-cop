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
from copthief_core.strategy.region import path_length, region_size

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
    "endgame_enabled": 1.0,  # M9-1 solver on/off (arena A/B arm toggle)
    "endgame_support_mass": 0.05,  # gate: mass a cell needs to count as support
    "endgame_max_support": 3.0,  # gate: widest support the solver will try to prove
    "endgame_max_horizon": 5.0,  # deepest forcing line searched (cop actions)
    "endgame_node_cap": 20000.0,  # node budget; exhausted -> defer to the heuristic
    "tie_epsilon": 0.0,  # M9-5: seeded choice among values this close (0 = deterministic)
    "contain_enabled": 0.0,  # M10 containment walling on/off (0.0 = shipped M9 stream)
    "contain_mass": 0.4,  # belief mass the top cell needs before walls are invested
    "contain_range": 3.0,  # BFS gap to the target within which a wall is invested
    "contain_cooldown": 3.0,  # turns between wall investments (tempo throttle)
    "contain_reserve": 2.0,  # quota held back for the solver's finishing walls
    "contain_min_shrink": 1.0,  # believed-region shrink a wall must buy (uncapped BFS)
    # M11-C1 (nis-yar1 g01 stall): 1.0 prices leaf distance as the wall-aware
    # path length instead of Manhattan — our own wall can otherwise create a
    # local minimum the 2-ply horizon freezes in (19 STAY turns, game conceded).
    "path_distance": 0.0,
    # M12 (best2934 forensics): 1.0 advances the posterior by the peak's observed
    # momentum before every read — the lag-1 claim-targeting fix. 0.0 = M11 stream.
    "intercept_enabled": 0.0,
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
    path_cache: dict[tuple[Coord, Coord], int] | None = None,
) -> float:
    """The non-terminal leaf: pressure the mass, starve mobility, shrink the region.

    `path_distance` armed prices the pressure term as the wall-aware BFS path
    (cache per board, owned by the caller); an unreachable mass costs a full
    board-crossing so a self-sealed pocket is never the leaf's best seat.
    """
    if opts["path_distance"] > 0.0 and path_cache is not None:
        key = (cop, thief)
        if key not in path_cache:
            steps = path_length(board, cop, thief, move_set)
            path_cache[key] = steps if steps is not None else 2 * board.grid_size
        distance = path_cache[key]
    else:
        distance = abs(cop[0] - thief[0]) + abs(cop[1] - thief[1])
    mobility = len(legal_moves(board, thief, move_set))
    region = region_size(board, thief, move_set, int(opts["region_cap"]), region_cache)
    return (
        -opts["w_distance"] * distance - opts["w_mobility"] * mobility - opts["w_region"] * region
    )
