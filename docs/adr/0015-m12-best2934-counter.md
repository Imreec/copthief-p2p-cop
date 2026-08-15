# ADR-0015 — M12: counter best2934's overhauled stack (the 35–75 lesson)

## Status

Proposed (built on `feat/m12-counter-best2934`, 2026-08-15 overnight; Imree's merge
of the PR is the approval). Strategy/arena layers only — no wire, canonicalization,
or hashing change (constraint 13 untriggered).

## Context

The 2026-08-14 evening friendly vs best2934 (their 9th same-day pair, cop `96d9b17`
/ thief `5324415`) ended 35–75, 1–5 — their first-ever captures of us (g03 step 28,
g05 step 30), all verified clean by full forensics. Their same-day overhaul: a
range-4 engage-gated area-shrink waller whose emergent 11-wall "plow" herds and
body-blocks (no partition plan exists in their code), and an exit-veto thief
(refuses entering ≤2-exit cells, leaves 1-exit seats) that survived our cop 3/3.
Forensics of our own logs found the true cop-side gap: our capture claims trailed
their thief's real cell by EXACTLY one step for 20+ consecutive steps in all three
cop games — 11–12 adjacencies per game, two literal co-locations ((5,5), g04/g06
step 12), zero conversions. Their repos are public (their own rule-49 declaration);
both played heads verified == origin HEAD.

## Decision

1. **Both best2934 arms rebuilt at the played heads** (offline study of their
   public code + our own g01–g06 logs; ADR-0011 practice, no code copied). Three
   structural fixes: `barrier_engage_range` 1 → 4 (their 08-14 re-derivation — the
   change that armed the plow), `region_cap` 40 → 49 (their `limit=40` is a node
   budget that never binds on the 49-cell board; the old clamp read 40 on both
   sides of every open-board diff and silenced their waller entirely), the rule-46
   seal-onto-thief-cell veto exemption; plus the full exit-veto chain and their
   strict N>S>E>W>STAY argmax in the thief. Replay-validated against the logs:
   wall-turn fidelity 14/14 in both cop games (10/14 exact cells), thief
   destination agreement ~75% under a delta-belief approximation.
2. **Cop: belief-momentum intercept** (`copthief_police/intercept.py`, knob
   `intercept_enabled`, default 0.0 = M11 stream byte-for-byte; armed in
   `game.toml` v1.07 with a book-v1 overlay explicit-OFF pin). Every posterior
   read goes through one `_observed_probs` seam that advances mass by the peak's
   observed unit drift (blocked/off-board mass stays; jumped/parked peaks carry no
   momentum). Measured (`m12-best2934-arena.md`): best-or-equal against every arm —
   4 → 10 captures vs doctrine-m11, 32/32 vs their rebuilt thief under the
   handicapped feed.
3. **Evader: the k-forecast truncation bug fixed by config, then swept up**. The
   fielded GA float `forecast_walls 1.7077…` int-truncates in `k_regions_by_dest`
   — the champion evader played the 08-14 friendly with a k=1 pocket forecast.
   Fielded k=1: 16/32 survivals vs their range-4 cop; k=3: 29/32; **k=4 (sweep
   winner, `m12-evader-sweep.md`): 31/32**. Champion knobs now pin
   `forecast_walls 4.0` / `forecast_wall_reach 2.0` explicitly (integer-valued —
   the truncation class is closed for the fielded stack). The k dial is a real
   TRADE against interception-class cops (`m12-best2934-arena.md`,
   anrbj666-police column): k1 32/32, k3 22/32, k4 15/32 — pocket-phobia buys
   builder-safety at the price of predictability vs an interceptor. k4 chosen:
   best2934 is the mission (thief-side sweep probability 0.91 vs 0.74 at k3),
   anrbj666 is a spent pairing (rule 52, counted banked), and `forecast_walls`
   is per-pairing config if an unplayed opponent (gal-roy1) fields that class.
