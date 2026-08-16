"""Expectimax over the belief (PRD_police_brain §5; book §6.3.1 "your own algorithm").

Position uncertainty is epistemic — a chance node: expectation over the truncated
belief support. Action uncertainty is adversarial — the thief KNOWS where it is, so
its reply is a min. Our plies maximize. Capture branches pay `w_capture` plus an
earlier-is-better bonus (remaining plies), so the search prefers the fast catch.
"""

from __future__ import annotations

from collections.abc import Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.domain.rules import is_imprisoned, legal_moves
from copthief_core.strategy.brains import Observation
from copthief_police.features import leaf_value


def commit_move(
    observation: Observation, probs: Mapping[Coord, float], p_commit: float
) -> str | None:
    """The capture-commit rule: step onto any adjacent cell holding ≥ `p_commit`
    of the (possibly momentum-advanced — M12) posterior, in sorted move order."""
    board, position = observation.board, observation.position
    for move in sorted(legal_moves(board, position, observation.move_set)):
        dest = board.apply_move(position, move)
        if dest != position and probs.get(dest, 0.0) >= p_commit:
            return move
    return None


def truncated_support(probs: Mapping[Coord, float], top_k: int) -> list[tuple[Coord, float]]:
    """The `top_k` most probable cells, renormalized (deterministic order).

    Takes the probs mapping rather than the filter so the M12 intercept can hand
    every consumer the same momentum-advanced view through one seam.
    """
    ranked = sorted(probs.items(), key=lambda kv: (-kv[1], kv[0]))[:top_k]
    total = sum(p for _, p in ranked)
    return [(cell, p / total) for cell, p in ranked] if total > 0 else []


def _captured(board: Board, cop: Coord, thief: Coord) -> bool:
    # M13 (ADR-0016): the STATE forms only (rules 46/47). Co-location is not a capture
    # state on the wire — the landing is a graded TRANSITION, scored where the cop moves.
    del cop
    return thief in board.barriers or is_imprisoned(board, thief)


def _cop_turn(
    board: Board,
    cop: Coord,
    thief: Coord,
    move_set: tuple[str, ...],
    plies: int,
    opts: Mapping[str, float],
    cache: dict[Coord, int],
    paths: dict[tuple[Coord, Coord], int],
) -> float:
    if _captured(board, cop, thief):
        return opts["w_capture"] + plies
    if plies == 0:
        return leaf_value(board, cop, thief, move_set, opts, cache, paths)
    values = []
    for move in sorted(legal_moves(board, cop, move_set)):
        dest = board.apply_move(cop, move)
        if dest == thief and dest != cop:  # a real landing — a STAY declares nothing (M13)
            values.append(opts["w_capture"] + plies)
        else:
            values.append(_thief_turn(board, dest, thief, move_set, plies - 1, opts, cache, paths))
    return max(values) if values else leaf_value(board, cop, thief, move_set, opts, cache, paths)


def _thief_turn(
    board: Board,
    cop: Coord,
    thief: Coord,
    move_set: tuple[str, ...],
    plies: int,
    opts: Mapping[str, float],
    cache: dict[Coord, int],
    paths: dict[tuple[Coord, Coord], int],
) -> float:
    if _captured(board, cop, thief):
        return opts["w_capture"] + plies
    if plies == 0:
        return leaf_value(board, cop, thief, move_set, opts, cache, paths)
    # M13 (ADR-0016): the cop's cell is a legal, ungraded reply — the thief escapes
    # THROUGH the cop on the wire (the vibecode/best2934 forensics). STAY guarantees
    # the reply set is never empty, so no "cornered" bonus exists.
    replies = [
        board.apply_move(thief, move) for move in sorted(legal_moves(board, thief, move_set))
    ]
    return min(_cop_turn(board, cop, dest, move_set, plies, opts, cache, paths) for dest in replies)


def action_value(
    board: Board,
    cop_after: Coord,
    support: list[tuple[Coord, float]],
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
) -> float:
    """Expected value of one root action over the belief support (fresh region and
    path caches per call — the board differs between move and barrier actions)."""
    cache: dict[Coord, int] = {}
    paths: dict[tuple[Coord, Coord], int] = {}
    plies = int(opts["search_depth"]) - 1
    return sum(
        p * _thief_turn(board, cop_after, cell, move_set, plies, opts, cache, paths)
        for cell, p in support
    )
