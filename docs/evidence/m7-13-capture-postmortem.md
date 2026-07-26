# M7-13 — Capture postmortem: how the g02/g06 cops actually won

**2026-07-26. Analysis of the three police-side games of the 2026-07-25 friendly vs
anrbj666 (`docs/evidence/m7-3-friendly-g02/g04/g06.jsonl`, committed at main `42e1c71`,
all replay Verified OK). Sub-games 2 and 6 are the first cop captures ever recorded
under `multiplicative_book_v1` by either team; sub-game 4 is the one game their thief
survived against our cop — the contrast case. The opponent announced they are building
counters from these same logs, so this is the baseline both rematch preparations start
from.**

## Method

Everything below is re-derived from the committed logs, not from memory of the night:

- **Our cop's positions** come from our own audit records (`audit` event: per-step
  `position`, `move`, cumulative barrier list in `state`).
- **Their thief's positions** are reconstructed from their audited move list
  (`audit_received` → per-step `action.move`, all `verdict: true`), applied from the
  signed start `(3,3)` under the board's top-left axis contract
  (`domain/board.py` deltas).
- **Cross-checks:** the reconstruction ends with cop == thief exactly at the capture
  step in g02/g06; every one of their `claim_response` echoes matches our claimed cell;
  the final response is `caught: true` at the reconstructed meeting cell (g02 `(5,1)`,
  g06 `(3,5)`).
- Belief accuracy is read from our `belief` events (argmax + grid) against the
  reconstructed true thief cell.

The reconstruction script is quoted at the end; it is analysis-only and deliberately
uncommitted (M6 evidence precedent).

## The three police-side games at a glance

| Game | Outcome | Steps | Thief STAYs | Longest STAY streak | Our belief argmax hits | Barriers we placed |
|---|---|---|---|---|---|---|
| g02 | **cop_capture** | 31 | 14/32 | **10** (steps 22–31, at `(5,1)`) | 5/32 | 7 |
| g04 | thief_survival | 34 | 14/35 | 5 (steps 30–34) | 1/35 | 8 |
| g06 | **cop_capture** | 11 | 6/12 | 4 | 1/12 | 2 |

For symmetry, our own thief's games (g01/g03/g05, all survived): 20, 17, 19 STAYs with
streaks of 14, 10, 12 — **our thief camps harder than his and survived every game.**
Camping is not inherently fatal; it is fatal against a cop that converts the resulting
scent beacon into an interception. Theirs never did; ours did twice. That asymmetry —
not a thief-side blunder unique to them — is the actual edge on display.

## g02 (31 steps): the camper becomes a beacon

The thief toured the south and east edges for 21 steps while our cop walked the scent
mass and spent its barrier budget shaping the board (`(5,4)`, `(4,5)`, `(3,6)` sealing
the south-east, later `(2,3)`, `(1,3)` cutting the northern corridor, finally `(3,1)`,
`(4,2)` narrowing the south-west). From step 22 the thief sat at `(5,1)` and never
moved again — ten consecutive STAYs.

Under `multiplicative_book_v1` a stationary thief pumps its own cell toward the 0.9
clamp every turn: a fixed, self-refreshing peak. Our belief argmax — noisy all game
(see below) — locked onto `(5,1)` at step 29 after seven turns of pumping, and the cop
marched `(3,3) → (4,3) → (5,3) → (5,2) → (5,1)`, claim-testing each cell on the way
(their own `claim_response` chain records the approach), capture on step 31.

**The capture cell was not sealed.** At the end all four neighbors of `(5,1)` —
`(4,1)`, `(6,1)`, `(5,0)`, `(5,2)` — were open. The barriers constrained the region
but the thief was free to run every single turn and chose not to: with no model of the
cop's position there was nothing telling it to. This is exactly the opponent's own
diagnosis ("trap-awareness currently exact-info-gated") — but note the mechanism that
actually killed it was **camping-under-scent-physics**, with the barriers only
shrinking the space it would have had to flee into.

## g06 (11 steps): walking into the cop

