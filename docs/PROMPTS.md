# Prompt Engineering Log

> Truthful, per-PR entries for **committed** work only (CLAUDE.md §7). Development prompts —
> runtime agent prompts live in source. Format: PR · driver/reviewer · what was asked · outcome.

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
