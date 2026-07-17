# PRD — Scent layer (mechanism PRD, milestone M3)

> **Status: DRAFT (gate M3-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-4,
> `docs/PLAN.md` §8. Sources of truth: book ch.4 (scent) > the **conformance kit** §5
> (pheromone vectors, byte authority) > **M2 spike observations of the running reference**
> (`docs/evidence/m2-oracle-spike.md` §3 SQ1, oracle sha `960499fd`). Covers TODO **M3-2**;
> feeds M3-3 (belief consumes the field) and the peer loop (transmitted grids). ADR-0004
> (scent-model form) lands with the code.

## 1. Scope & non-goals

**In scope (M3-2):** `copthief_core/domain/scent` — the emission/decay/merge field, its
wire snapshot/absorb forms, and the locked-model document (formula + numeric example)
exchanged at handshake per PLAN §4. Kit `pheromone.json` vectors join
`tests/conformance/` (constraint #13).
**Non-goals:** belief-side interpretation (PRD_belief) · hint text (M3-4) · rendering
(M4) · any anti-fabrication verification (the grid is unauthenticated — SQ3; the
post-audit physics check is PLAN §4 audit scope, M4/M5).

## 2. The locked model (kit-pinned; spike-confirmed against the running reference)

The kit pins the **reference form**; the book's prose describes multiplicative decay —
the release's own reference implements **subtractive** decay, and the kit SPEC documents
that contradiction and pins subtractive (academic-freedom choice, restated in ADR-0004
and the M8 README narrative).

1. **Emission (radial, Chebyshev):** depositing intensity `I` at cell `c` over the
   `M×M` window (`M = pheromones.pheromone_grid_size`, `half = M // 2`):
   `value(cell) = round(max(0, I − falloff · ring(cell)), 3)` where
   `falloff = I / (half + 1)` and `ring` is the Chebyshev distance from `c`;
   off-board cells are clipped. Merge into the trail is **max-wins** per cell.
2. **Emission gate:** `I` must be ≥ `pheromones.pheromone_min_center_intensity`
   (signed schema-1.3 key, M2 F4) — depositing below the gate is a hard error.
3. **Decay (subtractive):** every tick subtracts `pheromones.pheromone_decay` from every
   known cell, clamped at 0, rounded to 3 decimals.
4. **Wire forms:** `snapshot()` = `{"r,c": value}` for strictly-positive cells only;
   `absorb(grid)` = max-merge of a received snapshot, ignoring off-board keys.

**Timing (SQ1, observed):** the mover deposits AFTER applying its move, at the NEW
position, with `I = pheromones.pheromone_center_intensity`; then the whole own-trail
field decays ONCE; then the snapshot travels with the TurnMessage. The receiver absorbs
the grid, then decays its known-field once per received message. Consequence (numeric
example with the shipped config values 0.9 / 0.1 / 5×5, for the locked-model doc): a
just-laid center transmits at `0.9 − 0.1 = 0.8`, its ring-1 at `0.6 − 0.1 = 0.5`,
ring-2 at `0.3 − 0.1 = 0.2`.

## 3. Design (two fields per peer, one module)

`domain/scent.ScentField` (pure, no I/O/clock): construction from the pheromone params;
methods `deposit(cell, intensity)`, `decay()`, `absorb(grid)`, `snapshot()`,
`intensity_at(cell)`. Each peer holds **two instances** — `own_trail` (what we emit;
only its snapshot ever crosses the wire, never a coordinate) and `known_field` (what the
opponent transmitted; input to belief). The peer loop wires SQ1's order:
`apply move → own_trail.deposit(new_position, center_intensity) → own_trail.decay() →
snapshot into the outbound TurnMessage`; inbound: `known_field.absorb(msg.smell_grid) →
known_field.decay()`.

The session's current `smell_grid={}` placeholder is replaced by the real snapshot; the
wire layer is untouched (grids already validated by `check_smell_grid`).

## 4. Locked-model document (handshake artifact, PLAN §4)

A small canonical dict — formula name (`"subtractive_chebyshev_v1"`), the four config
values, and the §2 numeric example — hashed with the standard canonical form and
exchanged/logged at handshake so a scent-model dispute is diagnosable to a hash, not to
prose. Byte-shape pinned by a unit test; the exchange itself rides the existing
negotiate extras (tolerate-unknown keeps the reference compatible — it will ignore the
extra key; ours logs both).

## 5. Interop & fabrication posture

- **The transmitted grid is UNAUTHENTICATED** (SQ3, observed: not sealed, not even in
  the reference's log artifact). The scent layer therefore never treats an absorbed grid
  as ground truth — that stance lives in the belief PRD; scent just stores and reports.
- Our own emissions are honest by construction (deposit exactly at our position with the
  signed intensity) — anything else would be exposed by the post-audit physics check any
  competent opponent can run against our sealed positions.
- Reference tolerance: it max-merges whatever we send and never validates ring shape —
  the kit vectors, not the reference's runtime behavior, are the correctness bar.

## 6. Configuration

All quantitative values from the signed `pheromones` section (constraint #5); the module
takes them as constructor arguments — no config reads inside `domain` (purity).

## 7. Test plan (TDD; DoD of M3-2)

Conformance: every kit `pheromone.json` vector reproduced by our field (CI-blocking,
both repos). Unit (happy + error): emission ring math incl. corner/edge clipping ·
falloff derivation from grid size · min-center gate raises below threshold · max-merge
(fresh deposit never lowers an existing stronger cell) · subtractive decay with clamp-0
and round-3 · snapshot sparsity (no zero cells, `"r,c"` keys) · absorb ignores off-board
keys and max-merges · SQ1 order property: deposit-then-decay yields the §2 transmitted
values · determinism (no RNG). Coverage ≥ 90%, files ≤ 150 lines, `mypy --strict`, ruff.

## 8. Acceptance criteria (binary)

- Kit pheromone vectors green in keyless CI **in both repos** (post-sync).
- A peer-loop game transmits non-empty grids whose values match the §2 example for the
  shipped config (integration assertion over the queue transports).
- ADR-0004 committed (subtractive-vs-multiplicative contradiction + kit adoption).
- The locked-model dict hashes identically on both our peers in tests.
