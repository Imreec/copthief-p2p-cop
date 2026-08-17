"""Reply-distribution positioning (M13p2, ADR-0017) — ⚑ police repo.

The wire grades a landing against the thief's CURRENT cell (ADR-0016), so predicting
its NEXT cell buys positioning, not the landing itself: a cop destination is worth
more when the thief's reply mass lands ADJACENT to it — that is the geometry the
following turn's graded landing fires from. Co-located reply mass is excluded: a
thief standing on the cop cannot be landed on.

Motion model: uniform over legal replies per support cell (the belief's own predict
model). Pure geometry — no I/O, no clock, no RNG.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.domain.rules import legal_moves

__all__ = ["adjacency_value", "reply_distribution"]


def reply_distribution(
    probs: Mapping[Coord, float], board: Board, move_set: tuple[str, ...]
) -> dict[Coord, float]:
    """The posterior spread one thief-move: uniform over each cell's legal replies.

    Input: the hunted posterior (possibly momentum-advanced — the M12 seam), the
    current board, the signed move alphabet. Output: P(thief's next cell), summing
    to the input mass (walled replies are illegal, never redirected).
    """
    spread: dict[Coord, float] = {}
    for cell, mass in probs.items():
        moves = legal_moves(board, cell, move_set)
        if not moves:
            spread[cell] = spread.get(cell, 0.0) + mass
            continue
        share = mass / len(moves)
        for move in moves:
            dest = board.apply_move(cell, move)
            spread[dest] = spread.get(dest, 0.0) + share
    return spread


def adjacency_value(cop_dest: Coord, replies: Mapping[Coord, float]) -> float:
    """The reply mass landing ADJACENT to `cop_dest` (Manhattan 1) — next-turn
    convertibility. Co-located mass is excluded (not landable, M13)."""
    return sum(
        mass
        for cell, mass in replies.items()
        if abs(cell[0] - cop_dest[0]) + abs(cell[1] - cop_dest[1]) == 1
    )
