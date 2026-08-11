"""Cage-escape kit for the doctrine evader (M11-1) — orbit + pocket forecast.

The M10 exposure this closes (police-m10 converts doctrine-m10 32/32): a cage
is built from adjacency, and the correct counter is to flee the ENCLOSURE, not
the cop. Two instruments, both consumed by `doctrine_evader` behind the
`cage_escape` gate (0.0 = the shipped M10 stream byte-for-byte):

- `worst_k_region`: the k-wall pocket forecast over the belief support
  (`wall_forecast.worst_walls_region` MIN'd belief-native, like every other
  forecast term) — a cage is priced while its gap still exists. Measured on
  the signed starts vs police-m10: k=3/reach=2 carries 3 of the 4 survivals
  (k=0 keeps 1).
- `center_margin`: the orbit-zone term — hold the central margin band and
  sidestep, the shape of the only thief that ever survived a builder cop.

A third mechanism was built, measured, and REMOVED (the session hypothesis
said the flight cap should LIFT on observed opponent wall-turns so the evader
relocates while the cop builds): every lift variant converted survivals into
rim-corner deaths — max-flight relocation is rim-ward, which is exactly where
a builder wants us. The m11 evidence doc carries the numbers.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.wall_forecast import worst_walls_region

__all__ = ["CAGE_DEFAULTS", "center_margin", "worst_k_region"]

CAGE_DEFAULTS: dict[str, float] = {
    "cage_escape": 0.0,  # master gate; 0.0 = the shipped M10 stream byte-for-byte
    "forecast_walls": 3.0,  # k: wall investments the pocket forecast credits
    "forecast_wall_reach": 2.0,  # builder Manhattan reach per investment
    # The orbit-zone margin (the m11 seed-1 trace finding: with every room term
    # tied on an open board, even the DEMOTED flight tie-break herds the evader
    # to the rim). Ranks above that tie-break; 0.0 keeps it a constant = off.
    "center_margin_cap": 0.0,
}


def center_margin(board: Board, dest: Coord, cap: float) -> float:
    """Distance to the nearest board rim, capped — the orbit-zone term.

    The ring shape that survives builders holds the central margin>=cap zone
    (uoh-vibecode's fielded thief lived its whole 105-step life there); capping
    keeps every cell inside that zone equivalent, so the evader orbits freely
    instead of pinning to the exact center.
    """
    low = board.axis_start_index
    high = low + board.grid_size - 1
    margin = min(dest[0] - low, high - dest[0], dest[1] - low, high - dest[1])
    return min(float(margin), cap)


def worst_k_region(
    board: Board,
    dest: Coord,
    support: list[Coord],
    move_set: tuple[str, ...],
    quota_left: int,
    opts: Mapping[str, float],
) -> float:
    """MIN over the support of the k-wall pocket region for `dest` (0.0 disarmed).

    The wall budget clamps to the cop's live quota: a pocket needing more walls
    than remain is not a threat, and crediting it would re-corner the evader.
    """
    walls = min(int(opts["forecast_walls"]), quota_left)
    if opts["cage_escape"] <= 0.0 or walls <= 0:
        return 0.0
    return float(
        min(
            worst_walls_region(
                board,
                dest,
                cop,
                move_set,
                walls=walls,
                reach=int(opts["forecast_wall_reach"]),
            )
            for cop in support
        )
    )
