# PRD — The capture-claim channel (mechanism PRD, milestones M7-18 / M7-19)

> **Status: DRAFT — gate per CLAUDE.md §2. No build code starts until Imree approves.**
> Parent docs: `docs/PRD.md` FR-6 (strategy), `docs/PLAN.md` §3 (one rules module, two
> modes), `docs/PRD_belief.md` §4 (pipeline order), `docs/PRD_police_brain.md`.
> Sources of truth, in order: **the book** (App E rules 21–22, PDF p.145; the iron-rules
> paragraph and scoring table 2, PDF p.38) > the **conformance kit** (byte shapes —
> untouched by this work) > the **running reference** as oracle (`turn_sender.py`).
> Evidence this PRD feeds: `docs/evidence/m7-18-*.md` (half 1) and `m7-19-*.md` (half 2).
> Predecessor finding: `docs/evidence/m7-13-capture-postmortem.md` named the claim habit as
> the opponent's cheapest counter; M7-14 measured it (claim-reading collapses the plain
> chaser 18→5 of 32). **Every quotation below was re-derived from the PDF for this
> document, not inherited from a prior session's notes.**

## 1. Scope & non-goals

**In scope, in this order:**

- **M7-18 (half 1) — the evader reads claims.** Our thief-side belief consumes the
  opponent cop's `capture_claim` position. Cheap, legal, and sound against every
  opponent; worth building whether or not half 2 ever ships.
- **M7-19 (half 2) — the quiet-cop policy.** Model the claim channel inside the referee,
  then sweep a per-opponent claim threshold on expected **series points**.

**Non-goals:** any change to the wire *shape* (kit CORE — see §6) · any change to the
claim **response** duty (we answer honestly today and that never changes — §2.1) · the
hint/verbal layer · league operations (nothing is sent to the opponent team, and no live
game is played beyond the §6 localhost oracle check).

---

## 2. Legality — re-derived from the book

The extraction carries no inter-word spaces inside Hebrew runs (a property of the PDF's
text layer, see the extraction method in the session notes). Each quotation below gives
the extracted string, a spaced reading, and a translation.

### 2.1 What the book *does* mandate — the response duty

Iron-rules paragraph, **PDF p.38**, heading `חוקי ברזל: תנועה והצהרת אמת`
("Iron rules: movement and truth declaration"):

> `חובתאמתבתפיסה. כאשרהשוטרמכריז Capture Claim מוטלתעלהגנבחובהקריפטוגרפיתלהשיבאמת`
> `(פרוטוקול Capture); ניסיוןלשקרבשלבזהיתגלהבהכרחבשלבביקורתהיומן (audit-log) ויגרורפסילה`
> `מערכתיתמוחלטת.`
>
> *"Truth duty at capture. When the cop declares a Capture Claim, a **cryptographic duty
> falls on the thief** to answer truthfully (Capture protocol); an attempt to lie at this
> stage will necessarily be revealed at the audit-log stage and will cause absolute
> systemic disqualification."*

The duty this sentence creates is the **thief's duty to answer**, conditioned on the cop
having declared. It creates no duty for the cop to declare.

### 2.2 What the book *does* mandate — truthfulness, not frequency

**App E, PDF p.145**, rules 21 and 22:

> 21. `חובה — מכריזיםאמתבלבדבעתתפיסתגנב. סנקציה: פסילהמיידיתבגיןהכחשתמציאות.`
>     *"Obligation — declare only truth when capturing a thief. Sanction: immediate
>     disqualification for denial of reality."*
> 22. `איסור — איןמכריזיםכוזבותעלתפיסה; הכרזתשקרגוררתפסילהמיידית. סנקציה: ציוןאפס`
>     `והפסדטכניללאיכולתערעור.`
>     *"Prohibition — no false declarations of capture; a false declaration causes
>     immediate disqualification. Sanction: zero grade and technical loss with no right of
>     appeal."*

Both rules constrain the **content** of a claim that is made. Neither states how often a
claim must be made, and no rule in App E's 55 does.

### 2.3 The argument from contrast — the book knows how to mandate frequency

