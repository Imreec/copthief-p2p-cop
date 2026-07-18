# Prompt Engineering Log

> Truthful, per-PR entries for **committed** work only (CLAUDE.md §7). Development prompts —
> runtime agent prompts live in source. Format: PR · driver/reviewer · what was asked · outcome.

## PR #35 — feat/m5-4-genetic (M5-4 — genetic tuning, evolved weights deployed)

- **Driver:** Imree (AFK directive: "continue and build what you need for M5; merge
  nothing tonight") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR); chain position: top of the cop stack (#33 → #34 → this).
- **This PR:** RED `test_genetic.py` → GREEN `strategy/genetic/` (mirrored, stdlib-only,
  HW6 `policy/genetic` salvage adapted per ADR-0002: bounded genome over config-declared
  gene boxes · tournament/blend/gaussian operators · seeded elitist loop, best
  non-decreasing — the CI smoke pins determinism + monotonicity) + `config/ga.json`
  (role-blind: each repo evolves ITS brain; fitness seeds 201–216 disjoint from the DoD
  seeds — the gate is not a training target) + `scripts/ga_run.py` (deterministic
  artifact + curve writer). **Committed run: default 0.688 → evolved 1.000; validated
  OFF-suite: DoD 75%→94%, fresh holdout 78%→97% — deployed as config** (arena
  `brain_options` + `game.toml [strategy.police]`); arena regenerated, police-brain
  sweeps 24/24. Three more seed-coupled mirrored tests pinned to the M1 walk (the
  recurring PR-#29 lesson, now swept: local-minigame/symmetric-loop in #34, session/
  facade here). TODO M5-4 ticked; thief-side GA run rides the next sync.

## PR #33 — feat/m5-3-core-prereqs (M5-3 core prerequisites)

- **Driver:** Imree ("merge them, then continue" after approving #31/#32) · **Author:**
  Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **Context:** pre-sync audit caught a PR-#29-rule violation of my own making: the
  mirrored `test_peer_barriers` fixture matched the cop repo's literal `police_class`
  value and would have gone red in the thief repo on sync — the sync ritual was held
  until this fix. The rest is the role-neutral seam PRD_thief_brain §3 binds.
- **This PR:** RED `tests/unit/peer/test_hint_seam.py` → GREEN: Decision gains
  `hint_verdict`/`hint_landmark` (validated; `decide()` preserves hint fields through
  the clamp — the clamp governs actions, not talk) · `compose_hint` accepts an explicit
  decoy landmark (off-vocabulary falls back — the closed world never leaks) ·
  peer/turns + referee hand brains the deception construction kit (gazetteer, own
  transmitted trail so far, signed pheromone params — a self-mirror's inputs, nothing
  about the opponent's truth) · the fixture now rewrites the `police_class` KEY
  role-agnostically · split `strategy/referee_setup.py` (150-line rule).

## PR #32 — feat/m5-2-police-brain (M5-2 — PoliceBrain, the graded core ⚑)

- **Driver:** Imree ("merge them, then continue" after approving the M5-1 PRD pair) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR (stacked on #31):** `copthief_police` role package (never mirrored) —
  capture-commit (≥ `p_commit` adjacent mass → step onto it; the claim rides free,
  SQ2) · expectimax over the truncated belief (expectation over position, adversarial
  min over the thief's replies, max over ours; earlier capture pays more) · barrier
  graph-surgery (belief-weighted capped-BFS region shrink + trapped mass; only cuts
  ≥ threshold spend quota) · every knob config-owned (`features.DEFAULT_OPTIONS` data
  table, AppFTable pattern, overridden by `[strategy.police]`/arena `brain_options` —
  the M5-4 GA interface). Behavior pins authored before the implementation (pocket-seal,
  commit, quota, determinism, option-governs-policy); guards: App-E-25 AST scan,
  legality property, config perf ceiling. **DoD observed and CI-blocking: 24/32 = 75%
  vs `ref-thief` (floor 60%)** — `dod_series` in arena.json runs as a permanent test;
  `m5-arena.md` regenerated. Champion pin: `police-brain` dethrones `ref-police`
  (390 > 330), same-PR evidence. game.toml now selects the brain by dotted spec; five
  mirrored tests updated role-blind (config-resolved pins, not name pins). TODO M5-2
  ticked in the same change.

## PR #31 — feat/m5-2-core-seam (M5-2 — role-neutral core groundwork)

- **Driver:** Imree (same directive) · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN per cluster (4 pairs): Decision seam (`strategy/
  decision.py` + `BrainBase.decide/_decide`; barrier turn keeps position — reference
  MoveType.BARRIER semantics; baselines byte-identical through the new path) ·
  re-derived `ref-police`/`ref-thief` arena opponents (ADR-0002 interface-mirror
  @960499fd; perception held fixed on our BeliefFilter per PRD §2; attributed 0.15
  coin-flip rate config-owned) · seeded start-scenario suite (canonical-first;
  deterministic brains get meaningful win-rates) · referee applies full Decisions
  (barrier joins ground truth + BOTH beliefs; capture-by-barrier proven end-to-end) ·
  config-driven per-role arena (`config/arena.json` + `sdk/arena_config.py`; mirrored
  scripts/tests role-blind per the PR #29 rule) · peer outbound barrier path
  (`barrier_placed` outbound for the first time; sealed move `BARRIER`; SQ2 MOVE-only
  claims; full-loop proof: always-wall ref-police → mutual audit Verified OK + replay
  green) · `[strategy.<role>]` options tables · splits `peer/inbound.py`,
  `sdk/peer_run.py`. Champion pin: `ref-police` dethrones `greedy-manhattan` on the
  police table (330 > 240), same-PR evidence (`m5-arena.md`).

## PR #30 — docs/m5-1-police-brain-prd (M5-1 gate — PoliceBrain PRD + ADR-0005)

- **Driver:** Imree (M5 session opening brief: scope M5-1..M5-7, the role-split and
  reference-heuristic-opponent questions posed as PRD inputs, M3-8 scent internals fenced off)
  · **Author:** Claude (terminal) · **Reviewer:** Imree (docs gate — merge = the approval).
- **Context:** memory recalled (project-state, ops gotchas incl. format-gate + portable-pin,
  Alon coordination), then primary sources re-read: book ch.6 pp.57–68 from the extraction,
  reference `brains.py`/`belief.py`/`sealing.py`/`own_state.py` @960499fd, M2 SQ2/SQ3, M3
  arena/belief evidence, the strategy seams, `sync_core.py` MIRRORED list. Recon settled four
  facts the PRD binds: SQ2 makes claims free per-MOVE probes (claim policy → capture-commit in
  move scoring); deterministic brains on fixed signed starts degenerate the DoD to 0/100% (→
  seeded start-scenario suite); `tests/role/` is per-repo while `scripts/`+`tests/integration`
  are mirrored (→ arena roster/seeds move to per-repo `config/arena.json`, factory gains the
  book's dotted `package.module:Class` notation); the reference walls its step-cell at an
  attributed 0.15 coin-flip and a barrier turn moves nothing.
- **This PR:** `docs/PRD_police_brain.md` (role split · re-derived `ref-*` DoD opponents with
  perception held fixed on our BeliefFilter, disclosed as the harder-opponent direction ·
  Decision seam · scenario suite + per-role rosters · expectimax + barrier graph-surgery +
  capture-commit · weights→config as the M5-4 GA interface) + `docs/adr/0005-strategy-track.md`
  (belief+search over RL — indexed in PLAN §14 since Phase 2, written as the decision lands).
  TODO M5-1 ticked in the same change (true at merge). Sibling ThiefBrain PRD: thief repo PR #20,
  approved together.

## PR #28 — feat/m4-overlay (M4-4 — belief-vs-truth overlay + error curve)

- **Driver:** Eyal ("continue" directive, same session) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD (RED `a6a2f1a` → GREEN `6b39403`):
  `gui/models/overlay.py` (pure series prep: truth ONLY from revealed audit records —
  unaudited logs refused loudly; belief from logged snapshots, never recomputed; error
  = 1 − P(truth), the exact M3-3 metric, test-recomputed from raw events; single-role
  auto-detect), `gui/export.py` (matplotlib-Agg overlay + curve PNGs, dpi
  config-owned, axis-contract-aware), D2 landed (`viz` dependency group included into
  dev for the keyless PNG smoke), CLI `copthief overlay`. PNG magic bytes pinned.
  **Follow-up on Eyal's review of the first screenshots** ("looks a bit old"):
  dark-theme facelift commit `4ab6b1a` — shell-only within D1/D3 (new
  `gui/windows/theme.py` DRY chrome seam; `[gui]` font+theme knobs config-owned;
  models untouched; PyQt deliberately declined — new dep + PRD churn for
  stretch-priority polish). Screenshots retaken from the same audited game.

## PR #27 — feat/m4-replay (M4-3 — replay verifier + viewer)

- **Driver:** Eyal ("continue" directive, same session) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD (RED `ce6b77c` → GREEN `1ab6880`): `peer/replay`
  gains the book's exact banner strings + `verdict_for`; `revealed_records` reads
  v1.1 `audit_received`, `wire_turns` folds `turn_received` (deduped; malformed
  pre-validation archives skipped) — a one-sided live log now verifies BOTH sides.
  `gui/models/replay.ReplayWalk` (audited frames, clamped cursor) + thin viewer
  window + CLI `copthief replay` (exit 0/1 by verdict). Rule-19 mutation matrix as
  permanent CI regression: every sealed field + nonce + commit flips a real log to
  TAMPERED; opponent-audit tampering caught from the verbatim archive. One test bug
  fixed during GREEN: the one-sided filter had dropped our own audit (its sender
  lives inside the payload).

## PR #26 — feat/m4-live-gui (M4-2 — live view: heatmap + turn banner)

- **Driver:** Eyal ("continue" directive, same session) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD (RED `ede59f4`/`b41fa75` → GREEN `8f12a8e`):
  `gui/models/live.py` pure fold over the v1.1 stream (banner per state; config-
  anchored monotone `heat_color`; folds cross-checked against a real game's audited
  records; **local truth by construction** — no opponent-position field, no full-info
  imports, both pinned incl. an AST scan), thin Tk shells lazy-imported (keyless CI
  touches no display), `[gui]` config section, `--gui` on peer/local-match via the
  sdk. 150-line splits: `shared/private_config.py`, `sdk/p2p_match.py`. Coverage
  omit narrowed to `gui/windows/*` (D3): gui/models 100%. Real-game hidden-root
  smoke render clean.

## PR #25 — feat/m4-log-schema (workstream L — log schema v1.1)

- **Driver:** Eyal (relayed the M4-1 approval; "continue" directive after the gate
  merged) · **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model,
  on the PR).
- **This PR:** strict RED→GREEN TDD (RED `1f7b87f` → GREEN `bafa662`): `peer/events.py`
  (schema-v1.1 builders; module docstring carries the honest "verbatim = the parsed
  dict, losslessly" definition), inbound-verbatim archiving at the `peer/p2p` loop
  seams incl. rejected inbound (archived BEFORE validation — dispute evidence),
  `GameStateMachine` observer + trigger annotation (injected callable, domain stays
  pure; collapse reasons and the turn-deadline timeout travel as triggers), belief
  snapshot per inbound turn (mass == 1 pinned), decision provenance at seal time
  (cross-checked vs audited records), logger parent-dir creation (the M3 thief trap).
  Compat pinned: the committed M3 evidence log still replays Verified. Nothing on
  the wire — kit CORE untouched. 322 tests, coverage 96%, new modules 100%.

## PR #24 — docs/m4-prd (M4-1 gate: GUI/replay/observability PRD)

- **Driver:** Eyal (this session's terminal driver; commits authored as @eyalsht for
  `git shortlog` honesty) · **Author:** Claude (terminal) · **Approver:** Imree (the
  M4-1 gate — merge is the approval) · **Reviewer:** Antigravity (cross-model, on the PR).
- **Context:** M4 session opened on primary sources — book ch.7 (pp.69–75) re-read from
  the extraction (live/retrospective split, banner semantics, the simplified
  `verify_step` sketch vs the full ch.5 seal), App E rules 8/9/19/20 re-read from App E
  pages, both repos' M3 friendly evidence docs (the flagged inbound-logging gap), the
  real M3 JSONL event shapes, and the `peer/p2p` + `peer/replay` + `jsonl_logger` seams.
- **This PR:** `docs/PRD_gui_replay.md` — workstream L (log schema v1.1: inbound-verbatim
  `agreement_received`/`turn_received`/`audit_received` + the PLAN §7-promised
  `belief`/`transition`/`decision` events; log-only, nothing on the wire), M4-2 live GUI
  (single event stream feeds file + window, so rules 8–9 hold by construction), M4-3
  replay verifier (binary Verified OK/TAMPERED + per-field mutation matrix as permanent
  CI regression), M4-4 post-audit overlay + belief-error curve (metric identity with
  M3-3 `belief_eval`). Four flagged decisions: D1 Tkinter, D2 matplotlib `viz` group,
  D3 coverage-omit narrowed to `gui/windows/`, D4 backward-compatible log contract.
  M3-8 blockade honored (no scent/belief internals in scope). TODO M4-1 ticked in the
  same change.

## PR #23 — docs/m3-7-decision (ADR-0004 revision: REVISE decided)

- **Driver:** Imree (decision delegated conditionally — "if it isn't blocking we can go
  with your recommendation"; assessed not blocking: Alon's inputs gate the build, not
  the decision) · **Author:** Claude (terminal).
- **This PR:** M3-7 ticked with the decision record (REVISE: second named scent model,
  pair-locked, belief observation model parameterized) incl. the assessment's two
  corrections — per-field decay cadence is once per full turn in reference and ours
  alike, and the locked-model doc is hashed/logged but not terms-signed (step-0
  sealing added to the build scope to close it). New input-gated M3-8 build item
  (blocked on Alon's kernel numbers / cadence trace / rounding+ρ / lock fallback;
  PRD amendment + ADR-0004 v2 approve-before-build; not inside M4). Question list
  handed to Imree for Alon; kit PR #5 reviewed this session (all four hashes
  independently recomputed against the reference's own consensus_signature) and
  recommended for merge.

## PR #22 — docs/league-coordination (Alon's analysis folded into the roadmap)

- **Driver:** Imree (relayed the planning session's wrap-up instruction with "don't
  automatically agree — think about it") · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity (cross-model, on the PR). Source: `notes/LEAGUE-COORDINATION-ALON.md`.
- **This PR:** future-phase league-coordination items folded into TODO so later
  sessions discover them mechanically — M6-2 consensus-signature pin (spaced
  serialization + sign-then-insert, **re-verified in this session** against reference
  `report_writer.py` @960499fd before writing the line; credit Alon), M6-3/M6-8
  sealed per-step token counts (reference's own SQ3 schema), M7-1 conditional
  dual-model acceptance, M7-2 kit additions as "verify present, else add", and the
  new gated **M3-7: ADR-0004 revision decision (Imree's; approve-before-build, no
  scent code changes until)**. One test addition: the float-repr drift pair —
  **the relayed spec was corrected here**: 0.10000000000000001 IS 0.1 (same IEEE
  double → identical canonical bytes → signature verifies; asserting failure would
  be red forever). Pinned both directions: equivalent literals verify; a genuinely
  distinct double (0.1+0.2 vs 0.3) breaks the terms signature.

## PR #21 — feat/m3-arena (M3-6 — arena harness + champion regression gate)

- **Driver:** Imree (same overnight directive) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR) · **E review slot:** parked with
  Imree per TODO (Eyal reviews M3-6).
- **This PR:** strict RED→GREEN TDD: `sdk/arena.py` — an sdk CONSUMER
  (`SimulationSdk.referee_series` is the only game source): seeded round-robin over
  the baseline roster, per-role standings (wins/points from the signed scoring
  table), and `champion_regression` — the CLAUDE.md §5 gate, proven in BOTH
  directions in unit tests (green when the pinned champion tops its role table, red
  with the dethroning named when it does not / when the pin is unknown).
  `config/arena_champion.json` pins greedy-manhattan for both roles (the empirical
  winner on the fixed seed set: police 200 vs 185 points, thief 160 vs 85);
  integration runs the shipped pin blocking in CI + seeded reproducibility.
  `scripts/arena_run.py` regenerates the committed standings artifact
  (`docs/evidence/m3-arena.md`). TODO M3-6 ticked — **phase M3 build complete,
  M3 exit criteria all observed in CI.**

## PR #20 — feat/m3-brains (M3-5 — BrainBase seam + baseline brains)

- **Driver:** Imree (same overnight directive) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD: `strategy/brains.py` — the PLAN §8 seam
  (`_pick_move(observation, belief)`; public template method clamps every proposal to
  legality: illegal → first sorted legal move, walled-in → STAY, never stall) +
  RandomBrain (the M1 walk, seam-shaped; byte-identical seeded behavior keeps every
  M1/M2 pinned outcome) + GreedyManhattanBrain (chase/flee the belief argmax;
  deterministic tie-breaks) + config-name factory. `strategy/referee.py` — headless
  referee-mode games resolved by the ONE rules module (all three capture forms),
  brains fed peer-symmetric information (own truth + belief from the opponent's
  honest trail). Session now selects its brain from `game.toml [strategy]`
  (random/random shipped; role brains at M5). DoD observed in CI: seeded referee
  series (reproducible; capture path reachable) + peer-mode series over the queue
  transports with clean mutual audits. TODO M3-5 ticked.

## PR #19 — feat/m3-hints (M3-4 — gazetteer + hint templates + injection safety)

- **Driver:** Imree (same overnight directive) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD: `domain/gazetteer.py` (fractional anchors →
  Chebyshev cell balls on the signed grid; CLOSED-vocabulary parser — longest
  case-insensitive match within the signed word cap, total on any input; empty world
  for unknown map_areas), `config/gazetteer.json` (10 New-York landmarks, private,
  never wired), `strategy/hints.py` (template bank × landmark; reference verdict
  vocabulary truth/lie source-pinned from its constants; lie MECHANISM only — timing
  is M5), session wiring (outbound hints composed truthful with the verdict sealed
  as the record's intent; inbound hints reach ONLY the parser and feed
  `belief.update_hint`). Injection-safety suite over a hostile corpus (prompt
  injection, size bombs, RTL, JSON lookalikes, near-miss bait) proves: never raises,
  never leaves the closed vocabulary, game stays playable. M3 exit pin: our hints
  round-trip our own parser. TODO M3-4 ticked.

## PR #18 — feat/m3-belief (M3-3 — exact Bayes filter + F9 closure)

- **Driver:** Imree (same overnight directive) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR) · **E review slot:** parked with
  Imree per TODO (Eyal reviews M3-3).
- **This PR:** strict RED→GREEN TDD: `domain/belief.BeliefFilter` (signed-start delta
  prior; barrier-aware uniform-legal predict; scent likelihood reading each received
  cell's implied age under the subtractive model and spreading its voucher over the
  Manhattan age-ball; hint seam; never-eliminate floor; degenerate-collapse guard).
  **F9 closed:** inbound `barrier_placed` now enters the session board (our own move
  legality) AND the belief motion model — regression tests pin the g2 scenario and
  fail on the M2-era behavior. `LastKnownTracker` baseline under the certain-evidence
  reading (SQ3: grids are fakeable, so the naive tracker never reads them).
  Referee-mode eval harness (`strategy/belief_eval`): filter beats baseline on the
  primary metric on EVERY seed (mean 0.73 vs 0.94; argmax-hit 0.98 vs 0.06);
  `scripts/belief_eval.py` regenerates the committed evidence table
  (`docs/evidence/m3-belief-eval.md`); CI asserts the same claim. One likelihood
  iteration was needed mid-build: the first (flat voucher) model lost to the baseline
  on 2 of 10 seeds — the ball-spread reading fixed it; both are in the history.
  `[belief]` private tuning keys added to game.toml. TODO M3-3 ticked.

## PR #17 — feat/m3-scent (M3-2 — domain/scent per the approved PRD_scent)

- **Driver:** Imree (overnight M3 build directive: stacked chain M3-2→M3-6, merge
  nothing, full TDD + gates) · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD (3 cycles): `domain/scent.ScentField` (kit-pinned
  subtractive-Chebyshev form; kit `pheromone.json` joins tests/conformance as
  CI-blocking fixtures, constraint #13), the locked scent-model document
  (`subtractive_chebyshev_v1`, canonical bytes pinned literally in a test), and the SQ1
  peer wiring (deposit-after-move at the new position → one decay → snapshot on the
  wire; receiver absorbs then decays; deposits on STAY and the final caught message —
  source-pinned against the reference's unconditional send path). Session turn cycle
  extracted to `peer/turns.py` (150-line rule; mirrors the reference's
  turn_sender/turn_handler split). Handshake now carries the locked model as a
  negotiate extra (reference `verify_peer` provably ignores it) and records both
  hashes. ADR-0004 (subtractive-vs-multiplicative contradiction). Coverage 100% on all
  touched modules. TODO M3-2 ticked.

## PR #16 — docs/m3-prds (M3-1 — scent + belief mechanism PRDs; approved by Imree)

- **Driver:** Imree ("let's continue" after the M2-5 GO) · **Author:** Claude (terminal)
  · **Reviewer:** Antigravity (cross-model, on the PR) · **Approver:** Imree (M3-1 gate).
- **This PR:** `docs/PRD_scent.md` (kit-pinned subtractive-Chebyshev model with the SQ1
  emission timing observed at the spike, two-field design, locked-model handshake doc,
  numeric example from the shipped config, fabrication posture per SQ3) and
  `docs/PRD_belief.md` (exact Bayes filter: signed-start delta prior, barrier-aware
  motion model that closes spike finding F9, scent/hint likelihood updates under the
  never-eliminate rule, degenerate-evidence guard, belief-error metric vs
  last-known-position baseline as the M3 exit). No code — M3-2/M3-3 start only after
  approval.

## PR #15 — docs/m2-close (M2-5 GO recorded — phase M2 complete)

- **Driver:** Imree ("I think I'm satisfied, but are you? If you are, then let's
  continue" — GO conditional on Claude's candid assessment) · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** the assessment ran one extra check before answering: the reference cop
  placed 7 barriers in g2 and our skeleton ignores opponent barriers (new finding F9) —
  post-hoc path analysis proved our thief never occupied a barrier cell after placement,
  so the evidence stands. GO recorded; spike notes closed with §8 (residual gaps F9 /
  Stage-B / scent-live / series, scoped to M3-3, M7, M3-2, M6-6); TODO M2-5 ticked.

## PR #14 — feat/m2-negotiate-identity (M2 Stage A: F8/F8b + evidence + ADRs)

- **Driver:** Imree (OI-3 decision = Cloudflare named tunnel on `imreeyal.com`; domain
  purchase + `cloudflared tunnel login`; the Stage-A word) · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** Stage A executed vs the LIVE reference over public tunnels. Findings
  fixed in two RED→GREEN cycles: F8 (negotiate must mirror the reference's
  `{terms, nonce, signature, identity}` shape — observed as `unknown-group` +
  diverging game_uids) and F8b (the reference's declaration writer requires all seven
  identity keys — observed as its post-game crash). Infrastructure finding F-421
  (MCP DNS-rebinding protection vs tunnels → `originRequest.httpHostHeader` rewrite)
  fixed in tunnel config, documented in ADR-0006. Evidence: four JSONL game logs
  (both role pairings + fix-verification reruns; final run derived the SAME game_uid
  on both implementations, mutual audits Verified OK). ADR-0003 + ADR-0006 written;
  spike notes §6; TODO M2-1..M2-4 ticked. M2-5 GO/NO-GO remains with Imree.

## PR #13 — feat/m2-claim-flow (M2 spike, fix batch 3: SQ2)

- **Driver:** Imree (M2 session brief) · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity (cross-model, on the PR). Stacked on the F1/F2 transport PR.
- **This PR:** one RED→GREEN cycle implementing the observed SQ2 semantics: the police
  claims its landing cell on every moving turn; the thief answers honestly on its next
  turn; a caught thief sends the mandatory final message and both games end capture
  (wire "capture", capture score row via `scoring.scores_for`). Handshake extracted to
  `peer/handshake.py` (the reference's own split) to hold the 150-line rule. Real find:
  with claims live, the M1 default seeds (11/22) actually produce a mid-game capture —
  outcome-pinned tests moved to probed seed pairs (survival 1/2, capture 3/3). Observed
  live two-process: both endings with mutual audit Verified OK.

## PR #12 — feat/m2-symmetric-transport (M2 spike, fix batch 2: F1–F2)

- **Driver:** Imree (M2 session brief) · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity (cross-model, on the PR). Stacked on PR #11.
- **This PR:** two RED→GREEN cycles rebuilding the calling convention to the observed
  reference: session turn order flips (thief moves first; survival win_claim ends the
  game, cross-checked at audit with a threshold backstop and step-0 spec-record
  tolerance); then the symmetric push/inbox transport — `PeerTransport` protocol,
  in-process queue pair for keyless CI (replacing the response-carried MCP fake),
  `run_peer_game` (one loop, both roles), FastMCP tools that enqueue-and-ack, real
  `McpTransport` (retry-until-up, best-effort audit), sdk/CLI where `run peer` PLAYS a
  full standalone game. Two-process localhost run observed post-rewrite: mutual audit
  Verified OK both directions under the new convention. Debug find: FastMCP INFO access
  logs filled the spawned peer's stdout pipe and froze it — servers run at
  log_level=warning now.

## PR #11 — feat/m2-wire-reference-pins (M2 spike, fix batch 1: F3–F6)

- **Driver:** Imree (M2 session brief: run the oracle spike, fix M1 stubs on branches as
  findings come in) · **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model,
  on the PR).
- **This PR:** M2-1 groundwork first — reference cloned OUTSIDE the repos, pinned at sha
  `960499fd` (v3.0.0), run keyless (template banter, stub LLM, email disabled) to a clean
  localhost mutual audit; all observations in `docs/evidence/m2-oracle-spike.md`. Then four
  RED→GREEN cycles pinning our wire/domain/config to the observed reference: TurnMessage
  shapes (ISO timestamp, cell capture_claim, dict claim_response/win_claim, explicit-null
  tolerance, asdict-parity outbound with extras never emitted), AuditPayload result string +
  reference ControlMessage (kind-keyed), terms `max_steps` ← `survival_threshold`
  (discriminating test), loader reads `pheromone_min_center_intensity`. Kit conformance
  re-run per constraint #13. F1/F2 (push/inbox transport + thief-first) are the next branch.

## PR #10 — feat/jsonl-logger (M1-8 — phase M1 complete)

- **Driver:** Imree ("continue") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** one RED→GREEN cycle. `shared/jsonl_logger` (append-only canonical-JSON lines,
  monotonic seq, lossless unicode round-trip), match-runner instrumentation (provenance,
  negotiate/turn/audit payloads verbatim, per-step state snapshots, derived result),
  `peer/replay.replay_from_log` (pairs each traveled TurnMessage with its revealed audit
  record: commit-that-traveled == sealed commit, record re-hashes, revealed hint == traveled
  hint; moves reconstructed). DoD observed in CI: a logged game replays Verified; a tampered
  record and a hint divergence are both flagged. CLI gains `run local-match --log PATH`.
  **Phase M1 (walking skeleton) is complete: M1-1..M1-8 all ☑.**

## PR #8 — feat/peer-loop (M1-6, fake-transport half)

- **Driver:** Imree ("continue") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** three RED→GREEN cycles. `peer/sealing` (kit-pinned state string — first ADR-0002
  micro-snippet log entry; verifiable records, fresh nonce each), `peer/policy` (seeded legal
  walk + template hints, M1-only), `peer/session` (handshake gate: value-equal terms + signature
  → game_uid; turn choreography on the PLAN §5 machine; collapse-to-TECHNICAL_LOSS on any
  violation), `peer/audit_flow` (build/verify with our serializer, per-step tamper flags,
  derived results, submit_audit round-trip), `infra/fake_mcp` + `peer/match` (full mini-game
  over the fake: all four tools exercised, survival ending, mutual audit Verified OK — the
  fake-transport half of the M1 exit; observed in tests/integration/test_local_minigame.py).
  Also: MIRRORED hardened to whole test trees after tests/unit/wire silently missed the mirror
  (thief PR #6 closed red; role test moved to tests/role/). M1-6 marked ◐ — the one-command
  two-process form completes with M1-7's CLI + real FastMCP adapters.

## PR #9 — feat/sdk-cli (M1-7 + M1-6 completion)

- **Driver:** Imree ("continue") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** fastmcp 3.4.4 added (the milestone-planned first runtime dependency; API pinned
  by a scratchpad smoke before adapter work). `infra/mcp_server` + `infra/mcp_client` (thin real
  FastMCP adapters; M1 response-carried composition documented, M2 pins the reference's real
  call pattern), `peer/p2p` (initiator-side driving loop), `sdk/SimulationSdk` (the single
  business entry point: local-match / serve-peer / p2p-match with subprocess spawn+teardown),
  `sdk/cli` + `[project.scripts] copthief`. **M1 exit criterion OBSERVED:**
  `uv run copthief run p2p-match` → two OS processes over localhost FastMCP, 35 sealed turns,
  mutual audit Verified OK both directions (docs/evidence/m1-p2p-match.md). Live adapters are
  coverage-omitted with a documented rationale (PLAN §12 keyless CI) and covered by the
  @pytest.mark.live test + the committed evidence. TODO M1-6 + M1-7 ticked.

## PR #6 — feat/domain-state-machine (M1-4)

- **Driver:** Imree ("continue") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** one RED→GREEN cycle. `domain/state_machine` — frozen PLAN §5 transition table
  (11 legal pairs incl. the any-comm-state → TECHNICAL_LOSS escape hatch), IllegalTransition
  raised without state mutation, absorbing terminals. The 49-pair transition space is proven by
  exhaustive parametrization rather than sampling. Between PR #5 and this one, the deferred sync
  ritual ran: thief PR #4 ("sync: core from police@3e747bf" + config tree) merged, both repos'
  mains green with kit CORE vectors green in both CIs (M1-3 DoD closed).

## PR #7 — feat/wire-messages (M1-5)

- **Driver:** Imree ("continue") · **Author:** Claude (terminal) · **Reviewer:** Antigravity
  (cross-model, on the PR).
- **This PR:** two RED→GREEN cycles. `wire/validation` (primitive checkers, all problems
  collected into one WireValidationError), `wire/turn` (TurnMessage: PLAN §6 field set,
  reject-missing + tolerate-unknown with extras preserved through to_wire), `wire/audit`
  (AuditPayload with verbatim record payloads + per-index diagnostics; ControlMessage with the
  closed status/restart/quit action set, never sealed). Optional-field types flagged for M2
  verification vs the live reference. Between PR #6 and this one the M1-4 sync ritual ran
  (thief PR #5, `sync: core from police@7dc7e48`, merged green).

## PR #5 — feat/domain-crypto (M1-3)

- **Driver:** Imree (merge authorization + "continue") · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** two RED→GREEN cycles. (1) `domain/crypto` re-derived from kit CORE — canonical
  form, commit/verify, terms signature, `game_uid`; the four vector files copied verbatim
  (provenance in `tests/conformance/SOURCE.md`, kit@5b3927e) and driven by OUR code in
  CI-blocking conformance tests; all reproduce byte-for-byte. (2) `domain/terms` — the kit's
  14-key reference-named extraction; `min_center_intensity` added to the App F transcription as
  an optional negotiable row (default 0.5 flows through the loader when the signed file omits
  it). Also extends `sync_core.py` MIRRORED with the core test tree (PRD_crypto §7) so the
  post-merge sync keeps the thief repo's coverage gate green — the M1-2+M1-3 sync rides on this
  merge.

## PR #4 — feat/domain-engine (M1-2)

- **Driver:** Imree (merge authorization for #3 + "continue") · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** strict RED→GREEN TDD (5 cycles, RED commit before each GREEN): board geometry
  (axis contract incl. all four origin corners), rules (legality, barrier law, imprisonment,
  capture, end states), scoring (rows + series settlement; tie-rule interpretation documented
  and M2-flagged), App F guard (statuses from `config/app_f_table.json`, `num_games`
  counted-series scope), typed config loader (JSON-wins overlay, N.NN versions, rate-limits
  precedence). Four config data files landed; PRD_engine §8 acceptance test drives all four
  scored endings through a scripted referee-mode mini-game. Coverage 100% on the new modules.

## PR #3 — docs/m1-mechanism-prds (M1-1 gate)

- **Driver:** Imree (review + explicit approval, incl. the `num_games` terminology ruling) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **Context:** M1 session opened on primary sources — book ch.3/ch.5/App B/App F re-read from the
  extraction, kit SPEC + `verify_vectors.py` + all four crypto vector fixtures read in full.
- **This PR:** `docs/PRD_engine.md` (board/rules/scoring + state machine + App F guard; App F
  statuses transcribed to a data-file spec; four documented interpretations incl. counted match =
  six mini-games fixed) and `docs/PRD_crypto.md` (canonical JSON, commit/verify, terms signature
  with the reference-key-name extraction mapping, `game_uid`, conformance-fixture plan; two open
  items routed to the M2 spike). TODO M1-1 ticked in the same change.

## PR #1 — chore/m0-bootstrap (M0 process bedrock)

- **Driver:** Imree (direction, approvals, repo/remote setup) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model) + Eyal.
- **Context:** Phase 0 (book v3.0.0 absorbed: clarification page, App C/D/E/F, ch.2/3/4/5/6/7/8/9;
  kit verified; reference repo studied; rubric V3 diffed vs HW6) → Phase 1 decision grill
  (topics a–h + creativity round, each decision argued and approved one-by-one) → Phase 2 gated
  docs (PRD v2, PLAN, TODO, CLAUDE.md + ports plan — each explicitly approved by Imree; PRD/PLAN
  cross-model-reviewed pre-repo, findings adjudicated with sources).
- **This PR:** repo scaffolding (uv/pyproject/quality config), CI workflow + six gate scripts
  (file sizes, anti-patterns, no-hardcoded, sync-core manifest, self-grade validation, submission
  checklist), five adapted skills (eval-harness + self-grade rewritten for this project's
  inversions; HW6's "pipeline not strategy" and "repo is public" lines deliberately removed),
  approved PRD/PLAN/TODO/CLAUDE.md landed, ADR-0001/0002, process templates, package skeletons +
  version tests. Everything adapted from HW6 was audited line-by-line per the porting rule —
  nothing blind-copied.
