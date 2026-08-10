# ADR-0012 — M10 counter-tune: containment walling, room-first flight

## Status

Proposed (built on `worktree-m10-vibecode-countertune`, 2026-08-10; Imree's merge of the
M10 PR is the approval). Extends ADR-0011; changes no wire bytes, no negotiated term, no
signed value. Strategy layer only.

## Context

The uncounted friendly against vibecode (2026-08-10) was a 30–90, 0–6 sweep with both M9
brains live (repo `01248f8`, config v1.04). Interop was perfect (6/6 settled, all audits
Verified OK) and the forensic pass found no cheating — their play was simply better shaped
than ours in both roles. The logs (`logs/imreeyal-vs-vibecode_g0*.jsonl`) carry their full
audit-revealed tracks, and three findings fall out of them:

1. **Police:** belief argmax matched their thief's true cell 35/35 per game and the cop was
   adjacent from ~step 7 — yet the M9 stack placed ZERO of its 42 available walls across
   three games. Measured root cause: their thief holds a six-cell central loop, and in open
   center one wall shrinks the reachable region by exactly 1, so the surgery gain threshold
   (4.79) can never fire; the M9-1 solver correctly proves nothing on an open board (one
   pursuer without walls cannot force capture on a cycle). Both wall paths were built and
   validated against corner-shaped play; against a central evader the quota is dead weight.
2. **Thief:** the doctrine evader was herded into a corner and sealed in all three even
   games (identical deaths at steps 13–16) — WITH the cop's exact cell known every turn,
   because their cop truthfully claims its own cell on every turn and our peer loop has
   collapsed the belief on inbound claims since M7-18. Root cause is the score ordering:
   while hunted, capped flight rules, and maximum distance from an advancing cop is
   monotonically the far corner. The counter-shape was on display in the same logs — their
   thief's central oscillation survived exactly our cop class.
3. **Arms:** the pre-08-10 vibecode arena arms (modeled from anrbj666's 2026-08 series)
   describe a team that no longer exists — corner-oscillator thief, claim-less wall-blind
   cop. The M9 study table showed our cop beating that model 32/32 while the real one beat
   us 0–6; a stale arm is worse than no arm.

## Decision

Three mechanisms, all config-gated with shipped defaults OFF (the M9 decision stream is
byte-identical until config arms them), plus the arms rebuild:

1. **M10-1 containment walling** (`copthief_police/containment.py`, knobs in
   `features.py`): when the surgery threshold is silent, the belief top cell is sharp
   (`contain_mass`) and close (`contain_range`), quota sits above an endgame reserve and a
   cooldown has elapsed, invest the reachable wall that most shrinks the believed region
   (uncapped BFS — the surgery cap saturates in open space), tie-broken toward anchored
   cells (rim or existing walls) so investments accrete into cuts. The board shrinks until
   the M9-1 solver can finish. Armed live via `game.toml [strategy.police]
   contain_enabled = 1.0` (v1.05) and the shipped arena entry.
2. **M10-2 room-first flight** (`doctrine_evader.py` `room_first` + `flight_floor`): the
   ruling flight term is capped at a small safety floor and the worst-wall room terms
   (escapes, region) govern past it; full capped flight is demoted to a tie-break, not
   deleted. The evader keeps barely-safe distance and open ground — the central-orbit
   shape — instead of being herded to the rim. Armed in the thief repo's
   `[strategy.thief]` after the mirror sync.
3. **M10-3 arms rebuild** (`vibecode_thief.py` / `vibecode_cop.py`): modeled from our own
   08-10 logs. Thief: the six-cell counterclockwise center loop, the diagonal-cut STAY,
   the endgame vertical sprint, never a barrier; one ingredient is inferred, not observed
   (arc reversal under intercept — the minimal mechanism consistent with 105 steps and 0
   captures). Cop: scripted S,S,S opening, wall-aware BFS chase, exactly one seal wall on
   a penned ≤2-escape cell, every-turn claims modeled at the roster level
   (`claim_threshold: 0.0`). Both arms run `sharp199`, matching their demonstrated
   tracking. The measurement instrument is `config/arena_m10_vibecode.json` +
   `scripts/m10_probe.py` (signed-start series — the live geometry).

**Measured:** at the signed starts (the live geometry) the M9 police stack scores 0/8
against the rebuilt thief with zero walls — the live failure reproduced — while the M10
stack scores 8/8 inside 35 steps investing 6–8 walls; over the full 32-scenario suite the
same comparison is 3/32 vs 32/32 (`docs/evidence/m10-countertune-arena.md`). The claim channel finding closed as
already-implemented: the live loop reads claims (M7-18); what changed is the arena now
models the sender side so tuning happens under live information conditions.

## Consequences

- The live-loss geometries are pinned as unit tests: the g02 herding step (room-first
  refuses E at (3,5) with the cop known at (3,3)), the g01 containment fire (a wall placed
  where M9 demonstrably placed none), and the rebuilt arms' logged behaviors.
- `game.toml` → v1.05 (`contain_enabled`). Thief repo: `[strategy.thief] room_first = 1.0`
  + `flight_floor` by hand after the core mirror sync — config never travels with the
  mirror (the 3rd-instance lesson).
- **Honest caveat:** the rebuilt arms are behavioral approximations. The thief arm's
  off-ring and broken-ring behavior is extrapolated; the cop arm reproduces their hunt
  line but not reliably their live corner kill (their belief layer is unseen). Survival
  against the cop arm therefore does not discriminate m9 from m10 — the room-first case
  rests on the pinned live geometry plus non-regression. Nothing here is validated live
  until a second vibecode friendly is played; counted against them remains a
  30–90-class risk until that validation.
- The genetic layer can later tune the containment knobs; this ADR ships hand-picked
  values measured in the focused arena.

## Alternatives

- **Retune weights only (no new mechanism):** rejected — no `barrier_gain_threshold` value
  fixes a gain signal that is structurally ~1 in open center; lowering it to ~1 makes the
  cop wall constantly everywhere (measured in the focused runs as strictly worse).
- **Deeper solver horizon instead of containment:** rejected — the failure is not depth:
  on an open board no forcing line exists at any depth the node budget can afford; walls
  must exist before the proof can.
- **Corner-avoidance penalty bolted onto flight:** rejected in favor of room-first — the
  forecast terms already price openness exactly (escapes, region); a separate penalty
  would double-count and add a knob with no independent meaning.
- **Modeling their thief as adaptive (learned):** rejected — three games of evidence
  support a scripted-loop hypothesis with small inferred ingredients; a richer model would
  be fiction presented as data.