This is the load-bearing point, and it is not an argument from silence. **One sentence
later in the same p.38 paragraph**, the book mandates exactly the thing it declined to
mandate for claims:

> `הצהרתמחסוםגלויה. עלהשוטרלהכריזבאמתעל כל הצבתמחסוםועלמיקומההמדויק; איןלהציבמחסום`
> `בהיחבאואסורלשקרלגבימיקומו.`
>
> *"Open barrier declaration. The cop must truthfully declare **every** barrier placement
> and its exact location; **a barrier may not be placed in secret**, and lying about its
> location is forbidden."*

For barriers the book writes both halves — an **every**-placement duty (`כל`) *and* an
explicit prohibition on acting in secret (`בהיחבא`). For capture claims, in the adjacent
sentence of the same paragraph, it writes only the truthfulness half. A drafter who
distinguishes the two obligations one line apart has made a choice, not an omission.

### 2.4 The claim is constitutive of the landing capture

Scoring table 2, **PDF p.38**, the row that defines the capture end-event:

> `תפיסהמוצלחת: השוטרנוחתעלתאהגנב ומכריז Capture Claim`
>
> *"Successful capture: the cop **lands on the thief's cell and declares** a Capture
> Claim."*

So silence is not free, and its cost is priced by the book itself: **a cop that lands on
the thief's cell and does not declare does not score the capture.** That is self-punishing,
not illegal — which is precisely the right shape for a strategy knob, and it is also the
rule the referee model in §5.1 must implement.

