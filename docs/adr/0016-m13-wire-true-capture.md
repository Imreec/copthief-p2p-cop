# ADR-0016 — M13: wire-true capture semantics (the 4/18 conversion lesson)

## Status

Proposed (built on `feat/m13-wire-true-capture`, 2026-08-16; Imree's merge of the PR is
the approval). Strategy/arena/peer-decision layers only — no wire, canonicalization, or
hashing change (constraint 13 untriggered; `capture_claim` is an existing wire field).

## Context

Across six counted series the cop converted 4 captures in 18 cop games (22%) while the
belief was demonstrably good — and every conversion came in a game where the opponent
broke move-parity for us (nis-yar1 HOLDs, uoh-sqak stops). The 2026-08-16 forensic pass
over the counted logs isolated four mechanisms:

1. **Parity lock (vibecode 30–90).** Belief argmax == the thief's true cell 34/34 plies
   at p≈0.98 in all three cop games, distance pinned to 1 for 28 consecutive plies, and
   the cop played 0 STAYs and 0/14 walls: with both agents moving every ply, Manhattan
   distance changes by ±2/0 — from odd distance, co-location is arithmetically
   unreachable. The cop ran a literal 6-cell follow-the-leader ring (5 laps, numerically
   periodic beliefs) and emitted 0 claims (own-landing mass 0.0049 < the 0.1 gate).
2. **Claim-gate incoherence (best2934 47–47).** The live capture channel is ONLY a
   declared cop landing graded against the thief's post-move cell (empirical 19/19 of
   all counted claim/response pairs; `peer/inbound.py` holds no co-location check). The
   M12 intercept steered landings onto the thief's true cell, but `peer/turns.py` gated
   the claim on the RAW belief (`prob_at(landing)`), which under their lag-1 sender held
   0.0049 while the argmax sat one cell behind at 0.990: three literal co-locations
   (g02 s16, g04 s12, g06 s12) were forfeited silent. The thief side was perfect
   (30/30); the cop side donated the series. Live lag measured TWO steps (32/35), not
   ADR-0015's one; their parking thief nulls the momentum gate at breakout. Also
   `ClaimPolicy` never claims on STAY/BARRIER turns — nis-yar1 g05 s18 sat ON the thief
   at mass 0.985 with move STAY, no claim possible (book-consistent: a claim needs a
   landing; recorded as doctrine input, not a bug).
3. **Blind cop (najamjad 30–90).** All 35/35 inbound scent frames failed the physics
   check in every cop game and were withheld whole; belief matched truth 0/34 at every
   lag against a thief that STAYed ~80% of turns. The refusal design (M7-23) protects
   evidence integrity but proved strictly worse than degraded sight.
4. **The instrument lied (all cycles).** The arena/referee granted capture forms the
   wire does not have: co-location from EITHER mover (thief walking onto the cop),
   claim persistence across half-turns, and — in the search/solver — thief-onto-cop as
   suicide and cop-body cornering as a proven win. Every 32/32 that gated M9–M12 was
   measured under this generous physics; live play kept refuting it (M12's own caveat:
   swept offline, 0/3 live). The eval-harness Layer-1 invariant already states the
   capture triad "exactly" — the referee's extra forms violated our own spec.

Secondary finding, recorded not fixed: counted g04 == g06 byte-identical (tie_epsilon
0.25 is inert when expectimax values separate — the RNG is never consulted); an opponent
can replay a proven line across sub-games.

## Decision

1. **Referee grades wire-true** (`strategy/referee.py`): the landing form exists only at
   the cop's move, gated by that turn's claim decision, graded immediately; the
   thief-half check keeps ONLY barrier/imprisonment forms; no claim persistence.
2. **Search and solver model capture as a landing transition** (`copthief_police/
   search.py`, `endgame.py`): co-location is not a capture *state*; the thief's replies
   legally include the cop's cell; "no reply because the cop's body blocks the exit" is
   not a win. Rules 46/47 (barrier-on-thief, board-blocked imprisonment) unchanged.
3. **Claims ride the brain's hunted posterior** (`strategy/decision.py` gains
   `landing_confidence`; `peer/turns.py` + `referee.py` consume it, falling back to the
   raw belief for brains that do not set it). The M12 intercept and the claim gate stop
   contradicting each other; `claim_threshold` keeps its meaning against the posterior
   the brain actually hunts.
4. **Refused frames feed the belief at quarantine trust** (`[scent]
   refused_frame_trust`, default 0.0 = shipped behavior; armed 0.5 in `game.toml`):
   a physics-refused frame stays out of the known field and the audit evidence, but the
   belief may read it at scaled trust — SQ3's multiplicative floor bounds fabrication
   damage; the najamjad series proved blindness costs more.
5. **Parity-pressure knob** (`w_parity`, default 0.0 = byte-identical leaf): a leaf term
   rewarding even cop–thief distance, the minimal doctrine lever against the parity
   lock; adopted only if the wire-true arena sweep shows best-or-equal across all arms.
6. **Arena re-baseline**: our police roster entries carry the fielded
   `claim_threshold 0.1`; all champion/DoD tables regenerate under the honest physics;
   thresholds re-derived and recorded here (gates are never deleted).

## Consequences

- Offline numbers DROP, honestly — the instrument stops predicting captures the wire
  cannot grade. New tables land in `docs/evidence/` (m5-arena, pool) with before/after
  in this ADR once regenerated.
- The M9-1 solver loses its cop-body forcing lines (they were unsound live); its proofs
  are now claim-safe landings and wall forms only.
- Deeper interception doctrine (targeting the thief's reply distribution) is the next
  milestone, designed against the honest tables.
- League lane unchanged and explicitly out of scope: rule-46/47 concession pairing
  terms, `outcome_mismatch` escalation to a counted-report gate, per-pairing claim 0.0
  vs claim-blind opponents (config door exists), tie_epsilon/exploration diversity.
- Thief-repo sync PR + config propagation (`refused_frame_trust`, any adopted
  `w_parity`) owed post-merge — config never travels with the mirror (M12-5 pattern).

## Alternatives

- **Keep dual physics behind a knob** (historical vs wire-true referee): rejected — the
  generous instrument is the root defect; keeping it invites regressions to it.
- **Model claim timing inside the search's thief replies** (grade landings against the
  reply distribution): deferred to the doctrine milestone — the landing-transition model
  is sufficient to stop the lying, and the reply-model belongs with interception work.
- **Always-claim (threshold 0.0) as the global fix for the silenced landings**: rejected
  with ADR-0015's data (9 captures lost to a claim-reading evader; broadcasts our cell);
  the coherent confidence source achieves the conversions without the leak.
- **Trust refused frames fully**: rejected — the frame check exists for evidence
  integrity and adversarial senders; quarantine trust preserves both purposes.
