"""Landing-price seam (M13 claim intent, ADR-0016) — ⚑ police repo.

The claim gate's input is the brain's own P(thief on the cell this move lands on),
priced from the SAME posterior the brain hunted (`_observed_probs`) — the best2934
counted forfeits came from the emitter re-reading the raw, lagged belief instead.
One constructor so every move-returning path in the brain prices identically.
Pure — no I/O, no clock, no RNG.
"""

from __future__ import annotations

from copthief_core.domain.board import Coord
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.decision import Decision

__all__ = ["priced_move"]


def priced_move(observation: Observation, probs: dict[Coord, float], move: str) -> Decision:
    """A move Decision carrying its landing's mass under the hunted posterior.

    Input: the brain's observation, the (possibly momentum-advanced — M12) posterior,
    and the chosen move. Output: the Decision with `landing_confidence` set — 0.0 for
    a landing the posterior holds nothing on, so the gate can stay honest about
    non-capture steps.
    """
    dest = observation.board.apply_move(observation.position, move)
    return Decision(move=move, landing_confidence=probs.get(dest, 0.0))
