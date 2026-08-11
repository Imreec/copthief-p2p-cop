"""Cage-escape kit for the doctrine evader (M11-1) — tempo punishment + pockets.

The M10 exposure this closes (police-m10 converts doctrine-m10 32/32): a cage is
built from adjacency, so every wall costs the cop its ENTIRE move — 14 walls are
14 free tempi — and the correct counter is to flee the ENCLOSURE, not the cop.
Two instruments, both consumed by `doctrine_evader` behind the `cage_escape`
gate (0.0 = the shipped M10 stream byte-for-byte):

- `WallTempo`: reads opponent wall investment off the shared board (barriers are
  police-only — `decision.barrier_is_playable` — so barrier growth between our
  observations IS a cop turn spent building). While armed, the ruling flight cap
  lifts from `flight_floor` to `tempo_cap`: relocation across the board exactly
  when the cop cannot chase. Keying the lift on observed investment, not on
  being hunted, is what keeps the M10 anti-herding cap intact against an
  ADVANCING cop.
- `worst_k_region`: the k-wall pocket forecast over the belief support
  (`wall_forecast.worst_walls_region` MIN'd belief-native, like every other
  forecast term) — a cage is priced while its gap still exists.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.strategy.wall_forecast import worst_walls_region

__all__ = ["CAGE_DEFAULTS", "WallTempo", "worst_k_region"]

CAGE_DEFAULTS: dict[str, float] = {
    "cage_escape": 0.0,  # master gate; 0.0 = the shipped M10 stream byte-for-byte
    "forecast_walls": 3.0,  # k: wall investments the pocket forecast credits
    "forecast_wall_reach": 2.0,  # builder Manhattan reach per investment
    "tempo_window": 2.0,  # turns the flight lift outlives an observed wall-turn
    "tempo_cap": 12.0,  # ruling flight cap while the lift is armed
}


class WallTempo:
    """Per-game tracker of opponent wall-turns (Input: our per-turn observation of
    the shared board; Output: whether the tempo lift is armed this turn)."""

    def __init__(self) -> None:
        self._seen: int | None = None
        self._lift_until = -1

    def lifted(self, step: int, barrier_count: int, window: float) -> bool:
        """Record this turn's barrier count; True while a lift is armed.

        The first observation only baselines (a scenario may start mid-board);
        growth afterwards arms the lift for `window` turns including this one.
        """
        if self._seen is not None and barrier_count > self._seen:
            self._lift_until = step + int(window) - 1
        self._seen = barrier_count
        return step <= self._lift_until


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
