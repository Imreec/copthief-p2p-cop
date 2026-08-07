"""uoh-sqak's evader as an arena arm (M7-48) — ⚑ police repo, opponent model only.

Modelled from their PUBLISHED brain at github.com/salah-dev-stu/uoh-sqak-cop
(`src/cipherchase/strategy/thief_evader_v2.py` @ `1ca9d23`, (c) 2026 uoh-sqak — Salah
Qadah, Andalus Kalash). This is their REWRITE, not the thief we beat in the 2026-08-07
friendly: they diagnosed that one as forfeiting (it sprinted to a corner and stood
there) and replaced its objective, reporting survival 42% -> 82% against their own
strongest cop. So the friendly's three cop wins say nothing about this arm — which is
the whole reason to build it before a counted series rather than after.

Values are the ones they FIELD in `config/thief/game.toml [strategy]`, not the class
defaults: `w_exits` is 1.0 there against a class default of 0.3 (their comment: "0.3 ->
1.0 doubles survival") and `w_risk` is 1.0 against a default of 3.0.

Their objective is ROOM, not distance: exits and reachable area carry it, and distance
survives only as a tiebreak. Two behaviours are load-bearing and mirrored exactly:

  * near-ties within `tie_epsilon` are broken at RANDOM, seeded — an intercept-style
    predictor cannot read them, which is why our own cop must not be tuned against a
    single deterministic reply;
  * STAY is dropped from the tie set whenever any moving option ties with it. In the
    far corner STAY and stepping off score exactly equal at `w_exits` 1.0, and their
    old brain parked on that coin-flip — the seal that lost them the friendly.

⚠ Their thief is NOT deterministic across a series: their runtime seeds it
`Random(play.seed + sub_game_number)`, so each sub-game draws a different stream. Their
COP is deterministic; the thief is not, and a series projection that assumes one game
per role played three times is wrong on this half.
"""

from __future__ import annotations

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import STAY, Board, Coord
from copthief_core.domain.rules import legal_moves
from copthief_core.strategy.brains import BrainBase, Observation
from copthief_core.strategy.region import region_size

__all__ = ["EVADER_DEFAULTS", "SqakEvaderThiefBrain"]

EVADER_DEFAULTS: dict[str, float] = {
    "w_dist": 1.0,  # FIELDED; distance is only a tiebreak in their new objective
    "w_exits": 1.0,  # FIELDED (class default 0.3 — "0.3 -> 1.0 doubles survival")
    "w_reach": 0.15,  # their class default; absent from the config they field
    "w_risk": 1.0,  # FIELDED (class default 3.0)
    "tie_epsilon": 0.25,  # their class default; the width of the random tie set
    "region_cap": 49.0,  # their `reachable_cells` is uncapped on a 7x7
}


class SqakEvaderThiefBrain(BrainBase):
    """Their `EvaderBrain` (Input: the thief Observation + our belief over the cop;
    Output: a move, drawn at random from the near-tied best, never STAY on a tie)."""

    def _score(self, board: Board, target: Coord, cop: Coord, move_set: tuple[str, ...]) -> float:
        opts = {**EVADER_DEFAULTS, **self._options}
        distance = abs(target[0] - cop[0]) + abs(target[1] - cop[1])
        exits = sum(not board.is_blocked(cell) for cell in board.neighbors(target))
        reach = region_size(board, target, move_set, int(opts["region_cap"]), {})
        risk = 1.0 if distance <= 1 else 0.0
        return (
            opts["w_dist"] * distance
            + opts["w_exits"] * exits
            + opts["w_reach"] * reach
            - opts["w_risk"] * risk
        )

    def _pick_move(self, observation: Observation, belief: BeliefFilter) -> str:
        opts = {**EVADER_DEFAULTS, **self._options}
        board, move_set = observation.board, observation.move_set
        cop = belief.argmax()
        candidates = sorted(legal_moves(board, observation.position, move_set))
        if not candidates:
            return STAY
        scored = {
            move: self._score(board, board.apply_move(observation.position, move), cop, move_set)
            for move in candidates
        }
        best = max(scored.values())
        near_ties = [m for m in candidates if best - scored[m] <= opts["tie_epsilon"]]
        moving = [m for m in near_ties if m != STAY]
        return self._rng.choice(moving or near_ties)
