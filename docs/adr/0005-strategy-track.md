# ADR-0005 — Strategy track: belief + search, no-RL foundation

## Status

Proposed (drafted at the M5-1 gate; Imree's approval of the M5-1 PRD pair approves this ADR —
indexed in PLAN §14 / PRD §9 since Phase 2, written now that the decision lands with code).

## Context

Book ch.6 (§6.3/§6.3.1) offers three explicitly equal tracks for the move policy: (1) pure
heuristics — Bayesian belief map + Manhattan distance (the reference's shipped default), (2)
"your own heuristic algorithm" — richer deterministic policies incl. forward search
(minimax/expectimax against the belief), (3) reinforcement learning — optional, *not taught in
the course*, with the book's own reminder that many strong agents ship without it. The move
decision must be algorithmic in every track (App E rule 25; the LLM is verbal-layer only — the
book's mutual-consent exception for LLM-decided moves exists but is not taken by us). The graded
core is the strategy module (App F §5); reliability is the floor, strategy the score (PRD §2).
M3 landed the exact Bayes `BeliefFilter` (beats last-known baseline on every seed) and the
BrainBase seam; M5 must convert that perception edge into decision strength with committed,
reproducible evidence.

## Decision

Track (2): **deterministic search + engineered features over the exact belief** — expectimax +
barrier graph-surgery for the police brain, region-survival + articulation awareness + deception
timing for the thief brain — with **offline genetic tuning of the config-owned feature weights**
(M5-4, HW6 salvage) and **no RL anywhere in the decision path**. The reference's shipped
heuristic is re-derived as the arena's fixed DoD opponent (ADR-0002 posture; police PRD §2).

## Consequences

- Every decision is deterministic given (seed, config) → the arena, the champion-regression gate,
  and the ≥60% DoD tables are byte-reproducible in keyless CI; no training loop, no checkpoint
  artifacts, no GPU claim in the fairness declaration (G4 posture stays maximal).
- Strategy strength is legible for grading: features and search are inspectable code with unit
  pins, not opaque weights (self-grade categories reward engineering clarity, rule 55).
- Tuning is bounded to weight vectors (GA over config) — improvement is demonstrable via the
  committed fitness curve without destabilizing the decision architecture.
- We forgo potential RL upside; mitigated by the book's own equal-track framing and the arena:
  if an RL comparison is ever run, it is an **arena-judged experiment** (PRD §2 stretch), never
  the shipped foundation.

## Alternatives considered

- **Q-learning / tabular RL (book §6.3):** rejected as foundation — not course-taught, needs a
  training pipeline + exploration schedule alien to keyless CI, evidence (a Q-table) is opaque to
  the rubric's engineering-quality lens, and the opponent-adaptive setting makes it multi-agent
  RL (nonstationary — the book flags this) for marginal gain on a ≤100-cell board where exact
  belief + search is already tractable.
- **Pure track (1) (Manhattan + belief argmax only):** rejected as *ours* — it is the reference
  default we must beat by ≥60%; shipping it would be strategy parity by construction. It lives on
  as the `greedy-manhattan` baseline and the re-derived `ref-*` DoD opponents.
- **LLM-in-the-loop moves under the book's mutual-consent exception:** rejected — App E rule 25
  posture, hallucination risk the book itself documents (§6.5), token-fairness cost against G4,
  and it requires opponent consent we would never solicit.