Different mechanism entirely. The thief went north-east early (`(3,3) → (1,5)` by step
5), camped four turns, then walked `S, S` — directly into the cop's approach path. Our
cop moved `(3,4) → (3,5)` as the thief moved `(2,5) → (3,5)`: a head-on collision on
step 11. Our belief argmax said `(1,5)` (his abandoned campsite) at the moment of
capture — the cop was steering toward the stale scent mass and the thief **delivered
itself into the pursuit lane**. A thief with any estimate of the cop's likely position
does not descend into the one occupied column; a thief without one cannot know better.

## g04 (34 steps): the moving thief survived

The contrast case. Their thief kept relocating in long arcs — south-west corner, up
the west edge, across the top row, down the east side — and its longest STAY streak
before the endgame was 2. The cop chased an aged trail the whole game (argmax hit
1/35, distance-to-thief oscillating 2–4) and never got a stable fix. Even so, the
final camp at `(5,5)` (steps 30–34) nearly lost it the game: our cop closed to
Chebyshev distance 1 by step 33 and placed its last two barriers beside the camp —
the thief survived because the 35-step cap arrived first, roughly two steps ahead of
the interception. **His thief survived g04 by clock, not by evasion.**

## Cross-cutting findings

1. **The live logs confirm the M3-8 argmax finding at full strength** (cf.
   `docs/evidence/m3-belief-eval.md`): argmax hit-rates 5/32, 1/35, 1/12 under
   book-v1 saturation. But argmax *error distance* stayed small (Chebyshev ≤ 2 on the
   large majority of steps): the belief mass sits near the truth with an unstable
   peak. The cop's pursuit runs on the mass, not the peak, which is why it closes
   distance anyway — and why the argmax metric alone undersells the filter.
2. **Both captures are failures of opponent-position modeling, not of trap-dodging.**
   g02: voluntary terminal camping with all exits open. g06: voluntary descent into
   the pursuit lane. A "belief-native wall forecast" (his announced fix (a)) would
   have changed neither game by itself; a belief over the *cop* changes both. Our
   arena counter-model must therefore give the evader cop-tracking first and
   trap-avoidance second, or we will tune against the wrong fix.
3. **Stationarity is the largest single leak under book-v1 — for both teams.** A
   camper is a self-refreshing beacon under the multiplicative model. Our own thief
   camps *more* than his (streaks up to 14) and got away with it only because his cop
   never exploited the beacon. If he gives his cop the same beacon-following endgame
   ours has, our thief's current habit becomes the same losing pattern — the sibling
   retune must price this.
4. **The hint channel contributed nothing to the captures.** End-of-game profile:
   `hints 32, lies 0, motion_prior {None: 1.0}`, i.e. our parser extracted no
   directional content from his phrase-book, so belief updates rode scent alone. (His
   hints were in fact almost all honest against his audited moves; the one
   inconsistency — g02 step 17, "Chasing sunrise eastward" against an audited `W` —
   was invisible to us for the same parser reason.) Two consequences: our capture
   edge does not depend on reading him, and his announced counter-deception layer
   will be aiming at a channel we currently do not consume. The cheap robustness win
   on our side is making sure that stays true — belief must never weight an
   *unparsed* hint.
5. **The claim channel is pure downside for the cop as we play it.** Our cop
   claim-tests nearly every cell it enters (22 claims in g02); each `caught: false`
   response tells the thief, for free, exactly where the cop is — a full position
   feed to any evader that reads it. His current evader demonstrably does not read
   it: in g02 it sat at `(5,1)` while our claims marched `(5,3) → (5,2)` straight at
   it (steps 29–30) and never moved. **A
   belief-native evader that consumes claim coordinates gets our cop's position
   almost every turn without any scent inference.** Whether to keep claiming this
   aggressively is a strategy decision the arena should measure — it is likely the
   single cheapest counter available to him, and the single cheapest thing for us to
   stop volunteering.

## What this feeds

- **M7-14 (arena under book-v1 + trap-aware evader):** the opponent model must
  include, in priority order: (a) a belief over the cop's position built from the
  cop's scent field and *claim coordinates* (finding 5 — his cheapest counter), (b)
  an anti-camping term when the believed cop is near (findings 2–3), (c)
  barrier/mobility awareness (his announced fix). The measurement question is whether
  our champion cop's capture rate survives each layer.
- **Sibling retune:** our thief's camping habit (streaks to 14) is currently unpriced
  risk (finding 3).
