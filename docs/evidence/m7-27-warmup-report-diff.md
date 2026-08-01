# M7-27 — Cross-team warm-up + report diff (2026-08-01)

The uncounted warm-up agreed with team anrbj666 after the Rounds 15–19 arc: prove the
`game_uid` join end-to-end, prove the new negotiate declarations (M7-22 uid, M7-25
info_mode) and the M7-23 frame check against an independent implementation, then diff
the two auto-fired reports field by field. Both sides fielded their real tuned brains
(agreed 2026-07-24); full locked stack under `--rehearsal`; recipients = the two teams
only, never the lecturer.

## 1. The two windows

**T=15:30 IL — burned, opponent side, killed per the T-protocol.** s1 played and
settled clean (15:30:44). Then the opponent thief's handshake declared sub-game **1**
while our s2 police peer was on **2**; the M7-10 index check refused it — 163
push/refuse pairs over ~2.5 minutes, every refusal naming the agreed reason
(`"one game cannot carry two indices"`) — then both opponent edges went 502 and their
report email fired one sub-game deep (their side believed the series was over). Our
side was killed cleanly (zero orphaned processes verified); our report correctly did
NOT fire on a partial series. The refusal did exactly what it was built for after the
phantom-s6 incident: the mismatch surfaced at negotiate, in-window, instead of as two
irreconcilable artifacts after play.

**T=15:40 IL — the series, complete.** Six sub-games strictly s1→s6, roles
alternating (we play thief on odds — opponent parity), ~35 s per survival game, series
exit 0, one report auto-fired to the three friendly recipients.

## 2. Result

**imreeyal 60–40 (4 sub-games to 2), zero tokens both sides.** Our thief survived all
three of its games; our cop captured the opponent's rematch-built thief in s2
(13 steps) and was survived in s4/s6. Artifact:
`reports/imreeyal/result_anrbj666-vs-imreeyal.json` (sorted-pair M7-17 names,
first live use).

## 3. Verification (all from the committed logs, `m7-27-warmup-g0*.jsonl`)

| Check | Result |
|---|---|
| Replay verification | all six logs **Verified OK**, 378 records, zero problems |
| One `game_uid` | `e351176a-8883-7ce6-aad8-8a50bff637d7` in every settled row + both teams' artifacts |
| M7-25 info_mode lock | `info_mode_sha256 = 020947da…` declared and matching, **all six handshakes, both sides** |
| M7-23 frame check | **zero** `scent_frame_refused` across the series (~1,700 records) — the FP=0 prediction held against independent honest traffic |
| M7-26 concede pin | s2 is a live cop_capture ending refused by nothing (both concede shapes exempt) |
| M7-10 index/role check | 0 refusals in the played series; 163 correct refusals in the burned window |
| Audits | `audit_ok: true` all six; `opponent_claim` matches every outcome |

## 4. Report diff (their artifact vs ours, joined on game_uid)

Their artifact arrived by auto-mail (saved locally by Imree). **Key sets identical;
`final_result` matches exactly; every sub-game's result/score/roles/winner/tie/tokens/
audit agree.** The Round-14 promise — match on game_uid, field by field, no postmortem
— held on the substance. Four deltas, none touching results, each side off the
reference sample somewhere:

| Field | Ours | Theirs | Sample says | Deviation |
|---|---|---|---|---|
| `log_files` | subdir-prefixed | flat names | flat names | **ours** (fix = M7-28) |
| `timezone` | `Asia/Jerusalem` | `UTC` | `Asia/Jerusalem` | theirs |
| `groups` | flat id list | enriched objects | flat id list | theirs |
| `mutual_agreement` | `{sha256, confirmed}` | enriched + different hash | `{sha256, confirmed}` | theirs (hash difference is by construction — each side signs its own records; preimage registration proposed) |

**`github_commit`: a mutual gap with a book mandate behind it.** The book requires the
exact commit played per sub-game in the closing email's JSON; the reference's own
sample emits `"unknown"` (book-vs-reference contradiction — we resolve toward the
book). They fill their own column (value carries `-dirty`); we fill neither — our
sealed step-0 records the real hash (`peer/sealing.py` `current_commit_hash()`) but
`report/emit.py` never wires it through (its own comment says so — an M6-3 leftover).
Fix = **M7-28** (own column; the opponent column needs a negotiate-extras declaration,
proposed to the opponent team).

Opponent identity: their artifact names our members correctly (they read the identity
block we send at handshake) but their handshake sends only `group_id`, so our
declaration's block for them is nulls (no members / llm_model / hardware_spec). Asked
them to mirror. `smell_binding` was not declared by either side (legal — omission
never refuses; their drill needs its own window).

## 5. Standing decisions

Per Imree (2026-08-01): fix our two deltas (M7-28), then **one more friendly**, and
only then the counted series — counted play starts when both teams' artifacts converge
with nothing left on the list.
