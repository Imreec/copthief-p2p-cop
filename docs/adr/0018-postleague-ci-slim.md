# ADR-0018 — Post-league CI slim: strategy evals move to an on-demand lane

**Status:** Accepted (2026-08-24) · **Deciders:** Imree (asked for it explicitly), Claude
**Context milestone:** M8 (submission hardening; league cap reached 10/10, strategy frozen)

## Context

During the league season the per-PR `quality` suite lane carried the strategy-measurement
evals CI-blocking: the champion-regression round robin (`test_arena_harness.py`), the DoD
win-rate floors (`test_arena_dod.py`), and the GA smoke (`test_genetic.py`'s evolution +
pool tests). That was correct then — brains changed weekly and a regression had league
consequences. It also made the suite lane cost ~26 minutes wall (measured 2026-08-24:
the arena fixture alone 17.6 min, the GA smoke 9.8 min, the DoD floors 2.2 min — everything
else in the 1,156-test suite totals ~2 minutes), and chained it to the self-hosted 24-core
runner, which queues silently when the runner is down (a real ops landmine documented in the
ops memory). With the league over and the strategy frozen, every remaining change is docs,
assets, or cleanup — the heavy evals measure a quantity that no longer changes, at the exact
moment CI latency matters most (submission night).

## Decision

1. A new pytest marker **`arena`** tags the strategy-measurement evals: the arena-harness
   module, the DoD-floor module, and the two slow GA tests. Default `addopts` becomes
   `-m 'not live and not arena'`.
2. The per-PR/push `quality` suite lane runs the slimmed suite **on `ubuntu-latest`**
   (timeout 15 min) — no self-hosted dependency left on the merge path. Coverage still
   gates at 85 (measured on the slimmed suite: 1,150 tests in ~31 s locally, 95.1%).
3. A new **on-demand workflow `arena.yml`** (workflow_dispatch, self-hosted `fast24`)
   runs `-m "arena and not live"`. **Policy: it is mandatory before merging any change
   that touches a brain, a weight table, or the referee** — trigger it from the PR and
   link the green run on the thread. `make test-arena` is the local twin.
4. Arena seeds and the solver node cap are untouched — they are the measurement, never
   speed knobs. Nothing about the evals themselves changed; only when they run.

## Consequences

- PR CI drops from ~30 min to ~5; CI stays green with the local runner off (the `gates`
  lane always was hosted; now the whole merge path is).
- The champion gate is no longer *mechanically* enforced per-PR — it is enforced by
  policy + review checklist (this ADR + the workflow header + CLAUDE.md §5's pointer).
  Accepted because the remaining project window is docs/cleanup only; any future strategy
  work reactivates the lane by running it, or by reverting this ADR.
- The slimmed default suite still covers the arena/GA *code* (unit tests for the arena
  engine, config loading, genome/fitness plumbing) — what left the lane is the expensive
  *measurement*, not the correctness tests.

## Alternatives considered

- **Keep everything, shrink seeds/caps:** rejected — seeds and caps are the measurement;
  a cheaper measurement is a different (worse) instrument (the M13 lesson about trusting
  instruments applies squarely).
- **Nightly schedule instead of workflow_dispatch:** rejected — nothing changes nightly
  anymore; a scheduled 30-minute burn on a personal machine buys nothing.
- **Split coverage across both lanes:** rejected as complexity — the slimmed suite alone
  clears the 85 gate with ~10 points of headroom.
