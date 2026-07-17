# M3-2 scent-verification friendly — our COP vs the reference THIEF (2026-07-18)

> Closes residual gap #3 from the M2 spike notes §8 (scent live-interop untested — our
> M2 grids were legally empty). **One** keyless friendly, authorized by Imree for the
> M3 overnight session, this pairing only: our cop vs the reference thief is F9-safe
> (thieves place no barriers; the full pairing waits for the M3-3 barrier fix).
> Friendly — draft-tier, no league reporting, nothing announced.

## Setup

| Item | Value |
|---|---|
| Reference | `FinalProject\reference\Game-P2P-Cop-Chase`, pinned sha `960499fd` (v3.0.0) |
| Transport | Cloudflare named tunnel `copthief`: our cop bound :8802 behind `cop.imreeyal.com`, reference thief :8801 behind `thief.imreeyal.com` (Host-rewrite per ADR-0006) |
| Keyless posture | Ours: template hints, no LLM path exists at M3-2. Theirs: `--stub-llm`, `[trash_talk] provider="template"`, `email.enabled=false`. 0 tokens both sides |
| Our commit | `feat/m3-scent` @ the M3-2 tree (PR #17, CI green before the run) |
| Command (ours) | `uv run copthief run peer --role police --seed 11 --port 8802 --opponent-url https://thief.imreeyal.com/mcp --log docs/evidence/m3-scent-friendly-g1.jsonl` |
| Command (theirs) | `uv run python -m police_thief peer --role thief --stub-llm --no-gui` |

## Result

| Check | Observed |
|---|---|
| Outcome | `thief_survival`, 35 steps (their count) / 34 ours — the known one-turn-short asymmetry on the inbound win claim |
| Shared game_uid | `f757f50d-d4f4-17e7-06cf-755905739b16` — derived identically both sides (matches M2 g4: same terms, same groups) |
| Our audit of theirs | **Verified OK** (`audit_ok: true`, `problems: []`) |
| Their audit of ours | **passed, 34/34 steps verified, failed_steps []** (their `thief_match.json` summary) |
| Mutual agreement | `mutual_agreement.confirmed = true` in their result artifact |
| Their process | exit 0, full artifact set written under `logs/segal-thief-team/` (no F8b-style crash) |

## Scent findings (the point of the run)

1. **Our transmitted grids are live-compatible.** All 34 of our turns carried a
   non-empty `smell_grid` with exactly one fresh center at `0.8` and locked-model ring
   values (first turn observed verbatim in the JSONL: center `1,0` = 0.8, ring-1 = 0.5,
   ring-2 = 0.2). The reference consumed every one — its belief pipeline
   (`observe_smell`) multiplies our values in directly, and its game/audit completed
   normally.
2. **The locked scent-model negotiate extra is reference-safe, live-confirmed.** The
   handshake carried our `scent_model` document; the reference (whose `verify_peer`
   indexes only `terms`/`nonce`/`signature`/`identity`) ignored it exactly as
   source-pinned, agreed terms, and derived the same game_uid.
3. **Their grids are consumable by us.** Every inbound reference turn passed wire
   validation and was absorbed + decayed into our `known_field` (any failure would have
   collapsed the session to TECHNICAL_LOSS; the game ran to survival).
4. **SQ3 re-confirmed at M3-2:** smell grids appear in NEITHER side's sealed records —
   the audit passes are position/move-sealed only; grids stay unauthenticated
   (belief-layer trust stance, PRD_belief).

## Limitation (honest)

Our JSONL records our OUTBOUND turns verbatim but not inbound message bytes, so the
reference's transmitted grid values are not archived on our side (nor in its own log
artifact — sealed records exclude grids per SQ3). Inbound-verbatim logging is worth a
line in the M4 replay/observability scope; for this friendly, inbound compatibility is
proven by live consumption, not by archived bytes.

## Artifacts

- `docs/evidence/m3-scent-friendly-g1.jsonl` — our full outbound log (negotiated + 34
  turns + audit + peer_result).
- Reference-side artifacts remain in the reference checkout (not committed here —
  EULA posture, ADR-0002); the verdict lines above are quoted from
  `logs/thief_match.json` and `logs/segal-thief-team/result_imreeyal-vs-segal-thief-team.json`.
