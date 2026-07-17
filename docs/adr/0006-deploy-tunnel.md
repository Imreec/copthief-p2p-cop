# ADR-0006 — Deploy split + tunnel choice (OI-3)

**Status:** Accepted (M2 Stage A, 2026-07-18) · **Deciders:** Imree (choice + account), Claude (setup)

## Context

Live games need each peer's FastMCP server reachable by the opponent over the public
internet (PLAN §2: named tunnel exposing the local port). HW6 proved ephemeral
`trycloudflare` quick tunnels, but their per-run URLs are exactly what OI-3 exists to
retire: counted matches and the M7 sparring host need stable, pre-shareable endpoints.
Candidates: Cloudflare named tunnel (needs a domain zone) vs ngrok reserved domain
(no domain, but free tier = one static hostname + one agent session — a conflict the
moment the M7 VPS needs its own tunnel).

## Decision

**Cloudflare named tunnel** on the operator's account with the purchased zone
`imreeyal.com` (bought via Cloudflare Registrar — at-cost, zone auto-active). One tunnel
(`copthief`, id `a6663e0c-0703-4608-ba86-e7c22978bfe0`), two public hostnames:

| hostname | origin |
|---|---|
| `cop.imreeyal.com` | `http://127.0.0.1:8802` (police peer) |
| `thief.imreeyal.com` | `http://127.0.0.1:8801` (thief peer) |

Config at `~/.cloudflared/config.yml`; DNS CNAMEs routed via `cloudflared tunnel route
dns`. The operator's one-time interactive step was `cloudflared tunnel login`; everything
else is scripted/re-runnable.

**Load-bearing detail (observed M2 Stage A, would break any team fronting a fastmcp
peer):** the MCP streamable-HTTP server ships DNS-rebinding protection that rejects any
request whose `Host` header is not the local bind address — through a tunnel every
request arrives with the public hostname and gets **HTTP 421 Misdirected Request** (both
our peer and the lecturer's reference peer, fastmcp 3.4.x, failed identically). Fix at
the tunnel, not in code: per-hostname `originRequest.httpHostHeader` rewrites Host to the
origin (`127.0.0.1:<port>`). This keeps the reference peer untouched (EULA posture) and
our code free of deployment-specific carve-outs.

## Consequences

- Stable, DNS-clean endpoints for M2-2, friendlies, counted series, and the kit's
  pre-match checklist; no interstitials, no request caps, no agent-session limits.
- The M7 sparring VPS reuses the same account and pattern (its own tunnel + hostnames or
  this tunnel's credentials file copied over) — Stage B is a file copy, not a redesign.
- Annual domain cost (~US$10); tunnel/DNS free.
- The 421/Host-rewrite requirement goes into the kit's deployment notes (M7-2) — it is
  reference-peer-relevant for every team.

## Alternatives considered

- **ngrok reserved domain** — no domain purchase, but one static hostname + one
  simultaneous agent session on free tier (collides with M7), browserish interstitial
  edge cases. Kept as documented fallback.
- **trycloudflare quick tunnels** — zero setup (HW6-proven) but ephemeral URLs;
  fine for throwaway smokes, unusable as league identity.
- **Render/PaaS hosting (HW6)** — hosts a public HTTP service but inverts the model:
  peers run ON the PaaS, not on the operator's machine; wrong fit for the
  peer-process-per-operator topology and for GUI-attached live play.
