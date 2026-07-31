# ADR-0010: Wire shape — resolving the book's Ω_i self-contradiction

> Joint ADR, co-signed with Alon/Renat's team (their round-2 commitment); lives in the
> cop (lead) repo — the thief repo references it rather than carrying a copy (docs are
> not core-synced) — and is referenced from the kit's shared registrations (kit issue #6).
> Numbers in [brackets] = our extraction's PDF pages; printed pages differ
> (App D §4 = printed p.125).

## Status

**PROPOSED — text final; awaiting the two signatures below.** The tick of TODO M7-0
happens when both are recorded, and not before.

**Finalization note (2026-07-27).** The text below was finalized 2026-07-22; between
then and landing, every item it still listed as open was discharged by events rather
than by the planned call:

- **Their independent verification (2026-07-20): FULLY GREEN** on the staged game
  `deee14f6…` — 35 commit-reveals, byte-identical `smell_grid`s under their
  from-scratch `subtractive_chebyshev_v1`, barrier growth 0→7, and they re-derived our
  `game_uid` from our committed config themselves.
- **Decision 6 is confirmed by adoption and by fire, not by a call:** both teams
  implemented the receiver contract (their round-8 adoption of the commit-keyed dedup,
  our M7-8), and the 2026-07-25 friendly exercised it live in both directions —
  handshake re-push storms, bystander refusals, and duplicate tolerance across seven
  scheduled windows. The formal both-directions duplicate drill stays on the next
  warm-up's checklist as the remaining ceremony.
- **The corroboration is no longer demo games.** On 2026-07-25 the two teams played
  the league's first fully autonomous cross-team series under `reference-v3`: six
  sub-games, one wire-derived `game_uid`, every mutual audit clean both ways, one
  auto-fired report per side agreeing field-by-field on every game value (the two
  id-derivation defects the diff surfaced were fixed by both sides within a day —
  see the M7-3 evidence and kit WARNINGS). This is the strongest corroboration the
  resolution can have: not that the shape is playable, but that it was played, settled
  and cross-audited end to end by two independent implementations.
- **The negotiate-extras family grew on the same truth table** decision 3 pins:
  `sub_game_number` + `role` (M7-10, mutual), `scent_model_sha256` (M3-8), and the
  declared `game_uid` (M7-22) all ride OUTSIDE `terms`, refuse only a comparable
  mismatch, and never refuse omission — the pattern is now shared league practice.

## Context

The book self-contradicts on what the wire may reveal:

- **Ch. 5's letter** [PDF ~50–52]: four binding phases in EVERY game step; the Reveal
  phase sends the Move (nonce withheld). With signed starts, per-step move reveal
  makes both positions computable every turn.
- **Ch. 1 §1.3's formal model** [PDF 20–23]: the game MUST be modeled as a Dec-POMDP
  whose eight-tuple defines {Ω_i} as "what each agent actually perceives — the core of
  uncertainty. **No agent sees its rival**: both the cop and the thief feed, each, on
  the rival's decaying scent traces and its verbal declarations." Figure 1: the true
  state S "is accessible to no agent"; each agent builds Ω_i "from its scent map plus
  a verbal hint — which may be false. The setup is symmetric." §1.4 [PDF 22]: "the
  **only** channel of deception is the verbal hint" (an active exploitation of O).
- **Corroborating derivations:** ch. 7's local-truth principle [PDF 70] states it
  "follows directly from the Dec-POMDP formalism: Ω_i is a partial subset of the true
  state S, and an interface exposing the full S would violate the game's rules";
  the capture-claim protocol presumes the claimant does NOT know the rival's cell
  (a truth-duty that is incoherent under common knowledge).

A wire that makes positions computable every turn contradicts the book's own
mandatory mathematics. This is a formal self-contradiction, so the academic-freedom
clause [PDF 5] applies: choose and document. Two internally consistent resolutions:

