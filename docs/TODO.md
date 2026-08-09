# TODO — Cops-and-Robbers P2P Race

> **Status: APPROVED (Phase 2 gate, 2026-07-16).** **This copy: the police (cop) repo.**
> Living document: checkboxes tick as work
> **lands on `main`**, never as aspiration. Statuses: ☐ not started · ◐ in progress · ☑ done.
> Owner key: **I** = Imree (drives, approves, operates sends/arming) · **C** = Claude (authors
> code/docs under I's direction) · **E** = Eyal (reviews, per-task ownership) · **AG** =
> Antigravity (cross-model PR review). Every task's DoD includes: CI green, ≤150-line files,
> tests per TDD, reviewed PR. ⚑ = role-repo-specific task.
>
> **Entry discipline (truth-pass, 2026-08-08):** an entry is a status plus one-to-three lines
> and pointers. Proof lives in `docs/evidence/`, decisions in ADRs, narrative in PR threads and
> `git log` — never here. A ☑ entry that grows past three lines gets compressed, not extended;
> the full pre-compression dossiers remain in this file's git history (`git log -p docs/TODO.md`).

## Phase M0 — Process bedrock *(gate: PRD/PLAN/TODO approved in repo form)*

- ☑ **M0-1** Scaffold both repos (uv, pyproject, ruff/mypy/coverage config, empty `src/` layout per PLAN §3) — I+C. DoD: CI green on empty src in both.
- ☑ **M0-2** Port + adapt CI workflows from HW6 (keyless gates: ruff, mypy --strict, pytest+coverage fail_under, 150-line check, no-hardcoded scan, secret scan) — C, review E. DoD: each gate demonstrably fails on a seeded violation.
- ☑ **M0-3** `scripts/sync_core.py` + `sync_manifest.json` + CI manifest gate — C, review AG. DoD: PLAN §13 M0 drift test observed (induced drift → sibling CI red).
- ☑ **M0-4** CLAUDE.md ×2 (HW6-derived, rubric-V3 diff applied, kit-conformance clause) — C, approve I.
- ☑ **M0-5** Port `.claude/skills/` + `docs/REVIEW_PROCESS.md` — C. DoD: skills reference this project, not HW6.
- ☑ **M0-6** Land approved PRD/PLAN/TODO as `docs/` in both repos (⚑ role deltas applied) — C, approve I.
- ☑ **M0-7** `docs/adr/0001-sync-mirror.md` + `0002-reference-reuse.md` — C.
- ☑ **M0-8** `scripts/check_submission.py` skeleton (App C table 6 + guidelines §17, red until items land) — C. DoD: runs in CI as non-blocking report.

## Phase M1 — Walking skeleton *(PRD_engine + PRD_crypto precede code)*

- ☑ **M1-1** `docs/PRD_engine.md` + `docs/PRD_crypto.md` — C, approve I.
- ☑ **M1-2** `domain/board+rules+scoring` (config-driven, App F guard) — C, review E/AG. Capture-by-barrier, imprisonment, tie rule; ≥90% cov.
- ☑ **M1-3** `domain/crypto` from kit CORE + kit vectors as CI fixtures — C. All CORE vectors green in both repos.
- ☑ **M1-4** `domain/state machine` (transition table per PLAN §5) — C. Property tests reject all illegal transitions.
- ☑ **M1-5** `wire/` dataclasses + validation (mirror reference fields; reject-missing/tolerate-unknown) — C.
- ☑ **M1-6** `infra/mcp` server (4 tools) + client + in-process fake; `peer/` minimal loop — C, review AG. Observed 2026-07-17: full localhost mini-game, self-audit pass (`docs/evidence/m1-p2p-match.md`).
- ☑ **M1-7** `sdk/` facade + CLI entry — C. All M1 flows callable only via sdk.
- ☑ **M1-8** JSONL logger (verbatim bytes, transitions, decisions, provenance) — C. M1 game replayable from log.

## Phase M2 — 🚦 Oracle spike (go/no-go gate)

- ☑ **M2-1** Reference peer as oracle (sha 960499fd); Cloudflare named tunnel, both hostnames (ADR-0006) — I+C. Reachability both directions observed 2026-07-18.
- ☑ **M2-2** Both role pairings vs the live reference over public URLs: negotiate → play → mutual audit Verified OK both directions — I+C. Spike notes §6 + four JSONL logs in `docs/evidence/`.
- ☑ **M2-3** SQ1/SQ2/SQ3 answered in writing against the running reference (spike notes §3/§6) — C.
- ☑ **M2-4** `docs/adr/0003-crypto-early.md` + `0006-deploy-tunnel.md` — C.
- ☑ **M2-5** **GO/NO-GO review — GO, 2026-07-18** (Imree, on Stage A evidence; residual gaps scoped to M3/M6/M7 in spike notes §8) — I.

## Phase M3 — Perception + arena

- ☑ **M3-1** `docs/PRD_scent.md` + `docs/PRD_belief.md` — C, approved I (PR #16).
- ☑ **M3-2** `domain/scent` (kit-pinned form; ADR-0004) — C. Kit pheromone vectors + decay/emission tests green.
- ☑ **M3-3** `domain/belief` exact Bayes filter (motion×scent×hint) — C, review E. Beats last-known-position tracker (PLAN §13 M3).
- ☑ **M3-4** Gazetteer + hint templates; injection-safety tests (hostile hint corpus) — C.
- ☑ **M3-5** Baseline brains (random, greedy-Manhattan) via BrainBase seam — C.
- ☑ **M3-6** Arena harness (seeded round-robin; champion regression gate in CI) — C, review E.
- ☑ **M3-7** 🚦 **ADR-0004 revision — DECIDED: REVISE** (I, 2026-07-18): add `multiplicative_book_v1` beside `subtractive_chebyshev_v1`, pair-locked + refusal rule, belief observation model parameterized. Full assessment record in ADR-0004 v2 + `notes/LEAGUE-COORDINATION-ALON.md`.
- ☑ **M3-8** Named scent models — BUILT (gate PR #56 = approval): `domain/scent_models` + `scent_book`, six kit registrations verbatim in `config/locked_models.json`, `scent_model_sha256` declared at negotiate (SPEC §7 truth table as permanent CI), model hash sealed at step 0. Real finding: the book model costs most of the filter's edge (hit-rate 98%→17%) — later addressed by M7-14's innovation fix. Evidence: `docs/evidence/m3-belief-eval.md`.

## Phase M4 — Observability

- ☑ **M4-1** `docs/PRD_gui_replay.md` — C, approved I (PR #24).
- ☑ **M4-2** Live GUI (heatmap + turn banner; local truth only) — C (PRs #25/#26). Evidence: `assets/m4-live-heatmap.png` + `docs/evidence/m4-observability.md`.
- ☑ **M4-3** Replay verifier (Verified OK / TAMPERED) — C, review AG (PR #27). Rule-19 mutation matrix pinned in CI.
- ☑ **M4-4** Belief-vs-truth overlay + belief-error curve export — C (PR #28).

## Phase M5 — Intelligence ⚑

- ☑ **M5-1** ⚑ `docs/PRD_police_brain.md` — C, approved I (PR #30; ADR-0005 rides it).
- ☑ **M5-2** ⚑ PoliceBrain: expectimax over belief + barrier graph-surgery + capture-commit — C, review E/AG (PRs #31/#32). DoD observed, CI-blocking: 24/32 = 75% vs ref-thief (floor 60%); `docs/evidence/m5-arena.md`.
- ☑ **M5-3** ⚑ ThiefBrain — delivered sibling-side (thief PRs #21/#22, 78% survival DoD there). This copy tracked it as unstarted until 2026-07-20; doc↔repo gap corrected then.
- ☑ **M5-4** Genetic tuning (PR #35): improving fitness curve committed, off-suite validation 75%→94%, evolved weights deployed as config; smoke GA permanent CI. `docs/evidence/m5-ga.md`.
- ☑ **M5-5** Post-audit opponent profiling (PR #38): lie-rate + motion priors with prior-shift CI test; hint trust never below `profile_hint_floor`; belief math untouched.
- ☑ **M5-6** Template-bank A/B (cop PR #39 = the instrument; thief-led measurement, winner `classic` shipped). Lie efficacy real but tiny — disclosed in the thief repo's `docs/evidence/m5-template-ab.md`.
- ☑ **M5-7** `notebooks/results_analysis.ipynb` committed WITH outputs; renders-clean pin permanent CI (PR #40).

## Phase M6 — Reporting & fairness rail

- ☑ **M6-1** `docs/PRD_reporting.md` + `docs/PRD_gatekeeper.md` — C, approved I (PR #43).
- ☑ **M6-2** Four artifact schemas + writers; byte-level conformance battery vs reference sample-run as permanent CI (PR #44). ⚠ Consensus signature = SHA256 over spaced-separator dumps, sign-then-insert (a third canonical variant — credit Alon; verified vs reference `report_writer.py`).
- ☑ **M6-3** Step-0 declaration builder + signing (PR #45); token counts sealed INSIDE the record; real-HEAD commit pin in CI.
- ☑ **M6-4** Gmail sender + interlock (PR #47); live draft observed 2026-07-20 (`docs/evidence/m6-email.md`). Draft posture later superseded for counted play by M7-6/ADR-0008; the rail itself stayed correct.
- ☑ **M6-5** Gatekeeper (quota → token bucket → DoS lock; limits ≥ signed minimums) — C (PR #46). Load test + breaker trip/cooldown/reset in CI.
- ☑ **M6-6** Series runner (`num_games`, per-game config commit, role alternation per F2) — C (PR #48).
- ☑ **M6-7** Chaos drill harness + watchdog/persistence (FR-8) + FR-11 scent-physics evidence check — C, review E (PR #50). 10-drill battery permanent CI; `docs/evidence/m6-chaos.md`.
- ☑ **M6-8** COST.md + token accounting (PR #49); `test_zero_tokens.py` makes the 0-token claim tamper-evident.

## Phase M7 — League ops *(nothing announced unless true of the tree)*

> ⚑ M7-16, M7-21, M7-30, M7-46, M7-47, M7-51 are thief-repo milestones — see its TODO.
> Core fixes below marked "mirrored" reached the sibling via the sync ritual (its sync commits).

- ◐ **M7-0** Wire-shape mutual ADR — text landed as `docs/adr/0010-wire-shape.md` (PROPOSED) + the 2026-08-01 three-tier addendum; balance evidence `docs/evidence/wire-shape-balance.md` (PR #41). **The DoD (both teams' signatures) was never met — signatures were never collected** — but the counted series vs anrbj666 played and cross-agreed byte-level anyway (M7-41), and one-counted-per-opponent means no counted game vs them remains. **Disposition: no longer a blocker; at M8 either record it closed-as-overtaken or collect the kit co-sign for its own sake.**
- ☑ **M7-1** Sparring capability — **delivered in evolved form (Imree's ruling 2026-08-08): the hosted host was superseded by the KIT's local sparring peer** (`sparring/` in the kit repo — full rulebook, no mail, `python -m sparring.cli selfplay`, docker "await" mode a peer can dial, `sparring-` group-id prefix). Local-not-hosted is deliberate (kit SPEC, "Sparring peer" note), which voids OI-4's 24h-hosted DoD. Our repo-side guard (`shared/sparring`, 2026-07-22: no tuned weights, no mail) stands for any future hosted use.
- ☑ **M7-2** Kit additions — **verified against the kit tree 2026-08-08; all substance landed** (largely by kit-side sessions): `tools/netcheck.py` + pre-match discipline (`docs/LEAGUE-OPS.md`), SPEC `_g<NN>` naming, `vectors/report_consensus.json` (spaced form, sign-then-insert, Alon's team credited by name), the Host-header/421 note (SPEC App D), scent-model + lock-schema vectors (`locked_model.json`, `scent_book_v3.json`, `smell_binding.json`), wire-shape registrations with `bookletter-v3` as a documented deviation, audit fixtures via `examples/pairing-artifacts` + `tools/check_artifacts.py`. One divergence from the original list, deliberate: formal JSON Schemas were never added — the kit chose executable vectors instead.
- ☑ **M7-3** First external friendly PLAYED AND AUTO-REPORTED 2026-07-25 (imreeyal 75–35 vs anrbj666, six sub-games, all audits clean, replays Verified OK, one auto-report to both teams). Evidence: `docs/evidence/m7-3-first-external-friendly.md` + `reports/imreeyal/`. Both raised discrepancies resolved 2026-07-26.
- ☑ **M7-4** First counted series — discharged by M7-41 below.
- ☑ **M7-4b** *(a second entry historically also numbered M7-4)* Live-series machinery: sealed `--sub-game` index seam, `report/summary_from_log` + `series_from_logs` (report exactly what we archived; refuse an incomplete series), `sdk/live_series` as the series owner, `RunMode` CLI flags. Evidence: `docs/evidence/m7-4-live-series.md`. Its two residuals (full 6-sub-game rehearsal, live send) were discharged by M7-10/M7-27.
- ◐ **M7-5** Counted series vs distinct teams — **two played, App F pass floor met** (anrbj666 M7-41; uoh-sqak M7-52, won +10 diversity). Third candidate best2934: their kit-CORE handshake gap closed BY THEM (`05b3886`), but the 2026-08-08 19:00 friendly did not play — **tool-name dialects disjoint except `negotiate`**; they are adopting our four-tool dialect (kit `vectors/turn_message.json` + SPEC §7.5 pin it), T unnamed pending their build. gal-roy1 counted offer (kit #48, through Tue 11 Aug) held on Imree's word.
- ☑ **M7-6** 🚦 Email posture correction (ADR-0008, PRs #54/#55): automatic send is the posture (App E rules 32/35, §9.3); **authorization = the configured recipient**; draft dropped, token re-consented to `gmail.send` only (verified: `getProfile` 403s); recipient is a list; artifact attached (rule 34); lecturer-guard refuses his address whenever `counted` is false. CLAUDE.md #16/§4 amended in both repos + parent workspace.
- ☑ **M7-7** 🚦 Real-tunnel kill-drill defects — all four fixed + push-exhaustion residual (PR #60): watchdog measures loop liveness not I/O (signed budget untouched), snapshot pinned to `logs/`, flush-before-exit, replay reads `peer_result` + ≥1-record guard. Live re-drill + both mid-push drills clean (lost by rule, not self-termination). Evidence: `docs/evidence/m6-chaos.md` §M7-7 + drill logs.
- ◐ **M7-8** At-least-once inbound tolerance — code half + them→us live half DONE (`peer/inbox_order.InboundSequencer`, dedup keyed on the commit; 6 chaos drills; live duplicate absorbed over the real edge 2026-07-22, evidence §M7-8). **The us→them-dedup and reorder live halves were never drilled; two clean counted series have since retired the practical risk. Disposition: accepted residual — KNOWN_LIMITATIONS candidate at M8.** (Reference-oracle finding kept on record: the reference applies duplicates twice — a physics mismatch we raise may be caused by a duplicate WE sent; evidence-grade only.)
- ☑ **M7-9** `RunMode` split (ADR-0009): `strict_rules` × `counted_series`; lecturer needs BOTH by construction; `--rehearsal`/`--counted` CLI flags carried into every child. Recorded honestly: before this, every live game ran with App F rows disarmed.
- ☑ **M7-10** Handshake pairing + redelivery + port guard (+ M7-10b preflight: a report-owing run refuses to start if it cannot deliver): `negotiate` declares sealed `sub_game_number` + `role`, kit §7 truth table (omission never refuses); agreement re-pushed each lap; one live peer per role. First project email really sent 2026-07-24. **Opponent's half confirmed on the wire by Alon/Renat (Round 15) — closed both directions.**
- ☑ **M7-11** Per-role opponent dialing (`sdk/series_endpoints`; role-split topology) + **M7-11b** bystander refusal (`PairingRefusal` refuses on the record and keeps waiting, bounded). Rig-proven vs a faithful two-runner simulator; vs Alon's shape we run `--role thief`.
- ☑ **M7-12** Refusal names absence, not just disagreement (terms-less bookletter greeting vs value-unequal terms — distinct messages; pinned both ways).
- ☑ **M7-13** Capture postmortem of the friendly (g02/g06 mechanism = opponent-position modeling; our claim-per-step habit hands a claim-reading evader our cop's cell — fed M7-18/19). Evidence: `docs/evidence/m7-13-capture-postmortem.md`.
- ☑ **M7-14** Strategy under counted physics: scent-model doors for referee/arena/GA, `BeliefEvaderBrain`, **the belief innovation fix (argmax 17%→61% under book-v1)**, book-v1 GA retune committed but NOT deployed. Evidence: `docs/evidence/m7-14-bookv1-strategy.md` + generated instruments.
- ☑ **M7-15** Generalist retune: `opponent_pool` GA fitness, four-cop/five-thief gate both physics, `[strategy.<role>.<scent_model>]` overlays — pool vector deployed on the book-v1 overlay, base table keeps the proven reference vector.
- ☑ **M7-17** `game_id` = the sorted pair, derived like the reference (`domain/crypto.series_game_id`); all construction sites derive; historical artifacts stay as played.
- ☑ **M7-18** Claim channel half 1: `BeliefFilter.note_claim` hard collapse — tracking at decision time 0.311→0.936 under book-v1; corrected the committed model (channel is LAG 0, not lag-1). Evidence: `docs/evidence/m7-18-claim-channel.md`.
- ☑ **M7-19** Claim channel half 2 (quiet cop): claim-gated landing capture in the referee + `ClaimPolicy` on the live emitter; sweep says one standing threshold (0.1) is best-or-tied vs readers AND non-readers — deployed on the book-v1 police overlay. A claim-reader's tracking of our cop falls 0.936→0.433. Evidence: `docs/evidence/m7-19-quiet-cop.md`.
- ☑ **M7-20** Cop retune under the claim policy — **NULL RESULT, not deployed** (loses the champion gate in both physics; weights kept as a labelled negative artifact). Reusable lessons recorded: measure per-member spread before believing a flat GA curve; the claim policy removes its own selection pressure. Evidence: `docs/evidence/m7-20-ga-under-the-claim-policy.md`. Research follow-ups it named were overtaken by M7-45/48/49 matchup work.
- ☑ **M7-22** Derived `game_uid` declared at negotiate (refuse a comparable mismatch at T instead of at the report diff; omission never refuses) — the mutual closure of the opponent's 2026-07-25 uid bug.
- ☑ **M7-23** In-play scent-frame validity check (`domain/scent_frame.frame_explained`, verdict-only firewall; refusal tally rides settlement; FP=0 pinned). PRD_scent §10; evidence in PRD status note + tests.
- ☑ **M7-24** DECIDED 2026-07-29 (Imree + opponent concurring): NO wire change — `transmitted: false` not enforced on send for the counted series; `{}` convention agreed. Registry question routed to the kit.
- ☑ **M7-25** `info_mode_sha256` declared at negotiate (Round-16 settlement; counted series plays `info_mode: belief`); `{}` = absence of data, never impossible data.
- ☑ **M7-26** Concede pin: a caught final is never refused, even as a zero-step re-send (Round 17; both shapes pinned; their convention accepted into the kit §7 co-sign text).
- ☑ **M7-27** Cross-team warm-up + report diff 2026-08-01 (window 2 complete: 60–40, 4–2; all Rounds-15–19 mechanisms promoted live; report substance agreed, four cosmetic deltas → M7-28). Evidence: `docs/evidence/m7-27-warmup-report-diff.md`.
- ☑ **M7-28** Result conformance: own `github_commit` from the sealed step-0 (book-over-reference, documented), `log_files` flat. TDD; mirrored.
- ☑ **M7-29** Thief adjudicates rules 46/47 against itself — concede at the seal via the mandatory caught-final shape (opponent's finding, verified on all three prongs; their symmetric half stands their side). Six pins.
- ☑ **M7-31** Referee thief Observation carries the barrier quota (closes the thief M7-30 instrument defect at the core; cop arenas proven inert byte-identical).
- ☑ **M7-32** Warm-up 2 (2026-08-03): score EQUALS his corrected adjudication (45–85), M7-28/29 proven live, artifacts converge — **the counted gate was met here.** Evidence: `docs/evidence/m7-32-warmup2-convergence.md`.
- ☑ **M7-33** Both `github_commit` columns honestly (role-aware own via `commit_for_module`; opponent's from their revealed step-0; "unknown" never invented).
- ☑ **M7-34** League fields in `final_result` (`games_played_including_this`, `first_meeting_between_groups`, `diversity_reward_applied`) from the `counted_opponents` ledger; warm-ups count nothing; fields stay outside the signed symmetric outcome.
- ☑ **M7-35** Two-channel identity: `counted_games_played` + step-0 commit declared at negotiate in plaintext, sourced FROM the sealed record so our channels agree by construction.
- ☑ **M7-36** 16:00-window artifact defects: log-rebuild path learns the opponent commit (`domain/step_zero.revealed_commit`, shared by both paths); league bump keys on `counted_series`, not `strict_rules` (no more false counted claims in rehearsal artifacts).
- ☑ **M7-37** Four-template evidence mail (Moodle item 4 superset read) — **attachment policy superseded by M7-40**; the artifact SET still lands in the repos; multi-attachment transport kept + pinned.
- ☑ **M7-38** Identity reader accepts the declaration-shaped `hardware_spec` key beside `spec` (their 16:00 null-hardware mystery = our missing tolerance; validated on the real log).
- ☑ **M7-39** Four repo links ride the result (`report/league.github_links`; rule 49 + p.96; opponent links only from what THEY declared) + the truthful `_remark` (single deliberate divergence from the reference sample, pinned exactly).
- ☑ **M7-40** Series mail is result-only again (Round 29: chatbot ruling + the reference's own emailing code + pair symmetry); one-line flip back retained if the lecturer ever rules otherwise.
- ☑ **M7-41** 🏁 **FIRST COUNTED SERIES** vs anrbj666 (2026-08-04, T=01:00): 30–90, six sub-games, all audits clean, one report to the lecturer alone, **cross-team agreement byte-level** (`mutual_agreement.sha256` matched). Ledger advanced to 1. Evidence: `docs/evidence/m7-41-counted-series-anrbj666.md` + `reports/counted-series/imreeyal/`.
- ☑ **M7-42** Audit continuity keys on record TYPE, not step number (uoh-sqak g01 settlement failure — root cause ours; closed set of non-game types, tamper-check kept; verified against his real bytes) (PR #107). The scent-registration underdetermination it exposed (combine + snapshot anchor) was settled with them pre-series: combine=`max`, order=`deposit_then_decay`.
- ☑ **M7-43** (+43b/44) Series pacing + completeness: hold, catch up, never settle an empty window; a partial series is never reported as whole (the 2-of-6 mail defect fixed) (PR #108).
- ☑ **M7-45** best2934 modeled as arena arms from their real code; matchup measured ~79–51 favoured (PR #109). Lesson pinned: never quote a rate from an instrument with one of our channels off.
- ☑ **M7-48** uoh-sqak's rebuilt thief as an arm (their Barrier Law fix + thief rewrite; 56/64 at the signed start; their thief is NOT deterministic) (PR #110). Evidence: `docs/evidence/m7-48-sqak-rewrite.md`.
- ☑ **M7-49** ⚑ The cop must not wall itself away from the thief — mass-weighted lockout veto (`lockout_mass_threshold`), worth 88%→97% vs their evader at the signed start (PR #112).
- ☑ **M7-52** 🏁 **SECOND COUNTED SERIES WON** 60–40 (4–2) vs uoh-sqak (2026-08-08) — **App F pass floor met (2 counted vs different groups), +10 diversity**; mutual sha matched byte-for-byte both ways; ledger advanced to 2 in both repos (PR #113).
- ☑ **M7-53** Absorb the opponent's opening handover (best2934's step-0 nil turn no longer collapses us into a technical loss on our cop windows) (PR #114).
- ☑ **M7-54** A signature refusal names the construction (PR #115).
- ☑ **M7-55** Opponent identity at negotiate — a stranger naming a different group is refused without consuming the window; omission never refuses (closes the rule-35 false-record shape; uoh-sqak's framing, credited). The rescued `9e7cd1c` re-landed and **merged as PR #117** (main `ee88445`); thief sync rides its PR #78.
- ☑ **M7-57** Every outbound tool call carries an explicit deadline (`[network] call_timeout_seconds`, reconciled against the SIGNED `response_timeout_sec` as budgets rule 6). `McpToolClient` passed no timeout, so a delivered-but-unanswered push inherited the transport library's own default; two of those plus a retry put our turn on the wire **61.0 s** after the opponent's, inside their signed 30 s budget — both best2934 sub-games died there (2026-08-09 friendly, their clock and ours agreeing to the second). Diagnosed by best2934 from the interval alone; their LLM-fallback hypothesis was wrong (`llm_model = "none"`) and the cause was the transport. **Open follow-up: we still open a NEW MCP session per call, which is the behaviour that makes their server stop answering in the first place.**

## Phase M8 — Submission hardening

- ☐ **M8-1** README academic reports ×2 (§9.4.2 sections + user-manual sections + contradiction-choices narrative + screenshots + sibling links) — C, review E+AG, approve I. DoD: `check_submission.py` README items green.
- ☐ **M8-2** KNOWN_LIMITATIONS.md + SELF_GRADE.md (`self_grade.py` output; code-quality only) — C, approve I.
- ☐ **M8-3** Full checklist sweep (`check_submission.py` fully green both repos; guidelines §17 + App C table 6) — C+I.
- ☐ **M8-4** Annotated tags `v1.0-submission` pushed both repos; Moodle per-member submission + PDF form + group ID (OI-1 resolved) — I.
- ☐ **M8-5** Final doc↔repo alignment audit (README numbers vs tree; PROMPTS.md truthful/complete) — C+I. DoD: zero contradictions found.

## Standing (every phase)

- ☐ **S-1** PROMPTS.md per PR (committed work only) — C.
- ☐ **S-2** Conventional commits; branch→PR→AG review→squash; never push main — all.
- ☐ **S-3** TODO statuses updated as work lands — C.
- ☐ **S-4** Risk register reviewed at each milestone exit (PRD §10) — I+C.
- ☐ **S-5** No email is ever sent to an address I has not configured for that run, and **never to the lecturer** without his explicit word — I (mechanical: the interlock refuses an empty recipient list, and refuses the configured `lecturer` address whenever `counted` is false). Reworded 2026-07-20 by ADR-0008. Outreach mail keeps the original per-send rule — see the parent-workspace `CLAUDE.md`.
