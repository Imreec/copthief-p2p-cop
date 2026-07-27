# M7-19 — The quiet cop: claim-gated physics and the threshold sweep (claim channel, half 2)

> Half 2 of the claim channel specified in `docs/PRD_claims.md`. Half 1 (M7-18) taught our
> thief to read the opponent cop's claims; this half asks what our own cop should announce.
> Generated instrument: `m7-19-claim-sweep.md`, regenerating deterministically from
> `config/claim_sweep.json` by the command in its header.

## 1. What the book actually gates

Scoring table 2 (PDF p.38) defines the capture end-event as the cop landing on the thief's
cell **and declaring** a Capture Claim. So the referee cannot resolve every same-cell
ending once claiming is a choice, and the cost of silence is priced by the book itself:
forfeit that landing. Self-punishing, not illegal.

Only the **landing** form gates. The barrier and imprisonment forms (PRD_engine E-4) come
from a placement the book requires be declared unconditionally, one sentence earlier in the
same paragraph. That asymmetry turns out to decide the whole result (§3).

Implementation: `domain/rules.check_end(claim_standing=...)` gates the landing disjunct
only; `strategy/referee_claims.ClaimPolicy` owns the decision; the referee gates **both**
half-turns on the cop's own most recent claim, because a same-cell ending can arise from
the thief stepping onto the cop — the friendly's **g06** capture was exactly that, riding
the cop's standing claim. **That case is a passing regression test**
(`tests/integration/test_referee_claims.py`), not a caveat: a cop that never declares never
converts a collision, and any threshold high enough would have cost us g06.

## 2. The sweep

`config/claim_sweep.json`: our **deployed book-v1 vector** repeated at six claim settings
against a mixture — one opponent that reads claims, one that ignores them, a trap-naive
camper, and the reference thief. Scored on the cop's **points per game** under the signed
table (capture 20 / survival 5), 32 seeds, `multiplicative_book_v1`.

| cop | threshold | claim-reader | claim-blind | camper | ref-thief | mean |
|---|---|---|---|---|---|---|
| `cop-unmodelled` | historical physics | 7.34 | 9.22 | 9.22 | 9.69 | 8.87 |
| `cop-t0` | **today's emitter** | 7.81 | 9.22 | 9.22 | 9.69 | 8.98 |
| `cop-t0p1` | 0.1 | **9.69** | 9.22 | 9.22 | 9.69 | **9.45** |
| `cop-t0p25` | 0.25 | 9.22 | 9.22 | 9.22 | 9.69 | 9.34 |
| `cop-t0p5` | 0.5 | 9.22 | 9.22 | 9.22 | 9.69 | 9.34 |
| `cop-t2` | never claims | 9.22 | 9.22 | 9.22 | 9.69 | 9.34 |

**A threshold of 0.1 is best-or-tied on every opponent in the mixture** — dominant here, not
a trade-off. It is worth **+1.88 points/game against a claim-reader** (7.81 → 9.69, +24%
over what we ship today) and costs exactly nothing against the other three.

### 2.1 Deployment: one standing setting — a stronger answer than the PRD asked for

The PRD anticipated a per-opponent decision and asked for "per-opponent-type optima, not one
number". **The measurement came back and said one number IS the answer:**

- against a thief that **reads** our claims, 0.1 is the best row (+24%);
- against a thief that **ignores** them, 0.1 **ties** the best row — no cost.

So the posture is a **single standing threshold of 0.1**, not a per-match choice. That is
what matters for a league rather than a duel: we play several teams, we will have no intel
on most of them, and a setting that is best-or-tied everywhere **needs no guess about which
kind of thief shows up** and cannot be wrong-footed by one we have never seen. A
per-opponent policy would have required knowing the answer in advance; this one does not.

This supersedes the PRD's provisional default ("always claim; the burden of proof is on
going quiet"). The burden is met. And note what 0.1 actually is: not silence, but
**declare when a capture is plausible, stay quiet when it is not** — which beats
unconditional claiming against a reader and matches it against everyone else.

### 2.2 Wired into the live emitter, and DEPLOYED on the book-v1 overlay

The sweep would be academic if the policy only existed in the referee, so `peer/turns.py`
now consults it too: `PeerSession.claim_policy` reads `claim_threshold` from
`[strategy.<role>]` with the M7-15 per-scent-model overlay, so the claim policy follows the
physics exactly the way the weight vector does. Absent ⇒ `0.0` ⇒ the historical emitter,
unchanged.

**Deployed** at `[strategy.police.multiplicative_book_v1] claim_threshold = 0.1`
(`game.toml` v1.02). It is **inert under the shipped default model** — the same posture
M7-15/16 used — because book-v1 is the only physics the sweep measured. Verified:

| selected model | resolved `claim_threshold` |
|---|---|
| `subtractive_chebyshev_v1` (shipped default) | absent ⇒ 0.0, historical emitter |
| `multiplicative_book_v1` (what a counted pair locks) | **0.1** |

