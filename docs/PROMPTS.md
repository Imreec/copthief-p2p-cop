# Prompt Engineering Log

> Truthful, per-PR entries for **committed** work only (CLAUDE.md §7). Development prompts —
> runtime agent prompts live in source. Format: PR · driver/reviewer · what was asked · outcome.

## PR #133 — feat/nis-yar1-counted (4th counted series banked; thief mirror #90)

- **Driver:** Imree (T set for the same evening; merge word "approved, you can merge") ·
  **Author:** Claude (terminal, league session) · **Reviewer:** AG review waived by Imree
  (evidence/config-only precedent).
- **What was asked:** run the counted vs nis-yar1 on the frozen commits, settle, report to the
  lecturer alone, bank the artifacts + ledger truthfully.
- **Outcome:** 90–30, 6–0 sweep (2026-08-11 T=22:37) — M11's first live outing, offline
  predictions validated exactly (cage-escape evader survived their cage cop 35×3; the M11 cop
  converted all three incl. the g01-class camper at 27/12/19). All audits Verified OK, zero
  problems, report SENT (exit 0), cross-diff vs their copy byte-clean (mutual sha 1bf79e75
  four-way equal). 20 evidence files + ledger 4 landed (`ab40f4f`); thief ledger mirror
  #90 (`95e53f3`). Counters truthful (ours 4/1 first-meeting true, +10 diversity ours).

## PR #132 — test/arena-determinism-cost (CI 25-min cap breach; thief sync #89)

- **Driver:** Imree (merge word) · **Author:** Claude (terminal) · **Reviewer:** cross-model
  posture per process; cost fix reviewed on the thread.
- **What was asked:** the M11 merge made the quality lane time out at the 25-min cap — the armed
  champion arena was effectively playing a SECOND full robin under coverage. Fix the cost
  without weakening what the test proves.
- **Outcome:** the arena reproducibility test now proves determinism on 2 reduced seeds instead
  of re-running the full robin (`aef719c`); quality lanes green both repos (cop 19m45s). Thief
  sync #89 (`d78badb`). The lesson is standing policy: heavy measurement lives in scripts +
  evidence docs, never in CI tests ([[ops-gotcha-ruff-format-ci]] carries the cadence rule).

## PR — m11-robust-brains (from patching to hardening; the 08-11 counted-eve build)

- **Driver:** Imree (session prompt `SESSION-PROMPT-M11-ROBUST-BRAINS.md` — red-team mandate
  outranking the work-item list — plus two mid-session live inputs: the nis-yar1 60–80 friendly
  logs and the directive to be ready for the same-evening counted; merge word is his) ·
  **Author:** Claude (terminal, isolated worktree `m11-robust-brains`) · **Reviewer:** pending.
- **What was asked:** stop one-opponent patching. Red-team both brains and check every attack
  against the tree; hunt silently-vacuous checks; close the police-m10-kills-doctrine-m10 32/32
  hole with a cage-escape/tempo-punish evader + k-wall forecast; measure before deferring to any
  prior design. Mid-session: fold in the fresh nis-yar1 loss (their cop = second independent
  cage killer, step 13 ×3; our cop dropped g01 to a camper) and make the stack counted-ready.
- **Outcome:** ADR-0013 + `m11-redteam.md` + `m11-hardening.md`. Vacuous-check hunt confirmed
  the big one: `note_claim`'s "false claims are sanctioned" justification is enforced by NO
  audit path — fixed with the physics-only `MotionEnvelope` plausibility gate (no-op for every
  truthful claimer, closes a role-blind belief-hijack channel). Cage-escape landed as orbit
  (k-wall pocket forecast + center-margin term + low flight floor): doctrine-m11 vs police-m10
  0/32 → 5/32 with forced walls 6–8, and 8/8 vs every rival cop class incl. the new lag-1
  nis-yar1 pin arm that reproduces their live kill class. The session prompt's own tempo-lift
  hypothesis was built, measured harmful in every variant, and REMOVED (the mandate's
  measurement-over-deference applied to the mandate itself). nis-yar1 postmortem found the g01
  root cause — containment range refusal + a Manhattan-leaf local minimum behind our own wall
  (19-turn freeze, 11 walls unspent) — fixed (`contain_range 4`, `path_distance`), both live
  geometries pinned as unit tests. game.toml v1.06 arms the cop knobs and pins the book-v1
  overlay explicitly OFF (session item 3a). Deferred past the counted window, recorded in the
  session prompt's terms: self-play loop, Alon-newest pool refresh, claim re-sweep, solver
  defer-rate measurement.

## PR — m10-vibecode-countertune (the 30–90 becomes a mechanism, not a mood)

- **Driver:** Imree (session prompt `SESSION-PROMPT-M10-VIBECODE-COUNTERTUNE.md`, written off
  the 08-10 forensics; merge word is his) · **Author:** Claude (terminal, isolated worktree) ·
  **Reviewer:** pending (AG).
- **What was asked:** three work items from the 30–90 vibecode friendly — make the police wall
  in a central evader (42 walls unused despite perfect tracking), fix the doctrine evader's
  flee-to-corner death, feed opponent capture_claims into the evader's belief — plus rebuild
  the vibecode arena arms from the real logs first; strategy layer only; M9-pattern gates.
- **Outcome:** ADR-0012. Item 3 closed as already-implemented (the live loop has collapsed
  belief on inbound claims since M7-18 — verified in the g02 log: belief == the claimed cell
  at every step — so the work moved to arena-side modeling: `claim_threshold 0.0` on their cop
  arm, `truth` claim-feed on our evader arms). Containment walling (M10-1) and room-first
  flight (M10-2) landed config-gated, defaults off. Arms rebuilt from
  `logs/imreeyal-vs-vibecode_g0*.jsonl`; three fidelity iterations were needed before the
  thief arm reproduced the live result (wall-less M9 cop: 0/8 at signed starts, was 8/8
  against the naive rebuild) — the tuning instrument is only as honest as its worst arm.
  Evidence: `docs/evidence/m10-countertune.md` + regenerated arena tables. Fixed en route:
  the live view-model crashed folding a wall turn (`BARRIER` is not a compass move) — latent
  since M5-2 because no committed fixture game ever placed a wall until containment armed
  (`gui/models/live.py` + wall-turn pin). Also surfaced: our replay tool flags vibecode's
  audit hints ("revealed hint differs") — their audit does not echo hints verbatim; the
  settlement contract does not compare hints, so live Verified OK stands (dialect note).

## PR — chore/m8-todo-truth-pass (the TODO stops being a second journal)

- **Driver:** Imree (asked for a pre-M8 cleanup: sessions drift, and he suspected the TODO's
  walls of text and unclear completeness) · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** diagnose the drift sources before M8, then fix the TODO without losing
  information. Found: 143 lines carrying ~46k tokens (M7 entries had become full dossiers), while
  the file was simultaneously STALE — M7-43/45/48/49/52/53/54 merged on `main` with no entry or a
  wrong status, two different entries both numbered M7-4, and counted-series items still ☐ after
  both counted series had been played.
