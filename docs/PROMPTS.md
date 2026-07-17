# Prompt Engineering Log

> Truthful, per-PR entries for **committed** work only (CLAUDE.md §7). Development prompts —
> runtime agent prompts live in source. Format: PR · driver/reviewer · what was asked · outcome.

## PR — feat/m2-symmetric-transport (M2 spike, fix batch 2: F1–F2)

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
