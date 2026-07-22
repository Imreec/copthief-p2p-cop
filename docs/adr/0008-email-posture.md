# ADR-0008 — Email posture: automatic send, recipient-authorized, send-only scope

> Numbered 0008, not 0007: the PRD §9 ledger reserves **ADR-0007 for the zero-token verbal
> layer** (planned, not yet written).

## Status

**ACCEPTED** (2026-07-20, PR #53 merged = Imree's approval; built in the M7-6 PR, which also
carries the decision-6 correction below) — supersedes the D1=A ruling recorded on PR #43 and the
CLAUDE.md §4 "compose-only" amendment that rode M6-4. Approval by Imree is the gate for
M7-6 code; **no production code until this ADR and the PRD_reporting §5 amendment are
approved** (CLAUDE.md §2).

## Context

M6-4 shipped the report email as a **draft-first rail with per-send arming**: the send path
required `enabled ∧ mode="send" ∧ an arming retype of the exact `game_uid``, and the shipped
resting state was `enabled=false, mode="draft"`. That design implemented CLAUDE.md
constraint #16 ("no email is ever sent without Imree's explicit **per-send** word") and the
parent-workspace standing rule.

While closing the M6-4 live evidence (2026-07-20, `docs/evidence/m6-email.md`) the book was
read directly on the question of whether counted games must send automatically. It must:

