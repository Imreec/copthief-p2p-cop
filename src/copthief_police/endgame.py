"""Forcing endgame solver (M9-1; PRD_police_brain §5 amendment) — ⚑ police repo.

The converter the 30–90 counted loss proved missing: with the belief sharp, the
2-ply expectimax correctly proves "no catch in two plies" and goes flat (the
M7-46 negative result — an ACCURATE belief made the cop passive). This module
turns sharpness into captures instead: when the support is small it searches,
by iterative deepening, for a single first action (move or barrier) that forces
capture within a bounded horizon against EVERY support cell and every legal
thief reply — the three capture forms of PRD_engine E-4 inside the search
(landing, barrier-on-thief rule 46, imprisonment rule 47).

Bounded and deterministic: a node budget aborts to None (the caller's heuristic
plays on), tie-breaks are sorted, and there is deliberately NO wall clock —
unlike the per-decision seconds pin at the brain level, the solver's budget is
counted in nodes so replays and CI see identical decisions. Concept studied
from anrbj666's shipped solver after the counted loss; re-implemented and
re-gated here (docs/PROMPTS.md records the study).
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping

from copthief_core.domain.board import Board, Coord
from copthief_core.domain.rules import is_imprisoned, legal_moves

__all__ = ["Action", "forced_action", "sharp_support"]

# ("move", "N") or ("barrier", (row, col)) — the single first action of the line.
Action = tuple[str, "str | Coord"]


class _BudgetExhausted(Exception):
    """Internal: the node budget ran out — the search aborts to a clean deferral."""


def sharp_support(
    probs: Mapping[Coord, float], *, mass_threshold: float, max_cells: int
) -> list[Coord] | None:
    """The solver's gate: the cells at/above `mass_threshold`, only when 1..`max_cells`
    of them qualify — otherwise None (belief too flat or too wide to prove anything)."""
    cells = sorted(cell for cell, mass in probs.items() if mass >= mass_threshold)
    if 1 <= len(cells) <= max_cells:
        return cells
    return None


def _captured(board: Board, cop: Coord, thief: Coord) -> bool:
    """All three capture forms after an action (the landing claim rides — SQ2)."""
    return cop == thief or thief in board.barriers or is_imprisoned(board, thief)


def _thief_replies(board: Board, cop: Coord, thief: Coord, move_set: tuple[str, ...]) -> list[Coord]:
    """Distinct legal destinations; stepping onto the cop is suicide, not escape."""
    dests = {board.apply_move(thief, move) for move in legal_moves(board, thief, move_set)}
    return sorted(dest for dest in dests if dest != cop)


def _actions(
    board: Board, cop: Coord, move_set: tuple[str, ...], quota_left: int
) -> Iterator[tuple[str, str | Coord, Board, Coord, int]]:
    """Root/ply actions in deterministic order: sorted moves, then sorted walls.

    Yields (kind, payload, board_after, cop_after, quota_after). The barrier law's
    reach — own cell + orthogonal neighbours, unblocked — matches `is_legal_barrier`.
    """
    for move in sorted(legal_moves(board, cop, move_set)):
        yield ("move", move, board, board.apply_move(cop, move), quota_left)
    if quota_left > 0:
        for cell in sorted((cop, *board.neighbors(cop))):
            if not board.is_blocked(cell):
                yield ("barrier", cell, board.with_barrier(cell), cop, quota_left - 1)


def _forces(
    board: Board,
    cop: Coord,
    thief: Coord,
    move_set: tuple[str, ...],
    actions_left: int,
    quota_left: int,
    budget: list[int],
    memo: dict[tuple[frozenset[Coord], Coord, Coord, int, int], bool],
) -> bool:
    """Cop to act: True iff capture is forced within `actions_left` cop actions."""
    if _captured(board, cop, thief):
        return True
    if actions_left <= 0:
        return False
    budget[0] -= 1
    if budget[0] < 0:
        raise _BudgetExhausted
    key = (board.barriers, cop, thief, actions_left, quota_left)
    if key in memo:
        return memo[key]
    result = False
    for _kind, _payload, next_board, next_cop, next_quota in _actions(
        board, cop, move_set, quota_left
    ):
        if _captured(next_board, next_cop, thief):
            result = True
            break
        replies = _thief_replies(next_board, next_cop, thief, move_set)
        if not replies:  # cornered: every escape is blocked or suicidal
            result = True
            break
        if all(
            _forces(next_board, next_cop, reply, move_set, actions_left - 1, next_quota, budget, memo)
            for reply in replies
        ):
            result = True
            break
    memo[key] = result
    return result


def forced_action(
    board: Board,
    cop: Coord,
    support: list[Coord],
    move_set: tuple[str, ...],
    opts: Mapping[str, float],
    *,
    barriers_used: int,
    max_barriers: int,
) -> Action | None:
    """The shallowest single first action forcing capture against every support cell,
    or None (no proof within the horizon/budget — the heuristic plays on)."""
    if not support:
        return None
    horizon = int(opts["endgame_max_horizon"])
    quota_left = max(0, max_barriers - barriers_used)
    budget = [int(opts["endgame_node_cap"])]
    memo: dict[tuple[frozenset[Coord], Coord, Coord, int, int], bool] = {}
    try:
        for depth in range(1, horizon + 1):
            for kind, payload, next_board, next_cop, next_quota in _actions(
                board, cop, move_set, quota_left
            ):
                if all(
                    _captured(next_board, next_cop, thief)
                    or not _thief_replies(next_board, next_cop, thief, move_set)
                    or all(
                        _forces(next_board, next_cop, reply, move_set, depth - 1, next_quota, budget, memo)
                        for reply in _thief_replies(next_board, next_cop, thief, move_set)
                    )
                    for thief in support
                ):
                    return (kind, payload)
    except _BudgetExhausted:
        return None
    return None
