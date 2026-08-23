# copthief-p2p-cop — Cop agent, Distributed Cops-and-Robbers over P2P

> **Status: playing the league (M12).** This project builds docs-first behind approved gates:
> see [docs/PRD.md](docs/PRD.md), [docs/PLAN.md](docs/PLAN.md), [docs/TODO.md](docs/TODO.md).
> This README becomes the full academic report at M8 (kept last); until then it only states
> what is true of the tree.

Final project, *Orchestration of AI Agents* (University of Haifa, Dr. Yoram Segal) — the **cop**
agent for the hidden-position pursuit race over P2P FastMCP, per the official book v3.0.0 and its
binding parameters table. **Sibling repo (thief agent):**
[copthief-p2p-thief](https://github.com/Imreec/copthief-p2p-thief). Byte-level interop follows
our public conformance kit:
[copthief-league-protocol](https://github.com/Imreec/copthief-league-protocol).

## What exists right now

- The full playing agent: pure domain core + belief filter, peer wire layer
  (negotiate/turns/audit over FastMCP), strategy brains (expectimax cop with graph
  surgery, containment, forcing endgame solver and belief-momentum intercept; doctrine
  evader with k-wall pocket forecast), automatic reporting behind the recipient
  interlock, replay GUI, and the arena/GA tuning instruments. Decisions: ADRs
  0001–0015 in [docs/adr/](docs/adr/); ten counted series banked (the league cap)
  (`reports/counted-series/`).
- Quality gates wired: ruff, mypy --strict, pytest+coverage, 150-line limit, anti-pattern /
  no-hardcoded scanners, core-mirror manifest check, self-grade validation, submission
  checklist, champion-regression arena gate.
- This repo is the **lead**: `src/copthief_core/` is developed here and mirrored to the sibling
  by `scripts/sync_core.py` (ADR-0001).

## Development

```bash
uv sync          # install (dev tooling only at M0; keyless)
make grade       # every quality gate, same as CI
```

Process: branch → PR → cross-model review → squash-merge (`docs/REVIEW_PROCESS.md`). Reporting is
**automatic** at the end of a series (App E rule 32; rule 35 zeroes both teams for a missing
report) — what is gated is the ADDRESS: no email is ever sent to a recipient that was not
configured for that run, and the lecturer is reachable only from a counted series (ADR-0008,
ADR-0009). The previous wording here described the per-send arming step ADR-0008 removed.
