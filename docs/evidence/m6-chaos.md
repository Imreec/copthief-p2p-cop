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

## Residual (disclosed)

The tunnel-kill variant against a real cloudflared edge is operator-run (needs the live
tunnel; PRD_gatekeeper §4 note) — it exercises the same deadline path proven here and
rides the next authorized live session alongside the M6-4 Gmail-draft evidence.
