# M5-2 friendly — our TUNED COP vs the reference THIEF, first live outbound barriers (2026-07-19)

> The PRD_police_brain §7 operator follow-up: after M5-2, re-confirm mutual audit in the
> our-cop-vs-reference-thief direction — the first time OUR side places barriers on the
> wire (constraint #13 evidence). Authorized by Imree (2026-07-19 delegated decision:
> "post-M5-2 friendly YES; localhost is sufficient for the byte-level interop evidence").
> Friendly — draft-tier, no league reporting, nothing announced. Three runs; the first
> two each exposed one interop finding (fixed with TDD in this PR), the third is clean.

## Setup

| Item | Value |
|---|---|
| Reference | `FinalProject\reference\Game-P2P-Cop-Chase`, pinned sha `960499fd` (v3.0.0) |
| Transport | localhost: our cop :8802, reference thief :8801 (per the delegated call — the tunnel adds nothing to byte-level evidence) |
| Keyless posture | Ours: template hints, zero LLM. Theirs: `--stub-llm`, template trash-talk, `email.enabled=false`. `tokens_total: 0` in their summary |
| Our commit | `feat/m5-inbound-final-step` (stacked on #36; PR CI green before evidence merge) |
| Our brain | `copthief_police.brain:PoliceBrain` with the M5-4 **evolved weights** from `game.toml [strategy.police]` |
| Command (ours) | `uv run copthief run peer --role police --seed 11 --port 8802 --opponent-url http://127.0.0.1:8801/mcp --log docs/evidence/m5-friendly-g<N>.jsonl` |
| Command (theirs) | `uv run python -m police_thief peer --role thief --stub-llm --no-gui` |

## Result (g3, the clean run)

| Check | Observed |
|---|---|
| Outcome | **`cop_capture`, 13 steps** — the tuned cop caught the reference thief (their summary: `"result": "capture", "winner": "police", "steps": 13`) |
| Outbound barriers | **2**, our first ever on the wire: steps 7 and 11, cells `[2,3]` and `[5,5]` — the reference consumed both (its game continued and its audit verified our barrier turns) |
| Shared game_uid | `f757f50d-d4f4-17e7-06cf-755905739b16` — derived identically both sides (matches M2 g4 / M3: same terms, same groups) |
| Our audit of theirs | **Verified OK** (`audit_ok: true`, `problems: []`) |
| Their audit of ours | **`passed: true, verified_steps: 13, failed_steps: []`** — including our two sealed BARRIER turns (their `thief_match.json` summary) |
| Mutual agreement | `mutual_agreement.confirmed = true`; `final_result.winner_group = "imreeyal"` (their result artifact) |
| Replay | `uv run copthief replay --log docs/evidence/m5-friendly-g3.jsonl` → **`Verified OK`, exit 0** (all 27 traveled turns re-hashed against both revealed audits) |
| Tokens | 0 both sides (their `tokens_total: 0`; our verbal layer is templates) |

## Findings (the point of running before merging)

1. **F10 — terminal-message step convention (g1, session collapse at the moment of
   capture).** The reference seals its mandatory "You got me." final message at its
   **current** step (a caught thief does not move): after our step-13 capture claim its
   final message arrived as step 13 again, our inbound demanded 14 and collapsed the
   session (`ProtocolViolationError`, log `m5-friendly-g1.jsonl`). Fix: tolerate the
   repeat on the terminal caught answer ONLY (`peer/inbound.py`); every other repeat or
   gap still collapses (pinned both ways). Our own outbound convention (increment,
   self-consistent, replay-verified) is unchanged — the audit re-hashes bytes, not grammar.
2. **F10b — the same convention in the revealed audit (g2, `audit_ok: false`).** With
   the inbound fix the game and audits completed, but the reference's revealed records
   run `[1..13, 13]` and our continuity check flagged them. Fix: accept exactly ONE
   trailing repeated final step (`peer/audit_flow.py`); mid-series repeats and gaps
   still fail (pinned). Log `m5-friendly-g2.jsonl`.
3. Both findings are capture-direction-only: every prior live pairing ended in thief
   survival (M2 g1–g4, M3), so this convention was unreachable until a cop strong
   enough to capture the reference thief existed — the M5-4 tuned brain caught it in 13
   steps on the first live attempt.

## Constraint-#13 accounting

No wire-format, canonicalization, or hashing change anywhere in this chain: the kit
CORE vectors run unchanged in CI; the two fixes relax INBOUND validation tolerance
only, each pinned in both directions. The rule-19 mutation matrix is untouched and
still green; our sealed-record shape (incl. barrier turns, sealed move `"BARRIER"`)
is exactly the M5-2 shape the reference just audited 13/13.

## Artifacts

- `docs/evidence/m5-friendly-g1.jsonl` — run 1 (F10 discovery: collapse at capture).
- `docs/evidence/m5-friendly-g2.jsonl` — run 2 (F10b discovery: `audit_ok: false`, continuity).
- `docs/evidence/m5-friendly-g3.jsonl` — run 3, clean end-to-end (quoted above).
- Reference-side artifacts stay in the reference checkout (EULA posture, ADR-0002);
  verdict lines quoted from `logs/thief_match.json` and
  `logs/segal-thief-team/result_imreeyal-vs-segal-thief-team.json`.