4. **Claim threshold 0.1 KEPT with data; claim 0.0 rejected as a default**:
   always-claim was free against their arms but cost 9 captures vs a
   claim-reading evader (our own doctrine reader). It also broadcasts our cell
   every turn. Available as pairing-specific config only.
5. **flight_floor raise REJECTED with data**: 5.0 measured 8/32 vs their cop
   (the M11 rim-death reproduced) — the disengage-by-distance hypothesis dies;
   room/forecast terms, not raw flight, carry the survival.
6. **Feed asymmetry as the honest projection bar**: in the study config OUR arms
   run `truth-lag1` (best2934 transmits scent one full turn lagged — their code;
   exactly the measured live claim-trail) while THEIR arms run buffed `sharp199`.
   Projection under that handicap: cop cell 32/32 captures, evader cell 31/32
   survivals → ~90–30, P(6–0 sweep) ≈ 0.91 per series.
7. **Champion gate GREEN with the armed stack** (`m5-arena.md`): police-brain
   tops its table (8/8 vs every thief arm incl. theirs; DoD floor 32/32 = 100%),
   doctrine-evader tops its table (8/8 vs their buffed cop). `arena.json` now
   also carries the fielded `tie_epsilon 0.25` (closing a measured live/gate
   divergence) and the buffed best2934 arms with their every-step claims.
8. **Intercept persistence gate, forced by the pool**: the raw single-step
   advance cost 8/32 vs anrbj666-thief and 5/32 vs sqak-evader (erratic peaks
   shift mass on noise). Momentum now needs the SAME unit drift twice running.
   Final pool (`m11p2-pool-arena.md`, regenerated): **zero cop dips** — anrbj666-
   thief back to exactly 26/6, sqak 32/0, vibecode improved 30/2 → 32/0,
   nisyar1 32/0 held, their rebuilt thief 32/0 — and the evader holds every arm
   except the documented anrbj666-police k-trade (22 → 15; item 3).
9. **Study matrix refreshed** (`m9-study-arena.md`, regenerated with final
   code): m12 champs added, oldest arms (police-m7, belief-evader) retired to
   hold matrix size.

## Consequences

- Offline numbers are predictions until a live game validates them; the standing
  caveat is SHARPER here: the fielded M11 cop also sweeps their thief mimic
  offline (both feed models) yet converted 0/3 live — a live/model gap remains
  (mimic ~75% fidelity and/or live claim timing). The intercept targets the
  MEASURED live failure mechanism, which is the robust play either way; the next
  friendly vs them is the validation.
- The evader knobs must hand-propagate to the thief repo's `game.toml`
  (v1.07 → v1.08) and all runbook config dirs; the cop knob (`intercept_enabled`)
  to the police-side dirs — config never travels with the mirror. Sparring stays
  generic, never tuned.
- k=4 raises the forecast's combinatorial cost (C(sites,4) per decision); the
  quality-lane arena-harness runtime was re-checked after arming (timing noted
  in the PR body; the M11 25-minute-cap lesson stands).
- Their thief's exit vetoes are cop-blind and partition-blind (their
  construction): our wall pressure + intercept exploits it. If they harden again
  (10th pair), re-run this ADR's method: forensics → mimic-at-sha → study config.

## Alternatives

- **Model them from tonight's tapes alone**: rejected — the anrbj666 decoy
  lesson; code-at-a-sha is the clean basis, the tapes validate.
- **Predict by running their actual brains (scout engine-reuse)**: rejected —
  proven unreliable 2026-08-12 (physics mistranslation grows with brain
  sophistication); arena-arm modeling is the validated method (nis-yar1 counted
  predicted exactly).
- **Claim 0.0 as the new default** ("their posture"): rejected with data (item 4).
- **A GA/self-play round on the refreshed pool**: deferred, not declined — the
  manual sweep already reached 31–32/32 on the target cells; the loop's marginal
  value must be weighed against a fresh pool-gate run when time is not overnight.