- **Outcome:** every ☑ compressed to status + pointers (evidence docs / ADRs / PR numbers; the
  full dossiers remain in this file's git history); every status re-verified against `git log`;
  missing milestones added; every open item given an explicit disposition (M7-0 overtaken,
  M7-1 delivered-as-the-kit's-sparring-peer, M7-2 verified in the kit tree, M7-8 accepted
  residual for M8, M7-5 blocked on best2934's handshake gap) — and the one genuinely open code
  item got its own number: **M7-55**, re-landed as PR #117 and merged. Header gains the
  entry-discipline rule so the file cannot regrow into a journal.

## PR — fix/m7-55-opponent-identity (the rescued commit, re-landed)

- **Driver:** Imree (the truth-pass surfaced the orphan; merge word is his) · **Author:** the
  2026-08-07 session (original commit `9e7cd1c`, rescued to `rescue/m7-opponent-identity`) ·
  **Re-lander:** Claude (terminal, cleanup session) · **Reviewer:** pending (AG).
- **What was asked:** make the M7-55 decision one-click. The rescue branch carried six commits,
  five of them M7-45 work already re-landed on `main` via PR #109 — only `9e7cd1c` (refuse an
  agreement from a group we are not playing) was still unmerged.
- **Outcome:** that single commit cherry-picked onto current `main`; the only conflict was
  `sync_manifest.json`, resolved by regeneration (`--write-manifest`, 319 files, verify OK).
  982 tests green, ruff + mypy --strict clean. Original authorship and the uoh-sqak credit
  preserved in the commit. **Mirrored core — the thief sync ritual is owed after merge.**

## PR — m7-48-sqak-rewrite (they rebuilt both roles overnight)

- **Driver:** Imree (sent the Barrier Law message) · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What was asked:** after the sibling repo's M7-46 found that uoh-sqak's cop was taking a
  step AND a wall in the same turn, and Imree raised it with them, measure what we actually
  face now — both of their roles, from their published source.
- **Outcome:** they fixed the Barrier Law inside two hours (`d07b654`), at the one chokepoint
  every one of their brains passes through, with a new test and a retune whose config comment
  records the same measurement we had made independently. They had also rewritten their thief
  (`1ca9d23`) after diagnosing the one we beat 3-0 as forfeiting. **So the friendly's record
  is void on both sides and projects nothing.**
- **Built:** `copthief_police/sqak_evader.py` — their new evader as an arm, carrying the
  values they FIELD rather than class defaults, their seeded tie-break, and their no-STAY
  rule. Never a role brain.
- **Two findings worth more than the numbers:** their THIEF is not deterministic (their
  runtime seeds it per sub-game, so a series draws a fresh stream each time — only their cop
  is deterministic, and their own "one game per role played three times" projection is right
  for one half and wrong for the other); and their rewrite fixed PARKING, not corner-seeking
  — on an open board it still rates the far corner highest, it simply no longer stands there.
- **Measured:** our cop takes their rewrite 20/32 on varied starts — the hardest thief in our
  pool — but **56/64 = 88% at the signed start**, which is the only start a counted game
  plays. Their fixed cop no longer threatens our thief at all (64/64), before or after the
  sibling's M7-46/47: their own fix did more for that matchup than ours did.
- **Caveat stated rather than buried:** the sibling's arm omits their L3 endgame solver,
  which cannot be expressed under a move-XOR-wall turn law, so 64/64 is an upper bound on our
  thief's comfort and not a guarantee.

## PR #107 — m7-42-audit-continuity-record-type (what a record IS, not what number it carries)

- **Driver:** Imree ("ok, so are you doing those fixes?" — after asking, twice, for plain
  language on what the killed window had actually found) · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the first live sub-game against `uoh-sqak` settled with
  `audit_ok: false`. Rather than accept the leading theory, the failure was reproduced by
  replaying the opponent's real `audit_received` payload through `validate_opponent_audit`,
  which named it exactly: `revealed game steps [1, 2, 1, 2, 3, … 35]`. An earlier guess in
  the same session — that his sealed records carried the wrong CONTENT — was wrong and was
  retracted before it reached him: 35 of his 38 records are proper move records. The real
  cause was ours, and one our own docstring had already described the intent of: non-game
  records were meant to be excluded from continuity, but were identified by step number
  instead of by type. TDD RED→GREEN with the live case as the acceptance test.
- **Outcome:** continuity keyed on a closed set of non-game record types; tamper checking
  untouched; two guards pinned (a tampered control record is still caught; an unknown type
  still counts, so the check cannot be emptied). His real audit now verifies clean.

## PR #103 — proof-window-artifacts (the 20:15 set: equal mutual hashes, on the record)

- **Driver:** Imree ("so there isn't anything i need to push right now right?") ·
  **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** the 2026-08-03 20:15 proof window's 20-file artifact set committed
  as the standing pre-counted evidence — the first window in cross-team history where
  both teams' result files carry the SAME mutual_agreement.sha256 (59147968…,
  verified against the opponent's arriving artifact field-by-field; only the two
  documented divergence classes remain). Also the live proof of the Round-29 mail
  (result-only, single attachment) and of M7-39's links.github in the wild. Artifacts
  only — no code, no mirrored path, no sync owed; clears the working tree for the
  counted-day clean-tree requirement.

## PR #106 — m7-41-counted-series-evidence (the first counted series, on the record)

- **Driver:** Imree (named the T with the opponent team, set the lecturer recipient
  himself after challenging why it was not automatic, then "sure, do it") ·
  **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** the first counted league series was played at T=01:00 and reported
  automatically to the lecturer alone (exit 0, six clean audits, single attachment). We
  lost 30–90. This PR is the evidence and the bookkeeping: the 20-file counted artifact
  set in its own `reports/counted-series/` tree, the six replay-verified logs, the
  evidence doc, and — the part that protects the NEXT counted game — the league ledger
  advanced to `counted_games_played = 1` / `counted_opponents = ["anrbj666"]` in the
  repo config, because a stale ledger would declare a false first meeting (rule 38).
  Three tests that hardcoded the shipped ledger values were rewritten to pin the
  invariants (count is an int ≥ 0, opponents unique, count ≥ distinct opponents,
  declaration equals what we carry) rather than today's numbers — the same gotcha-#9
  class as the config-version pins.

## PR #102 — m7-40-result-only-mail (the flip back, with the reasoning on the record)

- **Driver:** Imree ("i tend to agree with Alon, and if we are going back to the one
  attached thing make sure it's the last version ... with most of ours and Alons
  changes") · **Author:** Claude (terminal, fresh session picking up from the
  long-context one) · **Reviewer:** pending (AG).
- **What happened:** the opponent team's chatbot evidence (result-only mail; artifacts
  referenced, not embedded) was verified against the reference's own source before
  accepting — `emit_series` returns only the result "for emailing" and its sender puts
  it in the body — and the flip landed as a surgical supersession of M7-37's
  attachment policy only: result = body + single named attachment (the exact
  pre-M7-37 shape), `evidence_set` deleted, transport capability kept and pinned,
  full-sibling-set-on-disk pin proves nothing else ever rides. Every content
  improvement M7-33..39 built stays. Pair symmetry recorded as the tiebreaker (they
  flipped first; one-of-each is the only wrong state under rule 35); both Moodle
  readings stay documented; the forum one-liner to Yoram is the endorsed closer.
  PR #101 (links.github) was explicitly NOT scrapped — the opponent team's second
  letter recommends it.

