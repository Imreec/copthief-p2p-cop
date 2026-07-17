# M2 oracle spike — notes (living document during the spike)

> Status: **CLOSED — GO (M2-5, 2026-07-18).** Phase M2 complete; §8 lists the residual
> gaps carried into M3/M6/M7.
> The reference is an **oracle only** (ADR-0002 / EULA): run and observe, never copy code.
> SQ probes are throwaway harnesses — scratchpad only, never committed under `src/` or `tests/`.

## 0. The oracle, pinned

| Item | Value |
|---|---|
| Repo | <https://github.com/rmisegal/Game-P2P-Cop-Chase> |
| Commit sha (HEAD at clone, 2026-07-17) | `960499fd5e8777b4929625f5d8fdcf2ab4677b54` |
| Tag / declared code version | `v3.0.0` ("Release v3.0.0 — align code and guidelines-book versions to 3.0.0") |
| Declared book version | v3.0.0 (deep-linked, per README) |
| Local checkout | `FinalProject\reference\Game-P2P-Cop-Chase` (outside both impl repos) |
| Runtime | Python 3.13.2, fastmcp 3.4.3, `uv sync` (77 packages) |
| Keyless posture | `[trash_talk] provider = "template"` pinned explicitly in both role `game.toml`s; run with `--stub-llm`; `email.enabled = false` (shipped default) short-circuits the email path before any subprocess |

**All SQ findings and interop pins below bind to that sha.**

## 1. Localhost smoke (observed 2026-07-17, reference vs reference)

Two OS processes: `uv run python -m police_thief peer --role {thief|police} --stub-llm --no-gui`
(thief:8801, police:8802, loopback). Result (verbatim CLI JSON): `"result": "survival",
"winner": "thief"`, thief steps 35 / police steps 34, exit 0 both sides, 0 tokens.
Mutual audit **Verified OK both directions**: police re-verified 36/36 thief records
(step-0 spec + 35 steps), thief re-verified 35/35 police records; `game_uid`
`7132f6ae-5e09-92a9-3e85-625e138e52cb` derived identically on both sides with no round-trip;
`mutual_agreement.confirmed = true` with matching result sha. Four artifacts emitted per group
under `logs/<group_id>/`. This proves the oracle is runnable and keyless on this machine —
M2-2 proper (OUR peers vs it, over tunnels, both role pairings) is still ahead.

## 2. Interop findings — M1 stubs vs the reference (source-pinned, live-verify at M2-2)

Each item: what the reference actually does vs what our M1 skeleton stubbed. Fix path:
branch -> PR -> review -> Imree merges -> sync ritual. **F1/F2 are architectural; F3-F7 are
shape fixes.**

- **F1 — MCP calling convention (stub WRONG).** Reference tools all return `{"ok": true}`
  and only enqueue: each peer PUSHES to the opponent's server (`negotiate`/`receive_turn`/
  `submit_audit`/`receive_control`, tool arg `message`, except `submit_audit` -> `payload`);
  replies arrive as the opponent's own inbound call into MY server's thread-safe inboxes
  (`PeerInboxes`, drained by polling). No response-carried composition anywhere. Our M1
  response-carried pattern (`negotiate` response carries `"peer"`, `receive_turn` response
  carries `"turn"`) breaks against it in both directions: their client ignores our response
  extras (harmless) but their server never answers ours (fatal for our driving loop).
  Adaptation: rebuild `infra/mcp_server` + `peer/p2p` as symmetric push + inbox transport
  (`exchange_agreement` = send mine, block on inbox for theirs; `send_turn`/`poll_turn`;
  `exchange_audit` = best-effort send + always check own inbox). Peer sessions stay.
