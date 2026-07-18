"""SimulationSdk — the facade every consumer calls (PRD FR-14; PLAN §3).

Input: a config tree directory. Output: match results / played peers. The facade owns
process spawning for the two-process form so callers hold no transport knowledge. Under
the M2 F1 convention a "peer" PLAYS a full mini-game (own server + symmetric loop), it
does not passively serve tools.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from copthief_core.peer.match import MatchResult, run_local_minigame
from copthief_core.peer.p2p import PeerGameResult, run_peer_game
from copthief_core.peer.session import PeerSession
from copthief_core.sdk.p2p_match import P2PMatchResult, play_p2p_match
from copthief_core.shared.config import load_all, load_gazetteer
from copthief_core.shared.jsonl_logger import JsonlEventLogger
from copthief_core.strategy.referee import RefereeGameResult, play_referee_series


class SimulationSdk:
    """One config tree, all flows (Input: config dir; see method docstrings)."""

    def __init__(self, config_dir: Path, *, counted: bool = False) -> None:
        self.config_dir = config_dir
        self.constitution, self.private, self.rate_limits = load_all(config_dir, counted=counted)

    def run_local_match(
        self,
        *,
        police_seed: int,
        thief_seed: int,
        log_path: Path | None = None,
        gui: bool = False,
    ) -> MatchResult:
        """Full mini-game, both peers in-process over queue transports (keyless CI path).

        With `log_path`, the game is JSONL-logged and replayable (peer/replay, M1-8).
        With `gui`, one live window per role renders the SAME event stream (M4-2)."""
        if not gui:
            return run_local_minigame(
                self.config_dir, police_seed=police_seed, thief_seed=thief_seed, log_path=log_path
            )
        from copthief_core.gui.windows.launch import run_with_views

        return run_with_views(
            ["police", "thief"],
            self.constitution,
            self.private.gui,
            lambda tee: run_local_minigame(
                self.config_dir,
                police_seed=police_seed,
                thief_seed=thief_seed,
                log_path=log_path,
                tee=tee,
            ),
        )

    def referee_series(
        self, police_brain: str, thief_brain: str, *, seeds: list[int]
    ) -> list[RefereeGameResult]:
        """Headless referee-mode series (M3-5/M3-6) — the arena's only game source."""
        return play_referee_series(
            self.constitution,
            police_brain_name=police_brain,
            thief_brain_name=thief_brain,
            smell_trust=self.private.smell_trust_weight,
            seeds=seeds,
        )

    def run_peer(
        self,
        *,
        role: str,
        seed: int,
        host: str,
        port: int,
        opponent_url: str,
        log_path: Path | None = None,
        gui: bool = False,
    ) -> PeerGameResult:
        """Play ONE full mini-game as a standalone peer: own FastMCP server on `port`,
        symmetric loop against `opponent_url` (blocking until the game settles)."""
        from copthief_core.infra.mcp_client import McpToolClient
        from copthief_core.infra.mcp_server import start_server
        from copthief_core.infra.p2p_transport import McpTransport
        from copthief_core.peer.transport import PeerQueues

        inboxes = PeerQueues()
        start_server(role, inboxes, host=host, port=port)
        transport = McpTransport(
            McpToolClient(opponent_url),
            inboxes,
            connect_timeout=self.private.connect_timeout_seconds,
            retry_interval=self.private.poll_interval_seconds,
        )
        gazetteer = load_gazetteer(
            self.config_dir / "gazetteer.json",
            map_area=self.constitution.world.map_area,
            board=self.constitution.board.make_board(),
        )
        session = PeerSession(
            self.constitution, self.private, role=role, seed=seed, gazetteer=gazetteer
        )
        sink = JsonlEventLogger(log_path).log if log_path is not None else None

        def play(extra: Any = None) -> PeerGameResult:  # noqa: ANN401 - optional LogFn tee
            def fan(event: dict[str, Any]) -> None:
                if sink is not None:
                    sink(event)
                if extra is not None:
                    extra(event)

            return run_peer_game(
                session,
                transport,
                turn_timeout=self.private.turn_timeout_seconds,
                poll_interval=self.private.poll_interval_seconds,
                log=fan,
            )

        if not gui:
            return play()
        from copthief_core.gui.windows.launch import run_with_views

        return run_with_views([role], self.constitution, self.private.gui, play)

    def run_p2p_match(
        self, *, police_seed: int, thief_seed: int, thief_port: int, host: str
    ) -> P2PMatchResult:
        """The one-command two-process form (sdk/p2p_match): spawn the thief peer as a
        second PROCESS, play the police side in-process; each side reports its own
        audit verdict."""
        return play_p2p_match(
            self,
            police_seed=police_seed,
            thief_seed=thief_seed,
            thief_port=thief_port,
            host=host,
        )