Note what is *not* claim-gated: the other two capture forms (`PRD_engine` E-4 — a barrier
on the thief's cell, and imprisonment) are produced by barrier placement, whose declaration
is unconditional per §2.3. **A quiet cop keeps its entire trap game and forfeits only
landing captures** — a fact that matters strategically, because our deployed book-v1 vector
is herding-shaped (`w_budget = 0`; M7-14).

### 2.5 The reference claims every moving turn — that is code, not rule

`reference/Game-P2P-Cop-Chase/src/police_thief/peer/turn_sender.py:45-48`:

```python
capture_claim = (
    list(rt.state.position)
    if rt.role is Role.POLICE and decision.move_type is MoveType.MOVE else None
)
```

Unconditional on every police MOVE turn. Ours mirrors it deliberately —
`peer/turns.py:117-123`, whose comment says so ("the police claims its landing cell on
every MOVING turn — free, automatic"). Under CLAUDE.md's interface-mirror rule we copy the
reference's **interface**; its *policy* is not part of that contract and never was.

### 2.6 Verdict

1. Claiming **truthfully** is mandatory whenever we claim. Unchanged, non-negotiable.
2. Answering the opponent's claim **honestly** is mandatory. Unchanged, non-negotiable.
3. Claim **frequency** is unregulated. A cop may stay silent; the priced consequence is
   forfeiting a landing capture on a turn it stayed silent (§2.4).
4. Reading an opponent's claim is unregulated in every direction — it is data he sent us.

Nothing in §3–§5 depends on a contested reading. Point 3 is the only one that could be
argued, and even a maximally strict reading of rule 21 ("you must declare *when* you
capture") leaves half 1 untouched and costs half 2 only the turns where the cop is in fact
on the thief's cell — which §5.1 already models as forfeiture.

---

## 3. The channel as it stands (verified in the tree, 2026-07-27)

### 3.1 We emit on every moving turn

`peer/turns.py:117-123`, as quoted. A `STAY` or `BARRIER` turn emits `None`.

### 3.2 We discard everything we receive

`peer/inbound.py:84-89` — the whole of our claim consumption:

```python
if message.capture_claim is not None:  # SQ2: answer honestly on our next turn
    session.caught = tuple(message.capture_claim) == tuple(session.position)
    session.pending_claim_response = {...}
```

The claimed **cell** is compared against our own position and then dropped. `session.belief`
— which is exactly a distribution over *where the opponent is* — never sees it. This is the
gap; half 1 is its closure.

### 3.3 The finding: under the current policy the channel is not a leak, it is perfect information

Sharper than the M7-13 postmortem recorded, and derived here from the tree:

- The opponent's start is **signed constitution** (`constitution.board.cop_start`, read at
  `peer/session.py:120-124`) — known to the thief before step 1.
- A claim gives the cop's exact post-move cell — and it is not merely trusted: the same
  message's `commit` seals that position (`seal_turn(position=...)`), so a false claim is
  provable at audit against the reveal. §2.2's sanction makes lying self-destructive.
- **Absence is equally informative**: `capture_claim is None` from a cop running the
  reference policy means the cop did not MOVE (`STAY` or `BARRIER` — and `peer/turns.py:64-71`
  confirms a barrier turn leaves `session.position` unchanged), so the cop is exactly where
  it last was.

Chained from the signed start, a claim-reading thief facing a reference-policy cop knows the
cop's exact cell on **every turn of the game** — not a strong observation, but full
observability of the pursuer. That is what half 1 collects and what half 2 denies.

---

## 4. M7-18 (half 1) — the evader reads claims

### 4.1 Design

One new certainty-grade observation on the filter, and one call site.

- **`domain/belief.BeliefFilter.note_claim(cell: Coord) -> None`** — collapse the
  distribution onto `cell`. This is consistent with the module's existing treatment of
  declared-and-sealed evidence: `note_barrier` already eliminates mass. The never-eliminate
  invariant (SQ3) exists because the **scent grid is unauthenticated**; a claim is a
  plaintext pre-reveal of a value sealed in the same message's commit and sanctioned by
  rules 21–22, so it is in the barrier class, not the scent class.
- **Call site `peer/inbound.py`**, immediately after `predict()` and before
  `update_scent()`. Order rationale: the claim describes the opponent's position *after*
  its move, so it must follow `predict()`; and certainty ahead of probabilistic evidence
  mirrors the pipeline's existing shape (barriers → predict → scent → hint,
  `PRD_belief` §4). The scent and hint updates still run — they are near-inert on a
  degenerate distribution, and `update_scent` must run regardless to maintain
  `_last_scent` for the M7-14 innovation path.
- **Role-blind.** `peer/inbound.py` and `domain/belief.py` are **mirrored core**. Nothing
  in this change names a role: whichever side receives a claim consumes it. In practice
  only the thief receives one, because only a cop emits one — but that asymmetry lives in
  the *emitter*, and the mirrored code must not encode it (gotcha #9).

### 4.2 Deliberately NOT built in half 1: absence-reading

Exploiting §3.3's absence signal requires assuming the opponent claims on every MOVE turn.
Against an opponent who ships half 2 himself, that assumption inverts into a belief
collapsed onto a stale cell. **Present-claim reading is sound against every opponent;
absence-reading is sound only against an unconditional claimer.** Absence-reading is
therefore scoped as a separate opponent-modeling arm — measured in the M7-19 sweep as an
arena arm, config-gated, default **off**, and never deployed without evidence that the
specific opponent claims unconditionally (§5.4 gives the instrument that decides it).

### 4.3 Measurement

Existing instruments, no new machinery: the M7-14/15/16 arena configs. The claim-reading
opponent is already modeled as `truth-lag1` (`strategy/info_feed.LagTruthFeed`), which is a
faithful model of unconditional claiming — a claim describes the cop's cell at the end of
its move and is consumed on the thief's next turn. **Expectation to test, not assert:** the
deployed thief survives 5/16 against the belief-chaser under book-v1 (M7-16); half 1 should
close much of that gap. If it does not, the measurement is the finding and the doc says so.

---

## 5. M7-19 (half 2) — the quiet-cop policy

### 5.1 Referee claim modeling

`strategy/referee.play_referee_game` currently resolves any same-cell ending through
`check_end`, unconditionally. Under §2.4 that is wrong once claiming is a choice.

- **Claim-gate the landing capture on both half-turns.** `check_end`'s same-cell form
  counts only if the cop claimed on **its own most recent turn**. Both half-turns are
  gated on that one standing claim, because a same-cell ending can arise from the thief
  moving onto the cop as well as the cop moving onto the thief — and the friendly's g06
  capture was exactly the second kind, riding the cop's standing claim. The other two
  capture forms stay ungated (§2.4).
- **Honesty requirement, non-negotiable.** The cop's claim decision is
  `decision.barrier is None and police_belief.prob_at(cop) >= claim_threshold` — evaluated
  on the belief as it stands after the thief's move, i.e. "how likely is it that I just
  landed on the thief". At g06 **our belief was wrong at that moment**, so any positive
  threshold suppresses that claim and forfeits that capture. The model must reproduce
  that, not paper over it; a sweep that cannot lose g06 is measuring the wrong thing.
- **Per-roster-entry `claim_threshold`** on police roster entries, default 0.0 (= always
  claim = today's behavior, so every committed arena number stays reproducible).

### 5.2 Claim-conditional thief information

The thief's feed becomes composed rather than fixed: on a turn the cop claimed, a truth
delta at the claimed cell; otherwise the hidden scent feed. **Composition happens in the
referee loop** — it dispatches between two feed objects it already holds. The `BeliefFeed`
Protocol does not change, and neither `ScentFeed` nor `TruthFeed` learns about claims.

### 5.3 Sweep objective — series points, across a mixture

- **Objective = expected series points**, not capture rate, under the counted scoring in
  `config/game.json` (`capture_cop` 20 / `survival_cop` 5 / `survival_thief` 10 /
  `capture_thief` 5). Capture rate is the wrong maximand: silence trades landing captures
  for information denial, and only the points table prices that trade.
- **Robust across an opponent mixture** — claim-reader **and** trap-naive sitter **and**
  reference thief, reusing the M7-15 `GaConfig.opponent_pool` machinery. A threshold tuned
  only against the opponent's announced counter would donate points against everyone else.
- **Report per-opponent-type optima, not one number.** The threshold is private config
  (`game.toml`, never signed, never on the wire) and counted series are one per opponent,
  so deployment is per-match exactly like the M7-15 weight overlays.
- **Default posture: always claim.** Silence only pays against a claim-reading thief; the
  burden of proof is on going quiet, and the sweep must clear it.

### 5.4 Two extra deliverables (measure, don't just build)

- **(a) Claim-reaction read in the postmortem tooling** — does a given opponent's logged
  thief move in a way that correlates with our claimed cells? The friendly logs give the
  baseline: the opponent's current thief demonstrably ignores them. This is the instrument
  that decides whether going quiet against a *specific* opponent is worth anything at all,
  and it also gates §4.2's absence-reading arm.
- **(b) In-series adaptive policy — OPTIONAL, cost/benefit assessed before building.**
  Mirroring the M5-5 hint profiler: claim normally in the early sub-games, detect
  claim-reaction, go quiet for the rest. **If the static per-opponent threshold captures
  most of the value, prefer it and record why** — an adaptive policy adds a live-path
  behavior change for a benefit the static sweep may already have banked.

---

## 6. Wire & conformance posture

- **Kit CORE constraint #13 is not triggered.** Nothing here changes wire format,
  canonicalization, or hashing. `capture_claim` is an existing optional field
  (`wire/turn.py:38,56,75,83-92,112`); half 2 changes only *how often we populate it*, and
  half 1 changes only what we do with a received one. This will be stated in the PR body.
- **Verify-first, before any policy ships (M7-19 blocker).** Claim-less cop turns already
  occur today — `STAY` and `BARRIER` send `null`, and those turns played clean through the
  opponent's client in the 2026-07-25 friendly — but that is inference from logs, not a
  test. Before half 2's policy lands, run claim-less cop turns against the **live reference
  oracle on localhost** (no tunnel, no opponent, no report owed) and confirm the reference
  peer accepts a `MOVE` turn carrying `capture_claim: null`. Verify, don't infer.
- **Response duty untouched.** `peer/inbound.py`'s honest answer is unchanged by both
  halves; half 1 only *adds* a belief update beside it.

## 7. Configuration

| Value | Location | Notes |
|---|---|---|
| `claim_threshold` (police) | `game.toml` `[strategy.police]` + per-model overlays | private, unsigned, never on the wire; default `0.0` = always claim |
| arena roster `claim_threshold` | `config/arena*.json`, `config/ga*.json` police entries | default `0.0` — every committed number stays reproducible |
| absence-reading arm | `game.toml` `[strategy.thief]`, default **off** | §4.2; opponent-modeling, not protocol-sound |

No new quantitative value enters source (constraint #5). Both configs bump `version`.

## 8. Test plan (TDD, RED→GREEN, keyless)

**Half 1 (M7-18)** — mirrored, therefore role-blind:
1. `note_claim` collapses to the claimed cell; `prob_at(cell) == 1.0`; support is that cell.
2. `note_claim` on a cell outside the current support still collapses (the claim is truth;
   our prior was wrong) and the filter stays normalized — no NaN, no empty support.
3. `predict()` after a claim spreads over exactly that cell's legal moves, barriers honored.
4. Inbound integration: a turn carrying `capture_claim` leaves belief argmax **at** the
   claimed cell; the honest `claim_response` is still produced (regression on §6's duty).
5. Inbound integration: a turn with `capture_claim: None` leaves belief behavior byte-identical
   to today (absence is not read — §4.2).
6. Pipeline order pinned: claim applied after `predict`, before `update_scent`; `_last_scent`
   still maintained on a claimed turn.

**Half 2 (M7-19)**, non-mirrored (arena/referee are cop-repo strategy):
7. `claim_threshold=0.0` reproduces every current referee outcome exactly (the pin that
   protects the committed arena tables).
8. A cop that lands on the thief below threshold does **not** end the game; play continues.
9. The g06 shape as a regression fixture: belief wrong at the collision turn ⇒ a positive
   threshold forfeits the capture. Asserted, not avoided.
10. Barrier-form and imprisonment captures are unaffected by any threshold (§2.4).
11. Composed feed: claimed turn ⇒ truth delta at the claimed cell; unclaimed ⇒ scent path.
12. Series-points objective computed from `config/game.json`, pinned against hand-worked
    outcomes for each of the four ending types.

## 9. Acceptance criteria (binary)

- [ ] Every quotation in §2 is reproducible from the PDF by the recorded extraction method.
- [ ] Half 1: `capture_claim` reaches the belief; §8.1–6 green; mirrored tests role-blind;
      thief pytest green **before** the sync commit.
- [ ] Half 1 measured on committed arena configs; the survival delta is reported honestly
      whichever way it goes; evidence doc regenerates deterministically.
- [ ] Half 2: `claim_threshold=0.0` reproduces the committed arena tables exactly.
- [ ] Half 2: the g06 forfeiture case is a passing regression test, not a caveat.
- [ ] Sweep reports **per-opponent-type** optima on series points across the mixture.
- [ ] Localhost reference-oracle check for claim-less turns recorded before any policy ships.
- [ ] Kit CORE vectors untouched; PR body states why #13 is not triggered.
- [ ] Nothing deployed to any sparring config; no league operation performed.

## 10. Open decisions for Imree

1. **Hard collapse vs. high-trust bump (§4.1).** Recommendation: **hard collapse** — the
   claim is sealed-and-sanctioned evidence, the same class as a declared barrier, which the
   filter already treats as certain. The alternative (a tunable `claim_trust` multiplier)
   buys robustness against an opponent who lies — but lying forfeits his entire game under
   rule 22, so the robustness is against a bug, not a strategy. Fallback if the sweep shows
   fragility, not a default.
2. **Whether §5.4(b), the in-series adaptive policy, gets built at all.** Recommendation:
   decide *after* the static sweep reports, and record the reasoning either way.
3. **Deployment posture for half 2** — per-opponent config, as with the M7-15 overlays.
   Merging the deployment PR is the deployment decision, as before; this PRD does not
   pre-authorize it.

## 11. Disclosed limits

- The arena's claim-reading opponent is a **model** (`truth-lag1`) of a claim-reader, not
  the opponent's actual build. It brackets a threat class.
- §3.3's perfect-information conclusion holds against a cop running the *reference* claim
  policy. It is a statement about that policy, not about every possible opponent.
- Half 2's value is entirely contingent on the opponent actually reading claims. §5.4(a) is
  the instrument that measures it, and the honest prior — from the friendly logs — is that
  the opponent's current thief does not.
