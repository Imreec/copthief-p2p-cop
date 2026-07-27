# M7-20 — Retuning the cop under the claim policy: a NULL RESULT, and what it exposed

> **Headline: the retuned vector LOSES the champion gate in BOTH physics and is NOT
> deployed.** The weights are committed as a negative-result artifact
> (`config/ga_weights_bookv1_claims.json`), clearly marked, so the run is reproducible and
> the finding is not lost. Generated instruments: `m7-20-ga-claims.md` (fitness curve),
> `m7-20-gate-bookv1.md`, `m7-20-gate-reference.md`.
> Opened by M7-18/M7-19: the cop's pool used a claim-reader model M7-18 proved wrong
> (lag-1 instead of lag-0), and the cop had never been evolved under M7-19's deployed
> claim threshold.

## 1. What was changed and why

Two corrections to the M7-15 GA pool, both consequences of the claim-channel work:

- **The claim-reading opponent was mis-modelled.** It used an unconditional `truth-lag1`
  feed. M7-18 measured the real channel at **lag 0**, and under M7-19's policy a reader
  only learns on turns we actually declared — so the faithful model is base-hidden plus
  `claim_feed: truth`, not `feed: truth-lag1`.
- **The candidate never evolved under its own claim policy.** With `claim_threshold = 0.1`
  deployed, an undeclared landing is forfeit (book scoring table 2), so fitness must score
  the captures a cop can actually convert.

Both required new GA knobs (`claim_threshold` run-level, `claim_feed` per pool member with
a run-level fallback). They are absent from every previously shipped GA config, and the
M7-14/15 run **reproduces byte-identically** with them in the tree — `ga_weights_bookv1.json`
regenerates to the same md5 and the same `0.641 → 0.688` curve. The knobs are inert on old
configs, which is the property that makes this experiment safe to run at all.

## 2. The gate says no — in both physics

Held-out seeds 1–32 (disjoint from the GA's 401–432). Both candidate cops carry the
deployed `claim_threshold = 0.1` under book-v1.

**Counted physics (`multiplicative_book_v1`), the one it was tuned for:**

| cop | points | wins |
|---|---|---|
| `cop-champion` (deployed) | **1760** | 64 |
| `cop-m7-20` (new) | **1700** | 60 |

It loses, and it loses **in every single pairing** — random 25 v 26, ref-thief 10 v 10,
evader-blind 8 v 9, evader-claim 9 v 10, camper 8 v 9. There is no arm it wins.

**Reference physics (no threshold — M7-19 deployed the policy on the book-v1 overlay only):**

| cop | points |
|---|---|
| `cop-champion` | **2900** |
| `cop-m7-20` | 2420 |

CLAUDE.md §5 is unambiguous: a new brain must not lose to the previous champion. This one
loses twice. **Not deployed.**

## 3. Why the run was weak — two separate causes, both measured

### 3.1 The first attempt was under-powered, not the landscape empty

At 16 seeds the curve was **completely flat**: default, deployed and evolved all scored
exactly 0.6406, despite the "evolved" vector having `w_distance = 0.66` against the
deployed `6.0`. Two radically different cops, identical score — which is a resolution
artifact, not a discovery. 64 games cannot separate vectors whose true spread is 0.03–0.25
per pool member. Rerunning at 32 seeds produced a real curve (0.500 → 0.516).

**Reusable lesson:** before believing a flat GA curve, measure the per-member spread across
deliberately extreme vectors. A flat curve is ambiguous between "no better vector exists"
and "the instrument cannot see one".

### 3.2 The claim policy removes the selection pressure it was supposed to add

Per-member spread across four spread-out vectors (default / deployed / chase-max /
wall-max), 32 seeds:

| pool member | no claim policy | with threshold 0.1 |
|---|---|---|
| claim-reader | 0.094 | **0.031** |
| claim-blind | 0.031 | 0.250 |
| ref-thief | 0.219 | 0.250 |
| random | **0.000** | 0.031 |

**By blinding the opponent we also blind our own tuner.** The claim-reader column was a
genuine source of pressure; the policy that neutralises the reader also flattens that
column. This is the policy working as designed, but it means the cop is now selected almost
entirely by the claim-blind and reference arms.

Note also `random`'s spread of **0.000** — that member contributes nothing but compute. The
pool is less informative than four members suggest, which predates this milestone.

## 4. The finding that outweighs the retune

Under the **counted** physics, the plain reference heuristic tops the table:

| cop (book-v1, 32 seeds) | points | vs random | ref-thief | evader-blind | evader-claim | camper |
|---|---|---|---|---|---|---|
| `ref-police` | **2075** | 26 | 18 | 21 | 2 | 19 |
| `cop-champion` | 1760 | 26 | 10 | 9 | 10 | 9 |

Our tuned vector is **mediocre everywhere** (9–10 captures against every arm); `ref-police`
is **much stronger against four arms and collapses only against the claim-reader** (2/32 —
it always declares, so a reader eats it). And it achieves that *despite* the worse claim
policy: it runs at threshold 0.0 here, its own faithful behaviour.

This is not new — the committed M7-14 table already had `ref-police` on top under book-v1 —
but it is now sharper: **our GA appears to be optimising toward flat mediocrity, and the
counted series runs on the physics where that costs most.** That is a bigger open question
than any single retune, and it should be answered before the counted games, not after.

**This is a statement about our TUNING, not an argument against the physics.** The
distinction matters enough to write down, because it is easy to slide from one to the other:
we **won** the 2026-07-25 friendly 75–35 under `multiplicative_book_v1`, and both of our cop
captures — the only cop wins in cross-team history — happened under it, with a cop that was
running the *reference-tuned base table* because the book-v1 overlay did not exist yet
(introduced by `5d9a2ff`, after the friendly). The number below says a plain heuristic beats
our tuned vector on our own roster; it does not say the model is bad for us, and nothing here
supports reopening the pair-locked scent model.

Under reference physics the picture inverts completely (`cop-champion` 2900 vs `ref-police`
1985), which is the same physics-specificity M7-14/15 recorded.

## 5. What is NOT claimed

- The gate roster is five modelled thief arms, not the league. `ref-police` topping it does
  not by itself mean we should field the reference heuristic.
- §4's comparison puts two different claim policies side by side (0.0 vs 0.1) by
  construction — each cop plays its own. If anything this understates `ref-police`, whose
  always-claiming is what the reader punishes.
- **§4's cross-physics gap is confounded by TUNING MATURITY.** Our reference-physics vector
  has had far more GA investment behind it (M5-4 onward); the book-v1 overlay has had two
  attempts — M7-14/15 and this failed one. So the difference between our standing in the two
  physics is partly the difference in how long each has been tuned, and must not be read as
  a property of the models themselves.
- Nothing here re-opens M7-19's threshold: 0.1 was measured against the *deployed* vector
  and that vector is unchanged, so the deployment stands. Had this retune shipped, the
  threshold would have had to be re-swept alongside it — §3.2 is exactly why the two cannot
  be chosen independently.

## 6. Follow-ups

1. **Ask why `ref-police` beats our tuned vector under book-v1** (§4). Highest value open
   question for the counted series; likely a fitness-shape problem (mean win-rate across a
   pool rewards flat mediocrity over sharp strength).
2. **Fix the pool's dead weight** — `random` discriminates nothing; the reader column
   flattens under our own policy. A pool that cannot separate vectors cannot tune one.
3. The thief-side retune (M7-16's vector was evolved under a hidden feed) is untouched here
   and still open.
