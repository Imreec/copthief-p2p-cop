# M11 — red-team of our own brains (2026-08-11)

> Mandate (session prompt, Imree 2026-08-11): play attacker against the cop AND the
> thief, list every way to beat each, check the list against what actually exists,
> and disposition each finding — fixed / work item / accepted-with-reason. Companion
> to ADR-0013. Every claim below was verified against the tree at `64871a1`, not
> reasoned from memory; file:line citations are to that commit.

## A. Attacks on our THIEF (doctrine-evader, M10-armed: `room_first=1.0`)

| # | Attack | What exists today | Disposition |
|---|--------|-------------------|-------------|
| T1 | **Cage-building cop** — invest sub-threshold walls at tempo, close a k-wall pocket. The forecast (`wall_forecast.py`) looks exactly ONE wall ahead; `region_cap=24` saturates on a 49-cell board so a forming cage is invisible until it is nearly shut; and when every room term saturates, even the DEMOTED flight tie-break herds the evader rim-ward. | **Proven twice**: our own police-m10 converts doctrine-m10 32/32 (m9-study-arena), and nis-yar1's cop — a second independent seal implementation — killed the fielded M10 evader at step 13 in all three thief games of the 2026-08-11 friendly (60–80 loss). | **FIXED (M11-1)**: k-wall pocket forecast + orbit margin + low flight floor — 0/32 → 5/32 vs police-m10, 8/8 vs the lag-1 nis-yar1 arm, live g02 kill-step pinned. NOTE: the session hypothesis (flight-cap lift on wall-turns) was built, measured HARMFUL in every variant, and removed — see m11-hardening.md. |
| T2 | **Claim-spoof herding** — send `capture_claim` cells that are lies. `belief.note_claim` (belief.py:78) collapses the posterior to CERTAINTY on any inbound claim; its docstring justifies this by "a false one costs the game (App E rules 21–22)". Verified vacuous: settlement validates only the end-of-game `result_claim` (`peer/p2p.py validate_opponent_audit`), no code path compares per-turn claims to the revealed track — and the book page itself (p.145) sanctions false *capture declarations* / denying-being-caught, while the lived wire (vibecode, 08-10: 42/43 speculative claims, both audits Verified OK) treats speculative claims as legal probes. A claim-spammer owns our belief at zero cost, every turn, after `predict()` and before scent. | Unenforced-rule justification in a load-bearing domain docstring — exactly the silently-vacuous class this session hunts. | **FIXED (M11-2)**: plausibility gate — a claim outside the motion-model reachable set no longer collapses (no-op for every truthful claimer by the SQ3 never-eliminate invariant; a lie constrained to plausible cells buys far less). Measured with a lying-claims arena arm. |
| T3 | **Plan replay from sealed logs** — our doctrine is deterministic per (config, seed); `tie_epsilon` randomizes moves, not plans; sub-game seeds differ but the POLICY is fixed, so series N's log predicts series N+1. | True by construction. | **WORK ITEM (M11 stretch, work item 5)** — seed-consuming plan diversity; do not ship if it donates win-rate. |
| T4 | **Hint poisoning** — adversarial hint text. | Closed-vocabulary gazetteer parse (injection-safe by shape), profiled trust with `profile_hint_floor`, lie-rate profiling validated live vs vibecode (lie_rate 0.29 absorbed). | **ACCEPTED** — bounded by design; no free steering found. |
| T5 | **Camper beacon** — force STAYs, read fresh-peak. | Stay cap (2) + STAY-last tie-break already ship. | **ACCEPTED** — already closed (M9). |
| T6 | **Belief-flattening cop** — move erratically so our top-3 support misses the true cell; the lethal gate MIN can then bless a lethal landing. | Inherent POMDP exposure; `hunted_radius` mass check narrows it; support widening costs elsewhere. | **ACCEPTED-WITH-REASON** — no counter that does not trade worse elsewhere; k-wall forecast (M11-1) shrinks the blast radius of a wrong support since pockets are priced earlier. |

## B. Attacks on our COP (police-m10: containment + solver + sharp199 + claim gate 0.1)

