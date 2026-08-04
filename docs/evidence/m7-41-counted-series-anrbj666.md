# M7-41 — The first COUNTED series: imreeyal vs anrbj666, played and reported

**2026-08-04, T = 01:00 Israel. One `copthief series --counted` invocation played all six
sub-games and fired the ONE report to the lecturer with no human step between the sixth
settlement and the mail. Series exit 0.**

Sealed commits — ours **cop `650dbd5`, thief `160d173`** (both clean trees, pushed);
theirs **police `c02793f`, thief `2df8dad`**, matching the hashes they declared in writing
before the T. Both sides' commit columns agree in both artifacts.

## Result

**anrbj666 wins 30–90, six sub-games to nil.** Artifacts:
`reports/counted-series/imreeyal/` (20 files, the counted tree's first use).

| Sub-game | Our role | Outcome | Steps | Audit |
|---|---|---|---|---|
| 1 | thief | cop_capture | 13 | OK |
| 2 | police | thief_survival | 34 | OK |
| 3 | thief | cop_capture | 13 | OK |
| 4 | police | thief_survival | 34 | OK |
| 5 | thief | cop_capture | 13 | OK |
| 6 | police | thief_survival | 34 | OK |

One shared `game_uid e351176a-8883-7ce6-aad8-8a50bff637d7` across all twelve halves; every
mutual audit clean; **zero scent-frame refusals and zero agreement refusals**; all six logs
replay **Verified OK** (committed as `counted-anrbj666/counted-*.jsonl`).

## League fields (the graded ones), truthful and counted

```
games_played_including_this   : {imreeyal: 1, anrbj666: 1}
first_meeting_between_groups  : true
diversity_reward_applied      : {imreeyal: false, anrbj666: true}
```

The diversity reward is **points for a victory over a new opponent** (App F table 18 row 2,
`קבוע 10`; ch. 9.2.1 *"ניצחון על יריבה שטרם שיחקתם מולה מזכה בתגמול המלא"*), so it goes to
the winner — here, them. Our ledger advanced to `counted_games_played = 1`,
`counted_opponents = ["anrbj666"]` in both repos, because a stale ledger would make the
NEXT counted game declare a false first meeting (rule 38).

## The report

Fired automatically at settlement: `{"action": "send"}`, recipients
**`rmisegal+uoh26finalgame@gmail.com` alone**, one attachment
(`result_anrbj666-vs-imreeyal.json`, the body being the same bytes). Result-only per the
M7-40 policy both teams adopted. Rule 32 requires the automatic send; rule 35 zeroes both
teams if either side fails to report, so each team mails its own copy.

## Cross-team agreement — the property rule 35 actually tests

The opponent's independently produced report agrees **field-for-field on every graded
value**: `mutual_agreement.sha256` byte-identical (`0bcf3c07…`), `total_score`,
`sub_games_won`, `winner_group`, `games_played_including_this`,
`first_meeting_between_groups`, `diversity_reward_applied`, `game_uid`, `links.github`,
and both teams' per-sub-game commit columns. The only differences are the two documented
classes: per-peer wall-clock timestamps (deliberately outside the signature — the
reference excludes them because two peers' clocks legitimately differ) and their shorter
`_schema` prose.

## Provenance of the machinery

Nothing in this series was exercised for the first time. The same stack had played five
clean warm-up windows in the preceding hours (2026-08-03 evening → 2026-08-04 00:33), four
of which were diffed against the opponent's artifacts with the same result. The counted run
differed in exactly two ways: the `--counted` flag (arming the App F rows, the counting
keys, and the lecturer's reachability) and the recipient. The interlock was re-proven both
directions immediately before the T — the counted config under `--counted` preflights to
`action: send` for the lecturer, and the *same file* under `--rehearsal` refuses with *"the
lecturer is addressable only from a counted series"*.

## Honest note on the competitive result

We lost every sub-game. Our thief was captured at step 13 in all three of its games and our
cop failed to convert in all three of its own; the pattern had appeared in the two windows
immediately before the counted series, after the opponent deployed an evader fix. Under
the book's one-counted-game-per-opponent rule this result is final for this pairing. It is
recorded here as played.
