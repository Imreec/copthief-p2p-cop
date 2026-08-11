"""Throwaway: action values in the g01 stall geometry under path_distance."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from copthief_core.domain.board import Board
from copthief_core.domain.rules import legal_moves
from copthief_police.features import resolve_options
from copthief_police.search import action_value

board = Board(
    grid_size=7,
    axis_origin_corner="top-left",
    axis_start_index=0,
    barriers=frozenset({(6, 3), (4, 3), (1, 4)}),
)
opts = resolve_options({"path_distance": 1.0, "contain_enabled": 1.0, "tie_epsilon": 0.0})
support = [((0, 4), 1.0)]
for move in sorted(legal_moves(board, (2, 4), ("N", "S", "E", "W", "STAY"))):
    dest = board.apply_move((2, 4), move)
    value = action_value(board, dest, support, ("N", "S", "E", "W", "STAY"), opts)
    print(move, dest, round(value, 3))

from copthief_core.strategy.brains import Observation  # noqa: E402
from copthief_police.containment import containment_wall  # noqa: E402

obs = Observation(
    board=board,
    position=(2, 4),
    move_set=("N", "S", "E", "W", "STAY"),
    role="police",
    step=16,
    barriers_used=3,
    max_barriers=14,
    max_moves=35,
)
for rng in (3.0, 4.0, 5.0):
    ranged = resolve_options({"contain_enabled": 1.0, "contain_range": rng})
    wall = containment_wall(obs, [((0, 4), 1.0)], ranged, last_wall_step=12)
    print(f"contain_range={rng}: wall={wall}")
