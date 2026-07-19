# PRD — Gatekeeper & fairness rail (mechanism PRD, milestone M6)

> **Status: DRAFT (gate M6-1, awaiting Imree's approval).** Parent docs: `docs/PRD.md` FR-8
> (reliability rail) + FR-9 (gatekeeper + config precedence) + FR-11 (audit extensions),
> `docs/PLAN.md` §4 (reporting pipeline: quota → token bucket → DoS) + §10 (reliability &
> chaos) + §13 (M6 exit). Sources of truth: book ch.8/ch.9 + App B `rate_limiter_gatekeeper`
> (App F table 19 minimums) · reference `shared/gatekeeper.py` + `shared/rate_limiter.py`
> **@960499fd — oracle only, ADR-0002** · HW6 `tests/email/test_email_gatekeeper.py` pattern
> (frozen; mined). Covers TODO **M6-5 / M6-7** + one scope rider (§5, FR-11 debt). Consumes
> `shared/config` (FR-9 precedence, already enforced), `peer/p2p` loop seams, `domain/scent`
> (read-only, for the §5 check).

## 1. Scope & non-goals

**In scope:** (M6-5) `shared/rate_limiter` + `shared/gatekeeper` — the single doorway for ALL
external calls (email, LLM): quota → token bucket → DoS lock, limits from `rate_limits.json`
(≥ signed minimums, loader-asserted — already live in `shared/config.load_rate_limits`);
(M6-7) watchdog thread + state persistence + controlled shutdown (the FR-8 pieces the tree
does not yet have — today only the turn-deadline discipline exists) + the chaos-drill harness
(`tests/chaos/`, PLAN §10 table) with committed drill evidence; (§5 rider) the FR-11
scent-physics audit check + its drill — **proposed to ride M6-7 with a TODO-line amendment**.
**Non-goals:** artifact/email content (PRD_reporting; the email sender merely CALLS
`service="email"` here) · M3-8 · any wire change (constraint #13 untouched: the §5 check
reads revealed audits + our own verbatim logs only) · inbound MCP throttling of the OPPONENT
(their call rate is their business; our defense there stays the wire validation + state
machine — a deliberate reading of "gatekeeper" as protecting OUR outbound external resources,
matching the reference's design; documented in §2).

## 2. Book/reference model absorbed & our adaptations

**Reference (oracle):** `ApiGatekeeper(config, service)` — every LLM/email call goes through
`execute()`: rate limiting, FIFO queuing on overflow, bounded retry on transient provider
errors, call logging, `get_queue_status()` observability. `RateLimiter`: sliding-window
requests-per-minute + bounded FIFO wait queue (`max_depth`, `drain_interval_seconds`,
`timeout_seconds`) + **injectable clock** (deterministic, instant tests — we adopt this
wholesale). Its `rate_limits.json` carries a `queue` block and per-service limits; ours is
still flat — extended here (§6).
**Our adaptations (PLAN §4 names three stages the reference only partially has):**
(1) **Quota manager** — budget ledgers checked BEFORE queueing: LLM tokens vs the signed
`token_budget_per_series`; email sends vs a private per-day cap. Over budget → refuse loudly
(never silently degrade a counted series into a budget breach).
(2) **Token bucket** — sliding-window rpm + a `concurrent_requests` semaphore (the signed key
the reference never enforces) + bounded FIFO queue; overflow/timeout → `RateLimitError` the
caller handles (queue, never crash).
(3) **DoS lock** — a circuit breaker on provider-side pushback: HTTP 429/refusals honor
`retry_backoff_sec` (escalating, capped by `max_retries`); repeated failure bursts trip a
cooldown lockout with a loud JSONL event, auto-reset after the cooldown. Protects our quota
AND the provider (App E fairness posture).
Both are `shared/` citizens (PLAN §3); threads-safe (locks; called from watchdog/inbox seams
only, guidelines §15); every numeric from config (constraint #5).

## 3. M6-5 — gatekeeper build

`shared/rate_limiter.py` (window + semaphore + queue + clock protocol) ·
`shared/gatekeeper.py` (`ApiGatekeeper` with quota + DoS stages, service registry `"email"` /
`"llm"`, `get_queue_status()`, JSONL `gatekeeper` events via an optional LogFn). The mock-LLM
CI path and the M6-4 email sender both route through it from birth — no external call ever
bypasses the doorway (a negative test greps the seams: `infra/` adapters hold no direct
retry/sleep logic). **DoD (M6-5 + PLAN §13):** synthetic-load test — N threads × M calls on a
fake clock: every call granted, queued-then-granted, or cleanly refused; zero crashes; FIFO
order preserved; queue refuses at depth. 429-backoff test: fake provider 429s twice → recorded
sleeps follow the `retry_backoff_sec` schedule → third attempt succeeds; breaker test: burst
of failures → lockout event → cooldown → recovery.

## 4. M6-7 — watchdog, persistence & chaos-drill harness

**Watchdog (FR-8, new):** a thread monitoring the peer-loop heartbeat (the loop beats every
iteration); silence past the signed `watchdog_timeout_sec` → **persist** a state snapshot
(`state_<game_uid>.json` under the logs root, git-ignored: machine state, step, positions we
own, sealed-record count, outcome-so-far) → **controlled shutdown** (stop server, flush JSONL,
exit loudly — a stall is never a silent freeze). Threads only at this seam + inboxes
(guidelines §15).
**Chaos harness (`tests/chaos/`, sdk-driven over in-process fakes; PLAN §10 table):**

| Drill | Defense asserted |
|---|---|
| kill transport mid-commit | deadline → TECHNICAL_LOSS + watchdog persistence fires |
| delay to the deadline edge | game CONTINUES (no false technical loss) |
| malformed TurnMessage | wire validation rejects; machine collapses per App E 3–7 |
| duplicate / replayed turn | step-continuity rejection (no double state advance) |
| oversized hint | `hint_max_words` rejection path |
| audit with tampered record | re-hash mismatch → audit fails, result derived not declared |
| fabricated scent grid (§5) | scent-physics mismatch → evidence-grade log event |

Each drill asserts its SPECIFIC defense (not just "no crash") and lands in keyless CI; a
committed run of the full battery becomes `docs/evidence/m6-chaos.md` (README evidence,
FR-8).
**Live-drill note:** the tunnel-kill variant against a real cloudflared tunnel is
operator-run evidence (needs Imree at the terminal), not CI.

## 5. Scope rider — FR-11 scent-physics audit check (decision D2)

The audit-side check PLAN §4 promises ("re-derive their expected trail from revealed moves +
locked model; diff vs the grids they transmitted") has no TODO line — PRD_gui_replay §1
deferred it to "M6 audit scope", and M4's inbound-verbatim logging exists precisely to feed
it. **Proposal:** build it at M6-7 as `peer/` post-settlement analysis + the table's last
drill; amend TODO M6-7's line to name it. Semantics per SQ3 (unchanged stance): grids are
unauthenticated and NEVER sealed, so a mismatch is **evidence-grade only** — a loud
`scent_physics_mismatch` JSONL event + dispute documentation; it never flips a result and
never feeds belief math (M3-8 boundary). Disclosed in KNOWN_LIMITATIONS as proving
inconsistency "only to us".

## 6. Configuration

**`rate_limits.json` v1.01 (private, versioned):** keeps the five flat keys (each still ≥ its
signed App F table-19 minimum — existing loader assertion extends unchanged) + a new `queue`
block (`max_depth`, `drain_interval_seconds`, `timeout_seconds`) + optional per-service
overrides (`email`, `llm`) which may only TIGHTEN (≤ global operational, still ≥ signed
minimums — asserted). New private keys for the DoS breaker (failure threshold, cooldown sec)
and the email day-cap. `watchdog_timeout_sec` is already signed (`network_and_league`) — no
signed value changes; App F guard untouched. Persistence root under the `[paths]` TOML key
(introduced in PRD_reporting §8).

## 7. Decisions requiring approval (with the PRD)

- **D1 — gatekeeper protects OUR outbound external calls only** (email/LLM); opponent-facing
  DoS defense remains wire validation + state machine + deadline (reference-matching reading;
  §1 non-goal). Alt: inbound MCP throttling — rejected as fighting FastMCP's own layer.
- **D2 — scent-physics check rides M6-7** + TODO amendment (§5). Alt: own milestone line
  post-M6 — more ceremony, same code.
- **D3 — breaker/day-cap knobs are PRIVATE config** (new `rate_limits.json` keys, versioned)
  — they tighten behavior beyond the signed minimums, never weaken (same precedence rule).
- **D4 — watchdog persistence artifact** is a git-ignored operational snapshot (not a signed
  artifact; disputes ride the JSONL + sealed records, not this file).

## 8. Test plan (TDD; keyless CI)

Unit: limiter — window math on a fake clock, semaphore cap, FIFO order, depth refusal,
timeout; gatekeeper — quota refusal pre-queue, 429 schedule, breaker trip/reset, status
shape; config — v1.01 parsing, per-service tighten-only assertion, minimums breach list.
Watchdog: heartbeat stall on a fake clock → snapshot written (shape-validated) + shutdown
callback fired; healthy loop → no fire. Chaos: the §4 table, one test file per drill
(150-line rule), each asserting its named defense + the JSONL event trail. Integration: a
full local mini-game with watchdog armed + gatekeeper-wrapped (mock) email at settlement —
green end-to-end. Coverage ≥85%/≥90% core; `mypy --strict`; ruff + format clean.

## 9. Acceptance criteria (binary — PLAN §13 M6 exit + gate hygiene)

- Gatekeeper limits proven by test: synthetic load queues and never crashes; 429 backoff
  honored; breaker observed tripping and recovering — all keyless CI.
- Watchdog fires on an induced stall: snapshot + controlled shutdown observed in a drill.
- Every PLAN §10 drill's defense observed; battery green in CI; committed evidence doc.
- Scent-physics drill (if D2 approved): fabricated-grid mismatch produces the evidence event;
  result unchanged; belief untouched (M3-8 boundary test).
- No signed value changed; `rate_limits.json` still ≥ minimums (loader test); kit CORE
  vectors green; sync ritual + TODO ticks + PROMPTS.md per PR.

## 10. Build order & PRs

M6-5 (limiter → gatekeeper, one PR) lands **between M6-3 and M6-4** (PRD_reporting §12) so
the email sender is born gated → M6-7 (watchdog + persistence → chaos battery + evidence, one
PR, review E per TODO) closes the phase alongside M6-8. Same chain discipline as ever.
