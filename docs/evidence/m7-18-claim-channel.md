# M7-18 — The evader reads capture claims (claim channel, half 1)

> Analysis half of the claim-channel work specified in `docs/PRD_claims.md` (approved
> 2026-07-27). Generated instruments this doc reads: `m7-18-claim-tracking.md` (peer-path
> probe) and `m7-18-claim-channel-arena.md` (referee A/B). Both regenerate deterministically
> from committed configs by the commands quoted in their headers.
> Predecessors: `m7-13-capture-postmortem.md` (named the habit), `m7-14-bookv1-strategy.md`
> (measured a model of it).

## 1. The gap

`peer/inbound.py` answered the opponent cop's `capture_claim` honestly and then discarded
the position it carried. `session.belief` — a distribution over *where the opponent is* —
never saw it, even though a claim is truthful by rule (App E 21–22: a false one costs the
game with no appeal) and is a plaintext pre-reveal of a cell already sealed in the same
message's `commit`.

The fix is two lines of behavior: `BeliefFilter.note_claim` collapses onto the claimed
cell, called after `predict()` (the claim names where they *are*, not where they were) and
before the probabilistic evidence — the same position a declared barrier already occupies.

## 2. What it is worth on the real peer path

`scripts/claim_probe.py` plays full mini-games through paired `PeerSession`s — the
production session logic, not a referee model — and at every moment the claim receiver is
about to decide, compares its belief argmax against the claim sender's true current cell.
16 games, seeds 1..31, step cap 60, identical parameters on both sides of the comparison.

| scent model | before (main `25dfd00`) | after | Δ |
|---|---|---|---|
| `multiplicative_book_v1` (**the counted physics**) | 121/389 = **0.311** | 364/389 = **0.936** | **+0.625** |
| `subtractive_chebyshev_v1` (shipped default) | 88/107 = 0.822 | 107/107 = **1.000** | +0.178 |

**The counted physics is where this matters.** Under the book model the belief was right
about the cop's cell barely a third of the time; it is now right on 94% of decisions. Under
the reference model the age-voucher belief was already near-perfect (the M3-3 finding), so
the channel adds little — which is exactly why this had to be measured under both.

Two details worth keeping:

- **52.7% of the sender's turns carried no claim** (205 of 389 — `STAY` and `BARRIER` claim
  nothing). Tracking still reaches 0.936, because a claim collapses certainty and the
  following silent turn's `predict` + honest scent usually keeps the argmax on the true
  cell. The channel does not need every turn to dominate.
- The residual 25 missed decisions are the silent-turn tail, not claim failures.

## 3. What it is worth against a brain — and a correction to the committed model

`config/arena_m7_18.json` isolates the channel: three thief arms, **same brain, same
options**, differing only in information feed. Survivals of 32 under `multiplicative_book_v1`:

| police brain | `evader-fix` (hidden) | `evader-lag1` (truth-lag1) | `evader-claim` (truth, lag 0) |
|---|---|---|---|
| `ref-police` (never met a claim-reader) | 11 | 27 | **30** |
| `police-brain-bookv1` (our deployed generalist) | 23 | 21 | **27** |
| `police-brain-lag1spec` (tuned *against* claim-readers) | 24 | 16 | **23** |
| **aggregate thief points** | 770 | 800 | **880** |

**The committed instrument understated the channel, and the correction changes the
conclusion.** M7-14 modeled claim-reading as `truth-lag1` — "the cop answers a listening
evader with its position one step late". The peer path does not work that way: the cop moves
to cell X, claims X, and *is still at X* when our thief decides. That is lag **0**, and §2
measures it directly (0.936 exact at decision time; the pure `truth` arm is 1.000).

Read at lag 1, claim-reading looked neutral-to-harmful against our tuned cops (21 and 16
survivals, versus 23 and 24 for the hidden feed). Read at the lag that actually occurs, it
is a **gain against every cop in the roster**: +19 survivals against an unadapted cop, +4
against our deployed generalist, and it strips the lag-1 specialist of most of its edge
(16 → 23 survivals; that cop's captures fall 16 → 9).

**Honest bracket on the arm:** `truth` is very slightly optimistic — it grants certainty on
silent turns too, where our thief gets none. §2's 0.936 is the true figure and sits just
below the `truth` arm and far above `truth-lag1`. So the table's `evader-claim` column is an
upper bracket, `evader-fix` the lower one, and reality is close to the upper.

## 4. Consequences

1. **Our thief is now the arm we were tuning our cop against — only stronger.** The
   `police-brain-lag1spec` vector was tuned against a *weaker* opponent than exists. Its
   value against a real claim-reader (9 captures) is materially below its lag-1 number (16).
   Naming this as a follow-up rather than acting on it: **the cop's book-v1 GA pool should
   use the lag-0 arm**, not `truth-lag1`. No cop weights are changed in this milestone.
2. **It sharpens half 2 (M7-19).** The mirror of §2 is that *our* cop hands a claim-reading
   opponent the same 0.936. Half 2 is where that is priced — on series points, across an
   opponent mixture, per the PRD.
3. **The deployed-thief number belongs to the sibling repo.** This repo's configured thief
   is `random`; the tuned `ThiefBrain` lives in `copthief-p2p-thief`, and its M7-16 baseline
   (5/16 survival against the belief-chaser under book-v1) is re-measured there once this
   core change arrives by sync. **Owed, not claimed here.**

## 5. Regression posture

Every previously committed measurement regenerates **byte-identical** after this change —
`m5-arena.md`, `m7-14-bookv1-arena.md`, `m7-14-reference-arena.md` all reproduce with no
diff. That is expected and is the point: the referee path reaches the belief through
information feeds, never through `peer/inbound.py`, and `note_claim` is new code no
existing instrument calls. The change is confined to the peer path it was written for.

## 6. Disclosed limits

- The arena's evader arms are **models** of an opponent, not his build. They bracket a
  threat class; the friendly logs remain the only evidence about his actual thief, and it
  demonstrably ignored our claims.
- `truth` slightly overstates our implementation (§3), `truth-lag1` substantially
  understates it. Neither is exact; §2 is the direct measurement and is what should be
  cited.
- §2's probe runs this repo's configured brains. It measures **belief tracking**, which is
  brain-independent in construction, but the trajectory a game takes is not — hence the
  arena in §3 as the outcome-level companion.
- Nothing here measures a live game against the opponent. Both halves meet a friendly
  before any counted game, per the PRD.
