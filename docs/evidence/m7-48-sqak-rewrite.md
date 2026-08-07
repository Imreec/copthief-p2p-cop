# M7-48 — uoh-sqak rebuilt both roles overnight; here is what we face now

> Both their repos are public. This measures the agents they field **as of 2026-08-07
> 19:29Z** (`1ca9d23` thief rewrite, `d07b654` Barrier Law fix), not the ones we played
> in the friendly. Neither side's friendly record survives those two commits.

## 1. What changed on their side, and why it matters to us

**`1ca9d23` — the thief.** They diagnosed the thief we beat 3-0 as *forfeiting*: it ran
to (6,6) in six moves and stood there for seven turns while our cop walked over and
sealed the corner with two barriers. Their fix replaced the objective (room, not
distance), raised `w_exits` 0.3 → 1.0, and — the load-bearing part — **dropped STAY from
the random tie set**, because in the far corner STAY and stepping off score exactly
equal and their brain kept flipping a coin onto "park". They report 42% → 82% survival
against their own strongest cop.

**`d07b654` — the Barrier Law.** Their cop had been taking a step AND a wall in the same
turn (a barrier on 13 of the 14 turns of each of our thief sub-games, while their cop
walked (0,0) → (0,4)). We raised it from the wire; they fixed it inside two hours, at
the one chokepoint every one of their brains passes through, added
`tests/domain/test_barrier_law.py`, and retuned (`min_gain` 1 → 2, `apex_barrier_cost`
0 → 1.0). Their config comment records the same measurement we had made independently:
*"at 0 the cop walls every turn and never closes — it caught nothing at all in 40 seeded
games."*

## 2. Their thief, modelled: `copthief_police/sqak_evader.py`

Their fielded values, not class defaults (`w_exits` 1.0 vs a default of 0.3; `w_risk`
1.0 vs 3.0), their seeded random tie-break, their no-STAY-on-a-tie rule.

**Two findings that change how we should think about them:**

⚠ **Their thief is NOT deterministic.** Their runtime seeds it
`Random(play.seed + sub_game_number)`, so every sub-game draws a different stream. Their
*cop* is deterministic; their thief is not. Their own message projected a series as "one
game per role played three times" — that is right for their cop half and **wrong for
their thief half**, and we should say so.

⚠ **The rewrite fixed PARKING, not corner-seeking.** On an open board their new
objective still rates the far corner highest — `w_dist` and `w_exits` are both 1.0, so
twelve cells of distance beat two lost exits (21.35 against 19.35 from (0,0)). What
changed is that the thief no longer *stands* there, so our cop no longer gets the free
tempo to seal a two-exit cell. The corner is still where it goes; it just keeps moving.
Pinned in `tests/role/test_sqak_evader.py` so it cannot rot.

## 3. Our cop against it

Varied starts (`config/arena_m7_48_sqak_thief.json`, 32 seeds) — their new evader is the
hardest thief in our pool:

| police arm | ref-thief | best2934-thief | **sqak-evader** |
|---|---|---|---|
| `police-brain` (ours) | 30 / 32 | 28 / 32 | **20 / 32** |
| `ref-police` | 10 / 32 | 15 / 32 | 8 / 32 |
| `greedy-manhattan` | 0 / 32 | 13 / 32 | 3 / 32 |

But **counted games only ever play the signed start**, and there the picture is very
different. 64 rng seeds at the signed pair, which is the honest projection because their
thief re-draws its stream every sub-game:

| our cop vs | captures |
|---|---|
| `sqak-evader` (their rewrite) | **56 / 64 = 88%** |
| `best2934-thief` | 64 / 64 = 100% |
| `ref-thief` | 64 / 64 = 100% |

## 4. Their cop against our thief, post-fix

The arm in the sibling repo (`copthief_thief/sqak_apex.py`) was updated to their new
fielded build. Under the Barrier Law their cop stops being a threat to us entirely:

| | signed start ×64 | varied starts ×32 |
|---|---|---|
| our thief (pre-M7-46/47) | 64 / 64 survive | 32 / 32 |
| our thief (shipped) | 64 / 64 survive | 32 / 32 |

Their fix did more for our thief than our own two milestones did — against *them*. The
M7-46/47 work still earns its place against best2934 and against any future waller;
it simply is not what carries this matchup any more.

⚠ Caveat, stated plainly: that arm omits their **L3 endgame solver**, a depth-8
alpha-beta that proves forced captures and played the last two turns of every sub-game we
lost. It cannot be expressed under a move-XOR-wall turn law without a rewrite of the
search. So 64/64 is an upper bound on our thief's comfort, not a guarantee.

## 5. Projection for a counted series (uoh-sqak)

Three sub-games per role from the signed start, book scoring (capture 20/5, survival
5/10):

| | ours | theirs |
|---|---|---|
| our thief × 3 (survive) | 30 | 15 |
| our cop × 3 (88% capture) | ~55 | ~17 |
| **total** | **~85** | **~32** |

Against the friendly's 77-77. The swing is not mostly our doing: roughly two thirds of it
is their Barrier Law fix removing an advantage they should not have had, and the rest is
our thief no longer losing the signed start automatically.

Hold it loosely. Both sides changed both roles in one evening, their thief is stochastic,
and our model of their cop is missing its strongest layer.

## 6. Reproduce

```
uv run pytest tests/role/test_sqak_evader.py
uv run python scripts/arena_run.py --config config/arena_m7_48_sqak_thief.json
```
