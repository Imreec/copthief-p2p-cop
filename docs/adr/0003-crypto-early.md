# ADR-0003 — Crypto layer first (build-order deviation), validated at the M2 spike

**Status:** Accepted (written at M2 per plan; decision executed at M1-3) · **Deciders:** Imree + Claude

## Context

The book's staged PRDs (ch.10) grow the game engine before the trust machinery. We
inverted that: `domain/crypto` (canonical JSON, commit/verify, terms signature,
`game_uid`) landed at M1-3, directly from the conformance kit's CORE vectors, before
scent, belief, or any strategy. Rationale at the time: serialization mismatch at audit is
a technical loss for BOTH sides — interop bytes are the grade floor, and the kit gave us
a byte-exact oracle months before a live opponent existed. The M2 oracle spike was set up
as the test of this bet: run the lecturer's reference peer and see which of our
constructions survive contact.

## Decision

Keep the crypto-first order, with the kit as the byte authority and the M2 spike as the
mandatory live confirmation gate before any perception/strategy work (M3+).

## Consequences (spike-verified, oracle sha `960499fd` = v3.0.0)

- **Every CORE construction survived unchanged:** canonical form, `SHA256(canonical|nonce)`
  commits, terms signature, `game_uid` derivation, the sealed state string — byte-for-byte
  against the running reference; mutual audits Verified OK in both role pairings over
  public tunnels (Stage A, 2026-07-18). Zero rework in `domain/crypto`.
- What DID need fixing was everything the kit deliberately does not pin — the wire
  envelope and conventions (spike findings F1–F8: calling convention, turn order, field
  shapes, terms-extraction source key, negotiate identity). The spike caught all of them
  in one day against the oracle instead of during a league match.
- Cost of the deviation: none observed — the crypto module needed no changes when the
  engine grew around it (the seal/verify seam was stable through the M2 transport
  rewrite).

## Alternatives considered

- **Book order (engine → crypto later):** every M1/M2 protocol piece would have been
  built twice — once loose, once against the hash reality; the audit gate makes late
  crypto the most expensive possible retrofit.
- **Vendor the reference's crypto:** barred by the EULA posture (ADR-0002) and would
  have skipped the byte-level understanding the kit work produced.
