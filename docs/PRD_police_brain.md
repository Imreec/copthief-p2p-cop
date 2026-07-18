# PRD — PoliceBrain (mechanism PRD, milestone M5) ⚑ police repo

> **Status: DRAFT (gate M5-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-6/FR-12
> + §2 (strategy = "the core of the grade"), `docs/PLAN.md` §8 + §13 M5. Sources of truth: book
> ch.6 (strategy module, pp.57–68) · M2 spike SQ2 (`docs/evidence/m2-oracle-spike.md` §3) ·
> reference `domain/brains.py` + `domain/belief.py` @960499fd (**oracle for behavior comparison
> only**, ADR-0002) · ADR-0005 (strategy track: belief+search, lands with this gate). Covers TODO
> **M5-2** plus the role-neutral core groundwork every M5 task stands on (Decision seam, reference
> arena opponents, scenario suite, per-role rosters). Sibling: `docs/PRD_thief_brain.md` in
> [copthief-p2p-thief](https://github.com/Imreec/copthief-p2p-thief) (approved together — the two
> PRDs share §2–§4 semantics; role algorithms differ).

## 1. Scope, role split, non-goals

**The role split (⚑ this PRD's first binding decision):** `PoliceBrain` lives in
`src/copthief_police/` — the role package this repo owns. Role packages are **NOT mirrored**
(ADR-0001; `sync_core.py` MIRRORED list): each repo builds its own brain, in its own tree, with
its own tests under `tests/role/` (per-repo by design — the mirrored test trees must never name
role-specific files, PR #29 lesson). What lands in **core** (`copthief_core/`, police-lead,
synced) is only the role-neutral machinery both repos need: the Decision seam extension (§3), the
re-derived reference-heuristic arena opponents (§2), referee/arena barrier support and the
scenario suite (§4). Core never imports a role package — role brains reach the arena and the peer
loop via the book's `package.module:Class` config notation (§5).

**In scope (M5-2):** `copthief_police.brain` — expectimax over the belief + barrier graph-surgery
+ the capture-commit policy (§3 reconciles "claim policy" with SQ2); the core groundwork above;
the outbound barrier path in the peer turn loop (we have never *placed* a barrier on the wire —
F9 only made us *respect* inbound ones); DoD evidence + champion-pin update.

**Non-goals:** scent/belief internals — **M3-8 stays blocked** (Alon inputs + PRD_scent amendment
+ ADR-0004 v2); brains consume `BeliefFilter` through its public read surface only (PRD_belief
§7) and never touch the Bayes/scent math · RL as decision foundation (ADR-0005; book §6.3: RL is
optional and was not taught — belief+search chosen) · LLM-decided moves (App E rule 25 + book
§6.5's warning; the book's mutual-consent exception is **not taken** — documented posture) · the
thief algorithm (sibling PRD) · wire-contract changes (`barrier_placed` exists since M1-5;
§3 uses it outbound for the first time — constraint #13 applies, see §7) · genetic tuning runs
(M5-4 executes; §5 fixes the weight→config interface it needs) · profiling (M5-5; §6 fixes the
seam) · template-bank A/B (M5-6, thief-led).

## 2. The DoD opponent: the reference heuristic, re-derived as an arena brain

The ≥60% DoD (PRD G3, PLAN §13 M5) is measured **against the reference's shipped heuristic** —
which our arena cannot import (EULA, ADR-0002: reference runs as oracle only; no code reuse
beyond attributed micro-snippets). So M5's first build step **re-derives both reference brains as
core arena opponents** (`ref-police`, `ref-thief`), interface-mirrored from the observed behavior
of `domain/brains.py` @960499fd:

- **`ref-thief`:** move to maximize move-distance to the belief argmax; tiebreak prefers cells
  not yet visited (the brain keeps its own visited set); final tiebreak deterministic on our
  sorted move order (the reference ties break on its `Direction`-enum order — an implementation
  accident, not strategy; documented micro-delta).
- **`ref-police`:** move to minimize move-distance to the belief argmax; when barrier quota
  remains, with probability `ref_police_barrier_chance` (reference class default `0.15`,
  attributed) it **walls the cell it would have stepped onto instead of moving** (a barrier turn
  moves nothing — reference `MoveType.BARRIER` semantics, confirmed in `own_state.apply_move`).
  Seeded RNG; capture claims are automatic on MOVE turns only (SQ2).
- Move-distance under our signed orthogonal `move_set` is Manhattan (reference `Board.distance`
  is Manhattan whenever diagonal play is off — same metric, no adaptation needed).

**Perception is held fixed — the second binding decision.** In our arena both sides read **our**
`BeliefFilter` (argmax = the reference's `most_likely()` analog). We deliberately do **not**
re-derive the reference's multiplicative `BeliefGrid`: that is the named-scent-model territory
M3-8 owns (blocked), and holding the perception layer identical on both sides makes the DoD
isolate what M5 grades — decision-layer strength. Consequence, disclosed: our "reference
heuristic" opponent is the reference's *policy* over a *stronger* belief than the reference
ships, i.e. a **harder** opponent than the literal reference peer — beating it ≥60% is evidence
in the safe direction. (Documented as an academic-freedom choice per CLAUDE.md; revisited only if
M3-8 unblocks and lands `multiplicative_book_v1` belief parameterization.)

## 3. The Decision seam (core; SQ2 reconciliation)

`BrainBase` today returns a bare move string; barriers need a richer action. Core grows a frozen
`Decision` dataclass — `move: str` **or** `barrier: Coord` (exclusive; a barrier turn keeps
position, mirroring the reference) — and `BrainBase.decide(observation, belief) -> Decision`, a
template method that: delegates to `_decide(...)` (default: wrap the existing `_pick_move`, so
`RandomBrain`/`GreedyManhattanBrain` behavior stays **byte-identical** — the M1-walk equivalence
pin must stay green untouched); clamps barrier proposals through `rules.is_legal_barrier` and
degrades an illegal barrier to the legality-clamped move (never stall); enforces quota.
`Observation` grows `barriers_used`/`max_barriers` (dynamic state; static game parameters arrive
at construction, §5).

**Capture-claim policy = move selection (PLAN §8 refined by SQ2).** The spike proved claims are
free, automatic per-MOVE probes answered honestly (lying = audit forfeit); there is no claim
*cost* to threshold. PLAN §8's "claim policy thresholded on belief mass" therefore lands as a
**capture-commit rule inside move scoring**: when a reachable cell holds belief mass ≥
`p_commit`, stepping onto it dominates herding — the claim itself rides the wire automatically
(peer layer, unchanged). The sealed-record encoding for our barrier turns (`move` value, state
string already carries the barriers list) is chosen at build time to stay self-consistent with
our replay verifier — the reference seals `"BARRIER:<dir>"`, ours mirrors our existing move
alphabet; the audit re-hashes bytes, not grammar (M2-observed), and rule-19 mutation coverage
extends to barrier turns.

## 4. Arena upgrades: barriers, scenarios, per-role rosters (core)

1. **Referee barrier support:** `play_referee_game` applies police `Decision`s — barrier →
   `board.with_barrier` + both beliefs' `note_barrier` + quota bookkeeping from the constitution;
   capture-by-barrier and imprisonment already resolve in `rules.check_end` (M1-2). Baseline
   brains never place barriers → existing referee outputs stay identical (regression-pinned).
2. **Scenario suite — the third binding decision.** Our brains and `ref-thief` are deterministic
   given a seed; on the fixed signed starts a head-to-head series degenerates to one repeated
   game (win-rate 0% or 100%). A meaningful *rate* needs varied scenarios, so the DoD series runs
   a **seeded start-scenario suite** (HW6 GA fitness-suite precedent, ADR-0002-attributed
   salvage): per seed, sample a legal start pair (uniform, distinct, Manhattan separation ≥
   `start_min_separation`) with the constitution's canonical starts always scenario #1.
   Referee-mode only — live games play the signed constitution untouched; the suite is an
   evaluation instrument, committed as config so the table regenerates byte-identically.
3. **Per-role rosters.** `run_round_robin` currently plays every brain in both roles — meaningless
   for role-specific brains (`ref-police` as thief would chase the cop). The arena takes
   `police_roster` × `thief_roster`; standings/champion-gate logic unchanged.
4. **Config-driven arena.** Roster names, seed set, scenario parameters, DoD threshold move from
   the mirrored script/test literals into per-repo `config/arena.json` (versioned, loader-
   validated) — required by the role split (this repo's roster names `copthief_police` classes;
   the thief repo's names theirs; the mirrored integration tests read whatever the local config
   lists — PR #29 rule) and by constraint #5 (no quantitative values in code).

## 5. PoliceBrain algorithm (`copthief_police.brain`)

**Root actions:** legal moves + the best barrier candidate (if any clears its threshold).
**Search — expectimax over the belief (book §6.3.1's "your own heuristic algorithm" track):**
truncate the belief to its top-`search_top_k` cells (renormalized); the opponent's *position* is
a chance node (expectation over that support — epistemic uncertainty); the opponent's *action*
from each supposed cell is adversarial (min over its legal replies — the thief knows where it
is); our levels maximize; depth `search_depth` of our-move plies. Leaf evaluation = config-
weighted feature sum: captured belief mass on our path (incl. barrier-on-cell and imprisonment
completions) · expected Manhattan distance to the belief mass (full distribution, not argmax —
our edge over `ref-police`) · opponent expected mobility · belief-weighted size of the thief's
safe reachable region · barrier budget remaining. **Barrier graph-surgery:** candidates = our
cell + orthogonal neighbors (the barrier law, `rules.is_legal_barrier`); each candidate scored by
the belief-weighted reduction it inflicts on the thief's reachable component (BFS from each
support cell with the candidate added) — corridor/articulation cuts naturally dominate; a
candidate enters the root only when its gain ≥ `barrier_gain_threshold` (quota is spent on
surgery, never on the reference's coin-flip). **Capture-commit:** §3's `p_commit` rule overrides
distance-herding. Deterministic given seed; worst-case node count `top_k × |moves|^(2·depth)` is
trivial on ≤100 cells — a perf test asserts the per-decision budget from config, generous, no
flakes.

**Weights → config, never code (constraint #5 + M5-4's interface):** all weights and search
parameters live in `game.toml [strategy.police]` (private, never signed, never crosses the wire)
with loader defaults; the M5-4 GA rewrites exactly this weight vector (fixed feature order,
per-gene bounds — HW6 genome pattern) and commits its artifact + fitness curve. Tuned weights
never deploy to the sparring host (generic brain only — CLAUDE.md §9).

## 6. Configuration & factory

`make_brain` accepts core names (`random`, `greedy-manhattan`, `ref-police`, `ref-thief`) **or**
the book §6.2 dotted notation `package.module:Class` (e.g.
`copthief_police.brain:PoliceBrain`) — core stays role-blind; `game.toml [strategy]
police_class` and `config/arena.json` roster entries use it (display alias per entry for tables
and the champion pin). The factory hands brains a params object assembled from the constitution +
`[strategy.*]` (baselines ignore it). **M5-5 seam:** profiling output adjusts per-opponent trust
weights (`[belief]` hint/smell trust) and `[strategy.police]` priors via config — the belief math
itself stays untouched (M3-8 boundary).

## 7. Interop & process guards

Outbound barrier turns are our first wire-visible *new behavior* since M3: `barrier_placed` is
already schema-mirrored and F9-validated inbound, so the **wire contract does not change** — but
constraint #13 still applies to the sealed-record shape: conformance/kit vectors re-run in CI,
the rule-19 replay mutation matrix extends to barrier turns, and the first friendly after M5-2
should re-confirm mutual audit against the reference cop pairing (reference cop places barriers —
our thief survived 7 of them in `m3-full-pairing`; now the mirror direction). Champion gate:
adding `ref-*` opponents and `PoliceBrain` to the roster may dethrone `greedy-manhattan`; any
dethroning updates `config/arena_champion.json` **in the same PR** with the regenerated table as
evidence (CLAUDE.md §5 / process rule).

## 8. File & test layout (≤150-line files)

Core (mirrored, synced post-merge): `strategy/decision.py` (Decision + clamps) ·
`strategy/reference_brains.py` (attributed re-derivations) · referee barrier/scenario extensions
(split `referee.py` as needed — it is at 139 lines) · `sdk/arena` per-role roster + config loader.
Role (this repo only): `copthief_police/brain.py` + `features.py` + `barriers.py` + `search.py`
as size demands; tests under `tests/role/police/` (unit + the DoD integration series). Mirrored
tests exercise core pieces with core brains only; the arena integration tests read
`config/arena.json` so each repo tests its own roster.

## 9. Test plan (TDD; DoD of M5-2)

Unit: Decision clamps (illegal barrier degrades to move; quota exhausted → move; never stall) ·
`ref-thief`/`ref-police` behavior pins (flee/chase the argmax; unvisited tiebreak; barrier-
instead-of-step under seeded RNG; claims only on MOVE) · expectimax picks the certain capture ·
capture-commit fires at `p_commit` · barrier surgery seals a corridor scenario and withholds
below threshold · determinism per seed · baseline byte-identity regression (M1 walk pin).
Property: decisions always legal; barrier count never exceeds quota; search value monotone in
captured mass. Integration (keyless CI, config-driven): referee applies barriers end-to-end
(capture-by-barrier + imprisonment observed) · scenario suite reproducibility · **the DoD
series** — PoliceBrain vs `ref-thief` over the committed suite, win-rate ≥ the configured 0.60,
CI-blocking · champion gate green on the updated pin. Coverage ≥90% on the deterministic core,
`mypy --strict`, ruff + format, file sizes, no-hardcoded — the full gate ritual.

## 10. Acceptance criteria (binary)

- All §9 tests green in keyless CI in **both** repos (core pieces post-sync; role suite here).
- `docs/evidence/m5-arena-police.md` committed: DoD table (PoliceBrain vs `ref-thief`, per-
  scenario outcomes + the rate) + regenerated per-role round-robin standings; regenerable by
  script, never hand-edited.
- `config/arena_champion.json` consistent with the committed tables (dethroning in the same PR).
- ADR-0005 (belief+search over RL) merged; ADR-0002 attribution notes cover `ref-*` brains and
  the scenario-suite salvage.
- The LLM-never-decides-moves invariant holds by construction (no LLM import anywhere in
  `copthief_police` or `copthief_core.strategy`) — AST-scan-style test, mirroring the M4 rules-8/9
  pin.
