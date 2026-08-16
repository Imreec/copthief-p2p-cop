# ADR-0017 — M13p2: interception positioning + the bestteam arm (the wanderer lesson)

## Status

Proposed (built on `feat/m13p2-interception`, 2026-08-16/17 overnight; Imree's merge
of the PR is the approval). Strategy/arena layers only — no wire, canonicalization,
or hashing change (constraint 13 untriggered).

## Context

The second bestteam friendly (2026-08-16 evening, our cop `2412bb4`) validated M13
end-to-end and exposed the next layer:

- **Sight fixed and proven live:** belief argmax == their thief's true cell 35/35 in
  all three cop games, zero frame refusals (bestteam fixed their scent emitter the
  same evening — their commit `a59fa05` cites our physics-check finding verbatim).
- **g02: a by-the-book rule-47 capture, unconceded.** The cop herded their thief
  into (6,0), sealed both exits by step 20; the thief sat imprisoned 20 revealed
  steps; their engine never conceded; our `outcome_mismatch` (rule 47, cell [6,0],
  held 20) fired at settlement. Offline study of their code CONFIRMS the defect
  mechanically: their reference/compat protocol path answers claims by positional
  equality only and never consults their own `rules.sealed_in` verdict — which
  their native path does call. The fix exists in their tree; the league ask is to
  wire the compat path through it. (League gate, Imree's ruling: no counted until
  fixed + confirmed in writing.)
- **g04/g06: the wanderer residual.** Perfect tracking, decision-time distance 2–4
  all game, 8–9 walls spent, no cage, zero claims — the M13-honest engine correctly
  refusing to chase unconvertible geometry, and lacking a lever to CREATE the
  convertible kind (decision-time adjacency).
- **Their thief decoded (offline study, their code executed):** expectimax depth 2
  over a destination-masked belief, `-1000` on believed-cop mass, room/cycle/seal/
  distance terms, trail-avoidance at the root, tie window 0.1 with a seeded draw.
  The live "modes" are emergent from belief sharpness: their pre-fix scent
  inversion read our frames blurred → every real move paid the captured term →
  the g02 camp; post-fix their belief is sharp → root ties → trail-gradient
  wandering. No corner term, no claim-reading (our `capture_claim` never reaches
  their belief), no bluffing; their tie RNG seed is a public constant.

## Decision

1. **Reply-adjacency positioning** (`copthief_police/reply_forecast.py`, knob
   `w_intercept`, default 0.0 = byte-identical): the wire grades a landing against
   the thief's CURRENT cell, so prediction buys positioning — cop destinations are
   valued by the thief's reply mass landing ADJACENT to them (co-located mass
   excluded: not landable). `best_move` split from `brain.py` (150-line rule).
2. **bestteam-thief arena arm** (`strategy/bestteam_thief.py` + `bestteam_eval.py`,
   registered `bestteam-thief`): a re-implementation of their policy against our
   seam (ADR-0011 method, no code copied, their shipped weights as the option
   table). Behavior pins encode the executed findings (diffuse⇒camp, sharp⇒corner
   climb-out, trail-avoidance ties).
3. **Fidelity, stated honestly:** [PENDING — tape validation vs their own code as
   golden oracle; numbers land here before the PR opens.]
4. **Sweeps under the wire-true instrument:** [PENDING — w_intercept × w_parity ×
   containment knobs vs the bestteam arm + full-pool regression; numbers land here.]

## Consequences

- [PENDING — measured tables.]
- Per-pairing options vs bestteam now on the table with code-level evidence:
  `claim_threshold 0.0` is free against their thief (their belief never reads our
  claims — their code, not conjecture); their public tie seed makes their draws
  reproducible in principle (documented, NOT built — desync-fragile).
- The rule-47 concession remains their fix; every offline conversion number vs
  their arm assumes it (stated wherever the numbers are used).

## Alternatives

- **Predict-by-running-their-engine live**: rejected again (ADR-0015 grounds);
  their code is used offline as a study source and a fidelity oracle only.
- **Exploit their public tie seed for exact move prediction**: rejected for the
  fielded stack — one belief-state desync and the "prediction" is noise; recorded
  as a possibility.
- **Corner-herding as a bespoke wall planner**: deferred until the sweep shows
  whether `w_intercept` + existing containment close the gap without it.