- **Negotiation calculus:** the two captures already moved book-v1 from "structurally
  cop-proof" to "cop-viable"; this postmortem sharpens it — the viability came from
  opponent-modeling gaps, so the scent-model term's value depends on how much of his
  announced fix lands before the counted series. Recorded here so the calculus is
  argued from mechanism, not from the 75–35 headline.

## Reconstruction script (analysis-only, uncommitted)

```python
"""Reconstruct the g02/g06 friendly captures from the committed cop-side logs.

Input: docs/evidence/m7-3-friendly-g02.jsonl / g06.jsonl (cop-side, audit_received
carries the thief's audited move list). Output: per-step table of cop pos, thief pos,
distances, belief argmax hit, barriers, claims - ASCII only (ops gotcha #3).
"""

import json
from pathlib import Path

REPO = Path(r"d:\HaifaUni\AI Agent Orchestration\FinalProject\impl\copthief-p2p-cop")
DELTAS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1), "STAY": (0, 0)}
COP_START = (0, 0)
THIEF_START = (3, 3)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def analyze(name):
    recs = load(REPO / "docs" / "evidence" / f"m7-3-friendly-{name}.jsonl")
    audit = next(r for r in recs if r.get("event") == "audit")["payload"]["records"]
    cop_moves = {}
    cop_pos = {}
    for rec in audit:
        p = rec["payload"]
        if "move" in p and "position" in p:
            cop_moves[p["step"]] = p["move"]
            cop_pos[p["step"]] = tuple(p["position"])
    aud_recv = next(r for r in recs if r.get("event") == "audit_received")["raw"]["records"]
    thief_moves = {}
    for rec in aud_recv:
        p = rec["payload"]
        if "action" in p and p.get("role") == "thief":
            thief_moves[p["step"]] = p["action"]["move"]
    our_turns = {
        r["message"]["step"]: r["message"] for r in recs if r.get("event") == "turn"
    }
    their_turns = {
        r["raw"]["step"]: r["raw"] for r in recs if r.get("event") == "turn_received"
    }
    beliefs = {
        r["payload"]["step"]: r["payload"] for r in recs if r.get("event") == "belief"
    }
    decisions = {
        r["payload"]["step"]: r["payload"] for r in recs if r.get("event") == "decision"
    }
    result = next(r for r in recs if r.get("event") == "peer_result")["payload"]

    print("=" * 78)
    print(f"{name}: outcome={result['outcome']} steps={result['steps']} audit_ok={result['audit_ok']}")
    print("=" * 78)

    cop, thief = COP_START, THIEF_START
    steps = sorted(set(cop_moves) | set(thief_moves))
    hits = 0
    n_beliefs = 0
    print(f"{'st':>3} {'cop_mv':>6} {'cop':>7} {'thief_mv':>8} {'thief':>7} "
          f"{'cheb':>4} {'manh':>4} {'argmax':>7} {'hit':>3} {'d(bel,thief)':>12} "
          f"{'barrier':>8} {'claim':>7} {'intent':>7}")
    for s in steps:
        cm = cop_moves.get(s, "-")
        tm = thief_moves.get(s, "-")
        cop = cop_pos.get(s, cop)
        if tm in DELTAS:
            thief = (thief[0] + DELTAS[tm][0], thief[1] + DELTAS[tm][1])
        cheb = max(abs(cop[0] - thief[0]), abs(cop[1] - thief[1]))
        manh = abs(cop[0] - thief[0]) + abs(cop[1] - thief[1])
        bel = beliefs.get(s)
        argmax = hit = dbt = "-"
        if bel:
            n_beliefs += 1
            am = tuple(int(x) for x in bel["argmax"].split(","))
            argmax = f"{am[0]},{am[1]}"
            hit = "Y" if am == thief else "."
            if am == thief:
                hits += 1
            dbt = max(abs(am[0] - thief[0]), abs(am[1] - thief[1]))
        turn = our_turns.get(s, {})
        barrier = turn.get("barrier_placed")
        barrier = f"{barrier[0]},{barrier[1]}" if barrier else "-"
        claim = turn.get("capture_claim")
        claim = f"{claim[0]},{claim[1]}" if claim else "-"
        intent = decisions.get(s, {}).get("intent", "-")
        cop_s = f"{cop[0]},{cop[1]}"
        thief_s = f"{thief[0]},{thief[1]}"
        print(f"{s:>3} {cm:>7} {cop_s:>6} {tm:>8} {thief_s:>6} "
              f"{cheb:>4} {manh:>4} {argmax:>7} {hit:>3} {str(dbt):>12} "
              f"{barrier:>8} {claim:>7} {intent:>7}")
    print(f"\nbelief argmax hit-rate: {hits}/{n_beliefs}")
    print(f"final: cop={cop} thief={thief} same_cell={cop == thief}")
    resp = {s: t.get("claim_response") for s, t in their_turns.items() if t.get("claim_response") is not None}
    if resp:
        print(f"thief claim_responses: {resp}")
    print("\nthief hints (deception layer):")
    for s in steps[:40]:
        t = their_turns.get(s)
        if t:
            print(f"  {s:>3}: {t.get('hint', '')!r}")


for game in ("g02", "g04", "g06"):
    analyze(game)
    print()
```