## PR #101 — m7-39-result-repo-links (rule 49's four links, and a truthful remark)

- **Driver:** Imree (relayed the opponent team's Round-28 mail-diff verdict: exit
  criterion met + three findings) · **Author:** Claude (terminal) · **Reviewer:**
  pending (AG).
- **What happened:** his one material finding accepted after checking rule 49/p.96
  against both sample sets — the result's links block now carries both teams' repo
  links (his shape); and his cosmetic catch cut deeper than cosmetic: our _remark
  repeated the reference's "these names are examples" sentence inside real
  artifacts. Fixed truthfully, with the conformance byte-pin reworked to document
  the single deliberate divergence rather than hide it.

## PR #100 — m7-38-identity-spec-tolerance (his values were there all along)

- **Driver:** Imree (relayed the opponent team's ready letter claiming hardware "was
  already filled in the 16:00 window — check the declaration") · **Author:** Claude
  (terminal) · **Reviewer:** pending (AG).
- **What happened:** his claim checked against the wire bytes rather than our
  artifact — and he was right: his identity carried real hardware under
  `hardware_spec` (declaration shape) while our reader expected `spec` (F8b shape)
  and printed nulls. Our tolerance gap, fixed: both spellings accepted, gpu_model
  remapped, validated against the live 16:00 log. Verify-before-assert saved us from
  sending him a wrong accusation twice in one week.

## PR #99 — m7-37-full-evidence-mail (the grader's instruction, met in full)

- **Driver:** Imree ("why not build M7-37 now as part of this PR? i though we were
  doing this as well" — after verifying Moodle item 4 himself and the superset
  resolution was agreed with the opponent team) · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the series email now attaches the complete four-template set
  (14 files on a six-window series) while the result stays the body and named
  attachment — correct under both the Moodle instruction and the book's
  result-is-the-report mandate. Two 150-line splits fell out (evidence_set,
  email_build). The same Moodle page's item 7 set the submission deadline
  (12/08 23:59) — M8 becomes the priority track after this lands.

## PR #98 — m7-36-live-path-truth (the window caught our own two gaps)

- **Driver:** Imree ("Alon is here, let's do 16:00" — the verification window whose
  whole purpose was catching exactly this) · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the 16:00 series settled clean (30–90 — his rematch evader now
  survives all our cop games) and the artifact sweep found the emitted result
  contradicting the driver twice: opponent commits "unknown" (only the in-memory
  path knew the M7-33 field; the live path rebuilds from logs) and a rehearsal
  claiming a counted first meeting + diversity reward (league bump keyed on
  strict_rules). Both fixed TDD; the step-0 reader now lives in domain/ and both
  paths share it; validated against the real 16:00 logs. One more short window owed
  before counted.

## PR #97 — m7-35-identity-channels (their keep, our mirror, one correction)

- **Driver:** Imree (relayed the opponent team's Round-23 letter: their two-channel
  keep + "let's answer him and i'll send him the files as well?") · **Author:**
  Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** verifying their "keep" against our own tree found an M7-34
  inaccuracy — the wire handshake never carried the count (only the report-path
  builder did). Fixed together with the mirror of their rule: the wire identity now
  declares counted_games_played + the step-0 commit, sourced from the sealed record
  so the channels agree by construction. Their catch about the professor-repo
  example set lacking the commit confirms our documented example-vs-reference
  contradiction; the four book-attached files go to them with the reply.

## PR #96 — m7-33-34-example-conformance (the book's own files, honored)

- **Driver:** Imree (asked the book chatbot, caught its citation, fetched the book's
  four attached example files, and asked the two-repo question — "are we using the
  cop's? what about the fact that we have two repos?" — then "let's build it") ·
  **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** the chatbot's answer was first called fabricated (the commits it
  cited appear nowhere in the book text), then RETRACTED when the real attached
  example files surfaced — verify-then-accept cut both ways this round. The files
  redefined "mails perfect": M7-33 fills both commit columns (role-aware own via the
  loaded brain's repo — Imree's two-repo catch; opponent from their revealed step-0,
  zero wire changes) and M7-34 adds the three league-standing fields (diversity
  semantics re-derived from §9.2.1 + App F before coding, kept outside the signed
  symmetric outcome). One PR for both, per Imree's fewer-PRs preference.

## PR #95 — m7-32-warmup2-evidence (honest play, agreed score, converged artifacts)

- **Driver:** Imree ("let's set the T for 12:15 (israel) today... my computer has been
  reset from yesterday so you might need to set your things up again", then the
  artifact path for the diff) · **Author:** Claude (terminal) · **Reviewer:**
  pending (AG).
- **What happened:** post-reset preflight re-verified (junction, token, entry point,
  strays), launched at T-3min, gates green with 2.5min margin, fired 12:15:00.2, six
  clean sub-games, exit 0. 45–85 to them — exactly their Round-20 corrected
  adjudication, which is the convergence proof. M7-28/29 live-proven; report diff
  joins clean with only designed differences; his hardware/llm nulls = the sole
  residual. Counted gate met per his own letter.

## PR #94 — m7-31-referee-thief-quota (the instrument tells the truth again)

- **Driver:** Imree ("the PR was merged, you can do the fix you wanted" — after this
  session's first-hand review of thief PR #61) · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the police-lead half of the M7-30 finding. `thief_observation`
  now carries the quota exactly as the wire does (barriers_used=0 own count,
  max_barriers from the constitution); police builder pinned unchanged. TDD; 903
  tests; committed cop-repo arena regeneration proven byte-identical (no thief arm
  here reads the quota). The sync deletes the thief repo's red-going gap pin per its
  own stated design.

## PR #93 — m7-29-rule47-self-concession (their finding, our verification, the fix)

- **Driver:** Imree (forwarded the opponent team's two Round-20 letters, then "let's
  build that fix") · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** their claim — three warm-up survivals were rule-47 captures —
  was verified before acceptance on all three prongs: the rule re-derived from App E
  p.149 (source ch.3), the code asymmetry confirmed (cop + referee consume
  `is_imprisoned`, the peer thief never self-checked), the game facts read from our
  own sealed records (s1/s3/s5: sealed at (6,6) from step 13, 23 further turns,
  identical). Fix TDD (RED→GREEN, 6 pins incl. the exact bug shape): the thief
  adjudicates rules 46/47 against itself at the moment an inbound barrier lands and
  concedes through the existing caught-final shape. Corrected warm-up score recorded
  honestly (45–85 to them). Their `i_am_captured` design credited in the code.

## PR #92 — m7-28-result-conformance (the book's commit mandate, honored)

- **Driver:** Imree ("are there things that need to be included in the email and we
  aren't including them yet? ... i rather we fix our gap and then try another friendly
  game before moving to counted") · **Author:** Claude (terminal) · **Reviewer:**
  pending (AG).
- **What happened:** his question audited the emailed artifact against the book. The
  answer: hardware/identity/tokens/mutual-agreement all correctly placed (verified
  against the reference sample schema), but `github_commit` — book-mandated per
  sub-game in the closing email — sat at "unknown" (an M6-3 leftover; the reference's
  own sample has the same hole, contradiction resolved toward the book), and our
  `log_files` used a subdir prefix the sample doesn't. Both fixed TDD (RED→GREEN);
  own column reads the sealed step-0 hash, opponent column awaits the proposed
  commit-in-negotiate declaration. Next friendly proves both live before counted.

## PR #91 — m7-27-warmup-evidence (the join proven, the deltas named)

- **Driver:** Imree (named the T twice — "let's do it 15:30" / "let's try again at
  15:40" — then "i rather we fix our gap and then try another friendly ... i want us
  to play counted when we are 100% sure") · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the agreed cross-team warm-up, run push-button off the refreshed
  runbook. Window 1 burned on the opponent side (their thief declared sub-game 1 at
  our s2; 163 M7-10 refusals, killed per T-protocol, zero orphans); window 2 complete
  (60–40, 4–2, six clean mutual audits, one game_uid). Live promotions: info_mode
  `020947da…` matched all six handshakes; zero frame refusals (FP=0 held); sorted-pair
  artifact names' first live use. Report diff vs their arriving artifact: substance
  matches exactly; four cosmetic deltas + the mutual `github_commit` gap → M7-28
  claimed. Six logs committed, all replay Verified OK (378 records). Their premature
  one-sub-game report email (burned window) is recorded as their-side evidence.

## PR #90 — adr-0010-addendum (nobody signs the pre-refinement claim bare)

- **Driver:** Imree ("check if the work in M7-0 the Wire-shape mutual ADR actually
  represent what we came up to and agreed to ... sure, go ahead") · **Author:** Claude
  (terminal) · **Reviewer:** pending (AG).
- **What happened:** a drift check of ADR-0010 against the Rounds-15–19 outcomes found
  one load-bearing overstatement — the Context's "structural concealment / positions
  genuinely hidden" claim, disproved for the scent channel by the very inversion memo
  the co-signatory wrote (224/224, both models, verified by both teams). Fixed by ADR
  discipline: the original text stands as finalized, a dated addendum refines the
  binary into three tiers (wire-structural moves / declared-and-firewalled scent /
  bare promise), records that the resolution is unchanged and bookletter is weakened
  strictly more, updates the info_mode wording (registered + mutually declared, no
  longer "reserved"), and pins that signatures cover the addendum. Header mirror-claim
  corrected (the thief repo references, not carries, the ADR). TODO M7-0 notes the
  same for the warm-up co-sign ask.

## PR #89 — m7-26-concede-pin (their bug, our probe, an explicit pin)

- **Driver:** Imree (relaying the opponent team's Round-17 letter: "check your
  receiver") · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** their letter claimed every capture ending logs a false refusal
  unless the receiver exempts the caught final. Probed before answering: ours has
  exempted it since the first M7-23 build (`final_caught` guard, PRD §10.2), for both
  concede shapes — theirs re-sends the last grid unchanged, ours advances the trail —
  and the committed integration fixture turned out to be a cop_capture game, so the
  ending was already inside the pinned evidence. This PR adds the explicit
  two-shape pin they asked for. Their zero-step-re-send convention is accepted into
  the held kit co-sign text (one rule: `{}` and the unchanged final are the two forms
  of nothing-to-rely-on).

## PR #88 — m7-25-info-mode-lock (the posture becomes a handshake artifact)

- **Driver:** Imree ("sure i approve what you say, so i'll send the message to Alon and
  you'll start working on the follow-ups?") · **Author:** Claude (terminal) ·
  **Reviewer:** pending (AG).
- **What happened:** the Round-16 settlement with the opponent team (options 1+2 for
  the counted series, option 3 registry-first) executed on the code side: the handshake
  now declares `info_mode_sha256` beside `scent_model_sha256` — same kit §7 family
  machinery, both-declare-and-differ refuses, omission never — turning the
  `info_mode: belief` honor term into a both-declared lock backed by each side's
  firewall test. Rode along: the Round-16 empty-grid pin (`{}` is absence of data —
  the trap the opponent team's checker had and ours must never grow), the M7-24
  decision recorded (no wire change; registry question staged for co-sign), and the
  negotiate key-set pin updated. Their reply's technical claims were verified first:
  the recovery-cost axis is transient-vs-persistent (2 vs 1, both models, sign never
  matters — a measured 2×2 correcting their additive/subtractive split), and the
  `{}`-not-absent-key convention checks out on both wire schemas.

## PR #87 — m7-23-frame-check (the validator built, and a probe corrects the plan)

- **Driver:** Imree ("the PR has been reviewed and approved, you can merge... let's go
  with your recommendations") · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** M7-23 built in five RED→GREEN cycles on the approved PRD_scent §10
  (Imree's §10.6 calls: gate ON / no escalation / tally rides settlement) —
  `domain/scent_frame.frame_explained` (verdict-only surface, firewall pinned by test),
  the `peer/inbound.py` call site, `[scent] frame_check` ON by omission, the
  `scent_frame_refused` loop event, the settlement tally, and an injection acceptance
  test (decoy refused, refusals [1,2] with the documented baseline-poisoning cascade,
  both audits clean). **The build corrected the plan once, on evidence:** a probe showed
  our sender transmits unconditionally under a book-v1 lock (the locked doc's
  `transmitted: false` is honored on receive only) and belief consumes the grid — so the
  gate follows the arriving grid, not the model flag, and the sender-side doc↔behavior
  mismatch became open decision M7-24 (wire-visible; Imree's, likely joint). It also
  likely answers whose frames the opponent team's memo analyzed: ours, from the friendly.

## PR #86 — m7-23-frame-check-prd (the inversion memo becomes a gated PRD)

- **Driver:** Imree ("Do you want to start working on the things you said we should
  implement based off that?") · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** the opponent team's 2026-07-27 scent-inversion memo was verified
  before anything was adopted from it — their transition inversion re-run here as a
  simulation under BOTH registered models (224/224 frame pairs invert to exactly one
  emitter, including 30-turn saturated dwells; the leak is model-independent, which
  extends their own claim), kernel arithmetic confirmed against the locked registry.
  The defensive half then became `PRD_scent` §10 + gated TODO M7-23: an in-play
  frame validity check in front of `absorb`, whole-frame refusal, evidence-grade only
  (SQ3/M6-7 class), with an explicit firewall — the validator never returns, logs, or
  feeds the candidate cell it matched, because the `info_mode: belief` posture offered
  to the opponent team binds our own build first. Docs-only; the build waits for the
  §10 gate. The other two memo items (commit-binding the grid, the info_mode lock for
  the counted series) are joint wire matters awaiting the opponent team's answer.

## PR #85 — adr-0010-wire-shape (the joint ADR, finally in the tree)

- **Driver:** Imree ("ok sure, but maybe just make sure before that what's in there is
  actually what we and Alon ended up doing?") · **Author:** Claude (terminal, worktree)
  · **Reviewer:** pending (AG).
- **What happened:** the wire-shape joint ADR — final text since 2026-07-22, staged in
  notes, displaced by live windows for five days — verified line-by-line against what
  the two teams actually did, then landed as `docs/adr/0010-wire-shape.md` (0006 was
  taken; 0007 stays reserved). The core survived verification untouched; four stale
  peripherals were reconciled in a dated finalization note: decision 6 was confirmed
  by adoption and the live series rather than the planned call; the corroboration of
  record is now the 2026-07-25 series, not demo games; the hosting consequence is
  discharged history; the negotiate-extras family (pairing / scent hash / uid) is
  recorded as shared practice on the same truth table. Status PROPOSED; M7-0 moves
  ☐→◐ and ticks only when both signatures are recorded (anrbj666's ask rides the
  warm-up exchange).

## PR #84 — worktree-m7-22-uid-declare (say your uid at the door)

- **Driver:** Imree ("do you want to do it now?" — yes) · **Author:** Claude (terminal,
  in a worktree; the strategy sessions owned the main checkout this weekend) ·
  **Reviewer:** pending (AG).
- **Why:** the opponent team's uid bug survived an entire six-sub-game series because
  the uid never crosses the wire — each side derives it independently and nothing
  compares them until the two reports meet, the morning after. The M7-10 pattern
  closes it at the handshake: declare the derived uid when the opponent is known a
  priori, refuse a comparable mismatch with the diagnosis in the message, omission
  never refuses. Milestone claimed as M7-22 in memory BEFORE building — the rule the
  M7-17 double-renumber bought.

## PR #83 — docs/m7-20-clarify-not-a-physics-argument (a wrong inference, caught by Imree)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What happened:** in conversation I extrapolated M7-20's `ref-police` finding into "the
  biggest lever is renegotiating the scent model away from `multiplicative_book_v1`". Imree
  asked the obvious question — that is the model we played him under, why replace it? — and
  the inference does not survive it. We **won** that friendly 75–35 under book-v1, both cop
  captures in cross-team history happened under it, and (verified from git) the cop was then
  running the reference-tuned BASE table because the book-v1 overlay did not exist until
  `5d9a2ff`, after the friendly. The cross-physics gap is also confounded by tuning
  maturity: our reference vector has had far more GA investment than the book-v1 overlay's
  two attempts.
- **Outcome:** the wrong framing had **never been committed** — the M7-20 evidence, TODO and
  PR #82 all state only the narrow tuning reading. This PR hardens that doc against the
  misreading anyway: an explicit "this is a statement about our TUNING, not an argument
  against the physics", and the tuning-maturity confound added to *What is NOT claimed*.
- **Lesson worth keeping:** a measurement that a heuristic beats our tuned brain supports
  "our tuning is weak", not "the rules are wrong". Two readings, very different actions; I
  took the expensive one first.

## PR #82 — m7-20-ga-under-the-claim-policy (a null result, reported as one)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** he asked whether the three named follow-ups could share one session
  and why I had not started them. Answer: 1 and 2 are co-evolutionary and 3 depends on 1,
  so the honest shape is "cop retune + re-sweep" as one session. Then I started item 1.
- **Outcome: the retune FAILED its gate in both physics and is not deployed.** The value
  of the session is what refusing to accept two suspicious results produced.
  (1) The first GA run came back perfectly flat — default, deployed and evolved all scoring
  exactly 0.6406 while their weights differed by an order of magnitude. Rather than write
  that up as "no improvement available", I measured per-member spread across deliberately
  extreme vectors and found the run was simply under-powered at 16 seeds. Rerunning at 32
  gave a real curve.
  (2) That diagnostic then produced the structural finding: **our own claim policy flattens
  the pool member that was providing the selection pressure** (claim-reader spread
  0.094 → 0.031). Blinding the opponent blinds the tuner.
- **Discipline notes:** the gate's `ref-police` row was initially unfair — it ran unmodelled
  while both candidates were claim-gated, so it got the historical "every same-cell ending
  resolves" physics for free; pinned to its own faithful policy and rerun before the table
  was committed. And the losing weights are committed as a *labelled* negative-result
  artifact rather than discarded, so the run stays reproducible.
- **Defect found in passing:** `scripts/ga_run.py` hardcoded `config/ga_weights.json` into
  every generated evidence doc regardless of the config's `artifact_out` — so the committed
  M7-14 evidence pointed readers at the wrong file. Fixed and regenerated; the regeneration
  doubled as proof that the new GA knobs are inert on old configs (same md5, same curve).

## PR #81 — m7-19-quiet-cop (the other half of the channel; heading corrected — #80 was the parallel session's docs PR)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** build half 2 on the approved PRD — model the claim channel inside the
  referee, then sweep a threshold on series points across an opponent mixture.
- **Outcome:** three RED→GREEN cycles, then the sweep. The result that mattered came from
  refusing to accept a suspicious table: three of the four opponent columns were IDENTICAL
  at every threshold, including a cop that never declares at all. That looked like the
  gate not reaching the arena path. Two probes settled it — a barrier-free chaser goes
  32/32 → 0/32 when silenced (so the gate works), and our deployed vector's captures are
  loud-equals-silent against every non-reading opponent (so it has NO landing captures to
  forfeit). Our cop wins by walling, which the book never lets a cop withhold, so the claim
  channel is pure downside for it.
- **Discipline note:** the contrast case is COMMITTED in the instrument rather than written
  up as a caveat — a plain chasing cop is destroyed by the same silence, which is what
  proves the comfortable result belongs to our weight vector and not to the game. The g06
  capture (which any positive threshold forfeits) is a passing regression test rather than
  a disclosed limitation. Nothing is deployed: merging changes no play.
- **Recommendation offered on Imree's open decision 2:** do not build the in-series adaptive
  policy — a dominant static threshold leaves it nothing to discover.
- **Corrected mid-PR on Imree's pushback.** My first write-up led with "his current thief
  ignores claims, so this is worth nothing against him today", which conflated *adds
  nothing* with *costs something* and buried the actual result. He was right: the point was
  always to handle thieves that DO read claims, the EX06 team has announced exactly that
  for the rematch, and we play several teams we have no intel on. The sweep's real finding
  is the robustness one — 0.1 is best-or-tied against readers AND non-readers, so one
  standing setting covers both and needs no guess about who we draw. The same pushback
  surfaced a bigger gap: I had built the referee model but NOT the live emitter, so the
  capability did not exist on the wire. Wired it (`PeerSession.claim_policy`) and deployed
  0.1 on the book-v1 overlay, with peer-path validation.

## PR #79 — m7-18-evader-reads-claims (the discarded certainty, collected)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** build half 1 on the approved PRD, with the recommendations he
  endorsed (hard collapse; adaptive policy deferred until the static sweep reports).
- **Outcome:** two RED→GREEN cycles, then measurement — and the measurement is where the
  work actually happened. Three things only came out of running it rather than reasoning:
  (1) the **counted physics is the whole story** — exact cop-tracking 0.311 → 0.936 under
  `multiplicative_book_v1` but only 0.822 → 1.000 under the shipped reference model, where
  the age-voucher belief was already near-perfect. Probing one physics would have produced
  a confident and misleading number either way. (2) **The committed instrument understated
  the channel**: M7-14 modeled claim-reading as lag-1, but the cop claims the cell it is
  *standing on* when our thief decides — lag 0. Read correctly, a result that had looked
  neutral-to-harmful against our tuned cops becomes a gain against every cop in the roster.
  (3) The first generated artifact **leaked a scratchpad path** (banned anti-pattern) and
  was unreproducible from committed config; fixed by giving the probe an in-memory
  `--scent-model` override rather than by editing the shipped config.
- **Discipline note:** the lag-1 correction is a finding *against our own prior work*, so
  it is recorded as a named follow-up (the cop's GA pool should retune against the lag-0
  arm) rather than quietly folded in. No cop weights changed here.

## PR #78 — m7-18-claim-channel-prd (the mechanism PRD for the claim channel)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** open the last open strategy item — the claim channel — in two
  halves, evader-reads-claims first, and gate it behind a mechanism PRD whose book
  citations are **re-derived, not inherited** from the prior session's memory.
- **Outcome:** docs-only PRD. The re-derivation changed the argument's shape twice.
  (1) The legality case is stronger than "the book is silent on frequency": one sentence
  after the capture clause, in the same p.38 iron-rules paragraph, the book mandates that
  the cop declare **every** barrier placement and forbids placing one in secret. It wrote
  both halves for barriers and only the truthfulness half for claims — argument by
  contrast, not from silence. (2) Scoring table 2 (p.38) makes the claim **constitutive**
  of the landing capture, which prices silence from the book itself (forfeit the capture)
  and hands the referee model in §5.1 its rule rather than leaving it a modeling choice.
  (3) Reading the tree rather than the notes sharpened the leak: the opponent's start is
  signed constitution and claim *absence* is equally informative under the reference
  policy, so a claim-reading thief has the cop's exact cell every turn — full
  observability, not a strong observation. That in turn is why half 1 deliberately does
  **not** read absence: present-claim reading is sound against every opponent, absence
  only against an unconditional claimer.
- **Gate:** no build code until Imree approves. Three decisions left open for him
  (collapse-vs-trust-weight, whether the adaptive policy is built at all, deployment
  posture) rather than taken silently.

## PR #80 — docs-uid-wording (the opponent's correction, honored in our evidence)

- **Driver:** Imree · **Author:** Claude (terminal, in a worktree — the claim-policy
  session held the main checkout) · **Reviewer:** pending (AG).
- **Why:** anrbj666's 2026-07-26 reply corrected our uid diagnosis — not a minted id but
  a deterministic derivation over the WRONG INPUT (their whole game.json vs the flat
  negotiated terms), with their bundle internally self-consistent — the sneakier class.
  Amended the evidence doc and the TODO M7-3 line to the corrected mechanism, recorded
  their fix's three-way verification, the game_id resolution (M7-17), and the residual
  mutual finding (uid divergence is silent during play; declare-at-negotiate proposed).
  PROMPTS history above stays as written — the log records what each PR knew at its time.

## PR #77 — m7-17-sorted-game-id (one match, one name, from either side)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **Why:** the cross-team report diff (2026-07-26) found each side naming the match
  self-first — the last cosmetic divergence between two otherwise field-identical
  reports. Verified against the oracle before changing anything: the reference DERIVES
  `game_id` sorted (`domain/game_ids.py`), the kit pinned it the same day (SPEC §4,
  swapped-order vector), and the opponent's naming already matched — ours was the
  divergent side. One RED→GREEN cycle: pure `domain/crypto.series_game_id` beside
  `game_uid`, three call sites derive through it, the test harness derives rather than
  re-encodes. Committed friendly evidence keeps its as-played names — evidence is
  never renamed. (Milestone renumbered twice mid-PR, M7-13→M7-16→M7-17: the parallel
  strategy session claimed M7-13..15 in this repo and then M7-16 in the sibling's TODO
  while this branch was open — the cost of two live sessions numbering from one
  sequence, worth a claim-the-number-in-memory-first habit.)

## PR #76 — feat/m7-15-mixed-ga (the generalist retune + per-model deployment)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** his direct challenge on the M7-14 follow-ups — "why are we
  leaving them open, whose responsibility is it?" Answer: ours; closed here.
- **What landed (2 TDD cycles):** the mixed-opponent GA pool (fitness = mean across
  members, pinned against the single runs it is built from) and the
  `[strategy.<role>.<scent_model>]` overlay mechanism, plus the rerun retune, the
  four-cop/five-thief gate tables in both physics, and the deployment itself — the
  pool vector on the book-v1 overlay, base table untouched (the merge is the
  deployment approval; the base-swap alternative is stated in the PR).
- **Honesty notes:** the pool vector loses the book-v1 aggregate to the plain
  chaser (which still collapses vs claim-reading, 5/32 — the aggregate is not the
  expected opponent distribution); the lag-1 specialist's single-arm superiority is
  stated, not smoothed; the peer-path validation's single-seed survival flip is
  disclosed next to the 32-seed tables that carry the claim.

## PR #75 — feat/m7-14-bookv1-arena (strategy under the counted physics)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** the strategy-session brief, deliverables 2–5 — a trap-aware
  evader opponent model approximating the opponent team's announced rematch
  counters, a seeded measurement of the champion cop's edge against it under
  book-v1, a GA retune under the counted physics through the champion-regression
  gate, and the belief filter's age-voucher weakness revisited.
- **What landed (12 TDD red→green cycles):** the scent-model doors through the
  whole referee/arena/GA path (one registry→model builder shared with the peer
  session), per-side information feeds incl. `LagTruthFeed` (the claim-reading
  counter as lag-1 truth), `BeliefEvaderBrain` with config-expressed ablation arms,
  the kernel-innovation belief observation (book-v1 argmax 17% → 61%, reference
  path byte-identical), two committed measurement arenas + the book-v1 GA config,
  and the three-cop champion comparison under both physics. Both weight vectors
  committed, nothing deployed — game.toml untouched.
- **Honesty notes:** the first arena tables were generated before the belief fix
  and regenerated after (both states in history, the doc quotes the final ones);
  raw-shape matching was tried, measured worse than the voucher baseline, and
  replaced by the innovation — the dead end is disclosed in the evidence doc; the
  GA's lag-1 specialization cost against naive evaders is stated, not smoothed.
## PR #74 — docs/m7-13-capture-postmortem (how the g02/g06 cops actually won)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** the strategy-session brief — a capture postmortem of the friendly's
  two cop wins as the first counted-series-prep deliverable, with the opponent known to
  be running the same analysis on his side.
- **What landed:** `docs/evidence/m7-13-capture-postmortem.md` — full per-step
  reconstruction of g02/g04/g06 from the committed logs (their thief's audited moves,
  our audit positions, claim/response cross-checks), the mechanism findings (beacon
  camping, pursuit-lane collision, the g04 clock-saved contrast), and the two
  intelligence items that redirect the arena work: the evader counter-model needs
  cop-tracking and claim-reading before wall-forecasting, and our claim-per-step habit
  is a free position feed we may want to stop volunteering. Analysis only — no source
  changed; the reconstruction script is quoted in the doc, uncommitted by the M6
  evidence precedent.

## PR #73 — docs/m7-3-friendly-evidence (the first external friendly, on the record)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What landed:** the M7-3 evidence — six committed logs (all replay Verified OK), the
  20-file artifact set under `reports/imreeyal/`, the evidence doc with the result
  (75–35), the cross-team report diff (every game value agrees; their minted `game_uid`
  vs the wire-locked one raised as the rule-35-relevant finding), and the seven-window
  campaign ledger with the hardening each burn produced. TODO M7-3 ticked on observed
  DoD. Nothing in the doc exceeds what the tree and the logs prove.

## PR #72 — m7-12-terms-absent-refusal (name the absence, not just the disagreement)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **Why:** during the 2026-07-25 friendly campaign, window T3 refused every handshake with
  `terms mismatch` when the truth was `terms ABSENT` — the opponent's bookletter greeting
  under a reference wire. The diagnosis took reading the raw inbound log; the refusal
  should have named it. One RED→GREEN cycle; both diagnoses pinned.

## PR #71 — m7-11-series-endpoints (dial the opponent service that plays THIS sub-game)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What he asked, and the correction behind it:** "what do you mean? something that we need
  to fix on our end? If so do it" — plus the standing demand that playing other teams *cannot
  be this complicated each time*. The answer had just come from primary source: he told us to
  read the opponent team's shared repo instead of waiting to ask them, and their committed
  `league_series.py` runs a series as TWO role-split services (police repo owns the odd
  windows, thief repo the even ones), while the reference runs it as ONE process at ONE
  address. Both topologies are real; our driver dialed one URL for all six sub-games, which
  is wrong half the time against the first shape.
- **Built (three red→green cycles):** `sdk/series_endpoints` (one address or a split pair,
  every ambiguous combination refused; the config default yields to explicit flags),
  per-role dialing in `subgame_player`, `--opponent-police-url`/`--opponent-thief-url` on
  `copthief series`. Wire untouched — this is dialing, not protocol.
- **The generality point, honored:** after this, ANY opponent topology is the same one
  command — one URL for a reference-shaped team, two flags for a role-split one. No
  per-team code.
- **Validation over trust:** the 2026-07-25 predecessor rig had deadlocked at sub-game 2 and
  the work was discarded rather than diagnosed. This one was rebuilt against a FAITHFUL
  opponent simulator (two independent sequential window-runners, started together, handshake
  re-push as the only barrier, the opponent's own 180s patience) — six windows settled
  strictly in order, roles alternating, one game_uid, exit 0. The M7-10 pairing refusals are
  what changed: the early window's pushes are refused by index instead of swallowed.
- **M7-11b, and the correction that found it:** Imree rejected the rig's dev-mode/no-email
  posture — *"a friendly is EXACTLY a real counted game... sending mail is also part of a
  real game"* — so the rig was rerun FULL-DRESS (`--rehearsal` both sides, tuned brains,
  real send to ourselves at the close). That run failed, informatively: a bystander's
  agreement (the opponent's other window pushing early — identical terms, valid signature,
  wrong only in WHICH game) raised the M7-10 pairing refusal out of `run_peer_game` and
  killed every window where we moved second; the dev-mode run had escaped by winning the
  arrival race. The driver honestly refused to mail an unsettled series (rule 35 behaving).
  Fix (TDD): `PairingRefusal` is refused on the record and outwaited, bounded by the turn
  budget; terms drift and bad signatures stay first-offense fatal. His methodological point
  stands proven: the defect was only reachable with the FULL format running.

## PR #70 — m7-10b-report-preflight (decide before the series, and the mail we actually sent)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What he pushed on, and he was right:** the report send was something I *decided after*
  the series (I had pointed the token at a missing file to prove the rail was *reached*
  rather than *worked*). His standing demand — stated across several sessions — is that a
  friendly is a real match minus the counting, and *what must be decided is decided BEFORE
  the series*. This makes that mechanical: a run that owes a report (`RunMode.strict_rules`)
  now calls `EmailSender.preflight()` before the first sub-game — the interlock plus a
  credential probe that refreshes the OAuth token without sending — and refuses to start,
  zero games played, if it cannot deliver. **A `--rehearsal` can no longer run with mail
  disabled.**
- **And the mail was actually SENT** (his authorization of the recipients being the
  authorization, constraint #16): the six-sub-game series fired its report to the team
  account + his personal address, body and attachment both the artifact, exit 0. The first
  email the project has sent.
- **Two book checks he asked for, both verified against primary sources, not memory:**
  (1) the subject is the reference's byte-exact string (`sdk/sdk.py`), and the book mandates
  none — so matching the reference is the interoperable choice. (2) Rule 34 says "ONLY as an
  attachment", but the book's own App A listing AND the reference send body-only — a
  book-vs-reference contradiction. We send **both**, which is the one form safe under a
  strict reading of the rule *and* under his grader's actual parser. Recorded in ADR-0008
  decision 5 per the academic-freedom clause.
- **Honest note:** the preflight changed what an earlier evidence run showed (a `--rehearsal`
  with disabled mail used to play 6/6 then refuse at the end; it now refuses at the top). I
  corrected the `m7-10-series-completes.md` sentence rather than leave it describing behaviour
  the code no longer has — the doc↔repo gap is the one fatal failure mode.

## PR #69 — m7-10-handshake-pairing (which game, which side, and who is still listening)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **Why it exists:** building #68 made two live-path defects visible by running the thing
  rather than reasoning about it. Neither was caused by the series driver; the driver is
  what made them observable. Imree's instruction was to build it before naming a T with
  the opponent team, because *"the difference between a rehearsal and another burned
  window"* is exactly this.
- **The question he asked first, and it sharpened the work:** *"part of the things we are
  doing in M7-10 should be addressed by him on his side, no?"* Yes — for one of the three
  pieces. Answering it honestly forced me to correct something I had implied: I first
  thought the swallowed-handshake fix needed the opponent, because our re-push only
  protects OUR greeting reaching THEIR new peer. It doesn't need them — the other
  direction is closed by refusing inbound traffic after our own settlement, so their
  existing retry delivers to our next peer. Two unilateral halves, not one.
- **What genuinely needs the counterparty** is the negotiate declaration: we can *send*
  `sub_game_number` + `role` alone (unknown fields are tolerated, the reference ignores
  them), but we can only *refuse on mismatch* once they send them too. Stated plainly in
  the TODO and in the staged reply rather than left as an assumption.
- **The draft was sharpened before sending on a concrete lesson:** the rehearsal lost a
  window to `payload` vs `message` and to a bookletter handshake arriving on a
  reference-v3 wire. So the reply carries the exact field shape and the exact refusal
  rule, instead of "declare the index" and a second round of interop discovery.
- **Result, and the reason to run things:** before these fixes a six-sub-game series had
  never completed — the sides desynchronised at sub-game 2. After them, 6/6 settle with a
  mutual audit on every one, one shared `game_uid`, the full artifact set, and the report
  rail firing at the end. Evidence `docs/evidence/m7-10-series-completes.md`.

## PR #68 — m7-4-live-series-report (the series-end email, and the thing that fires it)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked, in his words:** a friendly is a counted game in every respect except
  that it is not counted and the lecturer is not the recipient — *"in football they are
  playing the full two halves; the only difference is that it isn't counted."* So: all six
  sub-games, real rules, the full artifact set, and **one email auto-fired at series end**.
  The instruction was explicit that this comes first, because the previous session kept
  deferring it to chase live scheduling windows.
- **The gap turned out to be narrower and worse than "the email is missing":** every
  piece existed and was tested — `summary_from_log`, `series_from_logs`, `email_sender`,
  `email_interlock` — but a live series plays each sub-game in its own process, so **no
  process spanned the series** and nothing owned the moment it ended. A perfect 6/6 would
  have mailed nothing. What was missing was an owner, not a feature.
- **`RunMode` was merged and passed by nothing**, so every live game so far — including
  the 2026-07-24 rehearsal — ran with the App F rows disarmed. It is now a real CLI flag
  and, importantly, is carried into each sub-game CHILD: the child loads the config tree
  itself, so arming the rows only in the driver would have relocated the defect.
- **Running it live was the whole value.** Three defects fell out of the first two real
  runs, none of which any test I would have written had caught: a sub-game that left no
  log crashed the aggregation with a bare `FileNotFoundError`; a child that died left no
  trace of *why*; and a failed send took the entire run record with it, so the operator
  saw a traceback instead of "here is the artifact that did not reach the opponent."
  Each is now a test written from the observed failure, quoted in its docstring.
- **Two findings deliberately NOT fixed here** (`docs/evidence/m7-4-live-series.md`, new
  TODO M7-10): the `negotiate` payload names neither the sub-game nor the role — observed
  as two *thief* peers completing a handshake and deadlocking, which is the same hole that
  produced the rehearsal's phantom sub-game 6 — and a handshake can be swallowed by the
  opponent's previous sub-game peer, which desynchronises the series permanently. Both are
  interop work, mutual with the opponent team; the driver did not cause them, it exposed
  them. Saying so rather than folding a half-fix into this PR is the point.
- **One decision was Imree's and was asked for, not assumed:** committed `game.json`
  `num_games` 1 → 6. His reasoning went further than the question — better league evidence
  is coming from the real friendly, so ship the constitution we actually play under.

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

## PR #67 — m7-9-rehearsal-mode (splitting one overloaded flag)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** *"of course it isn't counted, it's a friendly game"* — Imree hit the
  naming confusion directly. He was right, and his confusion WAS the bug: `counted` did
  not mean "this scores league points", it meant two unrelated things at once, and one of
  them (arm the App F rulebook) is something a friendly very much wants.
- **The design question I brought back rather than deciding.** A naive split into two
  independent booleans would have made the lecturer *easier* to reach than today —
  ADR-0008's guard is strong precisely because `counted` cannot be set casually. So the
  split welds them back in the one direction that matters: `counted_series` without
  `strict_rules` raises at construction and cannot exist. Imree chose that option
  explicitly. The guarantee's strength is unchanged; only its spelling moved.
- **Why the email parameter got renamed too.** `decide_email_action(counted=…)` invited
  exactly the mistake being removed — a caller with a rules flag in hand and a parameter
  named for the run type. It now takes `lecturer_addressable`, named for what it permits,
  defaulting closed at both layers.
- **The finding that fell out of writing the ADR, and it is not flattering.** Because
  `counted=True` was unsafe to pass, *nothing in the codebase ever passed it*. Every live
  game — including the rehearsal series played against Alon/Renat's team that same day —
  ran with the App F rows **disarmed**. The constitution was counted-shaped only because
  someone set it by hand. Rules were being followed rather than enforced, and it looked
  identical from the outside. Recorded in the ADR's Context rather than quietly fixed.
- **Scope held deliberately:** `counted` is NOT renamed across its 146 mentions. The
  confusion that actually bites is at the email seam, and that is the one renamed.

## PR #66 — m7-4-series-artifact-and-subgame-seal (found mid-rehearsal)

- **Driver:** Imree · **Author:** Claude (terminal) · **Reviewer:** pending (AG).
- **What was asked:** make a friendly that looks exactly like a counted game. Imree's
  framing settled it: *"in football, friendlies don't change the rules — they play the
  full two halves; the only difference is it isn't counted."* I had been leaning on
  CLAUDE.md §9's "friendlies: format-free" to justify a lightweight report, which reads
  that clause exactly backwards — the sentence continues *"the format is proven on both
  sides before any counted game."* A lightweight report proves nothing about the format.
- **What that reframing immediately found.** Loading the constitution with `counted=True`
  arms the App F fixed rows, and the guard refused: *"num_games: fixed at 6 by App F, got
  1"*. So our config would have played six sub-games while every step-0 record declared a
  ONE-game match. Alon accepted it in one line (*"our own truth-duty argument decides
  it"*) and flipped his side too.
- **Then the same class of defect turned out to be ours, and deeper.** `sdk/peer_run`
  never passed `sub_game_number`, so it fell back to the static TOML value: every
  sub-game sealed `sub_game_number: 1`. `series_run` (self-play) always passed the real
  index — the LIVE rolling protocol, one process per sub-game, never did. **The index is
  inside the step-0 commit**, so unlike a report field it cannot be corrected afterwards:
  index 1 seals `9237f54c…`, index 4 seals `2337737826…`. Two already-played sub-games
  were unusable as artifacts no matter how cleanly they played.
- **The design choice in (b): rebuild summaries from the LOG, not from live memory.** The
  obvious fix was to hand the session out of `run_peer_flow`. Deriving from the committed
  log is better for a reason that has nothing to do with convenience — **what we report is
  then exactly what we archived**, and a third party can re-derive the artifact from the
  same bytes. `series_from_logs` refuses the whole series if any sub-game never settled,
  because a report that quietly drops a game is the contradictory report rule 35 punishes.
- **Honesty detail worth keeping:** the opponent's declaration block is copied from their
  archived `agreement_received`, and keys they never sent are recorded **blank rather than
  filled in**. A declaration block records what a team *stated* about itself; inventing a
  plausible `group_name` there would be fabricating a signed record.
- **A vacuous test I caught on myself:** `assert len(result["sub_games"]) == 6 if
  "sub_games" in result else True` passes when the key is absent. Replaced with real
  assertions including the scoring arithmetic (six survivals, alternating roles ⇒ 3–3
  tie) and the on-disk artifact set. Also rebuilt a fixture through the real
  `TurnMessage` after hand-listing its keys drifted twice.

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
