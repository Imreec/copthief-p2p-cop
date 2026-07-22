# Prompt Engineering Log

> Truthful, per-PR entries for **committed** work only (CLAUDE.md §7). Development prompts —
> runtime agent prompts live in source. Format: PR · driver/reviewer · what was asked · outcome.

## PR #65 — m7-1-sparring-guard (the standing-host rules, made mechanical)

- **Driver:** Imree (chose "build it now, TDD + committed" over hand-rolling it at the
  window) · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **Why now, ahead of its milestone:** the Alon/Renat team asked for a peer window within
  hours. Standing a peer up for an opponent to practise against is exactly the hurried
  path where "the sparring host runs the generic brain only" gets broken — so the rule
  stopped being something to remember and became something the CLI refuses to run without.
- **The design point: validate the OUTPUT, not the edits.** The script strips
  `[strategy.<role>]` tables textually, but TOML expresses the same table inline under
  `[strategy]`, which the loader reads identically and no text transform can see. So the
  derivation loads what it just wrote and puts it through the same guard the CLI uses.
  That gap is pinned as a test with the reasoning attached — it is a real hole in the
  transform, not a contrived one.
- **A test premise that was wrong, and what it taught.** My first "hostile source" case
  assumed an inline `recipient = [...] # comment` would slip past `rest_email`. It did
  not — the transform is line-prefix based and caught it. Rather than keep a test that
  passed for the wrong reason, I replaced it with the inline-table case above, which
  actually escapes. A drill that cannot fail proves nothing.
- **Left behind rather than ignored:** `ga_weights.json`, `arena*.json` and friends carry
  the very numbers that may not deploy. The peer never reads them, but a config directory
  holding them is one `--config` away from being played, so the derivation drops them.
- **Refusal shape:** JSON + exit 2, not a traceback. This is an expected answer to a wrong
  config and it has to be readable in an ops window at speed.
- **Honest scope:** this is the safety half of M7-1. No host is deployed, the 24h
  reachability DoD is untouched, and M7-1 stays ◐. What it buys today is that the peer
  window Alon asked for cannot quietly ship our GA weights.

## PR #64 — m7-8-live-duplicate-drill (the them-to-us half, over the real edge)

- **Driver:** Imree ("sure, let's try it") · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What was asked:** try to convert half the M7-8 evidence debt before the warm-ups by
  inducing a live redelivery against the reference implementation, with the caveat
  agreed up front that it is a race and might simply not reproduce.
- **The instrument changed the odds, and that was the whole call.** The M7-7 technique
  (kill `cloudflared` at `turn_received`) front-runs OUR push — it cannot produce an
  inbound duplicate. Making the opponent redeliver needs the failure to land between
  their push being delivered and their ack returning: milliseconds, against a session
  teardown. Instead of coin-flipping it, I put a lossy relay in front of our own peer
  that forwards their push and drops exactly that one response. Deterministic, and the
  tunnel never goes down. **First run, first turn, it fired.**
- **Checked before building the rig, not after:** whether the reference retries at all
  (`infra/mcp_client.py:42-55` — it retries any exception, and its `_call` wraps the tool
  call in `async with Client(...)`, so a teardown failure retries too). If it had not,
  the honest answer would have been "not inducible" and no rig would have been built.
- **What I did NOT claim.** The loss was induced by us, not by a random flap — that
  sentence is in the evidence, unhedged. What is not simulated is the reaction: the retry
  is the reference's own code, the second delivery crossed the public edge, and our dedup
  saw a real duplicate. The us-to-them half is still owed and the TODO still says ◐.
- **The finding I went looking for afterwards, by reading the oracle rather than
  guessing:** the reference has no step-continuity check at all — a duplicate is applied
  TWICE (belief diffuse, smell observe, absorb, decay). It fails silently where we failed
  loudly. That flips into a real interop note: our own retried push can make a
  reference-based opponent decay its scent field twice, so a `scent_physics_mismatch` we
  raise against them may be caused by a duplicate *we* sent. Evidence-grade only (SQ3),
  so it cannot flip a verdict — but it is now a named cause for a dispute write-up.
