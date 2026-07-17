# PRD — Belief layer (mechanism PRD, milestone M3)

> **Status: DRAFT (gate M3-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-5,
> `docs/PLAN.md` §8. Sources of truth: book ch.6 (belief/strategy) + **M2 spike
> observations** (`docs/evidence/m2-oracle-spike.md` §3 SQ1/SQ3, §8 F9; oracle sha
> `960499fd`). The reference's `BeliefGrid` is an **oracle for behavior comparison only**
> (ADR-0002) — ours is re-derived as an exact Bayes filter, which is the strategy edge
> the reference deliberately leaves basic. Covers TODO **M3-3**; consumes `domain/scent`
> (M3-2); hint likelihoods arrive with the gazetteer (M3-4).

## 1. Scope & non-goals

**In scope (M3-3):** `copthief_core/domain/belief` — an exact Bayes filter
`P(opponent at cell)` over the board; the barrier-aware motion model (closes spike
finding **F9**); scent-likelihood update; a pluggable hint-likelihood seam; the
belief-error metric + last-known-position baseline used by the M3 exit criterion.
**Non-goals:** move selection (M5 brains read the belief, never write it) · hint text
parsing (M3-4 supplies `cells → weight` likelihoods) · GUI heatmap (M4-2 renders this
filter's output) · opponent profiling priors (M5-5).

## 2. Model (exact, discrete, adversarial-input-aware)

State space: the `N×N` cells. All arithmetic is plain float over a dict/array — the
board is 49–100 cells; exactness is affordable, no sampling.

1. **Prior:** a delta at the opponent's SIGNED start cell (`thief_start`/`cop_start` are
   agreed terms — the game opens with certainty, observed in every M2 game).
2. **Predict (per opponent turn):** motion model = uniform over the opponent's legal
   actions from each support cell — the signed `move_set` steps that stay on-board and
   off known barriers, plus STAY (and, for the police, barrier-placement turns where the
   mover's position is unchanged). **F9 closure:** `barrier_placed` cells from inbound
   TurnMessages enter BOTH the board's legality set (our own moves must respect them —
   the M2 gap) and this motion model.
3. **Update — scent:** likelihood of the opponent occupying cell `c` given the received
   grid `G`. The locked model says a mover's fresh center transmits at
   `center_intensity − decay` (PRD_scent §2): cells whose received value is near that
   fresh-center value are strong evidence; older/weaker scent widens the plausible set
   by its implied age (each 0.1 of missing intensity ≈ one turn older under the
   subtractive model). Likelihood weights derive from the SIGNED pheromone params only;
   the private `[belief] smell_trust_weight` scales how sharply the update multiplies in
   (**SQ3 stance:** the grid is unauthenticated and freely fakeable — trust is a tunable,
   never an axiom, and a fabricated far-field grid must never zero out the true cell:
   the update multiplies, it never eliminates).
4. **Update — hints:** `update_hint(cells, weight)` — a seam taking the gazetteer's
   implied-cell set and a trust weight (per-opponent trust arrives with M5-5 profiling;
   M3 uses the config default). Same never-eliminate rule.
5. **Normalize** after every step; **degenerate-case guard:** if the posterior mass
   collapses to 0 (contradictory fabricated evidence), reset to the predict-only prior
   (motion-reachable set) rather than crashing or freezing — deception must degrade our
   estimate, never our process.

## 3. Evaluation (the M3 exit criterion, PLAN §13)

`belief_error(belief, truth_cell)` = `1 − P(truth_cell)` (primary) + argmax-hit-rate
(secondary), logged per step. Baseline: a **last-known-position tracker** (point mass at
the last cell any evidence certainly placed the opponent, else uniform). DoD: in
referee-mode simulations (full information available to the harness, seeded), the Bayes
filter's mean belief-error beats the baseline on the shipped config across the seed set.
Curves export for M4-4 / the README.

## 4. Purity & seams

`domain/belief` is pure (no I/O/clock/RNG); constructor takes board geometry + pheromone
params + trust weights. The peer session wires it: inbound TurnMessage → note barriers →
`predict()` → `update_scent(msg.smell_grid)` → (M3-4) `update_hint(...)`. Referee-mode
tests drive it directly with ground truth. `[belief]` private tuning lives in
`game.toml` (never signed, never crosses the wire).

## 5. Configuration

Signed values (board, move_set, pheromone params, starts) from the constitution;
private tuning (`smell_trust_weight`, hint trust default) from `game.toml [belief]` with
loader-supplied defaults. No literals in `src/` (constraint #5).

## 6. Test plan (TDD; DoD of M3-3)

Unit (happy + error): prior is a delta at the signed start · predict conserves
probability mass and grows support only through legal moves · barriers block diffusion
AND our own legality (F9 regression: the g2 scenario — barrier declared, our mover may
not enter it) · fresh-center scent collapses belief near the emitter · aged scent widens
consistently with the subtractive model · fabricated far-field scent shifts but never
eliminates the true cell · hint seam multiplies and renormalizes · degenerate-evidence
guard resets instead of NaN/zero-division · determinism. Property tests: mass ≈ 1 after
every operation; no negative probabilities. Referee-mode integration: the §3 metric run,
seeded, beating the baseline. Coverage ≥ 90%, files ≤ 150 lines, `mypy --strict`, ruff.

## 7. Acceptance criteria (binary)

- All §6 tests green in keyless CI in both repos (post-sync).
- The F9 regression test exists and fails against the M2-era behavior (barrier ignored).
- Belief-error comparison table (filter vs baseline, seeded) committed as the M3
  evidence artifact; filter wins on the shipped config.
- The GUI (M4) and brains (M5) consume the filter through its public read surface only.
