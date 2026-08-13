# ADR-0014 — M11 part 2: refreshed opponent pool, self-play loop, evader harvest

## Status

Proposed (built on `worktree-m11-part2-selfplay`, 2026-08-13/14; Imree's merge
of the PR is the approval). Strategy/belief layers only — no wire,
canonicalization, or hashing change (constraint 13 untriggered).

## Context

M11's counted validation (nis-yar1, 90–30 6–0) proved the offline-arm method
end-to-end, and deferred four items: the real-opponent pool refresh, a
self-play hardening loop, the claim-threshold re-sweep, and the solver
defer-rate measurement. The mandate carried over from M11: measurement over
deference, including toward M11's own choices; every gate verified to actually
gate.

## Decision

1. **Pool refresh as the gate for everything else** (`m11p2-pool-refresh.md`):
   every modeled arm resynced to a named source sha. The nis-yar1 counted logs
   invalidated both M11 arms (perch → runner; 2 walls → 6 with an exactly
   reproducible diagonal shared-corner rule) — both rebuilt. anrbj666's fielded
   cop AND thief modeled at their HEAD (`41e907d`/`f95b438`, ADR-0011 consent
   basis) as new arms — hunter-cop was their instrument, not their brain. Their
   friendly-overlay DECOYS ("training bait" by their own commits) are recorded
   as a standing warning: model opponents from code at a sha, never from
   friendly tapes. sqak byte-current; vibecode/best2934 stand.
2. **Champion hold-gate before self-play** (`m11p2-pool-arena.md`): GREEN —
   both champions held every M11 number; the refreshed pool surfaced one new
   threat class (anrbj666-police interception + dwell-release: 10/32 vs
   doctrine-m11) and one new bar (anrbj666-thief tops the pool thief table).
3. **Alternating best-response self-play with a per-phase pool gate**
   (`scripts/selfplay_loop.py` + `selfplay_gate.py`, trajectory in
   `m11p2-selfplay.md`): a harvest replaces a champion only if it
   holds-or-improves against EVERY pool arm and beats the champion's fitness.
   A `candidate_feed` GA door was added first so candidates evolve under the
   fielded sharp tier, not the hidden default.
4. **Evader champion FLIPPED** (the round-1 harvest): survival vs police-m11
   3/32 → 18/32; the anrbj666-police gap closed 22/32 → 32/32; all other arms
   held at 32/32. `config/arena.json` carries the knobs; the thief repo's
   `game.toml` + runbook dirs inherit via the post-merge propagation ritual.
5. **Cop champion KEPT — negative result with numbers**: the GA's best cop
   (fitness 0.958 vs 0.792) regressed vs doctrine-m11, vibecode-thief and
   sqak-evader; the pool gate refused it twice. This is the
   beats-ourselves-loses-to-real-opponents failure mode, caught by design.
6. **Claim threshold 0.1 KEPT with data** (`m11p2-claim-sweep.md`): 0.05–0.25
   point-identical under the M11 stack; always-claim donates ~3.3 pts/game to
   a claim-reading anrbj666-class opponent; silence still catastrophic.
7. **Solver node cap 20000 KEPT with data** (`m11p2-solver-defer.md`): 3125
   solver calls across the pool, zero budget-aborts at a 25x rescue cap —
   every defer is a proven no-proof.

## Consequences

- Offline numbers are predictions until a live game validates them — standing
  caveat; the harvest's first live outing is the validation.
- The hardened evader knobs must hand-propagate to the thief repo's
  `game.toml` and all runbook config dirs (v1.06 → v1.07) after the sync —
  config never travels with the mirror. Sparring stays generic, never tuned.
- The GA fitness pool now carries modeled rivals; any future pool-refresh
  invalidating an arm invalidates loop results built on it — refresh first,
  loop second, always.
- The plan-level diversity stretch item was NOT built: champions changed this
  session, and a diversity mechanism must be costed against the final stack
  (deferred, not declined).

## Alternatives

- **Trust the friendly tapes for anrbj666 arms**: rejected — their decoys
  poison exactly that source; code-at-a-sha is the only clean basis.
- **Adopt the higher-fitness cop anyway**: rejected — the pool gate exists to
  outrank fitness; three real-opponent regressions are disqualifying.
- **Widen the solver cap "just in case"**: rejected — the probe measured zero
  starved proofs; a bigger cap buys nothing and costs turn time.
