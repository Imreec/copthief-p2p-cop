# M11 — robust brains: measurement narrative (2026-08-11)

> Companion to ADR-0013 and `m11-redteam.md`. The generated matrix table is
> `m11-arena.md` (`config/arena_m11.json`); signed-start probes reproduce with
> `uv run python scripts/m11_probe.py`, variant sweeps with
> `scripts/m11_experiment.py`, the nis-yar1 log study with
> `scripts/m11_nisyar1_study.py`. The six 08-11 source logs are committed under
> `friendly-nis-yar1-2026-08-11/` so every arm and pin rebuilds from the tree.

## The target

M10's own matrix named the hole: police-m10 converts doctrine-m10 **32/32** —
and the league confirmed it live the same day this was built: nis-yar1's cop
(second independent cage/seal implementation, commit a0ba98d1) captured our
fielded M10 evader at **step 13 in all three thief games** of the 60–80
friendly. The M11 thesis: stop patching per-opponent; make the evader survive
the cage CLASS and the cop convert what it could not.

## Thief: the iteration trail vs police-m10 (signed starts, seeds 1–8)

| variant | survivals | notes |
|---|---|---|
| doctrine-m10 (baseline) | 0/8 | captures at 11–17 steps, 3–4 walls — a LOCAL trap, not a 14-wall cage |
| + tempo lift (session hypothesis) | 0/8 | walls forced up slightly; deaths unchanged — lift relocation is rim-ward |
| + banked floor (+1/wall permanent) | 0/8 | null; the floor itself is not the binding constraint |
| + low floor (2) + k-forecast (orbit, no margin) | 1/8 | first survival; remaining deaths: rim-drift via the flight TIE-BREAK when all room terms saturate (seed-1 trace: a row-5 walk into (6,0)) |
| **orbit: floor 2 + margin cap 2 + k3/reach2** | **4/8** | survivals force 8–9 walls; the shipped armed shape |
| ablations of the shipped shape | k=0 → 1/8 · k=2 → 3/8 · reach=1 → 1/8 · +lift → 0/8 · stay-cap 1 → 2/8 · stay-cap 0 → 1/8 | k3/reach2 carries the weight; every "discipline" tweak on top loses survivals |

Full 32-scenario suite: doctrine-m11 vs police-m10 **5/32 survivals (from
0/32), forced walls 6–8 (from 3–4)**. Two mechanisms were built, measured
against this table, and REMOVED (tempo lift, banked floor) — the session
prompt's tempo-punish hypothesis is refuted in its cap-lifting form: the tempo
profit is real but is collected by orbiting (the builder converts less per
wall), not by fleeing far.

## Thief: the nis-yar1 kill class

Their cop's kill (g02/g04/g06, identical): herd our evader down its own flight
line — they chase the SCENT WAKE, a lag-1 signal, which is what makes the herd
emerge — pin at Chebyshev 1 when the prey's escapes ≤ 2 (three logged STAY
turns at (5,5) against our (6,6)), then seal both escapes ([5,6],[6,5]) for the
rule-47 capture. Modeled as the vibecode-cop class + `pin_enabled` on a
`truth-lag1` feed (`nisyar1-police`):

```
nisyar1-police vs doctrine-m10: 3/8 kills, 1-2 seal walls   <- the kill class, reproduced
nisyar1-police vs doctrine-m11: 0/8 kills, 0 walls placed   <- no seal opportunity ever conceded
```

The decisive live moment is pinned as a unit test
(`test_the_nisyar1_g02_corner_step_is_refused`): at (6,5) with their cop known
at (5,4), the M10 doctrine stepped E into the (6,6) two-wall pocket; the k-wall
forecast prices that pocket at region 1 and refuses.

## Cop: the g01 camper stall (the dropped police game)

`scripts/m11_nisyar1_study.py g01`: our tracking was perfect (argmax == their
cell 35/35), our cop placed (1,4) directly between itself at (2,4) and their
thief perched at (0,4) — and then STOOD STILL 19 turns with 11 walls unspent.
Measured root causes and cures (both pinned in
`tests/role/test_police_path_distance.py`):

- containment refused at BFS gap 4 > `contain_range` 3 (its own wall made the
  gap 4). **`contain_range 4.0`** resumes investment in the logged geometry.
- the expectimax leaf prices distance as Manhattan, so the own-wall detour
  reads as "every move is worse" — a local minimum the 2-ply horizon froze in
  (STAY −39 vs −42 for every move, measured). **`path_distance 1.0`** re-prices
  the leaf wall-aware; open-board decisions provably unchanged.

Their thief is modeled as `nisyar1-thief` (flee-then-perch; wake inferred —
ONE game of evidence, played against our frozen cop). Both M10 and M11 cops
convert the arm 8/8 on signed starts; the arm validates camper-conversion
generally, while the stall itself is pinned at the exact logged geometry.

## Claim gate (M11-2)

`note_claim`'s unconditional collapse cited a sanction (rules 21–22) that no
audit path enforces — verified by reading settlement/audit/replay and by the
lived wire (vibecode: 42/43 speculative claims, all audits Verified OK;
nis-yar1: every-turn own-cell claims, same). The gate refuses kinematically
impossible claims via a physics-only `MotionEnvelope`; for every truthful
claimer it is a no-op by construction (their true cell is always inside its own
envelope — both live cage opponents' claim streams pass untouched). Pinned at
the domain and peer seams (`test_belief_claim.py`,
`test_an_impossible_claim_no_longer_hijacks_the_receivers_belief`).

## Honest caveats (do not skip)

1. **Everything here is offline.** The signed-start and matrix numbers are
   predictions until a live game validates them; the M10 lesson (three fidelity
   iterations) applies in full.
2. **The nis-yar1 arms are behavioral approximations**: the cop arm's pin and
   lag-1 feed are inferences that reproduce the kill CLASS (3/8 offline vs 3/3
   live — the live rate is hotter than the arm's); the thief arm rests on one
   game against a frozen cop.
3. **5/32 vs our own police-m10/11 is a real number, not a solved problem.**
   Our own builder cop remains the strongest thief-killer in the pool; the
   self-play loop (deferred past the 08-11 counted window) is the standing
   instrument for pushing this further.
