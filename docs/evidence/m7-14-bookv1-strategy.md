# M7-14 — Strategy under the counted physics: doors, counter-models, and the measured edge

**2026-07-26. The counted series vs anrbj666 will lock `multiplicative_book_v1`; the
opponent announced (2026-07-25, his own words) that he is building belief-native
trap-awareness and a counter-deception layer for the rematch. This session made the
arena able to measure that world, built the counter-model, fixed our own biggest
book-v1 weakness, and retuned the cop under the physics it will actually play.
Analysis layer over four generated artifacts: `m7-14-bookv1-arena.md`,
`m7-14-reference-arena.md`, `m7-14-ga-bookv1.md`, and the regenerated
`m3-belief-eval.md` — every number below is re-derivable from a committed config by
the quoted command.**

## 1. What was built (all TDD, keyless, deterministic)

- **The referee/arena/GA path can now select the scent model.** Until this session
  the whole strategy instrument ran `subtractive_chebyshev_v1` unconditionally —
  `referee_setup` never passed a model, so every GA weight we deploy was tuned under
  physics the counted series will not play. One shared builder
  (`shared/locked_models.build_scent_model` — the same doc-lookup + signed-terms
  guard the peer session uses, CLAUDE.md #11) now feeds `play_referee_game`, the
  scenario series, `config/arena*.json` (`scent_model`) and `config/ga*.json`.
- **Per-side information feeds.** `play_referee_game` takes a thief-side feed
  distinct from the cop's; `strategy/info_feed.make_feed` names them
  (`hidden` | `truth` | `truth-lag<K>`), built fresh per game because a lagged feed
  carries trajectory history. `LagTruthFeed` is the claim-reading counter-model: the
  M7-13 postmortem showed our cop claim-tests its landing cell on every moving turn
  (`peer/turns.py`), so each `caught: false` response hands a listening evader the
  cop's position one step late — lag-1 truth, continuously. (Conservative: the real
  feed has gaps on STAY/BARRIER turns; the model leaks every turn.)
- **`BeliefEvaderBrain`** (`strategy/evader_brains.py`), the opponent model, in the
  postmortem's priority order: expected flight distance from the believed cop
  (Manhattan + Chebyshev — Manhattan alone crowns the g02 corner camp), anti-camping
  under a Chebyshev threat radius, wall forecast via destination mobility +
  reachable region (`strategy/region.py`, moved from the police package — barrier
  surgery and wall forecasting are one geometric question). Ablation arms are
  config-expressed: `evader-nofix` (flight only), `evader-fix` (full model),
  `evader-lag1` (full model + claim-reading).
- **The book-model belief observation was rebuilt** (`domain/belief_observation.py`)
  — see §3.

## 2. Cross-validation: the instrument reproduces the opponent's own number

Under reference physics, `police-brain` vs `evader-lag1` = **27/32 captures**
(`m7-14-reference-arena.md`). The opponent team independently published exactly
"hidden lag-1 gives a trap cop 27/32" from their own implementation (round 4,
2026-07-20). Same shape, same number, two codebases — the strongest calibration
evidence the arena has.

## 3. The belief fix: argmax 17% → 61% under book-v1

The M3-8 measurement split the book model's 17% argmax hit-rate into **saturation**
(the model's own additive clamp pins revisited neighbourhoods flat at 0.9 —
inherent, untouched) and **ring/age conflation** (our voucher heuristic reading
intensity as age — a fresh ring-1 cell inverted to "age 4"). The fix is the M3-8
doc's own prescription, taken one step further: the filter now shape-matches the
observation **innovation** — observed field minus the decay-predicted previous
field, which by the model's own arithmetic is (up to clamping) exactly one fresh
kernel at the opponent's current cell — scoring each hypothesis
`sum(min)/sum(max)` against the kernel template. Flat saturated camp blobs read as
mismatch, not youth. Raw-field shape matching alone was tried first and measured
WORSE (0.086): a lingering thief saturates its ring cells too, so no shape survives
in the raw field — the innovation is what isolates it.