> Traces below stop at our cop's last move. The belief denominators in the summary
> table (32/35/12) count every logged `belief` event, including the one recorded
> after the final step — g02's fifth argmax hit is that post-capture event.

## Per-step trace: g02 (capture, 31 steps)

```
 st  cop_mv    cop thief_mv  thief cheb manh  argmax hit d(bel,thief)  barrier   claim
  1       E    0,1     STAY    3,3    3    5     3,3   Y            0        -     0,1
  2       E    0,2        S    4,3    4    5     3,3   .            1        -     0,2
  3       S    1,2        S    5,3    4    5     3,3   .            2        -     1,2
  4       S    2,2        E    5,4    3    5     3,3   .            2        -     2,2
  5       S    3,2        E    5,5    3    5     4,3   .            2        -     3,2
  6       E    3,3     STAY    5,5    2    4     4,4   .            1        -     3,3
  7       S    4,3        E    5,6    3    4     4,4   .            2        -     4,3
  8       E    4,4     STAY    5,6    2    3     5,4   .            2        -     4,4
  9 BARRIER    4,4        N    4,6    2    2     5,4   .            2      5,4       -
 10 BARRIER    4,4        N    3,6    2    3     4,5   .            1      4,5       -
 11       N    3,4        N    2,6    2    3     3,4   .            2        -     3,4
 12       E    3,5        N    1,6    2    3     3,6   .            2        -     3,5
 13 BARRIER    3,5        W    1,5    2    2     3,6   .            2      3,6       -
 14       N    2,5        W    1,4    1    2     2,5   .            1        -     2,5
 15    STAY    2,5     STAY    1,4    1    2     2,5   .            1        -       -
 16    STAY    2,5        W    1,3    2    3     2,5   .            2        -       -
 17       W    2,4        W    1,2    2    3     2,4   .            2        -     2,4
 18 BARRIER    2,4        W    1,1    3    4     2,3   .            2      2,3       -
 19       N    1,4        S    2,1    3    4     1,3   .            2        -     1,4
 20 BARRIER    1,4        S    3,1    3    5     1,2   .            2      1,3       -
 21       S    2,4        S    4,1    3    5     2,2   .            2        -     2,4
 22       S    3,4        S    5,1    3    5     3,2   .            2        -     3,4
 23       W    3,3     STAY    5,1    2    4     3,2   .            2        -     3,3
 24       W    3,2     STAY    5,1    2    3     3,1   .            2        -     3,2
 25 BARRIER    3,2     STAY    5,1    2    3     3,1   .            2      3,1       -
 26 BARRIER    3,2     STAY    5,1    2    3     4,2   .            1      4,2       -
 27       E    3,3     STAY    5,1    2    4     4,0   .            1        -     3,3
 28       S    4,3     STAY    5,1    2    3     4,0   .            1        -     4,3
 29       S    5,3     STAY    5,1    2    2     5,1   Y            0        -     5,3
 30       W    5,2     STAY    5,1    1    1     5,1   Y            0        -     5,2
 31       W    5,1     STAY    5,1    0    0     5,1   Y            0        -     5,1
```

## Per-step trace: g06 (capture, 11 steps)

