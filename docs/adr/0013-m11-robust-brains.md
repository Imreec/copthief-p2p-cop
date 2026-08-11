# ADR-0013 — M11 robust brains: cage-escape doctrine, claim gate, camper conversion

## Status

Proposed (built on `worktree-m11-robust-brains`, 2026-08-11; Imree's merge of the M11 PR
is the approval). Extends ADR-0012; changes no wire bytes, no negotiated term, no signed
value. Strategy + belief layers only.

## Context

M10's own evidence named the standing exposure: **police-m10 converts doctrine-m10
32/32** — the mechanism built to beat vibecode's thief kills our own evader every game,
and the league converges on cage-building (confirmed live the same day this ADR was
written: nis-yar1's cop, a second independent implementation, captured our fielded
doctrine evader at step 13 in all three thief games of the 2026-08-11 friendly we lost
60–80). Imree's M11 mandate: no more one-opponent patches — red-team our own brains,
verify every "passing" check actually checks something, and replace mechanisms that lose
to measurement. The full red-team table is `docs/evidence/m11-redteam.md`; the
measurement narrative is `docs/evidence/m11-hardening.md`.

## Decision

Five mechanisms; every brain change is config-gated with shipped defaults OFF (the M10
decision stream is byte-identical until config arms it). The claim gate is the one
always-on change, and it is a provable no-op against every truthful opponent.

