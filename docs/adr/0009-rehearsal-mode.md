# ADR-0009 — Rehearsal mode: the full rulebook without a reachable lecturer

## Status

PROPOSED (2026-07-24) — amends ADR-0008 decision 6's mechanism, not its posture.

## Context

`counted` was one switch doing two unrelated jobs:

1. **Arm the App F fixed rows.** `load_all(config_dir, counted=True)` makes the
   constitution refuse to load unless it is a genuine counted-shaped match — it is what
   produced *"num_games: fixed at 6 by App F, got 1 (deviation disqualifies)"*.
2. **Make the lecturer addressable.** `decide_email_action(counted=…)` refuses the
   lecturer's address entirely while it is false (ADR-0008 amendment 9b).

Welding them was deliberate and, for its purpose, correct: hanging the lecturer guard on
a flag that *cannot be set casually* is stronger than hanging it on a boolean anybody
could flip. But it made one mode unreachable — **play by the full rulebook while the
lecturer stays unreachable** — which is exactly what a dress rehearsal is.

Imree's framing (2026-07-24) is what surfaced it: a friendly should differ from a counted
game **only** in that it is not counted and the lecturer is not on it. Full ninety
minutes, same rules, same artifacts — like a football friendly. Under the old flag that
was impossible: arming the rules also unlocked the lecturer.

**The cost of the coupling, measured rather than argued:** because `counted=True` was
unsafe to pass, *nothing in the codebase ever passed it*. Every live game — including the
2026-07-24 rehearsal series against Alon/Renat's team — ran with the App F rows
**disarmed**. The constitution happened to be counted-shaped because it was set by hand;
nothing was enforcing it. Rules were being *followed*, not *enforced*.

## Decision

1. **Two axes, one object.** `shared/run_mode.RunMode` carries `strict_rules` (arm the
   App F rows) and `counted_series` (this run scores league points).
   `RunMode.rehearsal()` = rules armed, not counted. `RunMode.counted()` = both.
2. **The lecturer needs BOTH, enforced by construction.** `counted_series` without
   `strict_rules` raises at construction — it cannot exist. So splitting the axes never
   makes the lecturer *easier* to reach than under ADR-0008: he remains reachable only
   from a constitution the App F rows have vetted. Alon/Renat's phrasing for the
   principle, adopted here: **safety by shape, not by configuration.**
3. **The email layer is named for what it permits.** `decide_email_action` and
   `EmailSender` take `lecturer_addressable`, not `counted`. Handing the email layer the
   *rules* flag was the confusion this ADR removes; a parameter named for the run type
   invites exactly that mistake, and both default closed.
4. **`counted=` survives as the legacy spelling of axis 1 only.** `SimulationSdk(...,
   counted=True)` now means `RunMode(strict_rules=True)` — it can no longer imply the
   lecturer is reachable. Existing callers keep working with strictly less authority.

## Consequences

- A rehearsal can run the real rulebook with the lecturer **structurally** unreachable —
  not merely unconfigured, and not dependent on nobody typing an address.
- ADR-0008's guarantee is unchanged in strength: the lecturer is still reachable only
  from an App F-vetted counted constitution. Only the *spelling* moved.
- The disarmed-rules gap is now visible and fixable: a rehearsal run should pass
  `RunMode.rehearsal()`, and the App F rows then actually bite during play.
- The email layer can no longer be handed the wrong boolean without it reading wrongly at
  the call site.

## Alternatives considered

- **Two independent booleans.** Rejected: it would make the lecturer easier to reach than
  today, weakening the very guard the split was meant to preserve.
- **Rename `counted` everywhere to `strict_rules`.** Rejected for now — 146 mentions
  across 12 files, and the confusion that actually bites is at the *email* seam, which
  this ADR renames precisely.
- **Leave it welded and hand-set the constitution for rehearsals.** Rejected: that is the
  status quo, and it is what let six sub-games run with the rules disarmed while looking
  correct.