```
 st  cop_mv    cop thief_mv  thief cheb manh  argmax hit d(bel,thief)  barrier   claim
  1       E    0,1     STAY    3,3    3    5     3,3   Y            0        -     0,1
  2       E    0,2        N    2,3    2    3     3,3   .            1        -     0,2
  3       S    1,2        N    1,3    1    1     3,3   .            2        -     1,2
  4       S    2,2        E    1,4    2    3     3,3   .            2        -     2,2
  5       E    2,3        E    1,5    2    3     2,3   .            2        -     2,3
  6 BARRIER    2,3     STAY    1,5    2    3     2,4   .            1      2,4       -
  7 BARRIER    2,3     STAY    1,5    2    3     1,3   .            2      1,3       -
  8    STAY    2,3     STAY    1,5    2    3     0,4   .            1        -       -
  9       S    3,3     STAY    1,5    2    4     0,4   .            1        -     3,3
 10       E    3,4        S    2,5    1    2     1,5   .            1        -     3,4
 11       E    3,5        S    3,5    0    0     1,5   .            2        -     3,5
```

## Per-step trace: g04 (survival, 34 steps — the contrast case)

```
 st  cop_mv    cop thief_mv  thief cheb manh  argmax hit d(bel,thief)  barrier   claim
  1       E    0,1     STAY    3,3    3    5     3,3   Y            0        -     0,1
  2       E    0,2        S    4,3    4    5     3,3   .            1        -     0,2
  3       S    1,2        S    5,3    4    5     3,3   .            2        -     1,2
  4       S    2,2        W    5,2    3    3     3,3   .            2        -     2,2
  5       S    3,2        W    5,1    2    3     4,3   .            2        -     3,2
  6 BARRIER    3,2     STAY    5,1    2    3     4,2   .            1      4,2       -
  7       E    3,3     STAY    5,1    2    4     5,3   .            2        -     3,3
  8       S    4,3     STAY    5,1    2    3     5,3   .            2        -     4,3
  9       S    5,3     STAY    5,1    2    2     5,3   .            2        -     5,3
 10 BARRIER    5,3        N    4,1    2    3     5,2   .            1      5,2       -
 11    STAY    5,3        W    4,0    3    4     6,1   .            2        -       -
 12       N    4,3        N    3,0    3    4     5,1   .            2        -     4,3
 13    STAY    4,3        N    2,0    3    5     4,1   .            2        -       -
 14       N    3,3        E    2,1    2    3     4,0   .            2        -     3,3
 15       W    3,2        N    1,1    2    3     3,1   .            2        -     3,2
 16       W    3,1        E    1,2    2    3     3,1   .            2        -     3,1
 17 BARRIER    3,1     STAY    1,2    2    3     2,1   .            1      2,1       -
 18 BARRIER    3,1     STAY    1,2    2    3     3,2   .            2      3,2       -
 19       W    3,0        N    0,2    3    5     1,0   .            2        -     3,0
 20       N    2,0     STAY    0,2    2    4     1,1   .            1        -     2,0
 21       N    1,0     STAY    0,2    2    3     1,1   .            1        -     1,0
 22       E    1,1        E    0,3    2    3     0,1   .            2        -     1,1
 23       E    1,2        E    0,4    2    3     1,2   .            2        -     1,2
 24    STAY    1,2        S    1,4    2    2     1,2   .            2        -       -
 25 BARRIER    1,2        E    1,5    3    3     1,3   .            2      1,3       -
 26       N    0,2        S    2,5    3    5     0,4   .            2        -     0,2
 27       E    0,3        S    3,5    3    5     1,4   .            2        -     0,3
 28       E    0,4        S    4,5    4    5     2,4   .            2        -     0,4
 29       S    1,4        S    5,5    4    5     3,5   .            2        -     1,4
 30       S    2,4     STAY    5,5    3    4     3,5   .            2        -     2,4
 31       S    3,4     STAY    5,5    2    3     3,5   .            2        -     3,4
 32 BARRIER    3,4     STAY    5,5    2    3     3,5   .            2      3,5       -
 33       S    4,4     STAY    5,5    1    2     4,6   .            1        -     4,4
 34 BARRIER    4,4     STAY    5,5    1    2     4,6   .            1      4,5       -
```
