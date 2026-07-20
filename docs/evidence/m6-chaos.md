# M6-7 — chaos-drill battery (PLAN §10; FR-8/FR-11)

> Observed 2026-07-19, local run of the committed battery (`uv run pytest tests/chaos -v`,
> also permanent keyless CI on every pass). Each drill asserts its SPECIFIC defense fires —
> "no crash" alone never passes a drill.

| Drill (PLAN §10) | Defense observed |
|---|---|
| dead peer mid-game | deadline → `timeout` outcome, TECHNICAL_LOSS, transition trigger names `turn deadline exhausted` |
| delay to the deadline edge | game FINISHES — a slow-but-alive opponent costs nothing |
| malformed TurnMessage | wire validation collapses the machine BEFORE any state change (board/inbox untouched) |
| duplicate / replayed turn | step-continuity wall → collapse |
| oversized hostile hint | closed-vocabulary parser neutralizes it; message archived; play continues |
| audit with tampered record | re-hash mismatch fails the WHOLE audit (rule 19, "no almost-match") |
| fabricated scent grid | `scent_physics_mismatch` evidence event (per-step cell counts); verdict/result UNTOUCHED (SQ3) |
| stalled loop (watchdog) | snapshot persisted + shutdown callback fired exactly ONCE; a beating loop is never disturbed |

## Battery output (verbatim)

```
tests/chaos/test_audit_drills.py::test_drill_one_tampered_revealed_field_fails_the_whole_audit PASSED
tests/chaos/test_audit_drills.py::test_drill_fabricated_scent_grid_raises_the_evidence_event_and_nothing_else PASSED
tests/chaos/test_audit_drills.py::test_drill_honest_grids_raise_no_event PASSED
tests/chaos/test_comm_drills.py::test_drill_dead_peer_mid_game_is_a_clean_timeout_technical_loss PASSED
tests/chaos/test_comm_drills.py::test_drill_delay_to_the_deadline_edge_never_costs_a_false_loss PASSED
tests/chaos/test_inbound_drills.py::test_drill_malformed_turn_collapses_before_any_state_change PASSED
tests/chaos/test_inbound_drills.py::test_drill_replayed_turn_hits_the_step_continuity_wall PASSED
tests/chaos/test_inbound_drills.py::test_drill_oversized_hostile_hint_is_neutralized_and_play_continues PASSED
tests/chaos/test_watchdog_drill.py::test_drill_stalled_loop_persists_and_shuts_down PASSED
tests/chaos/test_watchdog_drill.py::test_drill_beating_loop_is_never_disturbed PASSED

============================= 10 passed in 1.70s ==============================
```

## Live wiring

`sdk/peer_run` arms the watchdog for every live peer: heartbeat per loop iteration
(`run_peer_game(heartbeat=…)`), timeout = the signed `watchdog_timeout_sec`, snapshot →
`logs/state_<role>.json` (git-ignored), then a loud `watchdog_stall` JSONL event and a
controlled exit. The scent-physics check runs at every settlement over the archived
inbound grids vs the revealed walk — evidence-grade only (FR-11; disclosed limitation:
grids are unauthenticated, so the proof binds only our side of a dispute).

## Real-tunnel kill drill (live — residual closed 2026-07-20)

> Run at cop `a23d7ce` against the live reference thief over the public Cloudflare edge
> (named tunnel `copthief`: our cop `127.0.0.1:8802` ↔ `cop.imreeyal.com`, reference thief
> `127.0.0.1:8801` ↔ `thief.imreeyal.com`; the reference's `config/thief/game.toml`
> `opponent_url` was pointed back at `https://cop.imreeyal.com/mcp` per ops gotcha #11 and
> **is left in that tunnel state**).

### Game 1 — full game over the public edge (not the drill; kept as evidence)

The first game completed before the kill could land (13 steps in ~10 s). It stands on its
own as the **first tunnel-borne full pairing since M2**, and re-confirms the M5 localhost
result over a real network path:

