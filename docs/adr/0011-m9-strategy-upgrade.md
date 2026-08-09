# ADR-0011 — M9 strategy upgrade: solver-then-sharpness, doctrine evasion

## Status

Proposed (built on the `worktree-brains-study` branch, 2026-08-09; Imree's merge of the
M9 PR is the approval). Extends ADR-0005's track-(2) decision; changes no wire bytes,
no negotiated term, no signed value.

## Context

The counted series against anrbj666 (2026-08-04) was a 30–90 sweep with one root cause
visible in our own sealed logs (`reports/counted-series/imreeyal/`): as thief we walked a
deterministic path into the (6,6) corner and camped until the two-wall seal closed —
three byte-identical games; as cop we advanced, placed three walls, and then played STAY
for ~20 turns while the clock ran out. Both failures reduce to the same pair: a
deliberately fuzzy belief plus a 2-ply search that converts certainty into passivity —
the M7-46 negative result (a sharp fresh-peak decoder lifted tracking 0.063→0.98 and
dropped the cop 45/64→0/64) had already proven the pair must be fixed **search-first**.

After that series, anrbj666 (Alon/Renat) shared their implementation repos with us for
study — their explicit offer, given that the pairing is played and can never recur in a
counted game (first-meeting-only scoring). Our post-series analysis therefore had three
sources: our own sealed logs, their shared implementation, and the public repos of
best2934 and uoh-sqak (MIT-licensed / public, the same basis as the existing modeled
arms of M7-45/M7-48). Their shipped architecture independently confirms the M7-46
ordering constraint from the other side: their exact endgame solver fired 0 times in
180 games until their belief layer got sharp.

## Decision

Five mechanisms, all re-implemented from behavior (no code copied), all config-gated,
landed together because the negative result forbids sharpness without the solver:

1. **M9-1 forcing endgame solver** (`copthief_police/endgame.py`): iterative-deepening
   exact search for one first action forcing capture within a bounded horizon against
   every sharp-support cell and every thief reply; barriers inside the search (capture
   forms of rules 46/47 included); node-budget abort to the heuristic; deliberately no
   wall clock (replay-identical decisions). Concept studied from anrbj666's solver.
2. **M9-2 fresh-peak observation tier** (`domain/belief_observation.observation_scores`
   + `[belief] fresh_peak_trust`): the M7-46 decoder re-landed behind the solver — the
   unique age-zero stamp under `subtractive_chebyshev_v1` names the emitter cell;
   ambiguous or stale frames abstain to the voucher path; SQ3 (boost, never eliminate)
   holds; 0.0 = the pre-M9 filter byte-for-byte. `SharpScentFeed` (`sharp<T>` feed
   grammar) scopes the tier per arena arm so modeled rivals keep the filter their real
   code fields.
3. **M9-3 worst-wall forecast + lethal gate** (`strategy/wall_forecast.py`,
   `strategy/doctrine_evader.py`): the barrier law makes the trap game exactly
   computable one ply ahead; a landing that ANY plausible cop cell can end next turn
   ranks below all others, and the gate sits above flight distance (inside a forming
   seal, "away" walks into the wall). Belief-native MIN over top-k support — their
   measured lag-1 collapse forbids a lone argmax.
4. **M9-4 anti-camp doctrine** (same evader): a stay cap (a camper is a
   self-refreshing beacon — any fresh-peak reader fields a camper's exact cell) and a
   hunted-only flight-cap lift keyed to belief mass NEAR US.
5. **M9-5 determinism kill + claim gate**: seed-consuming tie-breaks (cop
   `tie_epsilon`, evader exact-tie shuffle with STAY-last) so sub-game seeds actually
   vary play; `claim_threshold = 0.1` in the base strategy table — the confidence gate
   from our own published claim sweep (which anrbj666 adopted against us), NOT the
   m7-19 blanket silence that lost 32/32→0/32 captures.

The planned move-echo hint tier was **dropped as redundant**: under any reference-v3
wire the opponent's transmitted scent is fresh-peak-decodable exactly, so a literal
move-echo adds no information the filter does not already have.

## Consequences

- The counted-loss geometries are pinned as unit tests and now refuse: the g01 corner
  walk (doctrine evader), the g02+ STAY paralysis (solver seam pin — the shipped brain
  demonstrably answered STAY in that exact position).
- game.toml → v1.04. Live stack: fresh-peak 199, tie_epsilon 0.25, claim gate 0.1.
  Referee/arena instruments are unchanged unless a roster arm opts in (per-arm feeds).
- Full-suite runtime rose 68s→~245s (solver fires inside arena integration games);
  bounded by the node cap; revisit the default if CI tightens.
- The thief repo consumes M9-3/M9-4 via the core mirror; its `game.toml` must select
  `doctrine-evader` (or a tuned subclass) and set its own `[belief] fresh_peak_trust`
  — a follow-on sync PR there.
- Provenance recorded here per constraint #17's spirit: reference and rival code used
  as studied oracles, mechanisms re-implemented and re-measured in our own arena;
  anrbj666's sharing acknowledged; best2934/uoh-sqak read from their public repos.

## Alternatives

- **Copy the plateau pin** (their book-v1 localization): rejected for now — Monday's
  pairing locks the subtractive model where fresh-peak dominates; revisit only if a
  pairing locks `multiplicative_book_v1` (the kernel-innovation path already covers it
  in part).
- **RL brains**: rejected again (ADR-0005 posture; their own three-regime campaign
  measured the hidden-information evasion gap as structural and shipped the hand brain).
- **Blanket claim silence**: rejected (m7-19 evidence, unchanged).
- **Deeper generic expectimax**: rejected — the failure mode is proof-shaped, not
  depth-shaped; a forcing solver gated on sharp support buys exactness only where it
  is affordable and provable.
