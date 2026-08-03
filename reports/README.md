# `reports/` — what is official and what is a rehearsal

Read this first: the folder name tells you whether a game **counted**.

| Path | What it holds | Scores? |
|---|---|---|
| `counted-series/<group_id>/` | **The official counted league series** — one per opponent, played under `--counted`, reported by email to the lecturer. | **Yes** |
| `friendlies/<group_id>/` | The most recent **uncounted warm-up** against that opponent (played under `--rehearsal`; the lecturer is structurally unreachable in that mode). | No |
| `friendlies/archive/<date>-<label>/` | Earlier warm-up snapshots, kept because every run of one pairing overwrites the last (see below). | No |

Nothing counted ever lands outside `counted-series/`, and nothing uncounted ever lands
inside it — the two trees are written by the two run modes and never share a directory.

Uncounted warm-ups are not clutter — the book asks for them: ch. 9.2.1, *"משחקי חימום
(warm-ups) שאינם נספרים — מותרים ואף מומלצים, לצורך בדיקה וכיול לפני המשחק הנספר"*
("warm-ups that do not count are permitted and even recommended, for testing and calibration
before the counted game"). The same section fixes **one counted game per opponent**, so a
pairing can have many rehearsals and exactly one official series.

**Why rehearsals need archiving at all.** A pairing's `game_id` and `game_uid` are *derived*
(sorted group ids + the signed terms), so they are identical for every game between the same
two teams. Every run therefore writes the same filenames, and a later run overwrites an
earlier one in the working tree. Archiving a snapshot before the next window is how a
rehearsal survives as evidence.

**The `<group_id>` leaf is not our naming choice** — the reference implementation writes each
peer's four artifacts into a folder named after its own group id (`Path(out)/group_id`) so
that two peers on one machine cannot collide (they share a `game_id`, and roles alternate).
We keep that leaf for conformance and choose only the parent, which is what makes
`counted-series/` possible.

**Telling them apart from the artifact alone** (no folder needed): a counted result's
`final_result.games_played_including_this` counts this game for both teams, and
`diversity_reward_applied` can be true for the winner of a first meeting. A warm-up's
counters stay at zero and its rewards are always false.

## The four templates in every set

`declaration_<game_id>.json` (identity + hardware of **both** teams, signed) ·
`config_<game_id>_g<NN>.json` (the agreed physics/scoring, identical on both sides) ·
`log_<game_id>_g<NN>.json` (step-by-step commit/reveal + nonce + hash, replay-verifiable) ·
`result_<game_id>.json` (per-sub-game scores + aggregate — **the binding report emailed to
the lecturer**). Our Hebrew per-sub-game `report_<game_id>_g<NN>.json` files ride alongside;
they are ours, not one of the book's four.
