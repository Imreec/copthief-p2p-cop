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
3. **Fidelity, stated honestly** (`docs/evidence/m13p2-bestteam-mimic.md`): their own
   code, correctly fed, reproduces the tapes at 98% (103/105) — the input truth being
   scent-lag-2. Our mimic agrees **57/70 = 81%** tie-aware against their code's own
   per-step scores (golden fixture committed, floor pinned in CI), with divergence
   concentrated at wall-adjacent states. **81% < the 90% bar ⇒ every arena number
   against this arm is DIRECTIONAL**, and the live friendly is the decisive test.
4. **Sweep** (`m13p2-bestteam-arena.md`): vs bestteam-thief **32/32 at every
   w_intercept including 0.0** — the M13 stack already sweeps the mimic (cage forms
   included, so live conversion of those assumes THEIR rule-47 fix). vs doctrine-m12
   (our hardest evader): **25/32 → 29/32 (w_intercept 2–10) → 31/32 (20)** — the
   positioning term is a real, monotone gain against a strong mover.

## Consequences

- **Arming decision: `w_intercept` stays 0.0 fielded; 20.0 is a measured PER-PAIRING
  option.** Pool A/B (`m11p2-pool-arena.md`, police-m12 vs police-m12-i20, 32 seeds):

  | thief arm | i0 | i20 | delta |
  |---|---|---|---|
  | doctrine-m12 | 25/7 | 31/1 | +6 |
  | anrbj666-thief | 20/12 | **32/0** | +12 (closes the M13 wire-true dip) |
  | vibecode-thief | 32/0 | **24/8** | −8 (the ring-runner class punishes adjacency-chasing) |
  | nisyar1 / best2934 / sqak / bestteam | 32/0 each | 32/0 each | held |

  The zero-dip rule fails on the vibecode class — a SPENT pairing, but gal-roy1's
  unplayed thief could be that class, and their counted is LIVE. So the default
  holds 0.0 (byte-identical stream) and 20.0 arms per pairing on Imree's word
  against interceptor-resistant movers. Same posture as ADR-0015's k-trade.
- **vs bestteam: 32/32 at every w_intercept including 0.0** — the M13 stack already
  sweeps their mimic. DIRECTIONAL (mimic 81%), and the cage-form conversions among
  those 32 assume THEIR rule-47 concession fix. The live friendly is the test;
  nothing here is a projected series score.
- The pool instrument now carries the bestteam-thief row and the i20 A/B arm
  permanently; the golden fixture + fidelity floor are CI-pinned.
- Runbook propagation owed post-merge: none for defaults (0.0 ships); the
  per-pairing i20/claim-0.0 options are documented in the runbook M13 levers
  section, armed only by Imree per series.
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
