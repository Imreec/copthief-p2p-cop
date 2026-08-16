"""Move-only action selection (split from brain.py at M13p2 — 150-line rule).

The expectimax scan over legal moves plus the M13p2 reply-adjacency positioning
term (ADR-0017) and the M9-5 seed-consuming tie resolution. The brain owns the
posterior seam and the barrier decisions; this owns only "which move, given the
hunted posterior".
"""

from __future__ import annotations

import random

from copthief_core.domain.board import Coord
from copthief_core.domain.rules import legal_moves
from copthief_core.strategy.brains import Observation
from copthief_police.reply_forecast import adjacency_value, reply_distribution
from copthief_police.search import action_value, truncated_support

__all__ = ["best_move"]


def best_move(
    observation: Observation,
    probs: dict[Coord, float],
    opts: dict[str, float],
    rng: random.Random,
) -> str:
    """The best MOVE-only action over the hunted posterior.

    Input: the observation, the (possibly momentum-advanced) posterior, resolved
    options, and the brain's RNG (consumed ONLY inside the tie window — M9-5).
    Output: a move from the signed alphabet ("STAY" when nothing scores).
    """
    support = truncated_support(probs, int(opts["search_top_k"]))
    board, position = observation.board, observation.position
    moves = sorted(legal_moves(board, position, observation.move_set))
    if not moves or not support:
        return "STAY"
    # M13p2 (ADR-0017): reply-adjacency positioning — computed once per decision,
    # zero-cost when the knob is off (byte-identical stream at 0.0).
    replies = (
        reply_distribution(probs, board, observation.move_set) if opts["w_intercept"] > 0.0 else {}
    )
    scored = [
        (
            action_value(
                board, board.apply_move(position, move), support, observation.move_set, opts
            )
            + opts["w_intercept"] * adjacency_value(board.apply_move(position, move), replies),
            move,
        )
        for move in moves
    ]
    best_value = max(value for value, _ in scored)
    if opts["tie_epsilon"] > 0.0:
        # M9-5: seed-consuming resolution among near-equal values — an opponent
        # cannot replay a proven line across sub-games (the counted-loss lesson).
        ties = sorted(move for value, move in scored if value >= best_value - opts["tie_epsilon"])
        return rng.choice(ties)
    return next(move for value, move in scored if value == best_value)
