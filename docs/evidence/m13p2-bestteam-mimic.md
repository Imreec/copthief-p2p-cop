# bestteam-thief mimic — construction and honest fidelity (M13p2, ADR-0017)

## Source and method

Re-derived from their PUBLIC repos (their own disclosure practice), ADR-0011 method —
policy re-implemented against our seam, no code copied:

- `github.com/Diana-Koroblov/bestteam-thief`, HEAD `a59fa05` (2026-08-16 19:43 +0300);
  members Itay Malich, Diana Koroblov. Their played commit `f1e3095c…` exists only in
  their private monorepo (the public repos are `sync_from_repos.py` mirrors), so HEAD
  is the closest public tree; their thief strategy code last changed 2026-08-05.
- Study performed by executing their code offline (scratchpad clone, read/execute
  only, nothing enters any repo).

## Their policy (as re-implemented in `strategy/bestteam_thief.py` + `bestteam_eval.py`)

Candidates STAY,N,S,E,W (their insertion order); root score
`value_of(dest, depth 2) − 4.0·trail.cost_at(dest)`;
`value_of = belief[dest]·(−1000) + (1−belief[dest])·lookahead` over the destination-
masked, renormalized, predict-spread belief; leaf
`−400·capture_risk − 25·seal_pressure + 2·|reach₅| + 30·has_cycle + 1·E[dist]`;
tie window 0.1 in candidate order, seeded draw (fires 1–3×/game — near-deterministic).

Facts with league value, all verified in their code:
- **No claim-reading**: our `capture_claim` never reaches their belief (their compat
  path only equality-checks it against their own cell) — per-pairing claim 0.0 leaks
  nothing to their thief.
- **No rule-47 concession on the played path**: their compat `turns` path never
  consults their own `rules.sealed_in`; their native path does. The league ask is
  precise and cheap for them.
- **Their belief runs on our scent TWO steps stale** (they move first); barriers
  apply at one step. Arena feed: `truth-lag2`.
- Their g02 "corner camp" was 16 turns of FORCED STAY inside our completed cage
  (`exit_count == 0` from step 20; their own `is_immobilised` returns True).

## Fidelity — the honest numbers

**Golden oracle**: their own code, driven offline over the tapes with correctly
reconstructed inputs, reproduces the live tapes at **103/105 = 98%** (residuals: one
seeded tie-draw, one 1.6-point divergence). That is the ceiling any mimic can aim at.

**Our mimic vs the golden fixture** (their code's own per-step belief/trail/scores,
70 steps, committed at `tests/unit/strategy/bestteam_golden.jsonl`):

| metric | value |
|---|---|
| tie-aware move agreement | **57/70 = 81%** |
| mean per-candidate score deviation | 5.4 (on a ~50-point scale) |
| worst deviation | 53 (g6 s13, wall-adjacent state) |

A variant search over recursion semantics (predict with/without STAY, renorm, spread
placement) plateaus at 57/70 — the residual sits inside their `evaluate` details at
WALL-ADJACENT states, which is exactly the cage-relevant region.

**Consequence, stated plainly (ADR-0017): 81% < the 90% bar. Every arena number
measured against this arm is DIRECTIONAL, not a projection. The live friendly is the
decisive test; the fidelity floor (≥57/70) is pinned in CI so the arm cannot silently
regress further.**

Regenerate the fixture: the extraction recipe lives in the M13p2 session notes; the
golden lines were produced by their code and committed verbatim.
