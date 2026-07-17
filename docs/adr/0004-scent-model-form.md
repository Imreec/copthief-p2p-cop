# ADR-0004 — Scent model form: kit-pinned subtractive decay (vs the book's prose)

**Status:** Accepted (M3-2) · **Deciders:** Imree + Claude (decision pre-approved via PRD_scent, PR #16)

## Context

The book's prose (ch.4) describes pheromone decay **multiplicatively** — each step the
trail keeps a fraction of its intensity. The release's own reference implementation
(oracle sha `960499fd` = v3.0.0) implements **subtractive** decay: every known cell
loses the constant `pheromone_decay` per step, clamped at 0, rounded to 3 decimals.
The conformance kit (`copthief-league-protocol`, SPEC §5 + `pheromone.json` vectors)
documents this contradiction and pins the subtractive reference form as the
interop construction. The two models produce different wire bytes from turn 2 onward —
a mixed pair would silently read each other's trails wrong.

The emission form is not contradicted: radial over the `M×M` window with Chebyshev
rings, `falloff = intensity / (half + 1)`, round-3, max-merge, off-board clipped.

## Decision

`domain/scent` implements the **kit-pinned subtractive form** exactly (academic-freedom
clause: where book prose and reference code contradict, we choose and document). The
kit `pheromone.json` vectors are CI-blocking conformance fixtures in both repos
(constraint #13). To make the choice *diagnosable across teams*, the handshake
exchanges a **locked-model document** — formula name `subtractive_chebyshev_v1`, the
four signed pheromone params, and a per-ring numeric example (deposited / transmitted
after the one SQ1 decay) — hashed with the standard canonical form. A scent dispute
with any opponent reduces to comparing two hashes, not to prose.

SQ1 timing (spike-observed, live-confirmed at Stage A) is wired in `peer/turns`:
deposit AFTER the move at the NEW position → own trail decays ONCE → snapshot rides
the TurnMessage; the receiver absorbs, then decays its known field once per received
message. The reference deposits on EVERY outbound turn — STAY and the final caught
message included — and we mirror that (source-pinned in its `turn_sender.send()`).

## Consequences

- With shipped values (0.9 / 0.1 / 5×5) a just-laid center transmits at **0.8**, its
  ring-1 at **0.5**, ring-2 at **0.2** — the locked numeric example, asserted end-to-end
  by the integration suite over the queue transports.
- The transmitted grid stays **unauthenticated** (SQ3): scent stores and reports;
  trust decisions live in the belief layer (PRD_belief), and the post-audit
  scent-physics check (PLAN §4) can re-derive an opponent's expected trail because
  the locked model makes "expected" well-defined.
- A future book revision to multiplicative decay would be a kit-versioned change:
  re-verify vectors against the new reference before touching our field (CLAUDE.md #13).

## Alternatives

- **Book-prose multiplicative decay:** rejected — no interop partner runs it; the kit
  and the reference both pin subtractive.
- **Supporting both forms behind config:** rejected — an unsigned degree of freedom in
  a signed construction invites silent mismatch; one form, one hash.
- **Withholding the locked-model doc from the handshake:** rejected — the reference
  provably ignores the extra key (`verify_peer` indexes only its four), and the hash
  exchange is what turns a future dispute into evidence.
