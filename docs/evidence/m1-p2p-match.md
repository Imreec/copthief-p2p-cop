# M1 exit evidence — one command, two processes, localhost (PLAN §13 M1)

**Observed 2026-07-17** on the dev machine (Windows 10, Python 3.12.13, fastmcp 3.4.4),
branch `feat/sdk-cli` (merged as the M1-7 PR).

## Command

```
uv run copthief run p2p-match --police-seed 11 --thief-seed 22
```

## What ran

- The SDK spawned the **thief peer as a second OS process** (`python -m copthief_core.sdk.cli
  run peer --role thief --port 8803 ...`), serving the four wire-contract tools over real
  FastMCP HTTP on `http://127.0.0.1:8803/mcp`.
- The police process drove the full protocol as initiator over that endpoint: `negotiate`
  (terms value-equality + signature verification both ways → shared `game_uid`), 35 turn
  exchanges (each sealed with `SHA256(canonical|nonce)`, nonces withheld), then `submit_audit`
  — each side re-hashed every record the other revealed.
- The thief subprocess was terminated by the SDK on completion.

## Observed result (verbatim final stdout line)

```json
{"outcome": "thief_survival", "steps": 35, "game_uid": "186a5c22-04c6-93a2-860c-9804cdd23db2", "audit_ok_police_side": true, "audit_ok_thief_side": true, "scores": [5, 10]}
```

- `audit_ok_police_side` — our re-hash of all 35 thief records: **Verified OK**
- `audit_ok_thief_side` — the thief's re-hash of all 35 police records: **Verified OK**
- `scores` — derived from the survival outcome per the signed scoring table (5 / 10), never declared.
- The uvicorn access log showed 35 turn round-trips + negotiate + audit against the thief server
  (trimmed here; the full pattern is reproducible with the command above).

The other half of the M1 exit criterion — kit CORE vectors green in both repos' CI — has held
since the M1-3/M1-5+6 syncs (cop and thief `tests/conformance/` suites, CI-blocking).