| # | Attack | What exists today | Disposition |
|---|--------|-------------------|-------------|
| C1 | **Cage-escape evader** — punish containment's tempo: sprint when the cop stops to build (`contain_range=3` means the cop only invests when close; each wall is a free tempo for the runner). A relocating evader may make containment never converge → 35-step survival. | Exactly the thief M11-1 builds. Whether police-m10 still converts it is THE self-play question. | **MEASURED (M11-1 gate + self-play loop)**; if the cop stops converting, the counter-counter (corridor/predictive walling) is the next self-play round's work, with data. |
| C2 | **Claim-reading thief** — our cop claims at `claim_threshold=0.1` (measured under M7 brains); containment changes the cop's rhythm (stand-still wall turns are readable), so the claim leak may price differently now. | Threshold never re-measured under the M10 stack. | **MEASURED (M11-4 claim re-sweep)**. |
| C3 | **Thief-side claim-spoofing our cop** — `inbound.py:135` applies `note_claim` regardless of the sender's role: an adversarial THIEF sending speculative claims collapses our COP's belief onto arbitrary cells. No opponent has done it; nothing stops it. | Same vacuous-sanction root cause as T2. | **FIXED (M11-2)** — the plausibility gate is role-blind and covers both directions. |
| C4 | **Solver budget-abort at conversion** — `endgame_node_cap=20000` was tuned for chase positions; mid-cage branching is wider; a budget abort at the closing moment defers to a heuristic that may let the thief slip the half-built cage. | No instrumentation exists — a defer is indistinguishable from a proven no-proof. | **MEASURED (M11-5)** — defer-rate counters, decision gated on data. |
| C5 | **Fortress thief** — wall itself into an unreachable 2-cell pocket for guaranteed survival. | Barriers are police-only (`decision.py:54 barrier_is_playable` role gate; book ch.3) — illegal for every thief, ours and theirs. | **DISMISSED** — verified illegal. |
| C6 | **Wall-position info leak** — containment walls cluster near our belief argmax, telling a watching thief when we are locked on. | True; the information is only useful when our belief is already right. | **ACCEPTED-WITH-REASON** — the leak arrives exactly when it can no longer help them; re-visit only if self-play shows otherwise. |
| C7 | **Lockout bait** — bait the cop into a wall that seals it away from the mass. | `locks_us_out` veto (mass-weighted, 0.9) guards both wall paths, including containment (containment.py:87). | **ACCEPTED** — already closed (M7-49). |
| C8 | **Perch behind the cop's own wall** — camp just past a wall the cop placed; the Manhattan leaf reads every approach as worse (local minimum), containment refuses at gap 4 > range 3, and the cop freezes. | **Happened live** (nis-yar1 g01, found by this session's postmortem, not by red-team foresight): 19 STAY turns, 11 walls unspent, 34-step survival conceded — with tracking PERFECT (35/35). `locks_us_out` checks path existence, not path cost, so the veto passed the wall. | **FIXED (M11-C1)**: `contain_range 4.0` (measured to resume investment in the logged geometry) + `path_distance 1.0` (wall-aware leaf; open-board stream provably unchanged). Both pinned in `test_police_path_distance.py`. |

## C. Silently-vacuous checks audited this pass

| Check | Verdict |
|---|---|
| `note_claim`'s "false claims are sanctioned" justification | **VACUOUS — confirmed** (no enforcement anywhere in settlement/audit/replay; see T2). Fixed by M11-2. |
| Champion-gate arena (`config/arena.json`) really runs the M10 stack | **NOT vacuous** — verified `contain_enabled: 1.0` (police-brain) and `room_first: 1.0` (doctrine-evader) are in the shipped brain_options. |
| `multiplicative_book_v1` overlay missing M10/M11 keys (session-prompt item 3a) | **Latent, real** — under a book-v1 pairing the base-table `contain_enabled`/`room_first` (and now the M11 keys) would arm unmeasured via fallthrough. **FIXED**: overlay pins added, explicit 0.0 (off until measured under that physics). |
| Solver defer vs no-proof indistinguishable | **Confirmed blind spot** — M11-5 adds counters before any cap change. |
| M10 vibecode arms fidelity | Already disclosed in m10-countertune.md caveats; the M11 real-opponent gate (fresh anrbj666 HEAD arms + sqak HEAD re-verify) is the structural answer. |

Dispositions marked FIXED/MEASURED are backed by the M11 evidence docs in this
directory; nothing here is aspirational — each row's status matches the tree at
the commit this file lands in.