Result on the m3 instrument (10 seeds, `m3-belief-eval.md` regenerated): argmax
hit-rate **0.171 → 0.609**; mean belief-error essentially unchanged (0.9001 →
0.9062) — the fix sharpens the peak, which is the pursuit-relevant statistic. The
reference-model voucher path is byte-identical: 0.977 / 0.7314 stand, pinned in CI.

Live-path consequence: `peer/session` already passes the selected model into the
filter, so any live book-v1 game gets this observation model with no wire change.

## 4. The book-v1 arena (`m7-14-bookv1-arena.md`, 32 seeds per pairing)

| cop \ evader (captures/32) | ref-thief | evader-nofix | evader-fix | evader-lag1 |
|---|---|---|---|---|
| ref-police (argmax chaser) | 18 | 19 | 21 | **5** |
| police-brain (reference-tuned weights) | 4 | 4 | 8 | 11 |
| police-brain-bookv1 (retuned, §5) | 10 | 8 | 8 | **16** |

Findings, in strength order:

1. **The reference-tuned weights are wrong under book-v1.** With the belief fixed,
   the plain argmax chaser converts 63/128 while the tuned expectimax brain manages
   27/128 — the deployed vector was optimized for the old belief landscape and now
   underperforms a baseline. This is the measured cost of fact (b) in the session
   brief, and the reason §5 exists.
2. **The announced trap-awareness fix, WITHOUT better information, helps us** —
   `evader-fix` is captured more than `evader-nofix` by every cop (21 vs 19, 8 vs 4,
   8 vs 8). Trap-awareness under a hidden-info belief is mispriced motion: the
   mobility/region seeking drags the evader through territory the cop hunts. This is
   the trap-confound finding again, now measured from the evader side: *wire shape
   (information), not evaluation, selects whose trap-skill matters.*
3. **Claim-reading is the counter that matters.** `evader-lag1` collapses the
   chaser (18 → 5) and is the strongest evader arm in aggregate. The cheapest
   defense is ours to take: stop volunteering claims. Since claims are the capture
   mechanism, the lever is a belief-thresholded claim policy (claim only when
   `P(thief at landing cell)` clears a knob) instead of the current every-moving-turn
   habit — protocol-legal, small, **not built this session** (named follow-up).
4. Against a search-based, wall-spending cop, lag-1 information CUTS BOTH WAYS —
   police-brain captures `evader-lag1` more (11) than the naive arms (4): a
   deterministic reactive evader is predictable, and predictable is herdable.

## 5. The retune (`m7-14-ga-bookv1.md`, `config/ga_bookv1.json`)

GA under `multiplicative_book_v1` vs `evader-lag1` (the hardest measured world),
fitness seeds 401–432 — disjoint from the DoD seeds, the reference-GA seeds, and
the arena above. Capture-rate fitness: DEFAULT options 0.406 → evolved **0.531**.
Evolved vector (`config/ga_weights_bookv1.json`):

| knob | reference-tuned (deployed) | book-v1-evolved |
|---|---|---|
| w_distance | 3.8875 | 4.6788 |
| w_mobility | 3.6061 | 4.8418 |
| w_region | 0.1143 | 0.5184 |
| w_budget | 1.7277 | **0.0** |
| barrier_gain_threshold | 4.7893 | 5.0667 |
| p_commit | 0.2 | 0.3230 |

`w_budget = 0` is the headline: against an informed evader under book physics,
barriers are not a budgeted luxury — herding is the strategy. (Cross-check: it was
our barrier-heavy brain, not the chaser, that already did best vs `evader-lag1`.)

**Champion-gate comparison, both physics, same 32-seed instrument (the "new brain
must not lose to the previous champion" rule, run as a three-cop round-robin in
each table):**