- **App E rule 32** — report results automatically via the Gmail interface.
  *Sanction: "היעדר דיווח פוסל את הנקודות ממשחק זה"* (absence of reporting voids that game's points).
- **App E rule 35** — both teams agree the result and each sends its own final report;
  **one team's non-report, or contradictory reports, disqualifies the game for BOTH teams,
  score 0.**
- **§9.3** — *"בתום כל משחק חוקי… אין עוד מקום להתערבות אנושית"* (at the end of every legal
  game there is no longer room for human intervention); the lecturer address
  `rmisegal+uoh26finalgame@gmail.com` is *"הכתובת היחידה והמחייבת"* (the sole binding address).
- **App E rule 34** — the final report is sent **as an attached JSON file**, not free text.
  *Sanction: refused processing → score zero.*
- **App E rule 28** — a token-bucket rate limiter guards report sending.

A post-game human gate therefore does not merely risk our own points: under rule 35 it
**zeroes the opponent's game as well**. Caution aimed at protecting us would damage a team
that played cleanly.

**The book's own answer to the runaway-email fear is not human approval.** §9.3 raises it
explicitly — *"מה קורה כאשר לולאה אינסופית מתחילה לירות אלפי הודעות לדקה?"* — and answers
with the **Gatekeeper** (rule 28), which we already built at M6-5 (quota → token bucket →
breaker, `email.daily_cap`). That was always the real protection; the draft gate was a
second, weaker belt that happens to carry a sanction.

### The book contradicts itself on scope

- **App E rule 30** + **App A §1.3/§3** mandate `gmail.send` **only**
  (*sanction: security deviation → code disqualification*), on an explicit least-privilege
  rationale: *"סוכן הדיווח צריך רק לשלוח… אין כל סיבה שיוכל לקרוא או למחוק דואר"*.
- **App B's own `game.toml` listing** ships `[email] mode = "draft"`, and **p.139** describes
  the reference report as *"דוח JSON הנשלח כטיוטת Gmail"*.

Verified against Google's API reference (2026-07-20): `users.drafts.create` is authorized
only by `mail.google.com`, `gmail.modify`, `gmail.compose` — **`gmail.send` cannot create a
draft**. The book thus mandates a scope that makes its own shipped configuration impossible.
D1=A resolved this by taking `gmail.compose` and amending CLAUDE.md §4 — a defensible reading
of the *intent* (compose grants no mailbox read), but it was recorded as a conflict between
two of our own documents, and rule 30 and its sanction were never cited.

Also verified: `users.messages.send` is authorized by `gmail.send`, and recipients live in
the raw RFC-822 message (To/Cc headers) — **the scope does not constrain recipient count**,
so multi-recipient friendly reports work on a send-only token.

## Decision

1. **Automatic send is the operating posture for every real run.** No post-game human step
   exists on any path that plays a counted game (rule 32, rule 35, §9.3).
2. **Authorization is the configuration, and the recipient is the switch.** No separate
   arming flag or per-run `--authorize-send` argument. Rationale (Imree's, adopted): a
   boolean says only "sending is allowed", whereas the recipient says *who* — and nobody
   types the lecturer's address by accident. The specific act is the stronger signal.
3. **Draft is dropped as an operating mode, and the live token becomes `gmail.send` only.**
   Draft's sole unique property was "review before anything leaves the account"; sending to
   **ourselves** achieves the same review and exercises more of the path. Removing the need
   for drafts removes the need for `gmail.compose`, which resolves the rule-30 exposure
   **literally** rather than by argument. `CLAUDE.md` §4 reverts to send-only, this time
   citing rule 30 and App A. The draft code path is retained (written, tested, harmless) but
   is no longer the shipping posture and is unreachable on a send-only token.
4. **`recipient` becomes a list.** Friendly report exchange = ourselves + the opponent team.
   Counted series = the lecturer **only**, per the "sole and binding address" language — a
   friendly cross-check with a peer team is its own run, never a CC on a counted report.
5. **The result artifact is attached as a JSON file** (rule 34) **in addition to** the body,
   whose bytes remain byte-identical to the artifact on disk (the reference-mirrored
   behaviour proven at M6-4 and pinned by test).
6. **The sparring host stays hard-pinned to non-sending.** PLAN §2 pins `email.mode = "draft"`
   there; with draft dropped as a posture that wording no longer bites, so the pin becomes
   **`enabled = false` with no recipient**, which under decision 2 makes sending impossible.
   **Correction to the first draft of this ADR:** it said "asserted at startup" as though the
   assertion existed — it does not. No sparring runner exists yet (M7-1), so the assertion has
   no home; it is recorded here and in TODO M7-1 as work that lands *with* the sparring host,
   not as a guarantee already held. Until then the host does not exist and cannot email.
   **DISCHARGED 2026-07-22 (M7-1, ahead of the host itself):** the assertion now exists as
   `shared/sparring.assert_sparring_safe` and is enforced at the moment of use by
   `copthief run peer --sparring`, which refuses a config whose `[email]` is enabled or
   carries any recipient — and, per CLAUDE.md §9, one carrying tuned strategy weights.
   `scripts/make_sparring_config.py` derives a config that passes it and validates its own
   output, so the posture is mechanical rather than remembered. The host deployment (OI-4)
   is still open; the guarantee no longer waits on it.
7. **Runaway protection remains the gatekeeper** (rule 28 / M6-5), not human review.
8. **CLAUDE.md constraint #16 is amended in both repos, and the parent-workspace standing
   rule with it:** "no email is ever sent without Imree's explicit **per-send** word"
   becomes "**no email is ever sent to an address Imree has not configured for that run**".
   Imree still authorizes every send — by setting the recipient and launching the run — but
   authorization happens **before** the match, never inside it.
9b. **AMENDMENT (2026-07-20, same day): the lecturer guard — policy became mechanism.**
   As first written, decisions 2 and 9 left Imree's standing rule ("no email to the lecturer
   without my explicit word") as *documentation*: the interlock refused a run with **no**
   recipient, but had no idea which address was the lecturer's, so a friendly that named him
   would have mailed him automatically. Imree caught this and pointed out that the real
   distinction is not the address but **whether the run is initiated as a real game** — a
   concept the codebase already has. `counted` arms the App F counted-series rows, so a
   counted constitution **refuses to load** unless it is a genuine six-mini-game match
   (PRD_engine §6.1); it cannot be set by accident. **Decision:** the lecturer's address is
   config-owned (`[email] lecturer`, constraint #5) and the interlock **refuses it whenever
   `counted` is false**, matching case- and whitespace-insensitively, including when it hides
   in a list beside friendly recipients. Friendlies pay no ceremony. A rejected alternative
   (mine) was a separate named config key for the counted recipient — Imree correctly called
   it a second place to type the same address, i.e. the ceremony we removed with the arming
   flag, wearing a different hat.

9. **Sequencing is the risk control** (Imree's standing intent, adopted as policy): the
   lecturer is addressed only after friendlies to ourselves and to a peer team have shown
   the format is correct on both sides. Rule 35 penalises *contradictory* reports as harshly
   as missing ones, so proving agreement with Alon's team beforehand protects both teams.

## Consequences

**Positive**

- Rules 30, 32, 34 and 35 are satisfied by construction rather than by argument; no grader
  needs to accept a reasoning chain for the scope string to match the rule.
- The opponent's score is no longer hostage to our operator being at the keyboard.
- One token, one scope, one posture — less machinery than the dual-token alternative.
- Least privilege is genuinely stronger: `gmail.send` cannot create, read, modify or delete
  anything in the mailbox.

**Negative / accepted**

- We lose the "inspect the exact bytes before they leave" step. Mitigated by §9 sequencing
  (self-addressed and peer friendlies first) and by the M6-4 evidence, which already proved
  the emitted bytes equal the artifact file bytes.
- A fresh OAuth consent is required (send-only), and the **7-day Testing-mode refresh-token
  expiry** applies to it too — `scripts/gmail_auth.py` must be re-run before a counted series.
- The draft code path becomes unexercised in live use. Its unit tests stay (they cost
  nothing and document the interlock's whole-space behaviour), but it must not be presented
  as the shipping rail in the README.
- `docs/evidence/m6-email.md` records a draft observation. It remains **true as history** and
  is deliberately written to make no posture claim; this ADR is its forward-looking successor.

## Alternatives considered

- **Keep `gmail.compose` + draft-first, argue the contradiction in an ADR.** Rejected: it
  requires the reader to accept an argument before judging, and rule 30's sanction is code
  disqualification. The argument is sound; relying on it being read is the risk.
- **Two tokens — `compose` for dev/friendly drafts, `send` for counted runs.** Rejected as
  over-engineering once draft stopped being needed: it doubles the consent and expiry
  surface to preserve a mode with no remaining unique value.
- **An explicit per-run `--authorize-send` flag.** Rejected on Imree's reasoning (decision 2):
  the recipient is a more specific and more meaningful authorization than a boolean, and a
  generic flag adds ceremony without adding information. Note the sparring-host pin
  (decision 6) covers the accident the flag was meant to prevent.
- **Keep per-send arming for counted play.** Rejected: it is exactly what rule 32 sanctions
  and rule 35 punishes both teams for.