1. **M11-1 cage-escape doctrine** (`evader_cage.py` + `doctrine_evader.py` knobs, master
   gate `cage_escape`): flee the ENCLOSURE, not the cop.
   - `worst_k_region` (`wall_forecast.worst_walls_region`): the k-wall pocket forecast —
     min region a stationary builder with Manhattan-`reach` wall sites can leave a
     landing in after up to k investments, MIN'd over the belief support. A cage is
     priced while its gap still exists; the one-wall forecast saw only the closing wall.
   - `center_margin`: the orbit-zone term, ranked above the demoted flight tie-break —
     the seed-1 trace showed that tie-break alone herds the evader to the rim when every
     room term saturates on an open board.
   - Armed shape: `flight_floor 2.0` (sidestep, don't retreat) + `center_margin_cap 2.0`
     + `forecast_walls 3 / forecast_wall_reach 2` (ablation: k=0 keeps 1 of 4 signed
     survivals, k=3/reach=2 keeps 4).
   - **A hypothesized mechanism was built, measured, and REMOVED**: the session-prompt
     tempo lift (raise the flight cap on observed opponent wall-turns so the evader
     relocates while the cop builds). Every lift variant converted survivals into
     rim-corner deaths — max-flight relocation is rim-ward, exactly where a builder
     wants us. The banked-floor variant (permanent +1 floor per observed wall) measured
     null. Both are recorded in the evidence doc and not in the tree.
2. **M11-2 claim plausibility gate** (`domain/belief_envelope.py` + `note_claim`): the
   red-team verified that the rules-21/22 sanction `note_claim` cited is enforced by no
   audit path anywhere (settlement validates only the end-of-game `result_claim`), while
   the lived wire (vibecode 08-10: 42/43 speculative claims, all audits Verified OK)
   treats speculative claims as legal probes — so the unconditional collapse was a free
   belief-hijack channel for a lying opponent, in BOTH directions (inbound.py applies it
   role-blind). The gate is physics, not trust: a claim outside the kinematic
   `MotionEnvelope` (grown per opponent turn from legal moves + declared barriers,
   independent of the corruptible probabilistic support) is refused and counted; a
   truthful claimer's cell is always inside its own envelope, so the gate cannot change
   behavior against honest opponents. The envelope also replaces `_reachable` as the
   degenerate-collapse reset prior (a strict soundness upgrade: `_reachable` was
   belief-coupled and could lose the truth to a lying hint's hard exclusion).
3. **M11-C1 camper conversion** (the nis-yar1 g01 postmortem): our cop, tracking
   perfectly (35/35 argmax hits), placed a wall directly between itself and their
   perched thief and then STOOD STILL 19 turns with 11 walls unspent, conceding a
   34-step survival. Two root causes, both fixed:
   - `contain_range 3` refused investment at BFS gap 4 (the wall itself made the gap 4)
     — the armed M11 cop carries `contain_range 4.0`, measured to resume investment in
     the exact logged geometry (`test_police_path_distance.py`).
   - the expectimax leaf priced distance as MANHATTAN, blind to walls, so the cop's own
     wall created a local minimum the 2-ply horizon froze in — `path_distance 1.0`
     re-prices the leaf with the wall-aware path length (open-board decisions provably
     unchanged: the geodesic IS Manhattan there).
4. **M11-3 arms**: nis-yar1 modeled from our own 08-11 logs (committed under
   `docs/evidence/friendly-nis-yar1-2026-08-11/`): their thief as `nisyar1-thief`
   (flee-then-perch; one game of evidence, wake response inferred), their cop as a
   config variant of the vibecode-cop class (`opening_steps 0`, `max_walls 2`,
   `pin_enabled 1` — the observed zugzwang hold at Chebyshev 1 — on a `truth-lag1`
   feed, which is what makes the herd-to-corner emerge: they chase our scent wake, so
   the arm must too). The lag-1 pin arm reproduces the kill CLASS against doctrine-m10
   (3/8 with 1–2 seal walls); doctrine-m11 survives it 8/8 with zero seal
   opportunities conceded.
5. **Overlay pin (session item 3a)**: the `multiplicative_book_v1` per-scent-model
   overlays now pin every M10/M11 strategy knob explicitly to 0.0 — nothing arms via
   base-table fallthrough under a physics it was never measured in.

**Measured** (all offline; see `m11-arena.md` for the full matrix): doctrine-m11 vs
police-m10 moves 0/32 → 5/32 survivals with forced walls up from 3–4 to 6–8;
vs the lag-1 nis-yar1 arm 8/8 (doctrine-m10: 5/8); the decisive live geometries — the
g02 corner step and the g01 stall — are pinned as unit tests and refused/converted by
the armed brains.

## Consequences

- `game.toml` gains the armed M11 knobs on both sides at merge (thief:
  `cage_escape`-set; police: `contain_range 4.0`, `path_distance 1.0`), hand-propagated
  to BOTH repos and every runbook config dir (config never travels with the mirror);
  sparring stays generic.
- The claim-gate refusal count (`belief.claim_refusals`) is observable state; a nonzero
  count in a live game is evidence of an implausible-claim sender.
- **Honest caveat:** every number above is an offline prediction until a live friendly
  validates it. The nis-yar1 cop arm is a behavioral approximation from three games
  (the pin and the lag-1 feed are inferences that reproduce the kill class, not their
  code); their g01 thief arm rests on ONE game played against our frozen cop. Counted
  against nis-yar1 before a validating friendly carries the same class of risk M10
  documented for vibecode.

## Alternatives

- **Raise flight caps against builders** (the session-prompt tempo-lift hypothesis):
  rejected by measurement — see Decision 1.
- **Trust claims because the book sanctions lies** (status quo): rejected — the
  sanction is real on the page (App E p.145, rules 21–22) but enforced by no
  implementation in the league including ours, and the lived wire treats speculative
  claims as probes; an unenforced sanction is not a defense.
- **Model nis-yar1's cop as a fresh class**: rejected — the vibecode seal class plus a
  pin knob and a lag-1 feed reproduces the kill class with ~10 lines; a bespoke class
  would be fiction presented as fidelity (M10's arms lesson).
- **Solver-depth or node-cap changes for the stall**: rejected for M11-C1 — the stall
  was not a search-budget failure; no depth affordable at the node cap proves a capture
  against a camper with room, while containment + range 4 converts it structurally.
