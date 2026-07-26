# M7-15 — The generalist retune: mixed-opponent fitness, per-model deployment, and the four-cop gate

**2026-07-26, follow-up to M7-14 (`docs/evidence/m7-14-bookv1-strategy.md`), closing
the two follow-ups it named: the single-opponent GA's overfit (it beat the
claim-reader and stalled against a random walker) and the physics-specific
deployment question. Everything below regenerates deterministically from committed
configs.**

## 1. Mixed-opponent GA fitness

`GaConfig` gains `opponent_pool` — fitness is the plain mean win-rate across pool
members (`{spec, feed?, options?}`), pinned exactly against the single-opponent runs
it is built from; an empty pool is the old single-opponent path, unchanged.
`config/ga_bookv1.json` now tunes against the four measured worlds: the
claim-reading evader, the announced-fix evader, the reference heuristic, and a
random walker (seeds 401–416, disjoint from every gate).

Result (`m7-14-ga-bookv1.md` regenerated): pool fitness 0.641 → **0.688**. The
evolved vector is a different animal from the M7-14 lag-1 specialist — `w_distance`
at the box ceiling (6.0), `w_budget` restored (1.83), `p_commit` 0.55, `w_region`
≈ 0: a chase-heavy generalist, consistent with the post-belief-fix world where the
sharp argmax makes chasing pay.

## 2. The four-cop, five-thief gate (32 seeds per pairing, both physics)

Captures /32 under `multiplicative_book_v1`:

| cop \ thief | random | ref-thief | evader-nofix | evader-fix | evader-lag1 | points |
|---|---|---|---|---|---|---|
| ref-police (chaser) | 26 | 18 | 19 | 21 | **5** | **2135** |
| police-brain (old champion) | 27 | 4 | 4 | 8 | 11 | 1610 |
| police-brain-lag1spec (M7-14) | 26 | 10 | 8 | 8 | **16** | 1820 |
| police-brain-bookv1 (pool) | 27 | 10 | 9 | 9 | 11 | 1790 |

*(Full generated tables: `m7-14-bookv1-arena.md` / `m7-14-reference-arena.md`.)*

Reference-physics points: **pool 3080 · old champion 3050 · lag1spec 2705 ·
ref-police 2075.**

Gate reading:

- **The pool vector does not lose to the previous champion in EITHER physics** —
  it beats it under book-v1 (1790 vs 1610) and edges it under reference (3080 vs
  3050, within noise). The CLAUDE.md §5 rule is satisfied without a physics caveat.
- The lag-1 specialist keeps the best single-arm number against the ANNOUNCED
  opponent shape (16/32 vs claim-reading) but pays for it under reference physics
  (2705). It stays committed in the measurement configs as the option to revisit if
  intel firms up that the opponent ships claim-reading unchanged.
- The M7-14 passivity anecdote does not reproduce in referee aggregate (lag1spec
  26/32, pool 27/32 vs random) — it was a single peer-path seed, already disclosed.
- The plain chaser still tops the book-v1 aggregate (2135) on the strength of the
  naive arms, and still collapses against claim-reading (5/32). The aggregate
  weights all five arms equally, which is NOT the expected opponent distribution
  for the counted series — the announced counter makes the lag-1 arm the one to
  price highest.

## 3. Per-model deployment (`[strategy.<role>.<scent_model>]`)

The M7-14 finding that tuned vectors are physics-specific now has a mechanism
instead of a manual step: a `[strategy.police.multiplicative_book_v1]` sub-table in
`game.toml` overlays the base table ONLY when that model is the selected one
(`PrivateSettings.strategy_options(role)`, used by `PeerSession`). Configs without
sub-tables parse exactly as before (pinned).

**Deployed in this change:** the pool vector rides the book-v1 overlay; the base
`[strategy.police]` table keeps the proven reference-tuned vector. Rationale: the
counted series is the book-v1 world, where the pool vector clearly beats the old
one; the reference-physics margin (3080 vs 3050) is within noise and not worth
disturbing a vector with a full evidence trail. The alternative — swapping the base
table to the pool vector everywhere, defensible on the same tables — is the config
reviewer's call to take instead.

Live validation (peer path, scratchpad config copy under book-v1): the overlay
resolves to the pool vector, a full local mini-game plays with clean mutual audit
and a Verified-OK replay, and the shipped default config still resolves the base
vector untouched. (This seed pair happened to end in survival vs the random thief
where the old vector had captured — single-seed flips both ways; the 32-seed tables
above are the measurement.)

## 4. What remains open after this

- **Sibling thief retune** — next: the thief repo gets the pool machinery via the
  sync that follows this merge; its `ga_bookv1.json` (role thief, cop pool:
  ref-police / greedy-manhattan / random under book-v1) and its own
  `[strategy.thief.multiplicative_book_v1]` overlay ride that session.
- **Claim policy** — last open strategy item: measuring it honestly requires
  modeling the claim channel in the referee first (a naive threshold would have
  missed the g06 collision capture — the belief was wrong at that moment).

## Reproduction

```
uv run python scripts/ga_run.py    --config config/ga_bookv1.json
uv run python scripts/arena_run.py --config config/arena_bookv1.json
uv run python scripts/arena_run.py --config config/arena_evaders_reference.json
```