**Live peer-path validation** (paired `PeerSession`s under the book-v1 config):

- A claim-reading opponent's exact tracking of our cop falls from **0.936** (M7-18's
  always-claim measurement) to **0.433** — the mirror of half 1, measured on the same
  instrument. We now deny most of what we taught our own thief to collect.
- Full local mini-game: `thief_survival` at 35 steps, **mutual audits OK on both sides**,
  replay **Verified OK, 71 records**. The policy is wire-silent — it changes what we
  populate, never the shape of anything.

## 3. Why silence is nearly free — and why that is a fact about our vector, not the game

The claim-blind, camper and ref-thief columns are **identical at every threshold**, including
a cop that never declares at all. That looked like a plumbing bug, so it was checked rather
than assumed. Captures by our deployed vector, loud versus totally silent:

| opponent | loud | silent | landing-form captures |
|---|---|---|---|
| claim-reader | 5 | **9** | −4 (silence *gains*) |
| claim-blind | 9 | 9 | **0** |
| camper | 9 | 9 | **0** |
| ref-thief | 10 | 10 | **0** |

**Our deployed cop wins by walling, never by landing.** It has no landing captures to
forfeit, so the claim channel is pure downside for it: it gives away position and buys
nothing. That is the M7-14 headline (`w_budget = 0` — herding beats chasing an informed
evader) showing up as a protocol consequence.

**The contrast case is committed in the same instrument** rather than left as a footnote.
A plain chasing cop wins *only* by landing:

| cop | claim-blind | camper | ref-thief |
|---|---|---|---|
| `chaser-loud` | 20.00 | 20.00 | 18.59 |
| `chaser-silent` | **5.00** | **5.00** | **5.00** |

Silencing it is catastrophic — 32/32 captures become 0/32. **So a claim policy can never be
deployed independently of the weight vector it runs under.** The two are coupled, and the
sweep's comfortable answer belongs to our herding vector alone.

## 4. Regression posture

`claim_threshold` is absent from every **arena** config, which leaves claims **unmodelled**
there — the historical physics. All four committed arena instruments (`m5-arena.md`,
`m7-14-bookv1-arena.md`, `m7-14-reference-arena.md`, `m7-18-claim-channel-arena.md`)
regenerate **byte-identical** after both the referee change and the emitter change.

The one config that *does* set it is `game.toml`'s book-v1 police overlay (§2.2), which the
arena never reads — arena rosters carry their own options. So the deployment cannot
retroactively move a committed measurement, and the two live on separate rails by
construction.

`simulation.py` crossed the 150-line limit when the claim door was added and was **split**
into `sdk/simulation_referee.RefereeSeriesMixin` — never compressed.

## 5. What is NOT claimed

- **What IS deployed:** `claim_threshold = 0.1` on the **book-v1 police overlay only**
  (§2.2). Under the shipped default scent model the setting is absent and our cop plays
  exactly as before, so nothing changes until a pair locks book-v1 — which is what a
  counted series does. Merging is the deployment decision, as with the M7-15/16 vectors.
- The mixture is a **model** of opponents — four arms, not a proof over all thieves. It
  brackets the axis that matters (reads claims / does not), which is why the dominance
  result is usable, but a thief unlike all four could sit outside the bracket.
- **What the "his thief ignores claims today" fact does and does not mean.** It sets where
  the *gain* comes from, not whether to deploy: against a non-reader 0.1 ties, so nothing is
  risked, and the +24% arrives the moment any opponent reads claims. The EX06 team has
  announced claim-reading for the rematch, and the league has several other teams we know
  nothing about — so the reading arm is the one to plan for, and the non-reading arm is the
  one we must not pay for. 0.1 satisfies both, which is the whole point of sweeping a
  mixture rather than a single opponent.
- The referee models the claim channel faithfully enough to price it, but it is a model: a
  standing claim covers the cop's cell until it moves again, which approximates the peer
  protocol's claim/response exchange rather than reproducing it turn-for-turn.
- The sweep is run under `multiplicative_book_v1` only — the physics the counted series
  locked. It says nothing about reference physics.

## 6. Follow-ups named, not taken

1. **The GA pool should tune against the lag-0 claim-reader** (opened by M7-18), and now
   also **with the claim policy in the loop** — the sweep optimises a threshold against a
   vector that was itself evolved under always-claim.
2. **The in-series adaptive policy** (PRD §5.4b) — claim normally early, detect
   claim-reaction, go quiet. Imree's decision was to judge it after this sweep. **The static
   result argues against building it:** 0.1 is best-or-tied against every opponent type, so
   there is no per-opponent choice left for an adaptive policy to discover, and it would add
   live-path behaviour for no measured gain. Recommend not building it.
3. **The claim-reaction read in postmortem tooling** (PRD §5.4a) — still worth having, but
   its decision value drops for the same reason: with a dominant threshold we no longer need
   to detect whether a given opponent reads claims in order to choose.
