# M6-4 — the report lands as a Gmail draft (live; PLAN §13 M6 exit)

> Observed 2026-07-20 at cop `d819802`, on the dedicated team account created the same
> session (OI-5). This file records **what was observed**, not a posture: see
> [Disclosures](#disclosures) — the draft-first *operating* default is under revision
> after book findings made during this run.

## What was observed

One local series (`sdk/series_run.run_local_series`, the M6-6 DoD flow) played to
settlement and its result artifact was created **as a draft in a real Gmail mailbox**
through the full live rail: OAuth token → `infra/gmail.GmailTransport` →
`shared/gatekeeper` (service `email`, `daily_cap` 10) → `infra/email_sender`.

| | |
|---|---|
| Sender / mailbox | `imreeyal.copthief@gmail.com` (dedicated team account, OI-5) |
| OAuth scope | `gmail.compose` only (D1=A, PR #43) — no mailbox read |
| Consent | `scripts/gmail_auth.py`, Desktop client, GCP project `copthief-league`, Testing mode |
| `game_uid` | `2ff4b20b-3a12-b7ad-f18c-de5245e8c813` |
| Series | 1 sub-game (`counted=False` dev run; a counted match is fixed at 6 — PRD_engine §6) |
| Mutual audits | OK both sides |
| Email outcome | `action: draft` (exit 0) |
| Body | 2814 bytes, **byte-identical to `result_imreeyal-vs-imreeyal-mirror.json`** |

Screenshot: [`assets/m6-email-draft.png`](../../assets/m6-email-draft.png) — the Gmail
**Drafts** folder with the message open, showing the subject, the team sender identity,
and the artifact JSON in the body. The visible `"game_uid"` in the screenshot matches the
runner output below; that correspondence is the point of the evidence.

### Authorization chain, verified rather than assumed

- `token.json` scopes: `["https://www.googleapis.com/auth/gmail.compose"]`, refresh token present.
- Authorized mailbox confirmed by a live `users.getProfile` probe → `imreeyal.copthief@gmail.com`
  (the token's own `account` field is empty, so consent identity was checked against the API,
  not inferred from the browser session).
- `client_secret.json` and `token.json` both confirmed git-ignored by `git check-ignore -v`
  **before** the credential files existed on disk in usable form (constraint #6).

## Runner output (verbatim)

```
=== [email] block actually in force ===
    enabled = true
    mode = "draft"
    recipient = "imreeyal.copthief@gmail.com"
    sender = "imreeyal.copthief@gmail.com"
    token_path = "token.json"

=== series ===
    game_id      : imreeyal-vs-imreeyal-mirror
    game_uid     : 2ff4b20b-3a12-b7ad-f18c-de5245e8c813
    sub_games    : 1
    audits ok    : True
    result artifact validates: yes

=== email rail ===
    action      : draft
    reason      :
    game_uid    : 2ff4b20b-3a12-b7ad-f18c-de5245e8c813
    body bytes   : 2814 (== result artifact file bytes)
```

## How it was run (reproducible)

The committed `config/` tree was **not modified**. A throwaway copy was made in a scratchpad
directory and only its `[email]` block changed — so the shipped resting state
(`enabled = false`) could not reach a commit by accident (constraint #16). The complete
difference between the committed config and the config in force was:

```diff
 [email]
-enabled = false
+enabled = true
 mode = "draft"
-recipient = ""
-sender = ""
+recipient = "imreeyal.copthief@gmail.com"
+sender = "imreeyal.copthief@gmail.com"
 token_path = "token.json"
```

The runner is **not committed** — a committed entry point would be a public function without
a test (constraint #10); the CLI `report` verb remains the deferred M6-4 item. It is quoted
here in full so the run reproduces:

```python
"""M6-4 live evidence: one local series whose report lands as a Gmail DRAFT (OI-5)."""
from pathlib import Path
from copthief_core.report.schemas import validate_artifact
from copthief_core.sdk.series_run import run_local_series

SCRATCH = Path(__file__).parent
CONFIG_DIR = SCRATCH / "evidence_config"   # a copy of config/ with [email] enabled

outcome = run_local_series(
    CONFIG_DIR,
    base_police_seed=11,
    base_thief_seed=22,
    out_root=SCRATCH / "out",
    log_dir=SCRATCH / "logs",
)
# no transport injected -> EmailSender builds the real GmailTransport
print(outcome["email"])       # -> {"action": "draft", ...}
```

Invoked as `uv run --group email-live python <file>` from the repo root.

## What this does and does not prove

**Proves:** the live Gmail chain works end-to-end on the team identity — consent, token,
transport, gatekeeper, and byte-exact artifact delivery into a real mailbox.

**Does not prove:** the *send* path. By construction it could not: `mode = "draft"` makes
`email_sender` bind `create_draft`, and the `send` call is never constructed
(`report/email_interlock`; the truth-table test in CI proves exactly one combination sends).
Draft and send differ by that single bound method on an already-built message, so this run
de-risks — but does not exercise — transmission.

## Disclosures

1. **Operating posture is under revision (M7).** Sources found *during* this session
   establish that counted games must report **automatically**: App E rule 32 (sanction —
   absence of reporting voids that game's points), rule 35 (one team's non-report
   disqualifies the game for **both** teams, score 0), and §9.3 (*"אין עוד מקום להתערבות
   אנושית"* — no room for human intervention at game end). Our per-send arming interlock is
   therefore correct for dev/friendly runs and **wrong as the counted-series posture**. The
   book contradicts itself here — its own App B `game.toml` listing ships `mode = "draft"`,
   and p.139 describes the reference report as *"נשלח כטיוטת Gmail"* — which is why the
   draft rail exists at all. Resolution, the CLAUDE.md §16 amendment, and the ADR are M7
   work, tracked separately. **This document records the draft observation only; it does not
   claim draft-first is the shipping posture.**
2. **Scope vs App E rule 30.** Rule 30 requires send-permission only (sanction: security
   deviation → code disqualification), and App A §1.3/§3 specify `gmail.send`. We hold
   `gmail.compose` (D1=A), because `gmail.send` cannot create the draft the book's own
   config and reference description require. The security intent — no mailbox read — is
   satisfied; the literal scope string is not. Carried into the same M7 ADR.
3. **Token lifetime.** The OAuth app is in **Testing** publishing status, so refresh tokens
   expire after **7 days**. Re-run `scripts/gmail_auth.py` (~30s) before any counted series.
   Publishing to Production is deliberately not done: a restricted scope would trigger
   Google verification review.
4. **Two identical drafts.** The run was executed twice — the first had a cosmetic bug in
   the scratchpad runner's config *printout* (it split on the literal `[email]`, which also
   appears in an earlier comment, so it echoed the wrong section). Product behaviour was
   identical in both runs; the second is quoted above. Both drafts carry the same
   `game_uid` because `domain/crypto.game_uid` is deterministic by design
   (`SHA256(canonical(terms) | sorted group ids)`, kit §4 — both peers derive it without a
   round-trip).
5. **Self-addressed.** Recipient was the team account itself. No third party received
   anything, and nothing was sent.
