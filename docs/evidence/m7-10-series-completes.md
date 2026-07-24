# M7-10 — a six-sub-game series completes (evidence, 2026-07-24)

Building the M7-4c series driver made two live-path defects visible, and this is the
record of fixing them. The headline is simple: **before these three fixes, a six-sub-game
series had never completed — the two sides desynchronised at sub-game 2 and never
recovered. After them, 6/6 settle with a mutual audit on every one.**

## What was wrong

**(1) The handshake identified neither the game nor the side.** The `negotiate` payload
carried `{identity, nonce, scent_model_sha256, signature, terms}` — nothing that says
*which sub-game* or *which role*. Two peers could agree on everything signed and still be
playing different games. Observed directly: two of our peers had **both** taken thief,
completed a handshake, and deadlocked after one turn, each waiting for a police move that
was never coming. The same hole produced the 2026-07-24 rehearsal's phantom sub-game 6 —
the opponent's s6 and our s2 were one game wearing two indices, undetectable from either
side because identical terms give identical `game_uid`s.

Committed here as `m7-10-phantom-s6-g2.jsonl`: that very game, **34 turns, 35 sealed
records, sealed `sub_game_number: 2`, replays Verified OK over 70 records**. It was real
and mutually audited; it was simply filed under two different numbers.

**(2) A handshake could be swallowed by the opponent's PREVIOUS sub-game peer.** Under the
rolling-window protocol the two sides finish milliseconds apart. The faster side starts
its next peer and pushes its agreement into the slower side's previous peer — still
listening, which accepts it, enqueues it, and exits without ever draining the queue. The
slower side then waits out its entire connect budget for an agreement that was already
delivered.

The cost compounds: a failed handshake ends in ~60 s while a real game takes longer, so
the side that failed runs **ahead** and never re-synchronises. Observed: side B on
sub-game 4 while side A was still on sub-game 2. That is two teams describing different
series — the shape App E rule 35 zeroes both teams for.

## The three fixes

- **`peer/pairing` + handshake wiring.** `negotiate` now declares `sub_game_number` — the
  **sealed** index, read from the step-0 record so the handshake and the commit cannot
  disagree — and `role`. A peer whose index differs, or whose role *equals* ours, is
  refused before the `game_uid` is locked. Refusal follows the truth table the kit already
  uses (SPEC §7): a declared mismatch refuses, **omission never refuses**, and a value we
  cannot compare (wrong type, different spelling) is silence rather than disagreement —
  refusing over a peer's type choice would turn a cosmetic wire difference into a
  forfeited game, and the rehearsal already lost a window to `payload` vs `message`.
