# Archived friendly (uncounted) artifact sets

**One opponent, one pairing, several rehearsals.** Everything in this folder is an
**uncounted warm-up** against `anrbj666` (Alon Engel, Renat Karimov). The book permits and
recommends them explicitly — ch. 9.2.1: *"משחקי חימום (warm-ups) שאינם נספרים — מותרים ואף
מומלצים, לצורך בדיקה וכיול לפני המשחק הנספר"* — and only ONE game per opponent ever counts
for league points, so none of these carry any.

The **counted** series artifacts live in their own tree — `reports/counted-series/<opponent>/`,
never here. The most recent warm-up sits beside these folders in `reports/friendlies/<opponent>/`;
this folder keeps the older snapshots (see `reports/README.md` for the whole layout).

## `2026-07-25-first-friendly/`

The first external friendly, filed under the **pre-M7-17 naming convention**
(`imreeyal-vs-anrbj666`, each side naming itself first). M7-17 replaced that with the
reference's derived sorted pair (`anrbj666-vs-imreeyal`), so the same pairing appears under
two names across the repo's history. Evidence is never renamed after the fact — the files
stay exactly as they were emitted and are archived here instead, which is why a browsing
reader sees two naming lineages for what is one opponent. Result: imreeyal 75–35.

## `2026-08-03-warmups/`

The last warm-up window of 2026-08-03 (the day's series were played back to back; each run
overwrites the previous one's files, since a fixed pairing derives a fixed `game_id` and
`game_uid`). Kept as the final pre-counted snapshot: result-only mail policy (M7-40), the
four repo links in the result (M7-39), and a `mutual_agreement.sha256` byte-identical to the
opponent team's own artifact for the same window — the property both implementations adopted
in the Round-29/30 exchange. Result: imreeyal 30–90.

Raw JSONL event logs for the earlier windows are committed separately under
`docs/evidence/`; these folders hold the four-template JSON artifact sets
(declaration + per-sub-game config + per-sub-game log + result, plus our Hebrew per-sub-game
report files).
