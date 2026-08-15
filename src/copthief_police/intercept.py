"""Belief-momentum intercept (M12) — hunt where the thief WILL be, not where it was.

The 08-14 best2934 forensics found the cop's real conversion gap: the scent-driven
posterior is accurate but LAGGED, so against any mover the argmax is yesterday's
cell — our capture claims trailed their thief's true cell by exactly one step for
20+ consecutive steps in all three cop games (11-12 adjacencies, two literal
co-locations, zero conversions). This module advances the posterior by the drift
observed between consecutive belief peaks: when the peak moved one orthogonal step,
every support cell's mass is pushed the same way; mass whose destination is walled
or off-board stays put. A jumped or parked peak carries no momentum — the advance
only ever fires on the steady runs where it is exact.

Consumed by `PoliceBrain` behind `intercept_enabled` (0.0 default: the shipped M11
stream is byte-for-byte untouched). Pure geometry — no I/O, no clock, no RNG.
"""

from __future__ import annotations

from copthief_core.domain.board import Board, Coord

__all__ = ["InterceptTracker", "advanced_probs", "drift"]


def drift(prev: Coord, current: Coord) -> Coord | None:
    """The unit orthogonal step the peak just took, or None (parked/jumped = noise).

    Input:  the previous and current belief argmax cells.
    Output: (dr, dc) with |dr|+|dc| == 1, or None when no clean momentum exists.
    """
    delta = (current[0] - prev[0], current[1] - prev[1])
    return delta if abs(delta[0]) + abs(delta[1]) == 1 else None


def advanced_probs(probs: dict[Coord, float], delta: Coord, board: Board) -> dict[Coord, float]:
    """The posterior pushed one `delta` step; blocked/off-board mass stays put.

    Input:  the raw belief probs, the drift, the current board.
    Output: a fresh dict with each cell's mass moved to `cell + delta` when that
    destination is open, merged where shifted and parked mass meet.
    """
    advanced: dict[Coord, float] = {}
    for cell, mass in probs.items():
        dest = (cell[0] + delta[0], cell[1] + delta[1])
        target = dest if not board.is_blocked(dest) else cell
        advanced[target] = advanced.get(target, 0.0) + mass
    return advanced


class InterceptTracker:
    """Per-game momentum state (Input: one (step, argmax) reading per turn;
    Output: the drift in force for that step — stable across same-step re-entries,
    because the degrade path may re-enter the brain within one turn).

    Persistence gate (the pool-dip fix): one observed step is noise against an
    erratic evader — the pool measured a raw single-step advance costing 8/32 vs
    anrbj666-thief and 5/32 vs sqak-evader while a steady runner is exactly the
    case where two consecutive equal drifts are cheap to demand. The advance
    fires only when the peak took the SAME unit step twice in a row.
    """

    def __init__(self) -> None:
        self._step: int | None = None
        self._trail: tuple[Coord | None, Coord | None, Coord | None] = (None, None, None)

    def drift_for(self, step: int, argmax: Coord) -> Coord | None:
        """Record the reading once per step, and return the CONFIRMED momentum."""
        if self._step is None or step > self._step:
            self._trail = (self._trail[1], self._trail[2], argmax)
            self._step = step
        oldest, middle, newest = self._trail
        if oldest is None or middle is None or newest is None:
            return None
        confirmed = drift(middle, newest)
        return confirmed if confirmed is not None and confirmed == drift(oldest, middle) else None

    def observe(
        self, step: int, argmax: Coord, probs: dict[Coord, float], board: Board
    ) -> dict[Coord, float]:
        """One armed read: track the peak, then hand back the advanced posterior."""
        delta = self.drift_for(step, argmax)
        return advanced_probs(probs, delta, board) if delta is not None else probs