- **Handshake redelivery.** `exchange_agreement` re-pushes each lap instead of pushing
  once and waiting, so a greeting swallowed by a dying peer gets another chance at the
  real one. Classification is unchanged: never delivered is a `TransportError`, delivered
  but unanswered is `None` (the opponent's silence, which the peer loop judges).
- **`peer/port_guard` + inbox closing.** One live peer per role: refuse to start when
  something already holds our port, and refuse to play when *our own* server never came up
  (it runs on a daemon thread, so a failed bind raises where nobody is looking — exactly
  how the orphan's victim played on with an inbox the opponent could not reach). And a
  settled peer now **refuses** new arrivals on all four channels instead of swallowing
  them, which turns the opponent's silent loss into an ordinary transport failure their
  existing retry already resolves.

`run peer` answers both port refusals with a JSON object and exit 2, never a traceback —
and the series driver records which sub-game did not start, and why.

**Wire change, deliberate and safe (constraint #13):** the two declared keys ride
*outside* `terms`, which is the byte-identical signed constitution. No canonicalization,
hash or signature input moves; the kit CORE vectors are untouched. Same argument as
M3-8's `scent_model_sha256`, which the reference peer ignores.

## The run

Two real `copthief series` processes on localhost, `--rehearsal` on both (App F counted
rows **armed**), each sub-game its own peer process, `game.json` byte-identical between
the sides:

```
sg1 police cop_capture    steps=17  audit_ok=True
sg2 thief  cop_capture    steps=5   audit_ok=True
sg3 police cop_capture    steps=4   audit_ok=True
sg4 thief  thief_survival steps=35  audit_ok=True
sg5 police cop_capture    steps=8   audit_ok=True
sg6 thief  cop_capture    steps=6   audit_ok=True
```

- **All six settled, every one mutually audited**, roles alternating 3/3 (F2), and a single
  `game_uid` (`2befc104…`) shared by all six on **both** sides.
- The full artifact set for the series is on disk — 20 JSON files across the two sides —
  and the series result is committed here as `m7-10-series-result.json`.
- **The report was REALLY SENT.** On Imree's explicit authorization of the recipients
  (constraint #16: the recipient *is* the authorization), the series fired its own report
  at the end through the live Gmail rail:

  ```json
  {"action": "send", "reason": "", "game_uid": "2befc104-ee4c-afd0-98ac-d2eb7f2b9f17",
   "recipients": ["imreeyal.copthief@gmail.com", "imree.c@gmail.com"]}
  ```

  Subject `Police-Thief series result: winner imreeyal (reported by police)`; body and
  attachment both the 7095-byte `result_<game_id>.json` — the same bytes committed here as
  `m7-10-series-result.json`. **This is the first email the project has ever actually
  sent**, and it closes the last unproven inch of the report path: the 2026-07-20
  send-only token works, the multi-recipient form works (a friendly needs it — us + the
  opponent team), and no step between the sixth sub-game settling and the mail leaving
  involved a human. Exit 0 on both sides.
- The lecturer guard was live throughout: `[email] lecturer` was configured in that run's
  config, the run was `--rehearsal`, and he is not in the recipients — `RunMode` makes him
  unreachable regardless (M7-9 / ADR-0009).
- Two earlier runs of the identical rig pinned the other outcomes: a resting `[email]` gave
  the same 6/6 with `refuse: email disabled` at the end, and an enabled rail with
  `token_path` pointed at a non-existent file gave `{"action": "failed", …}` and CLI exit 3.
  **Both of those are now caught at preflight instead — see the M7-10b note below.**

## M7-10b addendum — a report-owing run refuses to START if it cannot report

The runs above exposed the last gap in the "friendly = a real match minus the counting"
requirement: the mail rail was consulted only *after* the sixth sub-game settled, so a
disabled rail, an empty recipient, or a stale OAuth token was discovered after six games had
been played — the moment App E rule 35 makes most expensive. `EmailSender.preflight()` now
runs at the top of the series whenever the run owes a report (`RunMode.strict_rules` —
rehearsal or counted): the same interlock the send runs, plus a credential probe that
refreshes the OAuth token without sending. Live proof, both refusing with **zero sub-game
logs written**, exit 2:

```
# --rehearsal, committed resting [email] (disabled)
{"refused": "the report cannot be delivered …", "problems": ["email disabled (email.enabled=false)"], "sub_games": []}

# --rehearsal, enabled + recipient set, but token_path absent
{"refused": "the report cannot be delivered …", "problems": ["the report transport is not ready: FileNotFoundError: … 'no_such_token_deliberately.json'"], "sub_games": []}
```

The real send-only token passes the same probe (`GmailTransport.verify_ready()` refreshed it,
no email sent), so a correctly-configured run is not blocked. **Consequence, stated plainly:
a `--rehearsal` can no longer be played with the mail disabled** — which is the whole point.

## What this does NOT yet prove

- **The opponent's half.** Our refusal is inert until they declare `sub_game_number` and
  `role` too; a mispairing is only detectable if both sides say what they are doing. The
  exact field shape has been staged for them so the two sides cannot spell it differently.
- **A send to the OPPONENT.** The rail is proven, but a friendly's recipient list is us +
  their team, and their address has never been configured for a run. That is Imree's to
  set, before the match and never inside it.
- **Their swallowed greetings.** Our peer no longer eats theirs, and our re-push covers
  ours being eaten — but a peer of theirs that keeps accepting after settlement will still
  swallow ours until they close their own inboxes. Our re-push is what makes that
  survivable rather than fatal.

## Files

- `m7-10-series-result.json` — the six-sub-game series result artifact.
- `m7-10-phantom-s6-g2.jsonl` — the rehearsal game that was filed under two indices
  (34 turns, `audit_ok`, sealed `sub_game_number: 2`; replays Verified OK, 70 records).
  Kept because it is the motivating evidence for fix (1), not as series evidence: that
  series was mutually discarded by both teams.
