# PRD — Reporting rail (mechanism PRD, milestone M6)

> **Status: DRAFT (gate M6-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-9
> (reporting rail) + FR-13 (series operations) + G4/G5, `docs/PLAN.md` §4 (reporting flow) +
> §7 (artifact schemas) + §13 (M6 exit). Sources of truth: book ch.8 (official Hebrew report)
> + ch.9 (each team emails its copy separately) + App A (Gmail flow) + App C (artifact table) ·
> reference `report/` package + `docs/sample-run/` **@960499fd — oracle only, ADR-0002** ·
> League coordination: the consensus-signature find is **credited to Alon** (verified by us
> against `report_writer.py` lines 22–25/81; `notes/LEAGUE-COORDINATION-ALON.md`) · HW6
> `email/gmail.py` + `scripts/gmail_auth.py` (frozen; mined per porting rule). Covers TODO
> **M6-2 / M6-3 / M6-4 / M6-6 / M6-8**. Consumes `peer/sealing` + `peer/settlement` (M2/M5),
> `strategy/profiling` (M5-5), `domain/crypto` (M1-3).

## 1. Scope & non-goals

**In scope:** (M6-2) `report/` package — four artifact builders/writers + the Hebrew report +
the consensus signature, validated **byte-level** against the reference `docs/sample-run/`;
(M6-3) `shared/sysinfo` + step-0 declaration record (real commit hash, game-count) + per-step
token counts INSIDE the sealed record; (M6-4) Gmail sender with draft default + the arming
interlock; (M6-6) series runner (`num_games`, role alternation, profiling carry); (M6-8)
COST.md + token accounting on every LLM path.
**Non-goals:** gatekeeper/chaos/watchdog — `docs/PRD_gatekeeper.md` (M6-5/M6-7; the email
sender CALLS the gatekeeper, built there) · M3-8 named scent models (own thread, still gated)
· M7-0 wire-shape ADR · kit posts (M7-2 carries the consensus-signature vector, credited) ·
any email actually sent (constraint #16: draft-only until Imree's per-send word) · no change
to wire format, canonicalization of existing constructions, or commit hashing (constraint #13:
kit CORE vectors stay untouched and green; the sealed-payload key-set grows, §4).

## 2. Book model & reference behavior absorbed (the M6-2 facts)

**The consensus signature is a THIRD canonical variant** (settlement-critical; Alon's find,
re-verified): `SHA256(json.dumps(data, sort_keys=True, ensure_ascii=False))` with **DEFAULT
spaced separators** `(", ", ": ")` — NOT our kit-CORE compact form. The reference uses it in
four places: (a) the Hebrew report's `חתימת_קונסנזוס_משותפת` — computed over the report dict
**BEFORE** the key is inserted (**sign-then-insert**); (b) the log artifact's
`mutual_agreement.sha256` over the full `records` list; (c) the result artifact's
`mutual_agreement.sha256` over a **symmetric-outcome dict only** (`{game_id, aggregate,
sub_games:[{sub_game_number, roles, result, winner_group, score}]}` — never per-peer tokens or
timestamps, which legitimately differ); (d) each declaration `group_block.signature`
(sign-then-insert again, over the block sans signature). The compact kit form stays for
`config_sha256` and ALL wire crypto. Both canonicals coexist deliberately — distinct helper
names (`canonical_str` vs `consensus_signature`) so one can never silently substitute for the
other; a `report_consensus_signature` kit vector is proposed at M7-2 (credit Alon by name).
**Why settlement-critical:** the emailed reports are what the lecturer adjudicates from — each
team emails its copy separately (book ch.9) and neither sees the other's outbox, so agreement
is checkable ONLY because both sides independently derive the SAME consensus signature from
the audited symmetric outcome. An opponent whose emailed report lies breaks that match, and
the sealed records + verbatim logs adjudicate. Corollary: a friendly **report exchange**
(each team sends the other its report; both check the signatures match byte-for-byte) is the
natural pre-counted cross-check of the two implementations — planned with Alon's team,
sequenced under M7-3 league ops, sends armed per S-5 as always.

**The four artifacts** (English-keyed, `schema_version "1.1"`, long `_schema` prose strings +
a `links` block with `_remark` — interop-required shape constants, attributed in the ADR-0002
log): `declaration_<game_id>.json` · `config_<game_id>_g<NN>.json` (`<NN>` = `%02d`) ·
`log_<game_id>_g<NN>.json` · `result_<game_id>.json`; filenames derived from `game_id`; each
peer writes into its own `logs/<group_id>/` subfolder (roles alternate — group_id is the
stable per-peer key). Serialization: `json.dumps(data, ensure_ascii=False, indent=2)`, UTF-8,
no trailing newline — the byte-level fixtures pin exactly this.

**Book §8 vs reference (contradiction → documented choice, D2):** the book's official report
is Hebrew-keyed; the running reference **emails the English result artifact** (body =
`json.dumps(result, ensure_ascii=False, indent=2)` — the same bytes as the file) and writes
the Hebrew report locally. We mirror the reference: email body = the result artifact **read
from disk** (canonical bytes = emailed bytes by construction, PLAN §4), subject
`"Police-Thief series result: winner <winner_group> (reported by <role>)"`; the Hebrew report
is built per book §8 (result vocabulary `לכידה/הישרדות/תוצאה_טכנית/פסילת_זיוף`, verified
step-log from inbound history, spec declaration read from the sealed step-0 record) and
written beside the four artifacts as `report_<game_id>_g<NN>.json`. ADR + README narrative.

## 3. M6-2 — artifact schemas & writers (`report/`)

`report/artifact_schemas.py` (shapes + `_schema` constants + validation: reject missing
required, tolerate unknown) · `report/artifacts.py` (pure builders, no I/O) ·
`report/report_writer.py` (Hebrew report + `consensus_signature`) · `report/emit.py` (disk
wiring for a whole series; returns the result dict for emailing). Per-game summaries come from
a reference-shaped summary built at settlement (result vocabulary via the existing
`wire_result` mapping; `history` = the verbatim inbound TurnMessages the session already
keeps; audit block `{passed, verified_steps, failed_steps}`). Every artifact is
schema-validated **before** write or send (PLAN §7).
**Byte-level DoD mechanics (permanent keyless CI, sample-run files as attributed fixtures):**
recompute `config_sha256` from the sample config's own terms → equality · recompute both
declaration group signatures → equality · rebuild the result's symmetric dict → equality with
its embedded `mutual_agreement.sha256` · recompute the log's records hash → equality · our
writer serializing the sample dicts reproduces the reference files **byte-for-byte** · Hebrew
report property: the signature verifies over the report-sans-key (sign-then-insert pinned).

## 4. M6-3 — step-0 declaration + sealed token counts + sysinfo

**`shared/sysinfo.py`:** stdlib-only best-effort hardware collection (os, cpu_type, cpu_cores,
cpu_freq_mhz, ram_gb, gpu_type, gpu_cores_or_cuda, vram_gb — the reference's spec key set);
every probe degrades to `"unknown"`, never raises; mocked in CI. Fills the handshake
`identity.spec` (closing the F8b `{}` placeholder) and the declaration's `hardware_spec`.
**Step-0 sealed record** (`peer/sealing`): payload `{step: 0, type: "system_spec", spec,
model, code_version, group_name, sub_game_number, github_commit, num_games_declared}`.
`github_commit` = the exact commit hash played, read once at startup (`git rev-parse HEAD`,
infra seam); the DoD test asserts the REAL repo HEAD lands in the record. `num_games_declared`
seals the truthful game-count declaration (rules 37–38). Note for the record: the reference's
log `_schema` says step-0 carries `github_commit`, but its code omits it (result shows
`"unknown"`) — we close their gap on our side; our result artifact fills our own commit hash
and reads the opponent's from their step-0 when present, else `"unknown"`.
**Sealed per-step tokens:** `seal_turn` payload gains `model`, `tokens_step`, `tokens_total`,
`response_seconds` (the reference's own sealed schema, SQ3 list) — delta accounting from the
LLM-provider seam; the 0-token template path charges 0 every step. Sealed records are
self-consistent per side (audit re-hashes bytes, not grammar — M5-2 precedent), so this is
interop-safe; we do NOT mirror `prompt_discussion`/`random_move` (0-token path has none; hint
provenance already lives in the JSONL `decision` event — disclosed deviation, D3).
**Constraint #13 discipline:** commit construction, canonical form, and wire messages are
untouched — kit CORE vectors re-run green; the rule-19 mutation matrix **extends to every new
sealed field**; replay stays tolerant of pre-M6 logs (M2–M5 evidence keeps verifying).

## 5. M6-4 — Gmail sender + arming interlock

**HW6 salvage:** `GmailTransport` (pure `build_raw` MIME→base64url, lazy Google-SDK import) +
one-time `gmail_auth.py` consent (OI-5: re-verified against HW6's working flow at build time).
Google libraries land as an optional uv dependency group (`email-live`) — keyless CI never
installs it (D5). `token.json`/`client_secret.json` git-ignored; `.env-example` updated.
**`[email]` TOML section (private):** `enabled` (default **false**), `mode` (default
**"draft"**), `recipient`, `sender`, `token_path` — config-owned, never signed.
**Interlock (constraint #16, mechanical not vigilance):** the send path requires ALL of
`enabled=true` ∧ `mode="send"` ∧ a per-invocation arming argument in which the operator
retypes the exact `game_uid` being reported (`copthief report send --game <uid> --arm <uid>`);
any shortfall → loud refusal, logged. Draft mode **provably cannot send**: the draft path
never constructs a send call (fake-transport truth-table test over all
enabled×mode×armed combinations — exactly one sends). Sparring hosts hard-pin draft (PLAN §2)
— asserted at startup. Every email invocation passes through the gatekeeper (`service=
"email"`, PRD_gatekeeper). **No send ever happens without Imree's explicit per-send word.**
**The recipient is per-run private config and the interlock is recipient-agnostic:** the
lecturer for counted series, a peer team for an authorized friendly report exchange (§2),
ourselves for live tests — arming gates WHETHER anything sends, never WHERE; each armed send
logs its recipient alongside the retyped game_uid. Nothing pins the rail to one address.
**D1 — draft semantics (decision):** PLAN §13 says "report lands as Gmail **draft**", but
CLAUDE.md §4 pins a **send-only** scope — and `gmail.send` cannot create drafts. Options:
**(A, recommended)** `gmail.compose` scope (create/send drafts; still cannot read the
mailbox): the draft lands IN Gmail — observable exit criterion, same behavior as the
reference, and Imree reviews the literal bytes in Gmail before anything leaves; requires a
one-line CLAUDE.md §4 amendment ("compose-scope: least privilege that supports the draft
rail"). **(B)** strict `gmail.send` + a local outbox directory as "draft" — stronger least
privilege, but deviates from PLAN's observable wording. Imree picks at this gate.

## 6. M6-6 — series runner

`sdk` entry `run_series`: server + transport built ONCE; one `PeerSession` per sub-game;
**roles alternate** (natural role on odd sub-games, opposite on even — the M2 F2 pin);
`num_games` from the signed constitution; per-sub-game seeds from config. **Profiling carry
(M5-5 seam):** a verified audit's profile shifts `hint_trust` for mini-game 2+ (floor
respected; the prior-shift CI test already pins the math). Per sub-game: config artifact
written + committed per CLAUDE.md §4; summary collected; at series end `emit.py` writes all
four artifacts and the per-game Hebrew reports. Role alternation live-vs-reference is the M2
§8 residual gap 4 — the DoD here is the **local** full series (in-process fake in CI + a real
two-process localhost series as committed evidence); a reference cross-check rides the next
friendly Imree authorizes.

## 7. M6-8 — COST.md + token accounting

`COST.md` (honest-disclosure triad): per-series token spend table where **every 0-token claim
carries two independent proofs** — the JSONL decision/gatekeeper events AND the sealed
`tokens_step`/`tokens_total` fields (M6-3), making the claim cryptographically auditable via
replay. Token accounting on every LLM path: the provider seam exposes per-call usage, the
gatekeeper logs it, the template path is constant-0. README numbers == repo state at every
commit (the one fatal failure mode).

## 8. Configuration

No signed value changes; App F guard untouched. New private `[email]` section (§5) +
`[paths]` artifacts root; `game.toml` version bump; `config_model`/`private_config` extended.
New optional dep group `email-live` (D5). Scanner stance: artifact schema strings and Hebrew
key constants are schema data, not quantitative values.

## 9. Decisions requiring approval (with the PRD)

- **D1 — Gmail scope/draft semantics:** A (`gmail.compose`, Gmail-draft rail, CLAUDE.md §4
  amendment) vs B (strict `gmail.send`, local-outbox draft). Recommendation: **A**.
- **D2 — email body = English result artifact** (reference-mirrored), Hebrew report written
  beside it (book §8 satisfied on disk) — the book-vs-reference contradiction choice; ADR.
- **D3 — sealed-payload extension key set:** + `model/tokens_step/tokens_total/
  response_seconds` (+ step-0 `github_commit`, `num_games_declared`); no `prompt_discussion`
  mirroring. Self-consistent-per-side stance re-affirmed.
- **D4 — reference `docs/sample-run/` files as attributed byte-level CI fixtures** (ADR-0002
  log entry; data, not code).
- **D5 — optional `email-live` dependency group** (Google SDK; second deliberate dep family
  after `viz`; keyless CI unaffected).

## 10. Test plan (TDD; keyless CI)

Unit (happy + error): consensus signature — spaced-form pins against reference-derived
vectors, Hebrew payloads, sign-then-insert property, and a **cross-guard** (compact ≠ spaced
on a nested fixture) · builders — all four shapes + Hebrew report; validation rejects missing
required fields · writers — §3 byte-level fixture battery · sysinfo — every probe's degrade
path · step-0 — real HEAD asserted; game-count sealed · sealing — token fields present, delta
accounting, rule-19 matrix extended, pre-M6 log compat · gmail — `build_raw` MIME pure test;
interlock truth-table (exactly one of eight combinations sends, on a fake transport; draft
constructs no send call) · series — alternation, profiling carry, seeds, truthful game-count.
Integration: full local series over the in-process fake → four artifacts validate + Hebrew
reports signed + every log replays Verified OK. Coverage ≥85%/≥90% core; files ≤150 lines;
`mypy --strict`; ruff + format clean.

## 11. Acceptance criteria (binary — PLAN §13 M6 exit + gate hygiene)

- Full local series (`num_games` ≥ 2) produces four valid artifacts, byte-validated shapes,
  committed as `docs/evidence/m6-reporting.md` + JSONL/artifacts.
- Report lands as draft (per D1 mode); the send path **provably requires arming** (truth-table
  test green); zero emails sent anywhere in M6.
- Step-0 record carries the real commit hash + sealed game-count; every sealed step carries
  token counts; replay verifies logs old and new.
- COST.md's 0-token claim doubly backed (log + sealed counts).
- Kit CORE vectors green (constraint #13); sync ritual after every mirrored merge (thief
  pytest BEFORE committing the sync); TODO ticks + PROMPTS.md ride each PR.

## 12. Build order & PRs

M6-2 (schemas/writers/consensus) → M6-3 (sysinfo + step-0 + sealed tokens) → **M6-5 from
PRD_gatekeeper lands here** → M6-4 (gmail through the gatekeeper) → M6-6 (series runner) →
M6-8 (COST.md; may ride M6-6's PR if thin) → M6-7 (chaos, PRD_gatekeeper). One branch/PR per
task, cross-model review per `docs/REVIEW_PROCESS.md`, stacked-chain lessons applied
(retarget children before merging parents; conflicts branch-side via `checkout --ours` first;
lead regenerates the manifest, follower keeps the synced one).
