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
| blocked outbound call (M7-7) | a live loop inside a declared I/O window is NEVER self-terminated — and a wedged loop, or an I/O wait past even the I/O budget, still fires |
| undeliverable outbound turn (M7-7) | an exhausted in-game push is OUR technical loss (App E symmetry), never a crash and never a unilateral claim; the retry runs on the turn budget; a non-transport error still propagates |

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
tests/chaos/test_watchdog_io_drill.py::test_drill_a_blocked_outbound_call_never_fires_the_watchdog PASSED
tests/chaos/test_watchdog_io_drill.py::test_drill_a_genuinely_dead_loop_still_persists_and_shuts_down PASSED
tests/chaos/test_watchdog_io_drill.py::test_drill_a_transport_that_never_returns_still_fires PASSED

============================= 13 passed in 3.22s ==============================
```

> Re-run 2026-07-20 after the M7-7 fixes; the three new drills are the ones the live
> kill run should have had.

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

## M7-7 — all four closed (2026-07-20)

Fixed on branch `m7-7-live-path-defects`, TDD RED→GREEN, keyless CI throughout.

**(1) The heartbeat now measures loop liveness, not I/O duration.** A blocking wire call
is a *deliberate, bounded* wait, not a wedge, so the loop declares it: `WatchedTransport`
(`peer/watchdog_transport`) wraps all four `PeerTransport` calls in an I/O window, and
inside a window the watchdog measures against the I/O budget instead of the loop budget.
Wrapping at the transport rather than beating inside the loop keeps `run_peer_game`
transport-blind (PLAN §12) and means a future transport cannot forget to declare a wait.

The **signed `watchdog_timeout_sec` is untouched** — the I/O budget is *derived*
(`turn_timeout_seconds + watchdog_timeout_sec`), so the fix is semantics, not a config
bump, and the App F guard is intact. `shared/budgets.reconcile_budgets` now asserts the
ordering **at config load**, which is the part that was missing entirely: the two budgets
had never been related to each other anywhere, and at runtime the wrong one won.

| Rule | Why |
|---|---|
| `watchdog_timeout_sec > 0` | an armed watchdog with no budget is not armed |
| `poll_interval_seconds < watchdog_timeout_sec` | an idle loop beats once per poll — a longer poll self-terminates a healthy waiting peer |
| `connect_timeout_seconds <= turn_timeout_seconds` | an outbound give-up must not outlast our own rule budget |
| I/O budget `> turn_timeout_seconds` | **the blocker**: our own deadline always expires first, so a silent opponent is lost by rule, never by suicide |

Shipped values satisfy all four: 60 / 0.5 / 60 / 180, I/O budget 240.

**(2)** The snapshot is role-derived into the git-ignored `logs/` (`sdk/peer_run.
snapshot_path`) and can no longer follow the log path; `state_*.json` is additionally
git-ignored repo-wide, so a future escape is still not committable.

**(3)** `peer/watchdog.announce_stall` writes the reason to stdout **and flushes** before
`os._exit(1)` — the flush is the whole point, since `os._exit` skips interpreter
shutdown and an unflushed buffer dies with the process.

**(4)** Replay reads `peer_result` as well as `result`. `RESULT_EVENTS` order is
**precedence, not preference**: a local log carries both, and a per-side `peer_result`
counts only its own side's steps — the M1 replay pin caught this the moment the fix
landed (4 steps reported where the match played 5). `game_uid` falls back to the
`negotiated` event, because a live result payload has none — it is settled at the
handshake. The rider is closed too: `ReplaySummary.records_verified` is now on the
summary and on the CLI banner, and **a verdict over zero records is TAMPERED**, not
"Verified OK". Re-replayed, banner now populated:

```
$ uv run copthief replay --log docs/evidence/m5-friendly-g3.jsonl
{"verdict": "Verified OK", "problems": [], "steps": 13, "outcome": "cop_capture",
 "game_uid": "f757f50d-d4f4-17e7-06cf-755905739b16", "records_verified": 28}
exit=0

$ uv run copthief replay --log docs/evidence/m6-tunnel-g1-capture.jsonl
{"verdict": "Verified OK", "problems": [], "steps": 13, "outcome": "cop_capture",
 "game_uid": "f757f50d-d4f4-17e7-06cf-755905739b16", "records_verified": 29}
exit=0
```

The aborted kill-drill log still replays **TAMPERED (exit 1)** — unchanged and
deliberate. The shared `game_uid` across all three is not a bug: it is derived from the
signed terms, which are identical across these games (kit §4, deterministic by
construction).

### Live re-drill — the blocker proven closed over the real tunnel (2026-07-20)

Same rig as the original drill (named tunnel `copthief`, reference thief on the public
edge), branch code, `cloudflared` killed the moment the handshake landed — so the tunnel
was dead for the whole game rather than for a few seconds. Log:
`docs/evidence/m7-7-redrill-g1.jsonl`.

| Elapsed since the kill | Observed |
|---|---|
| 0–178 s | cop **alive**, `watchdog_stall` count **0** — the old code fired at ~60 s |
| 183 s | process exits on **its own turn budget** |

The transition the log records — this is the whole point of the fix:

```json
{"event": "transition", "payload": {"from": "waiting_for_opponent",
 "to": "technical_loss", "trigger": "turn deadline exhausted"}, "sender": "police"}
```

and the console result:

```json
{"role": "police", "outcome": "timeout", "steps": 0,
 "game_uid": "f757f50d-d4f4-17e7-06cf-755905739b16", "audit_ok": false,
 "problems": ["audit skipped: timeout"], "opponent_records": 0}
