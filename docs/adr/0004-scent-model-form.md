# ADR-0004 — Scent model form: one pinned form (v1) → two named, pair-locked models (v2)

**Status:** v2 **ACCEPTED** — approved by Imree at the M3-8 gate (PR #56, main `ee8a78a`);
built in the ADR's own order at M3-8. v1 Accepted at M3-2 (PR #16), superseded in part by
this revision.
**Deciders:** Imree + Claude · **Revision trigger:** M3-7 decision "REVISE" (Imree, 2026-07-18)

---

## v1 (M3-2) — retained for the record

### Context

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

### Decision

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

### Consequences

- With shipped values (0.9 / 0.1 / 5×5) a just-laid center transmits at **0.8**, its
  ring-1 at **0.5**, ring-2 at **0.2** — the locked numeric example, asserted end-to-end
  by the integration suite over the queue transports.
- The transmitted grid stays **unauthenticated** (SQ3): scent stores and reports;
  trust decisions live in the belief layer (PRD_belief), and the post-audit
  scent-physics check (PLAN §4) can re-derive an opponent's expected trail because
  the locked model makes "expected" well-defined.
- A future book revision to multiplicative decay would be a kit-versioned change:
  re-verify vectors against the new reference before touching our field (CLAUDE.md #13).

### Alternatives (v1)

- **Book-prose multiplicative decay:** rejected — no interop partner runs it; the kit
  and the reference both pin subtractive.
- **Supporting both forms behind config:** rejected — an unsigned degree of freedom in
  a signed construction invites silent mismatch; one form, one hash.
- **Withholding the locked-model doc from the handshake:** rejected — the reference
  provably ignores the extra key (`verify_peer` indexes only its four), and the hash
  exchange is what turns a future dispute into evidence.

---

## v2 (M3-8) — two named models, locked per pair

### What changed, and why v1's rejection no longer holds

v1 rejected supporting both forms on two grounds. **The first is now factually false:**
"no interop partner runs it" — the EX06 partner team (anrbj666 — Alon Engel, Renat
Karimov) implements the book's multiplicative model, and locking book-v3 is their stated
condition for a counted series, citing App E **rule 23** (a decay-formula deviation voids
the game). They are our most engaged league partner and the only team that has
independently verified one of our games end to end.

**The second ground survives and shapes the design.** "An unsigned degree of freedom in a
signed construction invites silent mismatch" was the right worry — so the answer is not
config-selectable physics but a **named model, locked per pair and sealed into the
record**. The freedom is not unsigned: it is declared at handshake, hashed, and at step 0
it enters the commit chain. A pair that never declares anything keeps v1's behaviour
exactly.

Also corrected from v1's framing: the cadence delta is **not** "reference decays per
half-turn, book per full turn." Per individual trail, both decay once per full turn. The
real divergences are **anchor, order, and the receiver-side pass** (see the table below);
the earlier phrasing counted events across two fields.

### Decision

1. **Two named registrations**, both published in the kit (PR #7, SPEC §5.1 + §7):
   `subtractive_chebyshev_v1` (reference form, **our default**, unchanged from v1) and
   `multiplicative_book_v1` (the book's ch.4 model). `domain/scent` grows a `ScentModel`
   named object; the field delegates emission/decay/clamp/rounding to it.

2. **The lock rides the kit's locked-model doc schema**, not an ad-hoc dict — one schema
   (`family` / `name` / `params` / `example`) serving scent models, wire shapes, and
   info modes, hashed `sha256(canonical_json(doc))` and declared at negotiate as
   `<family>_sha256`. This is the M3-8 prerequisite: our structured doc and the partner's
   bare `scent_model_sha256` were not comparable artifacts until the kit fixed the bytes.

3. **Refusal rule: refuse only when BOTH peers declare and the hashes differ.** Omission
   is never refusal, in either direction. A lock that fail-fasts on a missing declaration
   cannot start a game against the unmodified reference peer, which declares nothing —
   that is a self-inflicted forfeit, not a safeguard. (The partner team's lock previously
   did fail-fast here and they have adopted this rule.)

4. **The model hash is sealed at step 0**, closing v1's known gap that the locked-model
   doc was hashed and logged but never commit-bound. The signed 14-key terms cannot carry
   it — the key set is reference-frozen and adding a key breaks the terms signature — so
   the step-0 sealed spec record is where it becomes tamper-evident.

5. **The belief observation model is parameterized by the selected scent model.** The
   exact-Bayes filter's scent likelihood assumes a falloff shape; it reads it from the
   model rather than hard-coding Chebyshev-linear.

6. **`min_center_intensity` is settled as a reference term, not a book parameter** — see
   the provenance note in `PRD_scent.md` §9.1. Under `multiplicative_book_v1` it is
   **inert**: it stays in the signed terms (frozen key set) but gates nothing, because the
   book's `Δτ` is the kernel, unconditioned by any minimum.

### The two models, side by side

| | `subtractive_chebyshev_v1` (default) | `multiplicative_book_v1` |
|---|---|---|
| Emission | radial, Chebyshev rings, linear falloff | verbatim 5×5 figure-4 kernel |
| Decay | `v − decay`, clamped at 0 | `(1−ρ)·τ` |
| Update | deposit, then decay | `clamp((1−ρ)·τ + Δτ, 0, center_intensity)` |
| Rounding | 3 decimals | **none** |
| Order | deposit-then-decay | decay-then-deposit (one expression) |
| Receiver pass | yes — decays a received copy on receipt | **no** — recomputed, never received |
| Upper clamp | none | `center_intensity` (0.9) |
| Start | empty | empty |
| On the wire | transmitted | not transmitted |

### Consequences

- **Constraint #13 applies in full**: this touches locked-model bytes, so kit CORE vectors
  are re-verified before merge and the new fixtures join `tests/conformance/` in both repos.
- **A per-model belief-eval rerun is required** — the M3-3 result (exact Bayes beats the
  last-known-position tracker on every seed) was measured under the subtractive model only,
  and must not be quoted for the book model until re-measured.
- **Evaluation order becomes load-bearing** under the book model, which rounds nothing:
  `(1−ρ)·τ + Δτ` and `τ − ρ·τ + Δτ` differ in the last IEEE-754 bit for 75 of 534 probed
  inputs. The order is pinned in code and in the kit fixture; the scent-physics check
  (M6-7) must compare recomputed fields with a tolerance, not byte-wise, when this model
  is locked.
- **Default behaviour is unchanged.** Against the reference peer, or any peer that declares
  nothing, we play exactly as v1 shipped. This revision adds a capability; it does not
  alter the resting posture.
- **The wire shape is a separate lock on the same schema** (M7-0, ADR-0006): registering
  the schema here is what lets that ADR pin its choice without inventing a second envelope.
- **The negotiate extras change shape for BOTH models.** Kit SPEC §7 is explicit that the
  doc never crosses the wire — only `<family>_sha256` does — so the pre-M3-8 `scent_model`
  key carrying the whole document is gone, and the hash is now over the kit's four-key
  envelope rather than our M3-2 ad-hoc dict. This is a wire-visible change on the default
  path; it is what makes our declaration comparable with the partner team's at all. The
  reference peer is unaffected (`verify_peer` indexes only its four terms keys). The
  *game* bytes — turn messages, smell grids, sealed records — are unchanged, and that is
  what `PRD_scent` §9.5's byte-identity criterion means (its wording is amended to say so).

### Alternatives

- **Hold one form, require partners to implement subtractive** (v1's position): rejected —
  it costs the counted series against our only verified interop partner, and their citation
  of rule 23 is sound. Their model is the *book's*; ours is the *reference's*; App D §4
  gives the book precedence where the two conflict, so demanding they adapt is the weaker
  claim of the two.
- **Config-selectable physics without a lock:** rejected, and this is v1's surviving
  objection — a silent degree of freedom in a signed construction is exactly how two
  honest implementations desynchronize.
- **Implementing the book kernel as a fitted Gaussian** rather than the printed table:
  rejected on evidence. The kernel *is* an exact radial Gaussian at printed precision, but
  only inside a narrow σ² window the book never prints, and the round-to-2dp window
  (`[1.3178, 1.3327]`) is **disjoint** from the truncation window (`[1.3436, 1.3538]`) —
  two teams each fitting in good faith diverge silently. The 25 printed values are the only
  thing both can reach. (This also settles the open reconciliation item between the two
  teams: their "exact Gaussian" reading was right about the shape, ours — "matches no clean
  formula" — was right about the reproducibility. Both point to verbatim pinning.)
- **Deferring M3-8 until after the counted series:** rejected — the lock is the partner's
  stated precondition for the series, so deferring it defers the series.
