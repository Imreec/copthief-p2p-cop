"""PoliceBrain (TODO M5-2; PRD_police_brain §5) — ⚑ the cop repo's graded core.

Pursuit policy: capture-commit when the mass is one step away (the claim rides free —
SQ2), otherwise expectimax over the truncated belief with barrier graph-surgery as a
root action. Deterministic given (config, seed): the RNG is interface-only, every
tie breaks on sorted move order. The LLM never appears anywhere in this package
(App E rule 25 — pinned by an AST-scan test).
"""

from __future__ import annotations

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.rules import legal_moves
from copthief_core.strategy.brains import BrainBase, Observation
from copthief_core.strategy.decision import Decision
from copthief_police.barriers import best_candidate
from copthief_police.features import resolve_options
from copthief_police.search import action_value, truncated_support


class PoliceBrain(BrainBase):
    """Expectimax + graph surgery over the belief's public read surface."""

    def _commit_move(self, observation: Observation, belief: BeliefFilter) -> str | None:
        """The capture-commit rule: step onto any adjacent cell holding ≥ p_commit."""
        opts = resolve_options(self._options)
        for move in sorted(
            legal_moves(observation.board, observation.position, observation.move_set)
        ):
            dest = observation.board.apply_move(observation.position, move)
            if dest != observation.position and belief.prob_at(dest) >= opts["p_commit"]:
                return move
        return None

    def _pick_move(self, observation: Observation, belief: BeliefFilter) -> str:
        """Best MOVE-only action (also the degrade path when a barrier is refused)."""
        commit = self._commit_move(observation, belief)
        if commit is not None:
            return commit
        opts = resolve_options(self._options)
        support = truncated_support(belief, int(opts["search_top_k"]))
        board, position = observation.board, observation.position
        moves = sorted(legal_moves(board, position, observation.move_set))
        if not moves or not support:
            return "STAY"
        best_move, best_value = moves[0], float("-inf")
        for move in moves:
            value = action_value(
                board, board.apply_move(position, move), support, observation.move_set, opts
            )
            if value > best_value:
                best_move, best_value = move, value
        return best_move

    def _decide(self, observation: Observation, belief: BeliefFilter) -> Decision:
        """Full action: commit beats everything; then wall-vs-move by expected value."""
        commit = self._commit_move(observation, belief)
        if commit is not None:
            return Decision(move=commit)
        opts = resolve_options(self._options)
        support = truncated_support(belief, int(opts["search_top_k"]))
        board, position = observation.board, observation.position
        if not support:
            return Decision(move=self._pick_move(observation, belief))
        wall = best_candidate(
            board,
            position,
            support,
            observation.move_set,
            opts,
            barriers_used=observation.barriers_used,
            max_barriers=observation.max_barriers,
        )
        move = self._pick_move(observation, belief)
        if wall is None:
            return Decision(move=move)
        move_value = action_value(
            board, board.apply_move(position, move), support, observation.move_set, opts
        )
        wall_value = (
            action_value(board.with_barrier(wall), position, support, observation.move_set, opts)
            - opts["w_budget"]
        )
        if wall_value > move_value:
            return Decision(barrier=wall)
        return Decision(move=move)