| Named shape | Reading | Model conformance |
|---|---|---|
| `reference-v3` | Moves sealed until the audit boundary; `smell_grid` transmitted; positions genuinely hidden. All four ch. 5 phases occur, with **Reveal deferred to the audit boundary** (the book's audit is itself a mass reveal) — deferred, not skipped. | **Implements the formal model** (Ω_i, O-deception, truth-duty). The shape of the reference implementation and the kit. |
| `bookletter-v3` | Per-step Reveal; replicated lockstep engines; positions common knowledge; belief machinery by policy. | Implements ch. 5's letter; **deviates from the book's formal model** (issue #6's own wording). |

**Evidence precedence** (Appendix D §4, principle 2 [PDF 141 / printed 125]):
"wherever the repository deviates from the book, the book and the binding parameters
table prevail." Therefore demo behavior is NOT this ADR's spine — the Ω_i argument is;
the demo-interop games (one **independently re-verified by Alon/Renat's team,
2026-07-20 — game `deee14f6…`, their tooling, physics recomputed under
`reference-v3`, every claim green**) were the corroboration at drafting time; the
2026-07-25 cross-team series (Finalization note above) has since superseded them as
the corroboration of record — the shape was played, settled and mutually audited end
to end by two independent implementations.

**Why a hidden game must be hidden by the wire** (argument contributed by Alon/Renat,
2026-07-21, and adopted here as the decisive one — it is stronger than the
"engineering effort" framing either side brought to the call): the two shapes are not
merely two ways to hide the same information. A pair could in principle play
`bookletter-v3` and simply *agree* not to look at the rival's revealed position — the
`info_mode: "belief"` term the kit reserves. But that term is an **honor term**: a
mismatch is provable from the artifacts, a *violation* is not. The book's deepest
principle is that truth is maintained **by cryptography and mutual audit, never by
trust** (ch. 5's commit-reveal, App E's audit duties, the whole zero-trust
architecture); *"a hidden game by promise is the one construction that architecture
exists to avoid — a hidden game by wire is the real thing."* Under `reference-v3` the
concealment is **structural**: the rival's position is not withheld by agreement, it is
simply not on the wire to be looked at.

**Balance evidence** (cop repo `docs/evidence/wire-shape-balance.md`, PR #41): on the
shipped constitution with both teams' brain class (heuristic, belief-driven), common
knowledge favors the EVADER — aggregate cop win-rate 45.8% → 26.6%; belief-exploiting
pursuit collapses vs perfectly informed evasion. The shapes differ competitively, not
just architecturally — a pair locking `bookletter-v3` should know this.

## Decision

1. **`reference-v3` is the shape that resolves the contradiction** and the default for
   cross-team play. Ch. 5 is honored with Reveal deferred to the audit boundary.
2. **`bookletter-v3` is a registered, named, documented deviation** — legitimate for a
   pair that locks it by explicit mutual sign-off under the book's agreement clause;
   the sign-off records (a) the deviation from the formal model, (b) the balance
   property above.
3. **The wire-shape lock rides the handshake locked-model doc schema** shared with the
   named scent models (name + params + worked message trace, canonically serialized,
   hashed; refuse loudly only when BOTH peers declare and mismatch). The kit pins the
   doc schema once for both parameter families.
4. **Kit registration** (issue #6): both shapes published with canonical description +
   worked trace; `bookletter-v3` fixtures contributed by Alon/Renat (credited), marked
   PROPOSED until independently reproduced.
5. Per-pair "who adapts" stays a negotiated, deliberate call — never a default imposed
   by either side's shipping schedule. **For THIS pair it is settled: the Alon/Renat
   team chose, on 2026-07-21 and of their own initiative, to build a `reference-v3`
   client, on the reasoning quoted in Context. Our series therefore plays the shape
   that resolves the contradiction, and no deviation sign-off arises for it.** The
   choice is recorded as theirs, with its cost acknowledged: a `reference-v3` client
   is not an emission layer bolted onto a bookletter engine (our pre-call position
   paper undersold this, and their correction is adopted) — hidden moves **fork a
   replicated-lockstep runtime**. Four subsystems change, from their own registration
   spec: (a) the `state_digest` chain stops being a shared pre-action anchor and
   becomes per-side, because the rival's action is not applicable locally until the
   audit; (b) `end_state_digest` loses its convergence meaning and is replaced by the
   mutual audit re-hash; (c) physics verification stops being re-simulation from
   revealed actions and becomes the transmitted-grid check (evidence-grade, since a
   self-reported grid is unauthenticated); (d) capture stops being engine-automatic
   and a real **capture-claim/response flow returns**, because a claimant under Ω_i
   does not know the rival's cell — which is precisely the truth-duty the formal model
   requires. `bookletter-v3` keeps its registration and its re-pin regardless of who
   plays it: the kit's record is about verifiability, not about our fixture list.

6. **Wire-contract robustness — at-least-once delivery is part of the contract, not an
   implementation detail** (raised by Alon/Renat, round 7; **both teams have now
   implemented it and converged on the same construction, round 8**). Both shapes ride
   an at-least-once transport: a push whose ack is lost is retried and arrives twice,
   and two of a peer's pushes can be in flight at once. A conforming receiver therefore:
   - **dedups a redelivered message ON THE COMMIT**, not on `(kind, step)`, and rather
     than treating it as a protocol violation — idempotently, so the game state is
     identical to a single delivery. The commit is the one field a redelivery cannot
     vary, so keying on it keeps a *second, different* commit for a consumed step
     distinguishable from a retry. A `(kind, step)` key collapses the redelivery
     correctly but would also silently swallow a conflicting commit — which is tampering
     evidence, not transport noise. (Construction proposed by us at M7-8; **adopted by
     Alon/Renat's receiver in round 8**, replacing their `(kind, step)` key.)
   - **buffers a bounded number of out-of-order arrivals** and replays them in order,
     raising only when the bound is exceeded;
   - **never lets tolerated traffic renew a turn deadline** — one clock per *expected*
     message, so a stall attempt burns the sender's budget and not the receiver's.

   This is a **mutual protection, not a courtesy**: under App E rule 35 one side's
   avoidable technical loss and the contradictory reports that follow zero **both**
   teams. The governing sentence, in both teams' words: **transport tolerance, no rules
   tolerance** — equivocation (a second, different commit for a step already played) and
   a flood past the buffer bound remain violations. **Both teams demonstrate it in both
   directions at the warm-ups** (duplicate-delivery drill) before anything is counted;
   neither side's claim about its own receiver is taken on description.

   **Observed failure mode in the wild — this clause is not theoretical.** The reference
   implementation performs **no step-continuity check at all**
   (`peer/turn_handler.py:41-48`, read as an oracle): a redelivered turn is appended to
   history and applied a second time — belief diffusion, smell observation, field
   absorption and decay all re-run on one real move. It fails **silently** where a strict
   receiver fails loudly, which is the rule-35 trap in its purest form: **a
   correctly-retrying sender can corrupt a vanilla peer's state with entirely clean
   hands**, the audits then disagree, and both teams lose the points with nobody having
   cheated. Our live drill (cop `docs/evidence/m6-chaos.md` §Live duplicate-delivery
   drill, 2026-07-22) proved the receiving half of this clause over the public edge; the
   reference reading established the hazard it exists to prevent.

## Consequences

- Our peers keep speaking reference-v3 unchanged; demo interop remains a live check.
- **For this pair, no adaptation work fell on us and no deviation sign-off exists to
  write.** The hosting consequence is discharged history: our peers served as their
  live acceptance targets through the warm-ups and rehearsal (2026-07-22..24), their
  client went e2e-green, and the 2026-07-25 series settled on it (generic brain only
  on any standing host remains the rule — tuned weights never deploy there).
- A bookletter-v3 counted game against a co-signing pair is legal and auditable; our
  client would need a per-step-reveal mode + a full-info-tuned brain first (not built;
  M6+ decision).
- **Decision 6 has already changed code on our side.** Auditing our own inbound path
  against it found three live-path defects (a retried push was a technical loss *and* a
  raised exception; no reorder buffer; the turn deadline renewed on unjudged input) plus
  a fourth found while fixing (the deadline was only evaluated on an empty poll, so
  continuous junk meant it was never evaluated at all). Closed at cop M7-8 with six
  permanent chaos drills, then exercised live across the 2026-07-25 series; the formal
  both-directions duplicate drill stays on the next warm-up checklist. Stated here
  because the ADR should record that the clause was load-bearing, not decorative —
  and because it is the honest answer to "was anyone actually exposed?": **we were.**
- The hint layer retains meaning only under reference-v3 (under common knowledge,
  deception has no target) — teams investing in the verbal layer are reference-v3
  stakeholders by construction.
- The kit gains one lock-schema pin serving scent models and wire shapes alike
  (M3-8 prerequisite discharged for both).

## Alternatives considered

- **Register the shapes as symmetric equals** (issue #6 as filed): rejected — an
  Ω_i-led ADR cannot co-equally bless a positions-common-knowledge wire; the issue's
  own text concedes the deviation.
- **Book-letter only** (per-step reveal for everyone): rejected — contradicts the
  mandated formal model, deletes deception/belief (ch. 4/6) and the truth-duty's
  meaning, and shifts balance to the evader on the standard config.
- **Demand every team build a reference-shape client**: rejected — the agreement
  clause makes shape per-pair; the kit's job is to make both shapes verifiable, not to
  legislate one league-wide.

## Addendum (2026-08-01) — the concealment claim, refined by Rounds 15–19

The text above is preserved as finalized on 2026-07-22/27; this addendum records what the
scent-inversion exchange (league Rounds 15–19, 2026-07-27..31) established afterwards,
because the signatures below are collected over the ADR *including* it, and because the
Context's decisive argument claims a property that turned out to be stronger than the
physics allows.

**What changed.** anrbj666's 2026-07-27 memo — independently verified by us before
adoption (224 of 224 consecutive frame pairs invert to exactly one emitter cell, under
BOTH registered scent models, saturated dwells included) — showed that wherever the scent
field crosses the wire under deterministic public physics, **the rival's position IS on
the wire to be looked at**: recoverable by arithmetic from two consecutive honest frames.
The Context's sentence "it is simply not on the wire to be looked at" and the shape
table's "positions genuinely hidden" are therefore overstated **for the scent channel**;
both teams' 2026-07-25 friendly transmitted such fields throughout.

**What survives, refined.** The binary of the original argument (hidden by wire vs hidden
by promise) resolves into three tiers, and the resolution this ADR records is unchanged —
`reference-v3` remains the shape that implements the formal model, and the finding weakens
`bookletter-v3` strictly more (there, positions are common knowledge by design):

1. **Wire-structural — the MOVE channel.** Moves stay sealed until the audit boundary;
   the capture-claim truth-duty keeps its meaning. This tier is exactly as the Context
   describes, and it is the tier that decides between the two registered shapes.
2. **Declared and firewalled — the SCENT channel under a transmitted field.** Both teams
   declare the registered `info_mode:belief` document at negotiate (`info_mode_sha256`,
   both sides `020947da…`; refusal on a comparable mismatch), and each side's frame
   validator is verdict-only by module contract, pinned by a test — the inversion is
   walled out of play, not absent from the wire. In anrbj666's Round-16 words: *an honor
   term with an artifact behind it on both sides.* The co-signed kit SPEC §7 (the
   `transmitted` rely-on reading, the pair-vouching clause, the `{}` and zero-step-final
   conventions) is the registry-level record of this tier; the registered `smell_binding`
   family (PROPOSED) is its future authenticity upgrade.
3. **Bare promise** — the tier the original argument rightly rejects, unchanged.

Where the Context says the `info_mode: "belief"` term is one "the kit reserves" and an
honor term whose violation is not artifact-provable: the enforceability half stands, but
the term is no longer reserved or promise-only — it is registered, mutually declared, and
handshake-refused on mismatch (our M7-25; their commits `554f4e4`/`0cad616`-family). The
finalization note's negotiate-extras list gains `info_mode_sha256` on the same truth
table. Decision 5(c)'s "physics verification … evidence-grade" likewise gains the in-play
frame validity check both teams now ship (whole-frame refusal, three shared exemptions:
empty field, zero-step final, never-judge-the-final) and the `smell_binding` path that
would upgrade its refusals to audit-grade.

The 224/224 measurement is published in the kit anchored to the fence it sizes, at
anrbj666's request — "the measured size of the oracle the `info_mode:belief` declaration
exists to fence … not a capability in use" — and this addendum cites it under the same
framing.

## Signatures

Recorded here verbatim when given; the ADR flips to ACCEPTED (and TODO M7-0 ticks)
only when both lines are filled. **Signatures cover the full text including the
2026-08-01 addendum** — collected that way deliberately, so nobody signs the
pre-refinement concealment claim bare.

- [ ] Imree (copthief-p2p-cop / copthief-p2p-thief) — pending
- [ ] Alon/Renat (anrbj666) — pending; the ask rides the warm-up exchange
