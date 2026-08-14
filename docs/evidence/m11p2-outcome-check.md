# Audit-time outcome re-derivation — the best2934 false-survival catch

## The live finding (friendly, 2026-08-14, g02/g04)

Our cop (unchanged M11 stack) sealed best2934's thief at (6,6) with walls
(5,6) + (6,5) completed at step 13 — rule-47 imprisonment, which the book
counts as capture. Their engine never emitted the boxed-in concession (the
scout's 08-12 offline prediction, reproduced live twice in byte-identical
form), so both sub-games settled as 35-step "survivals". Our auditor verified
motion, commits and continuity, said Verified OK — and never asked whether the
SETTLED OUTCOME matches the revealed trail it was holding. We co-signed a
result our own audit data refutes.

Fault split, honestly: live play cannot catch this (positions are hidden; the
concession is the imprisoned side's duty). The audit can — their disclosed
walk plus the final board makes the contradiction pure geometry — and ours
did not look. "Capture/score is derived, never declared" now applies
end-to-end.

## The check (`peer/outcome_check.py`, wired in `settle`)

On a thief "survival" claim: read the revealed walk (`revealed_positions`,
the M7-58 multi-spelling reader), take the final cell against the FINAL live
board, and emit a loud `outcome_mismatch` event when:

- the final cell IS a barrier cell (rule 46 — a wall on the thief), or
- the final cell is imprisoned AND was held across >= 2 revealed steps
  (rule 47; the hold requirement removes the final-turn-seal boundary where
  no concession window existed).

A run handed no coordinates emits `outcome_check_vacuous` instead of reading
as a clean pass (the M7-58 lesson). Deliberately a LOUD EVENT, never a
problems[] entry (the M6-7/SQ3 posture): a verdict change would accuse an
honest peer over a timing boundary; escalation to a counted-report gate is a
documented follow-up pending league validation of the event's precision.

## Validation

- 6 unit pins incl. the exact g02 geometry, the rule-46 form, a true
  survival, the final-turn-seal boundary (must stay silent), vacuity, and
  scope (police audits / capture claims exempt).
- **Live-oracle replay**: both real g02/g04 audits from the 2026-08-14
  friendly, fed byte-for-byte through the shipped check with the real final
  board, each produce exactly one `outcome_mismatch`
  (rule 47, cell [6,6], held_steps 31).

## League consequence

Games g02/g04 of the 2026-08-14 friendly are, by the book, cop captures at
step 13. The settled paperwork says survival on both sides — jointly wrong,
the rule-35-class shape. The fix on their side (emit the rule-47 concession)
plus written confirmation is a precondition for any counted leg with
best2934; the event gives every future series the receipt the league thread
needs, from our own logs, without accusing anyone of forgery.