```

**Lost by rule, not by suicide.** Under `a23d7ce` this exact scenario produced
`watchdog_stall` at ~60 s and `os._exit(1)`; here the watchdog stayed silent through
183 s of dead edge and our own `turn_timeout_seconds` classified the silent opponent,
which is what App E entitles us to. Defect (2) verified live in the same run: no snapshot
was written (the watchdog never fired) and `git status` stayed clean — no operational
artifact landed in a tracked directory.

**What this run does NOT cover:** the kill landed while we were *receiving*, so the loop
was polling, not pushing. The outbound-push case is the residual below.

**Residual raised by the #59 fix — now CLOSED (2026-07-21, Imree approved, PR #60).**
With the watchdog no longer firing at 60 s, a flap that caught us **mid-push** surfaced
as a `TransportError` from `_push_with_retry` — loud and logged, not a silent freeze, but
still our process ending rather than a classified loss, and the *pushing* half tolerated
only `connect_timeout_seconds` (60) where the receiving half tolerated 180. Both halves
of that gap are closed, scoped exactly to Imree's ruling (in-game pushes only,
transport-exhaustion only, no unilateral outcome claims, audit path verified):

- **The in-game push now retries on the TURN budget.** `McpTransport` gains
  `turn_push_timeout` (= `turn_timeout_seconds`); `send_turn` uses it while the handshake
  (`negotiate`) and the best-effort audit (`submit_audit`) keep `connect_timeout_seconds`.
  A mid-push flap now tolerates as long as a silent-opponent flap — the asymmetry is
  gone. (`connect_timeout_seconds` is private and unsigned, so unlike the signed watchdog
  budget this was a legitimate value change, not a semantics-only fix.)
- **An exhausted in-game push is OUR technical loss, not a crash.** `TransportError` moved
  to the protocol seam (`peer/transport`), so `run_peer_game` classifies transport-blind:
  on exhaustion the session takes `outcome="timeout"` → `TECHNICAL_LOSS`, trigger
  `outbound turn undeliverable past the turn budget` (distinct from the inbound
  `turn deadline exhausted`), and settles down the identical audit-skipped path. **No
  unilateral outcome claim** — we take our own loss (the 0/0 technical-loss row), never a
  declaration that the opponent lost. The thief's opening push, which happens before the
  loop, classifies the same way. A NON-transport error still propagates — only a real
  delivery failure is absorbed. Permanent keyless CI:
  `tests/integration/test_push_exhaustion.py` + `tests/unit/infra/test_transport_budgets.py`.

**Practical tolerance is now 180 s in both directions.**

### Live mid-push tunnel drills — the push path proven over the real edge (2026-07-21)

The residual note above said the push path was CI-only because the #59 re-drill's kill
landed while *receiving*. Imree authorized the mid-push drill; both variants were run
end-to-end over the real Cloudflare tunnel (our cop vs the reference thief, gotcha #11
both directions — the reference configs were already on the tunnel and were left
untouched). The reference thief moves first, so our cop's reply to its opening turn is our
first **outbound** push; the tunnel was killed the instant that inbound turn arrived
(`turn_received`), front-running our push into a dead edge.

**(a) heal-within-budget** — killed at the first `turn_received`, edge dead 90 s, then
`cloudflared` restarted. Log: `docs/evidence/m7-7-push-heal-g1.jsonl`.

| | |
|---|---|
| During the 90 s outage | our reply push retried; `watchdog_stall` count **0**; no classification |
| On restart | the retrying push **delivered**, the game resumed and ran to completion |
| Outcome | `cop_capture` in **13 steps**, mutual audit `audit_ok: true`, `problems: []`, 15 opponent records |
| Replay | **Verified OK** (exit 0), 29 records re-hashed |
| Process | exit 0; no snapshot; `git status` clean |

A network flap **inside** the budget costs nothing — the push waited it out and the game
finished normally. (Console noise, disclosed: the MCP client library's background
`post_writer` logged the dead-window `502`/`530` and a "Session termination failed"
during teardown; it is a library-level log, not our code — the game completed
`cop_capture` and exited 0 after it.)

**(b) budget-exhausted** — killed at the first `turn_received`, edge left dead past the
180 s push budget. Log: `docs/evidence/m7-7-push-exhaust-g1.jsonl`.

```
transport_error | receive_turn: opponent unreachable: Server error '530 <none>'
                  for url 'https://thief.imreeyal.com/mcp'
transition      | awaiting_reveal -> technical_loss,
                  trigger "outbound turn undeliverable past the turn budget"
```

console result:

```json
{"role": "police", "outcome": "timeout", "steps": 1,
 "game_uid": "f757f50d-d4f4-17e7-06cf-755905739b16", "audit_ok": false,
 "opponent_claim": "", "problems": ["audit skipped: timeout"], "opponent_records": 0}
```

Every item of the classified terminal, observed:

| Expectation | Observed |
|---|---|
| orderly shutdown | classified `TECHNICAL_LOSS`; process **exit 0**, no raw `TransportError` traceback |
| artifacts persisted | the JSONL log written; replays **TAMPERED (exit 1)** — the aborted-game convention, fail-closed and disclosed |
| dispute-evidenced "unreachable" | the `transport_error` event names the edge failure (`530`, opponent unreachable) — a committed record of *why* we lost |
| no unilateral outcome claim | `outcome: timeout` (our own technical-loss row, 0/0), `opponent_claim: ""` |
| report rail fires per posture | `decide_email_action` over the loaded resting `[email]` → `refuse: email disabled (email.enabled=false)`; nothing sent |
| no snapshot escape | no `state_*.json`; `git status` clean |

The distinction from the #59 re-drill is exactly the point: that kill landed while
receiving and classified via `turn deadline exhausted` (the inbound path); this one landed
mid-push and classified via `outbound turn undeliverable past the turn budget` (the #60
path). Both are our own technical loss by rule — neither is a crash, and neither claims
the opponent lost.