- **Ops hygiene:** reference configs were already on the tunnel and were left untouched
  (gotcha #11; verified by mtime, both predating the run), `cloudflared` stopped after,
  `git status` clean.

## PR #63 — m7-8-duplicate-reorder-tolerance (at-least-once delivery)

- **Driver:** Imree ("audit our inbound path, then TDD-fix any gap") · **Author:** Claude
  (terminal) · **Reviewer:** pending (AG).
- **What was asked:** audit the inbound path against the round-7 threat the Alon/Renat team
  raised — repeated `(kind, step)` delivery, reordered delivery, junk resetting the turn
  deadline — and fix what the audit found, keeping the strict state machine strict.
- **The audit was the work; the fix followed from it.** Three gaps were real and all on the
  live path (details in `docs/evidence/m6-chaos.md` §M7-8). The one that mattered most was
  not on the asked list: the deadline was only ever evaluated on an EMPTY poll, so a tunnel
  delivering junk continuously meant it was never evaluated at all. **A drill caught it, not
  a review** — drill E hung the test run instead of passing, which is exactly what a drill
  written against the real loop is for.
- **The design decision worth recording: dedup keys on the COMMIT, not on `(kind, step)`.**
  The proposal on the table was `(kind, step)`. A commit is unique per message and is the
  one field a redelivery cannot vary — so keying on it buys a property the step-keyed
  version cannot have: a *second, different* commit for a step already played is
  distinguishable from a retry, and stays a collapse. That is equivocation, which is the
  precise fraud the commit-reveal scheme exists to catch. Tolerance at the transport layer,
  nothing given away at the rules layer.
- **One threshold, not two.** The proposal also had a separate "raise on flooded buffer"
  rule beside the reorder window. Implemented that way, the flood branch is unreachable —
  the window and the capacity are the same number — so it collapsed into one rule whose
  message names the window. Dead code that looks like a defense is worse than no defense.
- **What this changed in the existing battery, deliberately:** the M6-7 drill
  `test_drill_replayed_turn_hits_the_step_continuity_wall` asserted the defect. It is
  amended in place (not deleted) with the reasoning, and paired with the equivocation drill
  that now holds that ground.
- **Honest status:** keyless CI only. The live both-directions duplicate drill is a warm-up
  item with their team and is NOT claimed here; M7-8 is ◐, not ☑.

## PR #62 — M7-7 live mid-push tunnel drills (evidence)

- **Driver:** Imree (authorized the mid-push drill, "run it end-to-end yourself, I'm
  reachable if something wedges") · **Author:** Claude (terminal) · **Reviewer:** pending.
- **What was asked:** two live tunnel games — (a) heal-within-budget, (b) budget-exhausted
  — with an exact list of observables for the classified terminal, gotcha #11 both
  directions, evidence committed before ticking M7-7.
- **The judgment call that made (b) real.** The #60 push-exhaustion path only fires when
  OUR outbound push is the one that exhausts, and every in-game push immediately follows a
  receive — so a mid-game tunnel kill usually leaves us *receiving*, which classifies via
  the #59 inbound path, not #60. The reference thief moves first, so our cop's reply to
  its opening turn is our first outbound push; killing the edge the instant that inbound
  turn arrived (`turn_received`) front-ran our push into a dead edge. It caught the push on
  the first try in both variants — the log proves it (`transport_error` on `receive_turn`,
  then the `outbound turn undeliverable` trigger, distinct from the inbound
  `turn deadline exhausted`).
- **What I verified rather than asserted:** the reference thief's own turn budget (180 s,
  from its config) — (a)'s 90 s outage only "continues the game" if the *opponent* also
  waits it out; a shorter reference budget would have broken it. And "report rail fires per
  posture" was evaluated over the actually-loaded `[email]` settings, not a hand-picked
  posture: `refuse: email disabled`.
- **Disclosed, not hidden:** in (a) the MCP client library's background `post_writer`
  logged the dead-window `502`/`530` and a "Session termination failed" during teardown —
  library-level noise, not our code; the game still finished `cop_capture` and exited 0. It
  is quoted in the evidence rather than filtered out.
- **Outcome:** both observations in the tree; the residual note that said the push path was
  CI-only is now retired — proven over the real edge.

## PR #60 — m7-7-push-exhaustion (M7-7 residual: undeliverable outbound turn)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** close the residual PR #59 raised and I flagged rather than fixed
  unasked — "both approved as scoped above — in-game pushes only, transport-exhaustion
  only, no unilateral outcome claims, audit path verified."
- **Why the scope line did the heavy lifting.** The naive read of "classify a failed
  push" is to reuse whatever ends the game. Two of those would have been wrong, and the
  scope named both: (a) **no unilateral outcome claims** — an undeliverable push must NOT
  become "we captured them" or "they forfeited"; it is symmetric with a silent opponent,
  i.e. *our own* technical loss (the 0/0 row). (b) **transport-exhaustion only** — a
  blanket `except Exception` around the push would have silently turned a genuine bug in
  the seal/serialize path into a technical loss; only `TransportError` is absorbed, every
  other error still propagates. I wrote the test for that propagation first, because it is
  exactly the kind of over-broad catch that looks fine until it hides a real defect.
- **What I checked rather than assumed:**
  1. **Where `TransportError` should live.** The loop must classify a delivery failure
     without knowing which transport it holds (PLAN §12), so catching the infra type in
     the peer loop would have inverted the layering. Moved it to the protocol seam
     (`peer/transport`) and re-exported from infra, verified nothing that already caught
     it breaks (`p2p_transport.TransportError is transport.TransportError`).
  2. **The turn-budget change is a *value* change, and that is only OK because the value
     is unsigned.** `connect_timeout_seconds` is private (App B), unlike the signed
     `watchdog_timeout_sec` I was explicitly forbidden to touch in #59 — so raising the
     in-game push budget to the turn budget is legitimate, not an App F breach. I stated
     that distinction in the evidence so the two "budget" fixes are not conflated.
  3. **"Audit path verified" meant running it, not asserting it.** The test settles a
     push-classified loss and checks it lands on the exact inbound-deadline path — audit
     skipped, zero opponent records, `problems == ("audit skipped: timeout",)`.
- **Outcome:** 663 keyless tests (9 new); the push path proven over the in-process
  transport. Candid limit stated in the evidence: no live mid-push tunnel kill was run
  (the #59 re-drill's kill landed while receiving); offered as a future authorized drill.

## PR #59 — m7-7-live-path-defects (M7-7: four live-path defects from the kill drill)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** fix all four defects the real-tunnel kill drill exposed at
  `a23d7ce`, with (1) — the watchdog outrunning our own turn deadline — named as THE
  pre-series blocker, then re-run the scripted battery and re-drill live.
- **The instruction that shaped the output, and the one I would have got wrong:**
  *"watchdog_timeout_sec is a SIGNED value — the fix is semantics, never a config bump."*
  The obvious repair is to raise the watchdog budget above the turn budget, and it would
  have passed every test I would have thought to write. It is also an App F violation
  dressed as a bugfix. Being told the constraint up front is what forced the actual
  design: the budget stays signed and untouched, and the *derived* I/O budget
  (`turn + watchdog`) carries the ordering instead.
- **The second instruction that did real work:** *"the two budgets must be reconciled
  EXPLICITLY (loader-asserted relationship, documented)."* The heartbeat fix alone would
  have closed the observed failure. But the deeper defect was that two budgets governing
  the same question had never been related to each other *anywhere* — they met for the
  first time at runtime, in a live game, and the wrong one won. `shared/budgets` states
  the ordering once and refuses a config that violates it. That is the part that stops
  the *next* instance, not just this one.
- **What I checked instead of assuming (each changed what shipped):**
  1. **`peer_result` alone was not the whole of defect (4).** Adding it to the read broke
     the M1 replay pin: a local log carries the two-sided `result` *and* both sides'
     `peer_result`, and a per-side payload counts only its own steps — 4 reported where
     the match played 5. The event order is now documented as **precedence**, and the
     regression is pinned. A test I already had caught a bug my fix introduced.
  2. **The manifest was wrong before I noticed the warning.** Two mirrored files rewritten
     by a Python helper came out CRLF (ops gotcha #6), so `--write-manifest` hashed
     CRLF while CI checks out LF. Committed tree `74a5235…` vs the correct `e019a3d…` —
     a red mirror check, caught only by reading the `git commit` warning line rather than
     scrolling past it.
- **Outcome:** all four closed; 654 keyless tests (13 chaos drills, three new); coverage
  96.16%, new modules 100%. Deliberately NOT widened: the flap now surfaces as a
  `TransportError` rather than a self-terminating watchdog, which is a real improvement
  but leaves open whether the outbound retry budget should be the turn budget — raised
  for Imree rather than fixed unasked.

## PR #58 — feat/m3-8-named-scent-models (M3-8 build: named models, locked, sealed)

- **Driver:** Imree (gave the build order explicitly and said "do not reorder") ·
  **Author:** Claude (terminal) · **Reviewer:** pending.
- **What was asked:** build M3-8 in ADR-0004 v2's order, with the kit's PROMOTED fixtures
  as the spec, the default model byte-identical, and the per-model belief-eval rerun
  treated as mandatory rather than optional.
- **The instruction that shaped the output:** "per-model belief-eval rerun — MANDATORY
  before any M3-3 number is quoted for the book model." Left to my own judgement I would
  have wired the second model, watched the existing suite stay green, and reported M3-8
  done — the M3-3 numbers were never *asserted* of the book model, so nothing would have
  looked wrong. Actually running it is what produced the session's biggest finding: under
  `multiplicative_book_v1` the filter's argmax hit-rate collapses from 98% to 17%. The
  gate item existed precisely because a silence is easy to mistake for a pass.
- **Two things I checked rather than assumed, both of which changed what shipped:**
  1. *Why* the book number is bad. A wrong `age_of` would look identical to a genuine
     result, so I probed the field instead of narrating a theory: additive kernel + upper
     clamp pins 12 of 49 cells at 0.9 by turn 4 (inherent to the registration), and our
     voucher heuristic reads a fresh ring-2 cell as 14 turns old (our machinery, not the
     book's). The evidence doc states both, so the number cannot be read as a verdict on
     the book's physics.
  2. The negotiate bytes. Kit SPEC §7 says the doc never crosses the wire — only
     `<family>_sha256` — while our M3-2 code shipped the whole document under
     `scent_model`. That is a wire-visible change on the DEFAULT path, contradicting
     PRD_scent §9.5's literal "byte-identical wire output". I took the ADR decision as
     controlling (it is the specific, later-reasoned instruction, and hash-comparability
     with the partner team is the entire point of M3-8), amended §9.5's wording to say
     "game bytes", and flagged it rather than letting a doc line quietly go stale.
- **A regression the existing pins caught, worth recording:** routing the belief filter's
  observation model through the scent model exposed that the legacy `ScentField`
  constructor never carried `emit_intensity` — harmless while only `deposit` used it,
  fatal once `fresh_center` did, since the anchor became `-decay`. The M3-3 per-seed
  test went red immediately. The pin earned its keep.
- **Scope discipline:** nothing posted, sent, or co-signed. The kit fixture's mojibake'd
  `kernel_source` em dash was left ALONE — it is inside the PROMOTED hash the partner
  team already matched byte-exact, so "fixing" it would break the agreed lock.

## PR #57 — docs/m7-0-verification-green (counterparty verification of the cited game)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending.
- **What was asked:** a small ride-along docs PR recording that the Alon/Renat team's
  independent verification of our full-pairing game came back green.
- **Why it is worth its own entry:** M7-0's argument cites six demo-interop games as
  corroboration, and until now that citation rested on *our* logs verified by *our*
  tooling — exactly the weakness the partner team warned about when they asked us to
  demote demo evidence to corroboration in the first place. Their re-verification of
  game `deee14f6…` with their own from-scratch implementation (35 commit-reveals,
  byte-identical `smell_grid`s, barrier growth 0→7, and our `game_uid` re-derived by
  them from our committed config) upgrades it to corroboration the counterparty
  confirmed. That is a stronger claim in the joint ADR, so the TODO line should say so.
- **Scope discipline:** TODO wording only. The ADR skeleton itself lives in private
  notes and was updated there; nothing was posted, sent, or co-signed.
## PR #56 — docs/m3-8-scent-gate (M3-8 approval gate: PRD_scent §9 + ADR-0004 v2)

- **Driver:** Imree (ordered the gates first, kit before repo, and "settle the
  `min_center_intensity` provenance THERE, inherit neither side's assertion") ·
  **Author:** Claude (terminal) · **Reviewer:** pending.
- **What was asked:** land the kit lock-schema first, then bring the M3-8 gate docs for
  explicit approval before any build code — a hard stop, not a formality.
- **The instruction that changed the output:** "inherit neither side's assertion." I would
  otherwise have taken `min_center_intensity: 0.5` as a book default, because both teams
  and our own PRD had been treating it as one. Reading the primary sources instead: the
  book never mentions it in any spelling — its own App B `game.json` listing and the App F
  table 16 pheromone block each carry exactly **three** keys — while the reference
  introduces it and then seals it into the 14-key signed terms. So App F does not bind it,
  it stays in the terms for signature compatibility, and under the book model it is inert.
  Three consequences that would each have been wrong under the inherited assumption.
- **Verify-before-accept paid twice more.** Re-deriving the partner team's relayed spec
  against the book rather than transcribing it: every number reproduced exactly (the
  `1.43→0.9` clamp, the `0.62→0.758→0.8822/0.8222` chain), which turns the fixture into
  independent confirmation instead of a copy. And the long-open "exact Gaussian" (theirs)
  vs "matches no clean formula" (ours) disagreement resolved in **both** directions: the
  kernel is an exact Gaussian at printed precision, but only inside a σ² window the book
  never prints, and the round-to-2dp window is disjoint from the truncation one — so their
  reading of the shape and our reading of the reproducibility both hold, and both argue
  for pinning the 25 printed values verbatim.
- **A finding nobody had raised:** the book model rounds nothing *and* each side recomputes
  the rival's field rather than receiving it, so evaluation order is interop-load-bearing —
  `(1−ρ)τ+Δτ` and `τ−ρτ+Δτ` differ in the last IEEE-754 bit for 75 of 534 probed inputs.
  A byte-comparison of two recomputed fields false-flags; the M6-7 scent-physics check
  needs a tolerance under this model. Pinned in the kit as `ordering_probe`.
- **Own error caught by the gate ritual:** the first cut of the kit generator built its
  cell set from a Python `set`, so fixture key order varied per interpreter run. Values
  were right and hashes unaffected (canonicalization sorts), but CI's regenerate-and-diff
  would have gone red on a clean checkout. Found by running the full CI sequence locally
  across three fresh interpreters rather than trusting one green run.
- **Deliberately NOT in this PR:** any M3-8 build code. The gate is the point.

## PR #55 — feat/m7-6b-lecturer-guard (the lecturer is addressable only from a counted run)

- **Driver:** Imree (the gap and the mechanism are both his) · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model).
- **What he caught:** asked whether the code now stops mail reaching the lecturer unless
  said explicitly, I had to answer **no** — the M7-6 interlock refused a run with *no*
  recipient but had no idea which address was the lecturer's, so a friendly naming him
  would have mailed him automatically. His standing rule was still policy in a document.
- **What he then fixed in my proposal:** I offered a separate named config key for the
  counted recipient; he pointed out the recipient is *already* stated before the run, so
  that is just a second place to type the same address — the ceremony we deleted with the
  arming flag, wearing a different hat. The real distinction is **whether the run is
  initiated as a real game**. That concept already exists as `counted`, and it already has
  teeth: it arms the App F counted rows, so a counted constitution refuses to load unless
  it is a genuine six-mini-game match. Tying the lecturer to it adds no new switch.
- **This PR:** RED (friendly naming the lecturer refuses · he cannot hide in a list beside
  friendly recipients · counted run sends normally · friendlies untouched · case/whitespace
  variants all caught · refusal names the gate · unconfigured lecturer disables the guard,
  not the rail · end-to-end through the sender, where `counted` defaults to False so a
  caller that forgets cannot reach him) → GREEN: `decide_email_action(..., counted,
  lecturer)` · `EmailSettings.lecturer` · `[email] lecturer` in game.toml (config-owned,
  constraint #5) · `EmailSender(counted=...)` · `series_run` passes `counted=False`
  explicitly. ADR-0008 amendment 9b records the gap, the fix, and the rejected alternative.
- **I also pushed back and was wrong:** I argued the guard should wait for M7-4, since no
  `counted=True` caller exists yet. He said build it now so the first real game inherits
  it. He is right — it is a pure function, fully testable today, and safety built at the
  moment it is first needed is safety built under pressure.

## PR #54 — feat/m7-6-auto-send (M7-6 build: automatic, recipient-authorized reporting)

- **Driver:** Imree (ADR-0008 approved by merging #53) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model).
- **This PR:** RED (interlock truth table re-enumerated over (enabled × mode ×
  **recipients**) with every no-recipient combination refusing · send-only SCOPES pin ·
  multi-recipient `To` · rule-34 attachment round-trip · settings: list, bare string,
  blanks dropped) → GREEN: `report/email_interlock` (arming retype removed; authorization
  is the configured recipient) · `infra/gmail` (`gmail.send` scope; MIMEMultipart body +
  attached JSON artifact) · `infra/email_sender` (no `armed` argument; logs `recipients`;
  passes `attachment_name`) · `shared/config_model` + `private_config._recipients`
  (`recipient: tuple[str, ...]`, list or bare string, blanks dropped) · `config/game.toml`
  resting state `enabled=false` + `recipient=[]` · CLAUDE.md #16 + §4 + §9 + anti-patterns
  · PRD FR-9 · PLAN §2/§4 · `scripts/gmail_auth.py`.
- **Two bugs my own tests caught before CI did:** `_recipients` treated the default `()`
  as a scalar, so the empty tuple became the literal string `"()"` — a recipient that
  looks like authorization (`isinstance(raw, list | tuple)` fixed it); and the split test
  module imported `tests.unit.infra.email_fixtures`, which does not resolve — the repo's
  convention is the bare `from email_fixtures import …` (as `report_fixtures` does).
- **150-line rule:** the sender suite hit 154 lines. Split per constraint #1 rather than
  compressed — fixtures extracted to `email_fixtures.py`, refusal paths to
  `test_email_refusals.py`, so neither file duplicates setup (constraint #11).
- **ADR correction shipped with the build:** ADR-0008 decision 6 claimed the sparring-host
  pin was "asserted at startup". It is not — no sparring runner exists yet, and with draft
  dropped, "pin draft" no longer bites. Corrected in place: the pin becomes
  `enabled = false` and the assertion lands with the host at M7-1. Status moved
  PROPOSED → ACCEPTED.
- **Not done here, and M7-6 stays ◐ for it:** the live token is still the M6-4
  **compose** one, so nothing can actually send until Imree re-runs `gmail_auth.py` for a
  send-only token; the thief sync and the parent-workspace standing rule also remain.

## PR #53 — docs/m7-6-email-posture-gate (M7-6 PRD/ADR gate — approval blocks the code)

- **Driver:** Imree (both design rulings are his) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model). **Gate PR: merge = the approval; no M7-6
  production code until then** (CLAUDE.md §2).
- **This PR:** `docs/adr/0008-email-posture.md` + `docs/PRD_reporting.md` §5a amendment
  + PRD §9 ledger entry + TODO M7-6 rewritten to the decided design. Docs only.
- **Imree's two rulings, both of which simplified my proposal:**
  (1) I offered an `--authorize-send` flag; he pointed out we had already settled that
  we always send and that what varies is **who receives it**. Adopted, and his framing
  is stronger than mine: a boolean says "sending is allowed", a recipient says *who* —
  and nobody types the lecturer's address by accident. No flag.
  (2) I offered "two tokens" vs "argue the compose case"; he asked **"do we even need
  draft?"** — and we don't. Draft's only unique property was reviewing bytes before
  they leave, which sending **to ourselves** does while exercising more of the path.
  Dropping draft removes the need for `gmail.compose`, which resolves App E rule 30
  **literally instead of by argument**. CLAUDE.md §4 reverts to send-only with the
  rule-30 citation it should have carried at PR #43.
- **Two facts verified against Google's API reference before writing them down**, since
  both are load-bearing: `users.drafts.create` is authorized only by `mail.google.com` /
  `gmail.modify` / `gmail.compose` — `gmail.send` genuinely **cannot** create a draft, so
  the book's own App B `mode="draft"` listing is impossible under its own rule 30; and
  `users.messages.send` carries recipients as RFC-822 headers, so **scope does not
  constrain recipient count** and multi-recipient friendly reports work send-only.
- **Numbering catch:** I first wrote this as ADR-0007, but PRD §9 already reserves 0007
  for the (unwritten) zero-token verbal layer — renumbered to **0008** before commit.

## PR #52 — docs/m6-7-tunnel-drill (M6-7 residual closed: real-tunnel kill drill)

- **Driver:** Imree ("continue as you suggested" — the drill authorized in the same
  session as the M6-4 close-out) · **Author:** Claude (terminal, ran the drill
  end-to-end) · **Reviewer:** Antigravity (cross-model).
- **This PR:** closes the M6-7 residual — the tunnel-kill variant against a real
  cloudflared edge — plus the two live logs. No production code changed; the four
  defects it surfaced are logged as TODO M7-7 rather than fixed here, so the
  evidence PR stays an observation record.
- **What actually happened, versus what I predicted:** I expected the loop to keep
  beating and the 180 s turn deadline to fire. Instead the outbound call blocked on
  the dead edge, the heartbeat stopped, and the **watchdog** fired at 60.34 s —
  persisting state and exiting cleanly. FR-8 proven live, but it exposed that the
  signed 60 s watchdog budget outruns our own 180 s turn deadline, so a network flap
  would lose a counted game by self-termination (M7-7 item 1, pre-series blocker).
- **Unplanned bonus:** the first game finished before the kill could land — our tuned
  cop CAPTURED the reference thief in 13 steps over the public edge, mutual audit
  clean, replay Verified OK. First tunnel-borne full pairing since M2, kept as
  evidence. It also produced the **first live firing of the M6-7 scent-physics
  check**: 1 cell at the capture step, consistent with the known F10/F10b terminal-step
  convention — recorded as evidence-grade only (SQ3), explicitly not alleged as
  fabrication.
- **Method discipline:** three claims were checked before being written down rather
  than after. A `steps: 0` replay summary looked like a vacuous "Verified OK" over
  committed M5 evidence — instrumenting the replay showed 26 turns and 29 records
  genuinely re-hashed, so the M5 claim stands and only the display key was wrong. A
  `replay exit=0` on a TAMPERED verdict looked like a broken exit code — it was my
  own shell reading `tail`'s status through a pipe. A repeated `game_uid` across two
  runs looked like a uniqueness bug — it is deterministic by construction (kit §4).

## PR #51 — docs/m6-4-email-evidence (M6-4 live Gmail-draft evidence; OI-5 closed)

- **Driver:** Imree (interactive, at the keyboard: created the team Gmail account,
  the GCP project + Desktop OAuth client, ran the consent, took the screenshot) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model).
- **This PR:** the live evidence closing M6-4 — `docs/evidence/m6-email.md` +
  `assets/m6-email-draft.png`; TODO M6-4 ☑. Asked for click-by-click guidance
  through OI-5 (account → GCP project → consent screen + test user → Desktop
  client → `gmail_auth.py`) and then one live draft run. No production code changed.
- **Method note:** the committed `config/` tree was never edited — the run used a
  scratchpad COPY with only `[email]` flipped, so `enabled = false` could not reach
  a commit (constraint #16 made mechanical rather than remembered). The runner stays
  uncommitted (a committed entry point = a public function without a test,
  constraint #10) and is quoted verbatim in the evidence doc instead.
- **Corrections I made and disclosed:** my console-navigation instructions were
  stale (the OAuth consent screen is now "Google Auth Platform") — Imree pushed back
  and was right; the client secret does still exist, which he confirmed. My first
  runner printed the wrong config section (split on the bare `[email]`, which also
  appears in a comment); fixed and re-run so the recorded transcript matches what
  the doc claims. A `game_uid` I flagged as suspiciously repeatable turned out to be
  deterministic by construction (kit §4) — checked before reporting it as a defect.
- **Finding that outgrew the PR (→ new TODO M7-6, pre-series blocker):** asked to
  verify rather than hedge on whether counted games must auto-send, I read the book:
  App E rules 30/32/34/35 + §9.3 require **automatic** reporting (rule 35 zeroes
  **both** teams if one fails to report), which makes our per-send arming interlock
  wrong as the counted posture — while App B's own listing ships `mode = "draft"`
  and rule 30 mandates a `gmail.send` scope that cannot create drafts. Imree's
  standing intent (auto-send; friendlies to ourselves + the opponent, counted to the
  lecturer) matches the book; the redesign amends CLAUDE.md #16 and is its own gated
  PR. Evidence doc records the draft observation only — it makes no posture claim.

## PR #50 — feat/m6-7-chaos (M6-7 watchdog + chaos battery + scent-physics rider)

- **Driver:** Imree (approved PRD_gatekeeper §4–§5 incl. D2: scent-physics rides
  M6-7 with a TODO amendment) · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity + Eyal (per TODO); stacked on #49.
- **This PR:** RED (watchdog fake-clock core + threaded drill · scent-physics
  unit: honest walk == zero mismatches, fabricated grid flagged per step ·
  10-drill chaos battery, each asserting its NAMED defense) → GREEN:
  `peer/watchdog` (beat/check core, persist-then-shutdown-once, daemon thread) ·
  `peer/scent_check` (revealed-walk re-derivation vs archived grids;
  settlement emits `scent_physics_mismatch`, evidence-grade only — SQ3) ·
  `p2p` heartbeat seam + `peer_run` arms the watchdog live (signed timeout,
  snapshot to logs/, loud exit) · `docs/evidence/m6-chaos.md`. RED-phase finds:
  my fixture walked an illegal state path (machine rejected it — good) and a
  3-step "survival" claim tripped the threshold backstop (also good — both
  defenses caught the test author first). Gotcha #7 struck once (PS round-trip
  mojibake) — repaired by reverse-decode, edits via file tools only since.
  TODO M6-7 amended (D2) + ticked.

## PR #49 — feat/m6-8-cost (M6-8 COST.md + the auditable 0-token pin)

- **Driver:** Imree (approved PRD_reporting §7: "0-token claims doubly backed") ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model); stacked
  on #48.
- **This PR:** `COST.md` (honest-disclosure triad member: the double proof — JSONL
  evidence logs AND the sealed per-step counts; match-time posture table; infra
  costs incl. credits earmarked for the Stage-B VPS; dev-time AI tooling disclosed;
  keep-honest rules) + permanent CI pin `test_zero_tokens.py` (real audited game:
  every sealed game record charges 0/0 and the log replays Verified OK — forging a
  count flips TAMPERED via the rule-19 matrix, so the claim is tamper-evident).
  Evidence pin over existing M6-3 behavior — no new logic, doc + test only.
  TODO M6-8 ticked.

## PR #48 — feat/m6-6-series (M6-6 series runner)

- **Driver:** Imree ("#47 approved, merge and continue") · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** RED (summary shape/vocabulary/audit-block pins · injectable-runner
  driver pins: F2 alternation, M5-5 trust carry, numbering · integration DoD over
  a num_games=2 tmp config) → GREEN: `peer/summary_build` · `peer/series` (one
  transport, signed num_games, profile-event carry) · `sdk/series_run` (honest
  "-mirror" self-play identity; emits everything; email rail attempted, resting
  state observed refusing) · `sdk/identity` split · PeerGameResult.opponent_records.
  Two RED-phase finds: test module name collision (integration file renamed
  test_local_series) and a protocol-order bug in my own fixture (a fresh thief
  must move first — F2 enforced by the state machine, good). TODO M6-6 ticked.

## PR #47 — feat/m6-4-gmail (M6-4 compose-scope sender + arming interlock)

- **Driver:** Imree (D1=A ruling + dedicated team account; "#46 approved, merge and
  continue; tell me when I need to create the gmail account") · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** RED (whole-space interlock truth table — exactly one combination
  sends · compose-scope + MIME UTF-8 round-trip · sender-through-gatekeeper: draft
  provably never sends, body bytes == artifact file bytes, refusals touch no
  transport, daily-cap quota · [email] safe defaults on omission) → GREEN:
  `report/email_interlock` (pure, total) · `infra/gmail` (HW6 salvage, lazy SDK,
  live paths operator-only) · `infra/email_sender` (byte-faithful, gatekept) ·
  `[email]` toml (kept LAST for the settings tests) · `email-live` dep group +
  scoped mypy override · `scripts/gmail_auth.py` · `.env-example` (constraint-#6
  debt: it was never actually committed) · CLAUDE.md §4 send-only→compose-only
  (D1=A record). Deferred by design: CLI verb → M6-6; live Gmail-draft evidence →
  OI-5 account + consent. TODO M6-4 set ◐ (code done, live evidence pending).

## PR #46 — feat/m6-5-gatekeeper (M6-5 quota → token bucket → DoS lock)

- **Driver:** Imree (approved PRD_gatekeeper §2-§3/§6; build order = gatekeeper
  BEFORE email so M6-4 is born gated) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** RED (window/semaphore/FIFO on a fake clock + the synthetic-load
  DoD · quota-before-queue · 429 schedule pins · breaker trip/cooldown/reset ·
  v1.01 parsing + tighten-only band) → GREEN: `shared/rate_limiter` (enforces the
  signed `concurrent_requests` the reference never does; queue-never-crash) ·
  `shared/gatekeeper` (three stages, loud JSONL events, auto-reset breaker) ·
  `shared/gatekeeper_build` (M6-4's seam; per-service overrides) ·
  `shared/limits_loader` split + `rate_limits.json` **v1.01** (queue/breaker/
  email blocks; FR-9 band [signed_min, global] asserted). Sync note recorded on
  the PR: thief needs a rate_limits.json v1.01 parity commit. TODO M6-5 ticked.

## PR #45 — feat/m6-3-step0-tokens (M6-3 step-0 declaration + sealed tokens)

- **Driver:** Imree (PRD_reporting §4 as the build spec; D3 sealed-key ruling) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model); stacked
  on #44.
- **This PR:** RED (sysinfo degrade-to-unknown + REAL-HEAD pin · step-0 key set w/
  `github_commit`+`num_games_declared` · seal_turn token defaults · identity.spec
  fill · settlement prepend w/ step math untouched · matrix extension incl. the
  unpaired-record gap) → GREEN: `shared/sysinfo` (stdlib probes, process-cached) ·
  `seal_spec_record`/`live_spec_record` · seal_turn +model/tokens_step/tokens_total/
  response_seconds · spec_record BESIDE game records, audit prepends · F8b spec
  closed · replay re-hashes EVERY revealed record (a tampered step-0 previously
  slipped past the pairing walk — real rule-19 gap) · overlay/moves game-records
  only. Two mirrored tests updated from index- to step-selection (they predated
  step-0). Reference gap noted: its log `_schema` promises step-0 github_commit,
  its code omits it — closed on our side. TODO M6-3 ticked.

## PR #44 — feat/m6-2-artifacts (M6-2 report writers + consensus signature)

- **Driver:** Imree (approved PRD_reporting as the build spec: "byte-level vs the
  reference docs/sample-run; spaced sign-then-insert consensus signature, credit
  Alon"; merge of #43 = the go) · **Author:** Claude (terminal) · **Reviewer:**
  Antigravity (cross-model, on the PR).
- **This PR:** RED (49 tests: consensus spaced-form + cross-guard vs compact ·
  builder shapes · sign-then-insert for group blocks AND the Hebrew report ·
  per-group scores + F7 series tie · emit byte discipline · sample-run conformance
  battery) → GREEN `report/` (consensus, schema_text EXTRACTED from fixtures never
  typed, schemas/naming/validation, blocks+builders, hebrew, scores, emit).
  Conformance find while pinning: the reference's config lock covers
  `schema_version`+`_note` (its shared game.json carries both; the artifact writer
  overwrites the displayed schema_version) — brute-forced against the fixture,
  documented in the test. Fixtures attributed (ADR-0002 log + SOURCE.md; PRD D4).
  No wire change (constraint #13; kit vectors green). TODO M6-2 ticked.

## PR #43 — docs/m6-1-mechanism-prds (M6-1 gate)

- **Driver:** Imree (M6 session brief: PRDs before any M6 code — hard gate; TODO-routed facts
  honored: spaced-separator sign-then-insert consensus signature credited to Alon, sealed
  per-step tokens, draft default + arming interlock, doubly-proven 0-token COST claims) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **Context:** memory recall + TODO M6 + PLAN §4/§9/§10 + M2 spike notes re-read; M6-2 primary
  sources read in full — reference `report/` package (`report_writer`/`artifacts`/`emit`/
  `artifact_helpers`) + all four `docs/sample-run/` artifacts @960499fd (oracle, ADR-0002);
  HW6 `email/gmail.py` + `gmail_auth.py` mined; current seams surveyed (sealing, settlement,
  config loaders, no watchdog yet).
- **This PR:** `docs/PRD_reporting.md` (M6-2/3/4/6/8 — four artifacts byte-pinned vs
  sample-run, third canonical variant mapped to its four usage sites, step-0 commit hash +
  sealed tokens, Gmail interlock truth-table, series runner, COST.md) and
  `docs/PRD_gatekeeper.md` (M6-5/7 — quota→bucket→DoS doorway, watchdog+persistence, chaos
  battery, FR-11 scent-physics rider + TODO amendment proposal). Five decision points routed
  to Imree on the PR (Gmail scope conflict PLAN-vs-CLAUDE.md chief among them). TODO M6-1
  ticked in the same change.

## PR #41 — feat/wire-shape-balance (wire-shape balance instrument + evidence)

- **Driver:** Imree (league-coordination brief: "referee-mode full-info balance sim
  using the existing rules module + arena machinery — decides whether adapting to
  bookletter-v3 is a concession or a trap, BEFORE the reply to Alon is drafted") ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** RED (TruthFeed certainty-delta pins · ScentFeed == legacy seam ·
  mirror-feed plumb-through proof — an early draft asserted hidden ≠ full-info
  outcomes and FAILED because they coincide for scent-honest core brains; replaced
  with an adversarial mirror-feed probe) → GREEN: `strategy/info_feed.py` (BeliefFeed
  protocol; ScentFeed = reference-v3 hidden positions, TruthFeed = bookletter-v3
  common knowledge) threaded referee → scenarios → sdk → arena as an optional
  default-None seam; `scripts/balance_run.py` + `config/balance.json` (32 seeds) →
  `docs/evidence/wire-shape-balance.md`. Finding: common knowledge favors the
  EVADER on the shipped config (cop 45.8% → 26.6%; police-brain vs evading thieves
  31/30 → 0 of 32) — perfect rival tracking erases the belief error pursuit exploits.

## PR #40 — feat/m5-7-notebook (M5-7 results notebook, executed + pinned)

- **Driver:** Imree (session brief: "M5-7 notebooks/results_analysis.ipynb — arena + GA
  curves + sensitivity; LaTeX + citations; renders clean, committed with outputs") ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity + Eyal (per TODO); stacked
  on #39.
- **This PR:** RED renders-clean pin (exists · every code cell executed · zero error
  outputs · figures present — caught a real miss: the first build forced the Agg
  backend and committed ZERO rendered PNGs; the figure assertion now guards it) →
  GREEN: executed `notebooks/results_analysis.ipynb` — intro with the $e_t = 1-P_t(c^*)$
  metric identity + GA fitness definition + citations (book ch.6/§6.3.1, ADR-0002/0005,
  PRD §§) · arena standings + champion gate GREEN · DoD 30/32 = 93.8% PASS (live-
  computed from committed config, matching the CI gate) · GA curve 0.688→1.000 with
  default baseline · w_distance/p_commit sensitivity sweeps across the gene boxes.
  `notebook` dep group (nbformat/nbclient/ipykernel). TODO M5-7 ticked; M5-6 ticked
  with the thief-led pointer (its table + winner live in the sibling). ⚑ thief
  notebook rides the thief chain.

## PR #39 — feat/m5-6-verbal-ab (M5-6 core: banks + referee verbal seam + A/B instrument)

- **Driver:** Imree (session brief: "M5-6 template-bank A/B — deception efficacy metric
  in referee mode; winning bank shipped; LLM never decides moves") · **Author:** Claude
  (terminal) · **Reviewer:** Antigravity (cross-model); stacked on #38; the thief-led
  A/B run rides the thief chain.
- **This PR:** RED (bank round-trips · verbal-seam trace direction pins · role-blind
  series determinism) → GREEN: named `BANKS` (bank-less callers keep today's wording
  byte-for-byte; unknown names never fabricate) · referee verbal seam (gazetteer in,
  hints feed the police belief in the peer's predict→scent→hint order; truth-anchored
  efficacy trace, error = 1−P(true cell) — measurable ONLY in referee mode) ·
  `deception_eval` (per-verdict induced-error summary + config-driven bank series) ·
  `[strategy] hint_bank` ships the A/B winner to the live verbal layer ·
  `scripts/deception_ab.py` (per-repo `config/deception_ab.json`; absent = repo opts
  out). Candid: wording is neutral to OUR closed-vocabulary parser by construction —
  measured differences come from word-cap parse survival + decoy policy (disclosed in
  the instrument's own evidence header). Defaults keep every referee pin byte-identical.

## PR #38 — feat/m5-5-profiling (M5-5 post-audit opponent profiling)

- **Driver:** Imree (session brief: "M5-5 opponent profiling — post-audit lie-rate +
  motion priors → next mini-game's belief trust weights; PLAN §13 prior-shift test") ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model); stacked on #37.
- **This PR:** RED (pure pins + the prior-shift series test) → GREEN
  `strategy/profiling.py`: `OpponentProfile` (lie-rate from sealed intent labels,
  motion prior from revealed moves; step-0 spec records excluded; merge across
  mini-games) + `shifted_hint_trust` floored by the new `[belief] profile_hint_floor`
  (distrust-but-never-eliminate — SQ3; scent honesty deliberately NOT profiled: grids
  are never sealed, no audit ground truth). Seams: `PeerSession(hint_trust=…)` override
  (the series runner's mini-game-2 injection point) + a `profile` JSONL event on every
  VERIFIED opponent audit (settlement). peer/p2p split → peer/settlement (150-line
  rule). Belief math untouched (M3-8 boundary). TODO M5-5 ticked.

## PR #37 — feat/m5-inbound-final-step (M5-2 friendly + F10/F10b capture-direction fixes)

- **Driver:** Imree (delegated decision: post-M5-2 friendly YES, localhost sufficient;
  session directive: build, merge nothing) · **Author:** Claude (terminal) ·
  **Reviewer:** Antigravity (cross-model); stacked on #36.
- **This PR:** the PRD_police_brain §7 operator follow-up run for real — our tuned cop
  vs the reference thief on localhost, our FIRST live outbound barriers (steps 7+11).
  **The tuned cop captured the reference thief in 13 steps**, and the capture direction
  (never reachable before — every prior live game ended in survival) exposed the
  reference's terminal-message step convention twice: F10 (final caught message repeats
  its CURRENT step → our inbound collapsed at the moment of capture, g1) and F10b (the
  same repeat in its revealed audit records `[1..13, 13]` → continuity flagged, g2).
  Both fixed TDD-first as inbound-tolerance-only (terminal caught answer / one trailing
  repeat; strictness pinned in the other direction); our outbound convention unchanged;
  kit vectors + rule-19 matrix untouched. g3 clean end-to-end: mutual audit OK both
  sides (theirs: passed 13/13 incl. barrier turns), shared game_uid, replay Verified OK
  exit 0, 0 tokens. Evidence: `docs/evidence/m5-friendly.md` + three JSONL logs.

## PR #36 — feat/m5-observation-signed-clock (core Observation signed clock)

- **Driver:** Imree (decision delegated 2026-07-19: "survival_threshold DOES go into
  Observation (+ max_moves)"; session directive: build the chain, merge nothing) ·
  **Author:** Claude (terminal) · **Reviewer:** Antigravity (cross-model, on the PR).
- **This PR:** RED (three pins: field contract, referee wiring, peer wiring) → GREEN:
  `Observation` gains `survival_threshold` + `max_moves` (defaults 0 — legacy callers
  and the M1-walk equivalence pins untouched); `play_referee_game` and `peer/turns`
  populate them from the constitution. Closes the deviation documented in the thief
  repo's `features.py` since M5-3: time-shaped brain knobs (survival ramp, trap sizing)
  can now anchor to SIGNED values instead of carrying private copies — the thief-side
  anchor change rides the post-#35 sync ritual. No wire change; mirrored tests read
  shared `game.json` keys only (gotcha-#9 clean).

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
