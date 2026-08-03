# M7-32 — Warm-up 2: the fixes live, the artifacts converge (2026-08-03, T=12:15 IL)

The second uncounted series vs anrbj666, agreed in Round 21 with the series shape
stated up front per the mutual protocol ("six windows, odd/even split, both runners").
One window, no burns: gates green 12:12:31, fired 12:15:00.2, his s1 edge 406 at T,
six sub-games settled strictly s1→s6, series exit 0, one auto-fired report to the
friendly recipients.

## 1. Result — and why the score itself is the headline

**anrbj666 85–45 (5 sub-games to 1).** His sealing cop captured our thief in s1, s3
and s5 — at step 13, identically — because our thief now **concedes when sealed**
(M7-29). This score equals, exactly, the corrected adjudication his Round-20 letter
computed for the first warm-up: two independent implementations of rules 46/47 now
produce the same outcome from honest play. The three losses are the cost of honesty;
the games were always his, and before M7-29 the scoreboard hid it. Our cop captured
his rematch-built evader again (s4, 13 steps — three captures across three warm-ups);
his thief survived s2/s6.

## 2. Live promotions this window (all from the committed logs, `m7-32-warmup2-g0*.jsonl`)

| Mechanism | Evidence |
|---|---|
| M7-29 rule-46/47 self-concession | three live firings: "You got me." finals at step 13 in g01/g03/g05, all settling `cop_capture`, mutual audits clean both sides |
| M7-28 `github_commit` | our result rows carry the exact commit played (`e650af3…`), replacing "unknown"; `log_files` sample-flat |
| M7-25 info_mode lock | `020947da…` on the record in all six handshakes, both sides |
| M7-23 frame check | zero `scent_frame_refused` (three warm-ups, zero false positives cumulative) |
| M7-10/22 pairing + uid | zero `agreement_refused`; one `game_uid` `e351176a…637d7` |
| Replay | all six logs **Verified OK** (246 records) |

## 3. The report diff — convergence achieved

His artifact (saved by Imree from the auto-mail) vs ours, joined on `game_uid`:
**key sets identical · `final_result` exact · every sub-game's substance agrees ·
`timezone` and `groups` now match (his Round-20 fixes verified live).** Remaining
differences, each understood and routed:

- **`github_commit`** — complementary own-columns BY DESIGN (ours `e650af3…`, his
  `87199cf…` — clean, no `-dirty`; his tracked-modifications fix verified). Closed
  fully by the agreed commit-in-negotiate declaration (kit PROPOSED entry pending).
- **`mutual_agreement`** — his enriched shape + different hash; both preimage
  constructions go to the kit registration both teams agreed (each side signs its
  own records — difference by construction, to be made legible to graders).
- **Sole residual defect:** his handshake identity block now carries `group_name` +
  `members` (our declaration's column for him finally fills) but `hardware_spec`
  arrived all-null and `llm_model` empty — flagged to him.

## 4. Standing

Per his Round-21 letter: "Counted T after this one settles clean." It settled clean.
The counted gate is met; scheduling is Imree's and theirs. Counted-run reminders:
recipient = the lecturer alone, set by Imree before the match; truthful game-count
declaration (rules 37–38); clean committed tree (both sides now emit their exact
commit).
