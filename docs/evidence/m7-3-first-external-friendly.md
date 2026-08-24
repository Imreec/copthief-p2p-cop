# M7-3 — The first external friendly: imreeyal vs anrbj666, played and auto-reported

**2026-07-25, T = 23:30 Israel time (seventh window of the evening). Cop repo at main
`129c3ff` (M7-11 + M7-11b), thief repo at `3a0dc9f`. One `copthief series` invocation
played all six sub-games and fired the ONE report with no human step between the sixth
settlement and the mail leaving.**

## Result

Winner **imreeyal, 75–35**, five sub-games to one (artifact
`reports/friendlies/anrbj666/2026-07-25-first-friendly/result_imreeyal-vs-anrbj666.json`
— archived there 2026-08-04 under the friendlies tree (`reports/` splits counted-series
from friendlies; see `reports/README.md`); the filenames are the pre-M7-17 self-first
convention and are deliberately unchanged; series exit 0; report
`{"action": "send"}` to `imreeyal.copthief@gmail.com`,
`alonisrael.engel@gmail.com`, `imree.c@gmail.com`).

| Sub-game | Our role | Outcome | Steps | Replay |
|---|---|---|---|---|
| 1 | thief | thief_survival | 35 | Verified OK, 70 records |
| 2 | police | **cop_capture** | 31 | Verified OK, 64 records |
| 3 | thief | thief_survival | 35 | Verified OK, 70 records |
| 4 | police | thief_survival | 34 | Verified OK, 70 records |
| 5 | thief | thief_survival | 35 | Verified OK, 70 records |
| 6 | police | **cop_capture** | 11 | Verified OK, 24 records |

One shared `game_uid e351176a-8883-7ce6-aad8-8a50bff637d7` across all twelve halves;
every mutual audit clean (`audit_ok` both sides, opponent records verified per game).
Logs committed beside this file as `m7-3-friendly-g01..06.jsonl`; the six per-game
configs, declaration, per-game reports and result are committed under
`reports/friendlies/anrbj666/2026-07-25-first-friendly/`.

**Competitive note:** sub-games 2 and 6 are the first cop captures recorded under
`multiplicative_book_v1` by either team — every previous game under the book model, in
either team's history, ended in survival (cf. `docs/evidence/m3-belief-eval.md` and the
wire-shape balance study). The pair lock for this series was book-v1 (the 2026-07-24
rehearsal agreement); our evader survived all three of its games.

## Cross-team verification

The opponent's own report (their email id `19f9afb3cfff26bb`, artifact saved at
`FinalProject/otherStuff/result_anrbj666-vs-imreeyal.json`) agrees **field-by-field on
every game value**: winner, totals 75–35, sub-games won 5–1, per-sub-game scores and
outcomes, zero tokens both sides. Two discrepancies, both evidence-grade and raised
with the opponent team:

1. **`game_uid` mismatch (substantive):** their report carries `2f0c25a9…` instead of
   the flat-terms-derived `e351176a…`. *(Diagnosis corrected 2026-07-26 by the opponent
   team, whose account supersedes our first read: NOT a freshly minted id — their
   derivation was exactly as deterministic as ours but hashed the WRONG INPUT, their
   whole `game.json` rather than the reference's flat negotiated terms. Their four
   artifacts were internally consistent on `2f0c25a9…` — the sneakier failure class,
   since a self-joining bundle looks healthy and only the CROSS-TEAM join breaks.)*
   Under App E rule 35 two counted reports with different uids would read as
   contradictory. Ours provably carries the flat-terms uid (all six logs + audits +
   replays). Fixed on their side same day, verified three ways (their emitted uid now
   equals `e351176a…` to the digit, pinned by test, reproduced in a live two-peer run).
   **Residual mutual finding:** the uid never crosses the wire — each side derives it
   independently — so this divergence was SILENT for the entire series and surfaced
   only at the report diff; a declare-at-negotiate check (the M7-10 pattern) is the
   proposed closure.
2. **`game_id` order (cosmetic, convention settled next day):** each side named itself
   first (`imreeyal-vs-anrbj666` vs `anrbj666-vs-imreeyal`). Resolved 2026-07-26: the
   reference *derives* the id by sorting the pair (`derive_game_ids`), the kit pinned
   it (SPEC §4), and our impl adopted the sorted form as M7-17 — their naming already
   matched it.

## The seven windows (the campaign ledger)

The series took seven scheduled windows; every failure was a launch-time default,
every abort was clean and pre-report, and neither team ever emitted a false artifact.
Burned-window logs are preserved under git-ignored `logs/burned-*/`.

| T (IL) | Verdict | Root cause |
|---|---|---|
| 18:40 | theirs | thief-role service never bound (sequential orchestrator binds one role at a time) |
| 19:00 | ours | cloudflared launched with an unquoted spaced config path → connector without ingress → 502-forever |
| 21:35 | theirs | parallel-runner switch dropped their wire flag; committed default `bookletter` → terms-less greetings, refused (kit CORE) |
| 21:52 | ours | run config still declared `subtractive_chebyshev_v1`; the pair lock is book-v1 → scent-lock refusal (their `934c220d…`) |
| 22:20 | theirs (+cascade) | their s2 window resumed a dead window's stored context off transport acks and went silent; 180s-patience math cascaded — but s1/s4 settled as the first real cross-team auto-series games |
| 23:10 | shared | protocol conflict: their new tempo barrier binds services per-window; the four-406-at-T rule couldn't hold — retired for "s1 counterpart at T; later edges judged by their own handshakes" |
| 23:30 | **played** | — |

Hardening that came out of it, all verified live at T7: quoted tunnel launch + an
end-to-end loopback gate (a bare 502 check cannot distinguish a healthy-idle tunnel
from a connector with no ingress); all local gates complete BEFORE T so nothing but a
real peer ever answers on the series path (a lax opponent transport had read our gate
listener's HTTP responses as delivery acks); stale same-`game_id` logs archived at
launch (the logger appends, and a burned attempt must never pollute a later
aggregation); `M7-12`'s refusal wording (terms-absent vs terms-differing) so the
21:35-class fault self-diagnoses from the refusal line alone.
