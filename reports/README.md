# `reports/` — what is official and what is a rehearsal

Read this first: the folder name tells you whether a game **counted**, and every
subfolder is one **opponent**.

| Path | What it holds | Scores? |
|---|---|---|
| `counted-series/<opponent>/` | **The official counted league series against that team** — exactly one per opponent, played under `--counted`, reported by email to the lecturer. Ten opponents, ten folders, twenty artifacts each. | **Yes** |
| `friendlies/<opponent>/` | That pairing's **uncounted warm-ups** (played under `--rehearsal`; the lecturer is structurally unreachable in that mode): the most recent set at the top, earlier dated sessions in subfolders. | No |
| `friendlies/snapshots/<date-label>/` | Whole-tree dated snapshots (every pairing's then-current files together), taken to preserve evidence around specific windows — see each snapshot's name. | No |

Nothing counted ever lands outside `counted-series/`, and nothing uncounted ever lands
inside it — the two trees are written by the two run modes and never share a directory.

Uncounted warm-ups are not clutter — the book asks for them: ch. 9.2.1, *"warm-ups that do
not count are permitted and even recommended, for testing and calibration before the counted
game"*. The same section fixes **one counted game per opponent**, so a pairing can have many
rehearsals and exactly one official series.

**Why rehearsals need archiving at all.** A pairing's `game_id` and `game_uid` are *derived*
(sorted group ids + the signed terms), so they are identical for every game between the same
two teams. Every run therefore writes the same filenames, and a later run overwrites an
earlier one in the working tree. Archiving a snapshot before the next window is how a
rehearsal survives as evidence.

**A note on the write-time layout.** The reference implementation's writer places each peer's
artifacts under a folder named after its *own* group id (`Path(out)/group_id`, an
anti-collision convention for co-located peers), and our writer keeps that convention for
conformance — so a live run creates `<out>/imreeyal/…`. The **submitted archive** you are
reading is curated per *opponent* instead, because that is the axis a reader actually browses
by; file names are untouched, and every artifact's `game_id` still states the pairing.

**Telling counted apart from the artifact alone** (no folder needed): a counted result's
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