- **F2 — who initiates / turn order (stub WRONG).** No initiator exists: the handshake is
  fully symmetric (both send `negotiate` and wait), start order irrelevant (client retries
  until the opponent's server is up, `connect_timeout_seconds`). The **thief takes the first
  game turn** (`runtime.run`: `if role is THIEF: take_turn(...)` before the receive loop).
  Our M1 stub had police-first driving. Note: across a series, **roles alternate per
  sub-game** (natural role on odd, opposite on even) with one runtime rebuilt per sub-game
  over a shared transport — matters for M6/M7 series design, not for one mini-game.
- **F3 — terms extraction: `max_steps` provenance (stub WRONG in a value-hidden way).**
  Reference `_translate_shared`: `rules.max_steps` <- `movement_and_barriers.survival_threshold`
  (NOT `max_moves`; `max_moves` maps to `rules.max_moves`, which the terms never read).
  Our `domain/terms.py` maps `max_steps` <- `movement.max_moves`. Byte-identical only while
  the two config values coincide (both 35 in the shipped config — exactly the trap
  PRD_crypto §8.3 anticipated). Fix `domain/terms.py`; conformance re-run required
  (constraint #13). Rest of the §5 mapping + key set verified identical, incl.
  `setting` <- `world.map_area`, `num_games` default 1, `hint_max_words` default 15,
  axis defaults `top-left`/`0`.
- **F4 — `min_center_intensity` provenance RESOLVED.** The reference's shipped `game.json`
  (schema_version "1.3") carries `pheromones.pheromone_min_center_intensity: 0.5` as a
  first-class shared key. Not a reference-code-only param as PRD_crypto §8.2 assumed —
  our `game.json` schema + App F guard should carry it as a signed negotiable-with-default
  key; PRD_crypto §8.2 note to be amended.
- **F5 — optional wire field types (stub WRONG).** Reference `TurnMessage`:
  `barrier_placed: list|null`, `capture_claim: list|null` (the claimed CELL `[r,c]`),
  `claim_response: dict|null` (`{"claim": [r,c], "caught": bool}`), `win_claim: dict|null`
  (`{"type": "survival"}`), `timestamp: str` ISO-8601 UTC with offset
  (`datetime.now(UTC).isoformat()`). Ours: `capture_claim: bool`, `claim_response: bool`,
  `win_claim: str`, `timestamp: float` — all four reject or mis-parse the reference's
  messages (`check_number` on timestamp fails first). Also `AuditPayload.result_claim` is a
  plain STRING (`"capture"|"survival"|"timeout"`), not our dict. Fix `wire/turn.py` +
  `wire/audit.py` + validation (+ conformance re-run, constraint #13).
- **F6 — the reference REJECTS unknown TurnMessage fields.** `TurnMessage.from_dict` does
  `cls(**data)` after checking required — an unexpected key raises TypeError inside their
  turn handler. Their dataclass `asdict()` also always emits ALL fields (explicit `null`s
  for unset optionals). Interop rule for us: **send exactly their key set** (all 10 keys,
  nulls included is what they themselves do; extras FORBIDDEN outbound), keep
  tolerate-unknown on inbound only. Our `extras`-echo in `to_wire` must never add keys when
  talking to the reference. `ControlMessage` differs: reference filters to known fields
  (tolerant), shape is `kind` ("enable"|"status"|"restart"|"quit"), `sender`,
  `sub_game_number`, `status`, `step_budget`, `payload` — ours (`action`/`message`) doesn't
  match; fix `wire/audit.py`'s ControlMessage.
- **F7 — tie rule + timeout scoring (stub CONFIRMED).** `aggregate`: on a two-group series
  tie, `tie_score` is ADDED to each side's equal total — matches our
  `scoring.settle_series`. Timeout/stopped/tamper sub-games score 0/0 (technical loss for
  both, even the "winner") — matches our `TECHNICAL_LOSS -> (technical_loss,
  technical_loss)` row.
- **Confirmations (no drift):** commit `SHA256(canonical|nonce)` with canonical
  `sort_keys, ensure_ascii=False, separators=(",",":")` — kit CORE form byte-for-byte;
  nonce `secrets.token_hex(16)`; `game_uid` = UUID over `sha256(canonical(terms)|sorted
  group ids)[:16]` — kit form; state string `grid=NxN;self=[r, c];barriers=[...]` with the
  space-after-comma Python repr (observed live in the smoke log); smell decay subtractive
  round-3 (kit-pinned form); negotiate message shape `{terms, nonce, signature, identity}`
  with identity NOT under the signature, terms compared by dict equality.

## 3. SQ answers (source-pinned + smoke-observed; live-confirm during M2-2/M2-3)

- **SQ1 — scent emission timing.** Emission happens AFTER the mover applies its move, at
  the NEW position: `deposit(position, emit_intensity)` (radial over the MxM grid, falloff
  `intensity/(half+1)` per Chebyshev ring, round-3, max-merge into the trail; center must be
  >= `min_center_intensity` or ValueError), then `decay_all()` (including the fresh deposit),
  then `snapshot()` goes on the wire. So the transmitted center of a just-laid scent is
  `emit_intensity - decay` (0.9 - 0.1 = 0.8 with shipped values), and the whole own-trail
  field decays once per own turn. The receiver `absorb`s (max-merge) then decays its own
  field once per received message. Belief pipeline on receive: `diffuse()` then
  `observe_smell(grid)` then absorb+decay. Feeds PRD_scent/PRD_belief (M3-1).
- **SQ2 — capture-claim semantics + cost.** The police attaches `capture_claim = its OWN
  landing cell` on EVERY MOVE-type action, automatically (never on HOLD/BARRIER). Zero cost,
  no limit, no penalty for a wrong claim anywhere in scoring — it is a free per-move probe
  answered honestly by the thief on its next message (`claim_response {"claim","caught"}`;
  lying is pointless because per-step positions are sealed and audited -> tamper forfeit).
  If caught, the thief sends the mandatory final "You got me." message (HOLD, truth,
  caught=true) and the game ends `capture` (police 20 / thief 5). Consequence for our
  PoliceBrain claim policy (M5): no thresholding needed on claim COST — the claim is
  implicit in movement; the real decision is move selection itself.
- **SQ3 — is the transmitted smell grid sealed? NO.** The sealed per-step payload is
  `{step, state, position, move, intent, verdict, hint, prompt_discussion, model,
  tokens_step, tokens_total, response_seconds, random_move}` — no smell grid. Observed in
  the smoke run: zero occurrences of "smell" in the emitted sealed log artifact. The wire
  smell grid is UNAUTHENTICATED: an opponent could transmit a fabricated grid and the audit
  would not catch it directly. Our planned scent-physics check (PLAN §4 audit) still works
  evidence-grade — positions/moves ARE sealed, so the expected trail is re-derivable and
  diffable against the grids we logged verbatim (M1-8 JSONL) — but it proves inconsistency
  only to US (their commitment covers positions, not grids; a dispute is our-log-vs-their-
  wire). Feeds PRD_belief + the audit PRD update (M2-3 DoD) and the M8 README
  contradiction/limitations narrative.

## 4. Operational pins for Stage A/B

- Reference peer config seams: `network.my_port` / `network.opponent_url` in
  `config/<role>/game.toml`; `network.host` respected for bind (default 127.0.0.1);
  shared terms ONLY in `game.json` (byte-identical or the signature gate refuses);
  `game.toml` version "1.10" must stay in the reference's supported list.
- Their turn timeout: `network.turn_timeout_seconds = 180` (private, per-peer);
  handshake wait `connect_timeout_seconds = 60`, poll 0.5s. Tunnel latency is a non-issue
  at these budgets.
- The GUI opens IDLE (Start button, sub-game count dropdown); headless `--no-gui` starts
  immediately with `num_games` from config. For tunnel runs, headless is the scriptable path.
- `[WinError 10048]`-style port conflicts: reference fails fast with a clear message.
- Windows console: reference prints ASCII-safe JSON; a "Session termination failed:"
  line on thief shutdown is a known-benign FastMCP teardown artifact (exit code 0).

## 5. OI-3 — tunnel choice (recommendation, decision is Imree's)

**Recommendation: Cloudflare named tunnel** (one `cloudflared` daemon, TWO public
hostnames routed to localhost:8801/8802 — Stage A needs both peers public simultaneously),
because: no request interstitial (ngrok free injects one for browserish clients and has
per-month request caps), stable hostnames that survive restarts, the exact same
tunnel+config re-deploys on the M7 sparring VPS (Stage B doubles as M7 infra), and HW6
already proved the cloudflared flow on this machine. Requirement: a Cloudflare account with
a domain zone (named tunnels ride your domain's DNS; a cheap/existing domain works — quick
`trycloudflare` tunnels need no account but are ephemeral, which OI-3 exists to avoid).
**Fallback if no domain:** ngrok reserved domain (free tier: one static
`*.ngrok-free.app` reserved domain + additional ephemeral tunnels in the same agent
session). One-line ADR lands in `docs/adr/0006-deploy-tunnel.md` at M2-4 once decided +
observed.

## 6. Stage A — vs the LIVE reference over public tunnels (observed 2026-07-18)

**Infrastructure (M2-1 DoD):** OI-3 decided = Cloudflare named tunnel (ADR-0006). Domain
`imreeyal.com` (Cloudflare Registrar), tunnel `copthief` (`a6663e0c…`), hostnames
`cop.imreeyal.com`→8802 / `thief.imreeyal.com`→8801. Reachability observed both
directions through the public edge.

- **F-421 (infrastructure finding, kit-worthy):** the MCP streamable-HTTP server's
  DNS-rebinding protection returns **421 Misdirected Request** to any tunneled request
  (Host = public hostname ≠ bind address). Both our peer AND the reference failed
  identically on first contact. Fix: `originRequest.httpHostHeader` rewrite in the
  tunnel config — no code change, reference untouched. Any team fronting a fastmcp peer
  with a tunnel will hit this → goes into the kit's deployment notes (M7-2).

**Games (M2-2 DoD, all keyless, 0 tokens, stub LLM + template banter both sides):**

| # | pairing | result | our audit of theirs | their audit of ours | log |
|---|---|---|---|---|---|
| g1 | our cop vs ref thief | survival (34/35 steps) | Verified OK (36/36 recs) | passed 34/34 | `m2-stageA-g1-…jsonl` |
| g2 | our thief vs ref cop | survival (35 steps) | Verified OK | passed 35/35 | `m2-stageA-g2-…jsonl` |
| g3 | g1 rerun, F8 fix | survival, audit OK | Verified OK | (ref crashed writing artifacts — F8b) | `m2-stageA-g3-…jsonl` |
| g4 | g1 rerun, F8b fix | survival (34/35), audit OK | Verified OK | passed 34/34 | `m2-stageA-g4-…jsonl` |

**g4 closed the loop:** both sides independently derived the SAME
`game_uid` (`f757f50d-d4f4-17e7-06cf-755905739b16`), the reference filed us as
`imreeyal` (artifacts `imreeyal-vs-segal-thief-team_*`), and its declaration carries our
full group block — the cross-implementation shared-uid property holds.

g2 also proved the SQ2 flow live: our thief honestly answered the reference cop's
per-move capture claims for 35 straight turns and closed with the survival win claim.

- **F8 (observed in g1/g2):** our negotiate message carried no `identity` dict → the
  reference filed us as `unknown-group` (artifacts named `…-vs-unknown-group`) and the
  two sides derived DIFFERENT `game_uid`s (`e8424ee7…` vs `6647b0af…`). Nothing gates on
  it mid-game — audits still Verified OK — but the shared-uid property and the
  declaration data were broken. Fix: mirror the reference's exact negotiate shape
  `{terms, nonce, signature, identity}`; read opponent group from `identity.group_id`
  (default "unknown-group", mirroring theirs).
- **F8b (observed in g3):** the reference's declaration writer (`group_block`)
  KeyErrors unless the identity carries ALL seven keys
  (`group_id, group_name, members, repos, mcp_servers, llm_model, spec`) — its game and
  audit completed, then its process died writing artifacts. Fix: full seven-key identity
  from `game.toml [game]` (spec `{}` until shared/sysinfo, M6-3 — its fields are
  .get()-safe in their writer).

## 7. Remaining for the gate

- [x] Stage A run (2026-07-18): tunnels live, both role pairings vs the live reference
  over public URLs, mutual audits Verified OK — §6. (Caveat stands: loopback-through-
  tunnel does not prove a different firewall/NAT environment — Stage B adds that; Stage A
  alone was accepted as sufficient for the gate.)
- [x] F3/F4/F5/F6 fixed — PR #11 (`feat/m2-wire-reference-pins`), conformance re-run green.
- [x] F1/F2 fixed — `feat/m2-symmetric-transport` (stacked on #11): symmetric push/inbox
  transport, one loop for both roles, thief-first, win_claim game end. Observed
  2026-07-17: `uv run copthief run p2p-match` under the NEW convention — two OS
  processes, real FastMCP, `{"outcome": "thief_survival", "steps": 34, "audit_ok_police_side":
  true, "audit_ok_thief_side": true, "scores": [5, 10]}` (each side now reports its OWN
  audit verdict; police legitimately ends one turn short on the inbound win claim).
  Debug find for the record: FastMCP INFO access logs once filled the spawned peer's
  stdout pipe and froze it mid-game — server runs at log_level warning now (the
  reference does the same).
- [x] SQ2 claim flow implemented — `feat/m2-claim-flow` (stacked): police claims its
  landing cell on every moving turn; thief answers honestly; caught thief sends the
  mandatory final message; capture pays the capture row. Observed live two-process
  2026-07-17: `{"outcome": "cop_capture", "steps": 3, ..., "audit_ok_police_side": true,
  "audit_ok_thief_side": true, "scores": [20, 5]}` (seeds 3/3) and the survival ending
  (seeds 1/2) — both with mutual audit Verified OK. The skeleton now speaks the full
  reference protocol shape end-to-end (scent grids still empty until M3-2).
- [x] M2-2 both role pairings vs the reference, mutual audit Verified OK both
  directions (§6); JSONL logs committed beside this file.
- [x] SQ1-SQ3 confirmed against the running reference (SQ2 exercised for 35 straight
  claims in g2; SQ3's absent smell grid observed in every exchanged log).
- [x] M2-4: ADR-0003 (crypto-early, spike-validated) + ADR-0006 (deploy + tunnel,
  incl. the 421/Host-rewrite requirement).
- [x] F8/F8b fix merged (PR #14 → cop main `4c30e82`) + synced (thief PR #11 → `2b2a5b5`).
- [ ] Stage B: sparring VPS (OI-4) — deferred past the gate; doubles as M7-1 infra.
- [x] **M2-5: GO — 2026-07-18** (Imree, on this evidence + Claude's candid assessment).

## 8. Residual gaps carried out of M2 (disclosed at the gate, none blocking)

1. **F9 — opponent-barrier tracking.** Our session validates inbound `barrier_placed`
   but does not note it into the board, so our own move legality ignores opponent
   barriers. In g2 the reference cop placed 7 barriers; post-hoc path analysis shows our
   thief never occupied a barrier cell after its placement (it crossed [3,5] at step 2,
   before the barrier landed) — the evidence is legitimate, but by luck, not
   correctness. **Fix rides M3-3** (barriers are constraints of the belief motion model
   anyway) and must land before any external friendly.
2. **Loopback-through-tunnel** does not prove a foreign firewall/NAT environment —
   Stage B (VPS, OI-4) adds that and doubles as M7-1.
3. **Scent live-interop** untested vs the reference (our grids were legally empty; the
   kit vectors pin the math) — M3-2 lands the field, re-verify in the first friendly.
4. **Series / role alternation** (`num_games` > 1) untested — M6-6 scope.
