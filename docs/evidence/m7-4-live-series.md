# M7-4c — the live series reports itself (evidence, 2026-07-24)

The gap this closes, stated plainly: **every piece of the series report existed and
nothing fired them.** `report/summary_from_log` rebuilds a sub-game summary from an
archived log, `report/series_from_logs` joins N of them into the counted-shaped artifact
set, `infra/email_sender` sends one through the interlock and the gatekeeper — but a live
series plays each sub-game in its own process, so no process spanned the series and no
code owned the moment it ended. A perfect 6/6 would have mailed nothing.

`sdk/live_series` is that owner, `copthief series` its verb. Roles alternate on the
signed `num_games`, the archived logs become the artifact set, and the ONE report the
series owes is sent automatically (App E rule 32; rule 35 zeroes BOTH teams for a missing
report — so a human step there is a sanction, not a safety).

## What was run

Two peers on localhost, each side a real `copthief series` process, each sub-game its own
`copthief run peer` child — the same rolling-window shape both teams played the
2026-07-24 rehearsal in. Side A is the natural police, side B a clearly-labelled
`-mirror` identity (PRD_reporting §6: self-play states exactly what it is). The two
`game.json` files were byte-identical, as the terms signature requires; the only
divergence from the committed tree was side A's `[email]` section, flipped in a COPY of
`config/` (the M6-4 method — the committed resting state is never edited to play a game).

### 1. Six sub-games under the armed rulebook

`copthief series --role police --rehearsal` on both sides, over the committed
constitution — `num_games` **6**, App F counted rows **armed** for the first time in a
live game (M7-9: nothing had ever passed the flag, so every previous live game ran with
the rulebook disarmed).

Sub-game 1 played clean in both directions: **`cop_capture` in 17 steps, `audit_ok: true`
on both sides, one shared `game_uid`.** The series then desynchronised — see the two
findings below, which are the real yield of this run.

### 2. One sub-game, end to end, with the mail rail live

A one-sub-game series (`num_games: 1`, so dev mode rather than `--rehearsal`, since App F
fixes six for counted play) to exercise the whole path in one run:

```
copthief series --role police --opponent-group imreeyal-mirror   (side A, reporting)
copthief series --role thief  --opponent-group imreeyal          (side B, resting [email])
```

Side A's run record, verbatim except for absolute paths:

```json
{"game_id": "imreeyal-vs-imreeyal-mirror",
 "sub_games": [{"sub_game_number": 1, "role": "police", "outcome": "cop_capture",
                "steps": 17, "game_uid": "2ff4b20b-3a12-b7ad-f18c-de5245e8c813",
                "audit_ok": true, "opponent_claim": "capture", "problems": [],
                "opponent_records": 19, "exit_code": 0}],
 "email": {"action": "failed",
           "reason": "FileNotFoundError: ... 'no_such_token_deliberately.json'",
           "recipients": ["copthief-selfcheck@example.invalid"]}}
```

- **The artifact set landed complete** — declaration, per-sub-game config, log and Hebrew
  report, and `result_imreeyal-vs-imreeyal-mirror.json` (committed here as
  `m7-4-live-series-result.json`).
- **The interlock ALLOWED the send** (enabled × send × a configured recipient) and the
  Gmail transport was really invoked — this is the first time the report rail has been
  reached from a live game rather than refused by posture.
- **Nothing could leave the machine, by construction:** `token_path` pointed at a file
  that does not exist, so the backend failed on credentials before any network call, and
  the recipient domain is `.invalid` (RFC 2606). A real `token.json` does sit in the repo
  root; the run never referred to it. The send half is pinned keyless instead
  (`tests/integration/test_live_series_report.py`): one email for the whole series, body
  bytes identical to the artifact file, the artifact attached (rule 34).
- Side B, on the committed resting `[email]`, recorded `refuse: email disabled` — the
  posture observed end-to-end on the same run.
- `copthief replay --log m7-4-live-series-g1.jsonl` → **Verified OK, 37 records
  verified**, exit 0.

## Three defects this run found, all fixed here

1. **A sub-game that left no log crashed the aggregation** with a bare
   `FileNotFoundError`. `summary_from_log` refused an unsettled log by name but had no
   answer for a missing one — an operator got a traceback where the design promises a
   named refusal. A missing log is now the emptiest case of the same fact.
2. **A dead child left no trace of why.** Five sub-games once "played" in three seconds
   because their peers failed at launch, and the record said only `outcome: unknown`. The
   child's stderr tail is now part of the record: a series that cannot say why a sub-game
   did not happen cannot be operated.
3. **A failed send swallowed the whole run record.** The missing token raised out of the
   driver and took the artifact paths and sub-game outcomes with it. Under rule 32 an
   undelivered report is the most important thing the operator can be told, and the
   telling is useless without the path of the artifact that still has to reach the
   opponent. It is now `{"action": "failed", "reason": …}` in the record, with CLI exit
   **3** — distinct from exit 2, which means no report was produced at all.

## Two findings NOT fixed here — they are the next piece of work

1. **The handshake identifies neither the role nor the sub-game.** The `negotiate`
   payload is `{identity, nonce, scent_model_sha256, signature, terms}`. Observed
   directly in this run: our sub-game 2 peer (thief) completed a handshake with a peer
   that was *also* playing thief, and the game then deadlocked after one turn. The same
   hole is what let the rehearsal's phantom sub-game 6 happen — his s6 and our s2 were
   one game wearing two indices, and neither side could tell. The fix agreed with the
   Alon/Renat team — **verify the sub-game index at negotiate and refuse on mismatch** —
   should carry the role with it, and only bites if both sides send the fields.
2. **A handshake can be swallowed by the opponent's PREVIOUS sub-game peer.** Under the
   rolling-window protocol the two sides finish a sub-game milliseconds apart; the faster
   side's next peer pushes its agreement while the slower side's previous peer is still
   listening, and that peer enqueues it into a queue it will never drain before exiting.
   The slower side then waits out its whole connect budget for an agreement that was
   already delivered — and, having failed 60 s faster than a real game takes, runs AHEAD
   of its opponent and never re-synchronises. This is at-least-once delivery arriving at
   the handshake, where M7-8's tolerance does not reach: the answer is to keep re-pushing
   the agreement until the game starts, the same "transport tolerance, no rules
   tolerance" rule the joint ADR already states for turns.

Both are live-path interop work, both are mutual with the opponent team, and neither is
caused by the series driver — the driver is what made them visible.

## Files

- `m7-4-live-series-g1.jsonl` — the sub-game log (replays Verified OK, 37 records).
- `m7-4-live-series-result.json` — the series result artifact the report rail was handed.
