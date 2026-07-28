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

---

## 9. Amendment — named scent models (M3-8)

> **Status: APPROVED and BUILT** (gate PR #56, main `ee8a78a` = Imree's approval; built at
> M3-8 in ADR-0004 v2's order). Sections 1–8 describe the shipped M3-2
> layer and remain accurate for the default model. Trigger: M3-7 decision "REVISE"
> (Imree, 2026-07-18). Interop counterpart: kit PR #7 (SPEC §5.1 + §7).

### 9.1 Provenance settled: `min_center_intensity` is a reference term, not a book parameter

M3-7 left this open with an instruction not to inherit either side's assertion. Checked against
both primary sources:

- **The book never mentions it, in any spelling.** Its own `game.json` listing (App B) prints
  exactly three pheromone keys — `pheromone_center_intensity: 0.9`, `pheromone_decay: 0.10`,
  `pheromone_grid_size: 5`. The App F binding table's pheromone block (table 16) lists the same
  three, all `קבוע` (fixed).
- **The reference introduces it.** `config/*/game.json` ships
  `pheromone_min_center_intensity: 0.5`; `shared/config.py:67-68` maps it to
  `smell.min_center_intensity`; `peer/sealing.py:20` includes `min_center_intensity` in the
  14-key signed `TERMS_KEYS`.

**Conclusion.** It is a **reference-introduced signed term**. Three consequences:

1. **App F does not bind it** — it has no row, so neither the `קבוע` nor the minimum-raise rule
   applies. Constraint #15's App F guard therefore has nothing to enforce here; its value is a
   negotiable term whose de-facto default is the reference's `0.5`.
2. **It stays in our terms regardless of model.** The key set is reference-frozen; dropping the
   key breaks the terms signature against every reference-derived peer.
3. **Under `multiplicative_book_v1` it is inert** — the book's `Δτ` is the kernel, unconditioned
   by any minimum, so the key is carried for signature compatibility and gates nothing. Under
   `subtractive_chebyshev_v1` it keeps its §2.2 emission-gate behaviour unchanged.

### 9.2 The second model — `multiplicative_book_v1`

Spec facts contributed by **anrbj666 (Alon Engel, Renat Karimov)**; every value re-derived here
from book ch.4 and App F before adoption, per the verify-before-accept rule.

- **Update, once per FULL turn** (after both agents have moved — the book's own cadence, ch.4):
  `τ′ = clamp((1 − ρ)·τ + Δτ, 0, center_intensity)`, `ρ = 0.10`, `center_intensity = 0.9`.
- **`Δτ` is the verbatim 5×5 figure-4 kernel** — centre `0.90`, orthogonal `0.62`, diagonal
  `0.42`, then `0.20 / 0.14 / 0.04`. Pinned as a table, not a formula: see ADR-0004 v2's
  alternatives for the disjoint-σ-window evidence.
- **The upper clamp is not in the book's printed formula**, which shows only `max(0, ·)`. It
  comes from the book's separate declaration that τ is continuous in `[0, 0.9]`. Without it a
  saturated cell that decays and is deposited on again reaches `0.9·0.9 + 0.62 = 1.43`, outside
  the book's own stated range. Re-derived independently; matches the partner's relayed case.
- **Empty start · end-of-turn anchor · decay-then-deposit · no receiver-side pass · no rounding.**
- **Not transmitted.** Each side recomputes the rival's field from revealed actions.

### 9.3 Design delta

- **`ScentModel` named object.** `domain/scent` gains a model protocol with two implementations;
  `ScentField` delegates emission, decay, rounding and clamping to it. `subtractive_chebyshev_v1`
  stays the default — behaviour against the reference peer is byte-identical to today.
- **Cadence policy.** The two isolated decay calls in `peer/turns` (the M3-7 seam assessment)
  become a model-driven policy: which pass runs, and whether a received field decays at all.
- **Belief parameterization.** The exact-Bayes scent likelihood reads its falloff shape from the
  selected model instead of assuming Chebyshev-linear (PRD_belief §3).
- **Handshake lock.** Doc built to the kit §7 schema, hashed, declared as `scent_model_sha256`;
  refusal **only when both peers declare and disagree** (omission is never refusal).
- **Step-0 sealing.** The model hash enters the step-0 sealed spec record (M6-3), closing v1's
  gap that the doc was logged but not commit-bound.

### 9.4 Test plan (TDD; DoD of M3-8)

Conformance: the kit's `locked_model.json` and `scent_book_v3.json` fixtures join
`tests/conformance/` as permanent keyless CI in **both repos** (constraint #13) — kernel,
clamp case, scalar chain, field walk, the model-divergence pin, the doc-schema hashes, and the
five-row refusal truth table. Unit: model selection from config · book-model update incl. upper
clamp and no-rounding · pinned evaluation order · empty start · cadence policy per model (the
received-field pass runs for one model and not the other) · belief likelihood follows the model ·
lock doc byte-shape · refusal matrix incl. both-silent and one-silent · step-0 seal carries the
hash. Coverage ≥ 90% on the model code, files ≤ 150 lines, `mypy --strict`, ruff.

### 9.5 Acceptance criteria (binary)

- Kit `locked_model.json` + `scent_book_v3.json` vectors green in keyless CI, both repos.
- Default path unchanged **in game bytes**: against a peer that declares nothing, every
  turn message, smell grid and sealed game record is byte-identical to the pre-M3-8 tree
  (regression-pinned). The **negotiate extras deliberately do change** — kit SPEC §7 puts
  only `scent_model_sha256` on the wire, never the document — because a declaration the
  partner team cannot compare is not a lock. See ADR-0004 v2's consequences.
- Both-declare-and-differ refuses at handshake; every other combination plays.
- Step-0 sealed record carries the model hash; replay verifies it.
- **Per-model belief eval rerun and committed** — `docs/evidence/m3-belief-eval.md` now
  carries a table per registered model. **Re-measured result: the book model costs most of
  the filter's edge** (mean belief error 0.9001 vs the reference form's 0.7314, against a
  0.9429 baseline; argmax hit-rate 17% vs 98%). Two separable causes, probed not assumed:
  its ADDITIVE kernel with an upper clamp saturates 12 of 49 cells at 0.9 by turn 4 on the
  signed 7×7 board (inherent to the registration), and our voucher heuristic reads
  intensity as age, so a fresh ring-2 cell inverts to age 14 (our machinery, improvable).
  This is a live input to the counted-series negotiation, not a settled verdict on the
  book's physics.
- ADR-0004 v2 committed.

---

## 10. Amendment — the in-play frame validity check (M7-23)

> **Status: APPROVED (PR #86 merge = the gate, 2026-07-28; §10.6 decisions taken by Imree:
> gate ON / no escalation / tally rides settlement) and BUILT (M7-23), with ONE correction
> discovered during the build — see the gating bullet in §10.2.** In short: the plan
> assumed the check is structurally inert under a book-v1 lock (`transmitted: false` ⇒ no
> inbound grid). Probing the tree showed otherwise: our SENDER transmits unconditionally
> (`peer/turns.py` mirrors the reference's unconditional send()) — the locked doc's
> `transmitted: false` is honored on receive only — and belief consumes the arriving grid
> (`peer/inbound.py`). So under the counted physics, grids ARE on the wire and the check
> matters most there; the shipped gate follows the ARRIVING grid, not the model flag. The
> sender-side doc↔behavior mismatch itself is a separate open decision (TODO M7-24).
> Trigger: the opponent team's (anrbj666) 2026-07-27 scent-inversion memo, which shipped
> the defensive half of this check on their side and raised the rest with us rather than
> using it. Every claim in it was re-derived here before adoption (verify-before-accept):
> their transition inversion reproduces **224/224 frame pairs to exactly one emitter
> candidate under BOTH registered models** — including 30-turn fully-saturated dwells at
> centre and corner — so the construction is model-independent, and round-3 quantization
> does not blur it. Their kernel arithmetic verified against our locked registry (21/25
> offsets at `Δ ≥ ρ·centre`; the four 0.04 corners never saturate, unclamped fixed point
> 0.40). §5's SQ3 posture and the M6-7 audit-time check are unchanged by this amendment.

### 10.1 What the check adds (and what it deliberately does not)

The transmitted grid rides beside `commit`, unauthenticated (§5). Today the receive path
absorbs whatever arrives: a stale field from a peer restarting mid-series, a malformed
grid, or a decoy degrades the belief silently and is only ever *seen* by the M6-7 check —
after the game, against revealed positions, evidence-grade. The inversion gives the same
physics a second, in-play use: across two consecutive frames from one peer the entire
history cancels, and a frame that **no** emitter cell can explain is provably not the
output of a rules-following peer — detectable at the moment it arrives, with no knowledge
of the opponent's position.

**Non-goals, load-bearing:** the same scan that validates also *localizes* (their §2; our
verification). This check must not become that. The `info_mode: belief` posture offered to
the opponent team on 2026-07-27 — the field reaches decisions only through the
probabilistic belief layer, no deterministic inversion pin — binds our own build first.

### 10.2 Mechanism

- **Pairing is trivial in our architecture.** The M7-8 sequencer accepts strictly in
  order, so every accepted frame's predecessor is the previous accepted frame
  (`session.inbound[-1].smell_grid`); step 1 pairs against the locked doc's
  `initial_field: "empty"`. The opponent memo's single-frame plateau fallback is therefore
  unnecessary here and is out of scope. Terminal caught-final messages are skipped (game
  over; also the M5 repeated-step convention).
- **Candidate scan:** for every board cell `e` — **barrier cells included**: our own
  sender deposits from its unchanged cell on a barrier turn (`peer/turns.py`, reference
  `send()` path alike), so excluding walls rejects honest frames — predict one advance of
  the previous frame under the locked model and compare every cell. Any candidate within
  tolerance ⇒ **accept**, stop scanning. Zero candidates ⇒ **refuse**.
- **Compare mode dispatched on `model.rounds`, exactly as M6-7:** slack 0 for the
  rounding reference form; `scent_physics_tolerance` for `multiplicative_book_v1` (75/534
  last-bit finding, ADR-0004 v2). **[CORRECTED AT BUILD, 2026-07-28]** the gate follows
  the ARRIVING grid (`frame_check` AND a non-empty `smell_grid` AND not the terminal
  message) — NOT the model's `transmitted` flag as first planned, because the probe
  showed grids on the wire and in the belief under a book-v1 lock (see the status note).
- **Refusal refuses the WHOLE frame** (their §4.3, adopted): `absorb` and `update_scent`
  are both skipped — half-believing an impossible field is how a bad one steers you.
  `known_field` still decays (time passed); predict/claim/hint evidence is untouched
  (separate evidence classes). One JSONL event `scent_frame_refused` `{step, cells}` per
  refusal, so refusals surface at the mutual audit, not only in a console. **A refusal
  never flips a result, never collapses belief, never touches the state machine** — the
  same evidence-grade class as M6-7 (SQ3).
- **The firewall (§10.1):** the validator's public surface returns accept/refuse plus the
  refusal diagnosis only. The matched candidate cell never leaves the function, is never
  logged, and never reaches belief or a brain. Pinned by test.
- Cost: ≤ `grid_size²` candidates × window cells per frame — negligible.

### 10.3 Design

Pure validator in `domain` (no I/O/clock/config reads; model + params as arguments,
constraint #5), one gated call site in `peer/inbound.py` before the absorb/update pass.
Mirrored core ⇒ the build owes the sync ritual; tests role-blind (both roles receive
grids). Config: a `frame_check` gate under game.toml's scent settings — private, unsigned,
never on the wire; tolerance reuses the existing `scent_physics_tolerance` key (same
physics-compare semantics as M6-7; no new numeric anywhere in code).

### 10.4 Test plan (TDD; DoD of M7-23)

Property (both models): honest random-walk frame sequences — moves, STAYs, barrier turns,
edge/corner clipping — are **never** refused (the false-positive property; a false
refusal is worse than no check). Unit: single perturbed cell refuses · a stale frame
(decayed twice / duplicated) refuses · step-1-vs-empty accepts and its forged variant
refuses · terminal skip · refusal leaves session state identical except the log event ·
the firewall pin (no public surface yields a cell) · book-v1 gate inert. Integration:
full local series with the check ON — zero refusals, game bytes byte-identical to
check-OFF (wire-silent; we change nothing we send); an injected-corruption game logs the
event and completes normally. Coverage ≥ 90%, ≤ 150-line files, `mypy --strict`, ruff.

### 10.5 Acceptance criteria (binary)

- False-positive property green in keyless CI, both models, both repos (post-sync).
- Injection game: refusal logged, game completes, outcome unchanged.
- Check-ON default series byte-identical on the wire to check-OFF.
- Firewall pinned: no candidate cell on any public surface or log line.
- Disclosure: the check proves impossibility only to us (unchanged SQ3 stance — the
  commit-binding amendment that would upgrade it is a joint wire matter, tracked with the
  opponent team, not this milestone). `KNOWN_LIMITATIONS.md` is the M8 triad deliverable
  and does not exist yet; this entry and the M7-24 sender-side mismatch are queued for it
  here, where the M8 session will collect them.

### 10.6 Open decisions (Imree's, not taken silently)

1. **Default posture of the `frame_check` gate** — recommend **ON**: abstention-safe (an
   accepted frame is the status quo; a refused one withholds one evidence class for one
   turn from a belief that never eliminates anyway), and the FP property is the evidence
   the recommendation stands on.
2. **Escalation on repeated refusals** (their memo suggests acting only after two
   consecutive) — recommend **NONE**: our refusal is already per-frame and low-stakes;
   evidence-grade logging only, no game-level consequence ever (SQ3, M6-7 class).
3. **Whether the refusal tally also rides the settlement/dispute emission** beside the
   M6-7 mismatches — recommend **YES** (one more line in `emit_scent_physics`'s file,
   built in the same milestone).
