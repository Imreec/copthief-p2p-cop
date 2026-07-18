# PRD — GUI, replay & observability (mechanism PRD, milestone M4)

> **Status: DRAFT (gate M4-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-10
> (+ FR-11 data feed), `docs/PLAN.md` §7 (JSONL contract) + §9 (GUI & replay) + §13 (M4 exit).
> Sources of truth: book ch.7 (pp.69–75) · App E rules **8** (live UI shows local truth only —
> mandatory), **9** (never render the objective board live — project disqualification), **19**
> (any hash mismatch at audit = technical disqualification, the "iron rule"), **20** (a replay
> viewing application is a threshold condition for submission) · App C (screenshots of the live
> heatmap AND the viewer's Verified OK are submission artifacts). Covers TODO **M4-2 / M4-3 /
> M4-4** plus the **inbound-logging gap** flagged in both M3 friendly evidence docs
> (`docs/evidence/m3-scent-friendly.md` §Limitation, thief `docs/evidence/m3-full-pairing.md`
> §Residual note). Consumes `domain/belief` (M3-3), `peer/replay` (M1-8), `domain/crypto` (M1-3).

## 1. Scope & non-goals

**In scope (M4):** (L) the observability log schema — inbound-verbatim events + the belief/
transition/decision events PLAN §7 already promises; (M4-2) the live per-peer GUI: belief
heatmap + turn banner, local truth only; (M4-3) the replay verifier/viewer: per-step
cryptographic re-verification → **Verified OK / TAMPERED**; (M4-4) the post-audit
belief-vs-truth overlay + belief-error curve PNG export.
**Non-goals:** scent/belief model internals — **M3-8 stays blocked** (Alon inputs → PRD_scent
amendment + ADR-0004 v2, approve-before-build; nothing here touches `domain/scent` or
`domain/belief` math) · the audit-side scent-physics **check** (FR-11, M6 audit scope — M4 only
archives the data that makes it possible) · report artifacts/email (M6) · brains (M5) ·
**anything on the wire: M4 changes no wire format, canonicalization, or hashing** (constraint
#13 not triggered; the verifier consumes `domain/crypto.verify` as-is).

## 2. Book model absorbed (ch.7) & our documented adaptations

The chapter defines **two non-overlapping axes**: live monitoring ("what is happening now?")
and retrospective witness ("did the past happen as claimed?"). Binding points we implement:
heatmap = the belief grid rendered as intensifying red, per side, symmetric (§7.3.1) · turn
banner green **YOUR TURN** when the inbound turn hands us the move, gray **LOCKED** from the
moment our commit is transmitted (§7.3.2) · replay loads the final log, steps forward/back
with controls, re-verifies every record, and one mismatch anywhere = red **TAMPERED** banner +
match void, no appeal (§7.4, rule 19) · the book's `verify_step` sketch (`nonce|move`) is
explicitly simplified — the real seal covers the full record `{state, move, intent, hint,
position, step}` per ch.5, which is exactly what our `peer/replay` already re-hashes.
**Adaptations (academic-freedom, stated here as the record):** (a) the book's input-lock
("clicks ignored while LOCKED") presumes a human mover; our agents are autonomous, so the live
view is **display-only** — the banner visualizes the state machine and there is no move input
to ignore (strictly stronger than the requirement); (b) the book names Tkinter/PyQt as
examples — we take **Tkinter (stdlib)**, decision D1 §8; (c) the book's log example is a JSON
file — ours is the M1-8 JSONL event log, already richer than the sketch.

## 3. Workstream L — the observability log schema (build first; feeds everything below)

**Gap being closed (M3 evidence, both repos):** the JSONL archives our outbound turns verbatim
but nothing inbound — the reference's grids/declarations were provable only via sealed-record
side-effects. PLAN §7 also promises belief snapshots, state transitions, and decision
provenance that the logger does not yet emit.

New events, all emitted at existing seams (`peer/p2p` loop, `peer/match`, server inbound):

| Event | Payload | Seam |
|---|---|---|
| `agreement_received` | opponent negotiate dict, **verbatim, pre-verification** | `run_peer_game` handshake |
| `turn_received` | inbound TurnMessage dict, **verbatim, pre-validation** (rejected messages are archived too — dispute evidence) | loop, before `handle_receive_turn` |
| `audit_received` | opponent AuditPayload dict, verbatim | `_settle` |
| `transition` | `{from, to, trigger}` | state-machine advance |
| `belief` | `{step, grid: {"r,c": p}, argmax}` snapshot after the inbound update pipeline | post-update in `peer/turns` seam |
| `decision` | `{step, brain, move, intent}` provenance (local secrets — the log is local; evidence is committed post-game only) | seal time |

**Honest verbatim definition:** FastMCP hands the tool a parsed dict; pre-parse wire bytes are
not accessible at our seam. "Verbatim" = the inbound dict archived losslessly under the
protocol's canonical dumps — sufficient to re-derive every hash, because commits are computed
over canonical dict serialization (kit CORE), and sufficient for the M6 scent-physics check
(their transmitted grids, per step, per sender, now on disk). Documented in the module
docstring. **Compat:** replay/GUI tolerate logs with or without the new events — the M2/M3
evidence logs must keep verifying unchanged (regression-pinned). `seq` still makes truncation
visible; `JsonlEventLogger` gains `mkdir(parents=True)` (closes the thief-repo fresh-path trap).

## 4. M4-2 — live GUI (belief heatmap + turn banner)

**Architecture (one stream, two consumers):** the `LogFn` seam fans out: file logger + a
bounded thread-safe GUI queue (threads only at existing seams, guidelines §15). The live
window renders **exclusively from that event stream** — and since the stream carries no
opponent position before the audit (SQ3: grids are unauthenticated fields, not positions),
**rules 8–9 hold by construction**, not by discipline. Referee-mode/full-info structures are
never imported by `gui/`; the `LiveViewState` model has **no opponent-position field to
populate** (negative test pinned).
**Layout (book fig. 9):** N×N grid — belief probability as red intensity, own position marked,
known barriers marked; banner **YOUR TURN** (green) in `COMPUTING_MOVE`, **LOCKED** (gray) in
all other non-terminal states, outcome text at terminal; step counter + last in/out hint.
**Structure:** `gui/models/` pure + tested (heatmap cell shading from a belief dict, banner
state from `GameState`, view-state fold over events) · `gui/windows/live.py` thin Tkinter
shell, coverage-omitted (D3 §8). **Entry:** `copthief run peer --gui` (primary) and
`copthief run local-match --gui` (dev: two windows, one process), via the sdk facade (FR-14).
**DoD:** screenshot from a real game saved to `assets/` (localhost is standing-authorized; a
tunnel friendly for a nicer screenshot needs Imree's word).

## 5. M4-3 — replay verifier & viewer (Verified OK / TAMPERED)

**Engine (pure, extends `peer/replay`):** per record, the M1-8 chain — traveled commit ==
revealed commit → record re-hashes to its commit (`domain/crypto.verify`) → traveled hint ==
revealed hint — extended to walk **both** sides from the audits (and to cross-check
`turn_received` events when present, closing the loop the M2/M3 logs couldn't). Verdict is
**binary and exact**: `"Verified OK"` iff zero problems, else `"TAMPERED"` (book's strings;
internally every problem is still enumerated for the dispute log). Deterministic: same log →
same verdict, property-pinned.
**Viewer:** `gui/windows/replay.py` — board rendered from **post-audit revealed records**
(objective replay is legal retrospectively; rules 8–9 constrain only the live view — book §7.2
draws exactly this line), step forward/back controls (book §7.4), verdict banner green/red.
Headless verdict for CI/scripts: `copthief replay --log <path>` prints the verdict JSON;
`--gui` opens the viewer.
**DoD (both observed, committed as evidence):** a real M2/M3 evidence log → Verified OK; a
mutated copy (one field of one sealed record) → TAMPERED. CI keeps a permanent
mutation-matrix test: for **each** sealed-payload field {state, move, intent, hint, position,
step} + nonce + commit, an in-memory single-field mutation of a committed real log flips the
verdict to TAMPERED (rule 19's "no almost-match", made a regression).

## 6. M4-4 — belief-vs-truth overlay + belief-error curve

**Post-audit only (FR-10):** truth = the opponent's revealed audit trajectory (their sealed
`position` per step — available exactly when an audit is in the log, never before). Belief
history = the logged `belief` snapshots (workstream L), NOT a recomputation — the overlay is
evidence of what we believed at the time, immune to later model drift. **Metric identity with
M3-3:** per-step error = `BeliefFilter.belief_error` semantics (`1 − P(truth_cell)`), the same
number the M3 eval tables report (`strategy/belief_eval`), so README curves and arena tables
speak one language. **Outputs:** (a) overlay render — truth path drawn over the belief heatmap
timeline; (b) belief-error-vs-step curve; both exported as PNG for the README via matplotlib
Agg (D2 §8), data-prep pure + tested in `gui/models/overlay.py`, the render shell thin.
**Entry:** `copthief overlay --log <path> --out <png>` via sdk. **DoD:** overlay + curve
rendered from a real audited game (a fresh local game under the L schema; the M3 logs lack
belief events and stay replay-only).

## 7. Configuration

No signed values change. New **private** `game.toml [gui]` section (never crosses the wire):
refresh interval ms, window cell px, heatmap color anchors, PNG dpi/figure size — every
quantitative value config-owned (constraint #5), loader defaults + version bump in
`config_model`/`config`, App F guard untouched (no signed key involved).

## 8. Decisions requiring approval (with the PRD)

- **D1 — Tkinter (stdlib) for both windows.** Zero new runtime deps; the book names it first.
  Alt considered: PyQt — heavier dep, no grade upside.
- **D2 — matplotlib as a `viz` dependency group** (uv group, dev/analysis-time only; match-time
  code never imports it). First dep beyond fastmcp, hence flagged. Alt considered: hand-rolled
  stdlib PNG writer — real effort, worse output, and M5-7's notebook needs matplotlib anyway.
- **D3 — narrow the coverage omit** from `src/**/gui/*` to `src/copthief_core/gui/windows/*`:
  `gui/models/` (all logic) is pure, tested, and counted; only the Tk/matplotlib shells stay
  omitted (keyless CI opens no windows). Keeps the ≥85%/≥90% gates honest.
- **D4 — the L log schema** (§3 table) as the v1.1 log contract, backward-compatible; log-only,
  nothing on the wire.

## 9. Test plan (TDD; keyless CI)

Unit (happy + error): L — every new event lands with correct shape + seq; rejected inbound
still archived; parents-created logger; old-log compat. GUI models — banner mapping for every
`GameState`; heatmap shading monotone in probability, bounded anchors from config; view-state
fold over a recorded event stream; **negative: no opponent-position field / referee import in
`gui.models`**. Replay — verdict binary + exact strings; the §5 mutation matrix over a real
committed log; both-sides walk; determinism property; M2/M3 evidence logs Verified OK as
fixtures. Overlay — error series == `belief_eval` numbers on the same trace; truth extraction
only from audit events; PNG export smoke (file exists, non-empty, Agg backend). Integration:
full local mini-game under the new schema → replay Verified OK → overlay renders. Coverage
≥85% global with D3 in force; files ≤150 lines; `mypy --strict`; ruff clean.

## 10. Acceptance criteria (binary — PLAN §13 M4 exit + gate hygiene)

- Live-GUI screenshot captured during a real game, committed under `assets/`, referenced by
  evidence doc (App C artifact).
- Replay: a real M2/M3 evidence log → **Verified OK**; a mutated copy → **TAMPERED**; both
  observed and committed as `docs/evidence/m4-replay.md` (+ the CI mutation matrix green).
- Overlay + belief-error curve PNGs rendered from a real audited game, committed for the README.
- Inbound-verbatim events present in a real game's log; M2/M3 logs still verify (compat pin).
- Kit CORE vectors green (nothing on the wire changed); sync ritual done (mirrored `gui/` +
  tests; thief config/docs parity commits); TODO ticks + PROMPTS.md ride each PR.
- `domain/scent` + `domain/belief` internals byte-identical to M3 main (M3-8 blockade honored).

## 11. Build order & PRs

L (log schema) → M4-2 (GUI) → M4-3 (replay) → M4-4 (overlay), one branch/PR each off the
approved PRD, cross-model review per `docs/REVIEW_PROCESS.md`, stacked-chain lessons applied
(retarget children before merging parents; conflicts resolve branch-side; manifest regenerated).