| | |
|---|---|
| Outcome | `cop_capture` in **13 steps** — our tuned cop captured the reference thief |
| Mutual audit | `audit_ok: true`, opponent claim `capture`, `problems: []`, 15 opponent records |
| Replay | **Verified OK** (exit 0) — 26 traveled turns paired, 29 revealed records re-hashed |
| Log | `docs/evidence/m6-tunnel-g1-capture.jsonl` |

**First live firing of the M6-7 scent-physics check** (FR-11): one mismatch, **1 cell at
step 13** — the capture step. That is consistent with the already-documented F10/F10b
reference convention (its terminal message repeats its *current* step), not with a
fabricated trail. Per SQ3 the check is **evidence-grade only**: verdict, belief and result
were untouched, exactly as designed. Recorded, not alleged.

### Game 2 — the drill: `cloudflared` killed mid-game

`taskkill /F` on `cloudflared.exe` at 27 log lines (step 3, while an outbound turn was in
flight). Observed, in order:

```
decision | {"brain": "PoliceBrain", "intent": "truth", "move": "S", "step": 3}
turn     | {}
watchdog_stall | {"reason": "loop stall: no heartbeat for 60.34s (state persisted)"}
```

then a controlled `os._exit(1)`. Snapshot written (quoted; it is an operational artifact,
not committed):

```json
{"game_uid": "f757f50d-...", "role": "police", "state": "awaiting_reveal",
 "steps_sealed": 3, "position": [1, 2], "barriers": [], "outcome": null}
```

**The defense that fired was the watchdog, not the turn deadline** — which contradicts the
prediction going in. The outbound HTTP call blocked on the dead edge, so the loop stopped
beating, and the signed `watchdog_timeout_sec` (60) elapsed long before the private
`turn_timeout_seconds` (180) could adjudicate the opponent as silent. FR-8 is proven live:
no silent freeze, state persisted, loud event, controlled exit. Log:
`docs/evidence/m6-tunnel-kill-g1.jsonl`.

Replaying the aborted log yields **TAMPERED (exit 1)** — every traveled turn lacks a
revealed record because the game never reached its audit. That is fail-closed and correct
for a binary rule-19 banner (book §7.4 fixes the two strings), but it means **an honestly
crashed game is indistinguishable from a dishonest one on replay**. Disclosed here rather
than papered over.

### Findings raised (→ TODO M7-7)

1. **Watchdog outruns our own turn deadline.** Signed `watchdog_timeout_sec` 60 < private
   `turn_timeout_seconds` 180, and a blocking outbound call stops the heartbeat entirely —
   so any network stall over 60 s self-terminates us *before* our own deadline can classify
   a silent opponent. In a counted game a transient flap would cost the game by suicide
   rather than by rule. The heartbeat should measure **loop liveness, not I/O duration**.
2. **Snapshot path escapes its git-ignore.** `peer_run` derives `state_dir` from
   `log_path.parent`, so logging into a tracked directory writes `state_<role>.json`
   *there*. The snapshot is specified as a git-ignored operational artifact
   (PRD_gatekeeper §7 D4) and `.gitignore` only covers `logs/`; this run left an
   untracked-but-committable state file in `docs/evidence/` (deleted by hand).
3. **The loud exit is silent on the console.** `os._exit(1)` skips stdout flushing, so the
   terminal printed **nothing** — the stall is discoverable only in the JSONL. An operator
   watching a live match sees an unexplained death.
4. **Replay's summary line is blank for every live game.** `replay_from_log` reads
   `event == "result"`, but live peer logs emit `peer_result`, so `steps`/`outcome`/
   `game_uid` render as `0`/`unknown`/`""` while the verdict itself is computed correctly
   over the real records. Verified: the M5 committed friendly log re-hashes 26 turns and 28
   records — its "Verified OK" claim is sound; only the display was empty. Related
   hardening: `verified = not problems` is vacuously true when nothing is checked, so an
   empty log would also print "Verified OK".