| physics | police-brain (old champion) | police-brain-bookv1 | verdict |
|---|---|---|---|
| multiplicative_book_v1 | 1045 pts (27 wins) | **1270 pts (42 wins)** | new beats old — gate PASS for book-v1 play |
| subtractive_chebyshev_v1 | **2425 pts (119 wins)** | 2110 pts (98 wins) | old beats new — reference play keeps the old vector |

The two vectors are **physics-specific** and both are now committed. Nothing is
deployed by this session: `config/game.toml [strategy.police]` still carries the
reference-tuned vector, and which vector fields the counted series is a config
review decision (the negotiated locked model should select it — a per-model
`[strategy.police.<model>]` override is a candidate follow-up if Imree wants the
switch mechanical rather than manual).

Disclosed limits: the GA specialized against `evader-lag1` — it pays for the lag-1
edge with captures against naive evaders (8–10 vs the chaser's 18–21), and the
plain chaser still tops the book-v1 aggregate table. A mixed-opponent fitness (or a
chase/herd mode switch on how informed the opponent behaves) is the obvious next
increment, not claimed here. The evader model approximates announced behavior; his
actual implementation will differ — the arms bracket the plausible range
(no-fix … fix … fix+claim-reading), they do not predict a point in it.

## 6. What this changes for the counted series

- **Negotiation calculus, updated:** at M3-8 the book model cost our filter most of
  its edge (argmax 17%) and read as evader-friendly; the friendly then produced two
  cop captures; this session's fix + retune move our book-v1 posture from "concede
  physics, keep wire" toward "book-v1 is playable for our cop" — 61% argmax, 50%
  capture rate against his announced-counter-plus-claim-reading model. The scent
  term is now materially less valuable to him than his R4-era data suggested.
- **His announced fix is not the threat; his information is.** If he ships
  trap-awareness without a cop-position feed, our capture rate RISES. The feed to
  deny him is the claim channel (finding 3) — ours to close, unilaterally.
- **The sibling retune** (our thief under book-v1 — its camping streaks up to 14 are
  unpriced risk the moment his cop learns to convert beacons) needs these same doors
  and rides the core sync after this branch merges; it is not started here.

## 7. Peer-path validation (the live loop, not just the referee)

Everything above is referee-mode. Because the belief fix is live on the peer path
(`peer/session` hands the selected model to the filter), two full local mini-games
were played through the REAL peer loop — both sides in-process, handshake, commits,
mutual audit, replay — from a scratchpad config copy flipped to
`multiplicative_book_v1` (committed `config/` untouched, resting `[email]` at rest,
dev mode owes no report):

- **Deployed (reference-tuned) vector:** `cop_capture` in 13 steps, both audits OK,
  replay **Verified OK, 27 records**.
- **Same seeds, retuned vector:** `thief_survival` 35 — the cop spent five barriers
  then chose STAY for the rest of the game. **A passivity mode exists** in the
  evolved vector against a diffuse (random-walk) belief from the canonical corner
  start. Quantified immediately over 16 varied scenario starts vs `random` under
  book-v1: old 11/16 captures, new 10/16 — statistically equal, so the stall is a
  one-seed mode, not dominant behavior; both audits and replays were clean in both
  runs (**the new observation model changes nothing on the wire**). Recorded here
  because the deployment review should know the mode exists; the mixed-opponent
  fitness follow-up is the structural fix.

Not run: a full six-sub-game `copthief series` under book-v1 — the series driver
itself is proven (M7-3 live, M7-11 rig) and adds no new coverage of the
belief/physics path beyond the per-game peer loop exercised above; the counted
rehearsal remains the place that composition is re-proven end-to-end.

## Reproduction

```
uv run python scripts/arena_run.py --config config/arena_bookv1.json
uv run python scripts/arena_run.py --config config/arena_evaders_reference.json
uv run python scripts/ga_run.py    --config config/ga_bookv1.json
uv run python scripts/belief_eval.py
```

All four are deterministic on this tree; the champion-gate CI arena
(`config/arena.json` + `config/arena_champion.json`) is untouched and green.
