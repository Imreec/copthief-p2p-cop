# M10 — vibecode counter-tune: diagnosis and arena evidence (2026-08-10)

> Companion narrative to ADR-0012. Generated tables: `m10-countertune-arena.md`
> (focused matrix, `config/arena_m10_vibecode.json`) and `m9-study-arena.md`
> (full modeled-rival matrix incl. the m10 stacks — the modeled-arm
> non-regression evidence). Signed-start probes reproduce with
> `uv run python scripts/m10_probe.py`; single-game traces with
> `uv run python scripts/m10_trace.py <police> <thief> <seed>`.
> The six source logs are committed under `friendly-vibecode-2026-08-10/`
> (runtime copies live in the git-ignored `logs/`), so the arms rebuild is
> reproducible from the tree alone. They sit in a subfolder deliberately — see
> the dialect note at the bottom.

## What the 30–90 logs showed (verified 2026-08-10, forensics clean)

- **Odd games (our cop):** tracking perfect — belief argmax == their thief's true
  cell 35/35 each game, cop adjacent from ~step 7 — and 0 of 42 walls placed.
  Their thief holds a six-cell counterclockwise loop around board center
  ((3,3)→(4,3)→(4,4)→(3,4)→(2,4)→(2,3)→…, 25+ consecutive steps in every game).
- **Even games (our thief):** three identical corner deaths (steps 13–16), one
  seal wall each — with the cop's exact cell in our belief every single turn,
  because their cop truthfully claims its own cell every turn and our peer loop
  collapses on inbound claims (M7-18, `peer/inbound.py`). The "cheap win" item
  was therefore already implemented live; the gap was arena-side modeling.

## Root causes, measured in-repo

- **Police:** one wall in open center shrinks the thief's reachable region by
  exactly 1 (measured: 25→24 capped, 49→48 uncapped), so the surgery gain
  threshold (4.7893) can never fire centrally, and the M9-1 solver correctly
  proves nothing on an open board. Both wall paths only ever worked near corners
  — which is all the pre-08-10 opponents ever gave us.
- **Thief:** while hunted, capped flight is the ruling score term, and maximum
  distance from an advancing cop is monotonically the far corner. Herding is not
  a bug in their cop; it is the gradient of our own objective.

## The fixes (both config-gated, shipped defaults OFF)

- **Containment walling** (`copthief_police/containment.py`): sub-threshold wall
  investments — close + sharp + cooldown + endgame reserve — on the cell that
  most shrinks the believed region (uncapped), anchored-first so walls accrete
  into cuts. Armed via `contain_enabled = 1.0` (game.toml v1.05 + shipped arena
  entry).
- **Room-first flight** (`doctrine_evader.py`): the ruling flight term caps at
  `flight_floor`; worst-wall room terms govern past it; full capped flight
  demoted to a tie-break. Armed via `room_first = 1.0` (thief repo config after
  sync; shipped arena entry here).

## Signed-start series (the live geometry; seeds 1–8)

```
police-m9  vs vibecode-thief: 0/8 captures, steps=[35×8], walls=[0×8]   ← the live failure, reproduced
police-m10 vs vibecode-thief: 8/8 captures, steps=[22,22,23,20,20,24,23,29], walls=[6,6,8,7,7,6,8,6]
vibecode-police vs doctrine-m9:  0/8 captures (35-step survivals)
vibecode-police vs doctrine-m10: 0/8 captures (35-step survivals)
```

The police-side definition of done holds against a faithful instrument: the
rebuilt thief arm is uncatchable by the wall-less M9 stack (as the real one was,
105 steps / 0 captures / 0 walls) and is converted 8/8 inside 35 by containment.
Over the full 32-scenario suite the same comparison is **3/32 (M9) vs 32/32
(M10)** — see `m10-countertune-arena.md`; their cop arm reproduces one
doctrine-m9 corner death in 32 (live: 3/3 — caveat 1 below) and scores 0/32
against doctrine-m10.

## Modeled-arm non-regression (full study matrix, `m9-study-arena.md`)

- **police-m10 tops the police table 255/256** (5105 pts; m9: 4535). Every M9
  sweep is kept — 32/32 vs best2934-thief, sqak-evader, greedy-manhattan — and
  the one matchup M9 loses (3/32 vs the rebuilt vibecode-thief) becomes 32/32.
  The rebuilt vibecode-thief otherwise TOPS the thief table (174 wins): no other
  cop in the pool — hunter-cop, best2934, greedy — catches it even once.
- **doctrine-m10: 157 wins vs doctrine-m9's 135.** Kept: 32/32 survivals vs
  best2934-police and hunter-cop. Improved: vibecode-police 29→32, police-m7
  10→27, police-m9 0→2. Only police-m10 (our own new cop) still converts it.
- **Champion gate (shipped `config/arena.json`, M10 stack armed): GREEN** —
  police-brain 40/40, doctrine-evader tops the thief table, police DoD floor
  30/32 = 94% (floor 60%) — `m5-arena.md`.

## Honest caveats (do not skip)

1. **The arms are behavioral approximations of three games per role.** The thief
   arm's arc-reversal under intercept is inferred (necessary to match "never
   caught"), and everything off the observed data — broken ring, both arcs
   covered — is extrapolation. The cop arm reproduces their hunt line (verified
   by trace against the g02 track) but not reliably their live corner kill:
   doctrine-m9 dies to the REAL vibecode cop 3/3 and survives the ARM 32/32.
2. **Survival vs the cop arm therefore does not discriminate m9 from m10.** The
   room-first case rests on the pinned live geometry (the g02 herding step,
   refused at its first move — `tests/unit/strategy/test_doctrine_evader_room.py`)
   plus non-regression across the full matrix.
3. **Nothing here is validated live.** The next step after merge is offering
   vibecode a second friendly; counted against them remains a 30–90-class risk
   until that validation. Tuned weights never deploy to the sparring host.

## Fixed en route

- **Live view-model wall-turn crash** (`gui/models/live.py`): the fold ran every
  decision through `apply_move`, and a wall turn's logged move is `BARRIER` —
  latent since M5-2 because no committed fixture game ever placed a wall; the
  armed local minigame surfaced it immediately. Position now holds on wall turns
  (reference semantics); pinned in `test_live_model_wall_turn.py`.
- **Dialect note:** our replay tool marks these six logs TAMPERED on the
  hint-echo check — vibecode's audit records do not echo hints verbatim. The
  settlement contract does not compare hints, so the live Verified OK verdicts
  stand; the logs live in a subfolder so the mirrored replay tests keep globbing
  our own-dialect fixtures.
