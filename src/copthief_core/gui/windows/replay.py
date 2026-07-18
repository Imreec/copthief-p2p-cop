"""Replay viewer shell (book §7.4): verdict banner + audited board + step controls.

Thin, coverage-omitted (D3): the verdict and every frame come from the tested models
(`peer/replay`, `gui/models/replay`). Post-audit data only — the objective board is
legal here, retrospectively (book §7.2); the banner is the book's binary outcome.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path

from copthief_core.domain.board import Board
from copthief_core.gui.models.replay import ReplayWalk
from copthief_core.peer.replay import VERDICT_OK
from copthief_core.shared.config_model import Constitution, GuiSettings


class ReplayWindow:
    """One window walking one verified log."""

    def __init__(self, root: tk.Misc, walk: ReplayWalk, board: Board, cell_px: int) -> None:
        self._walk, self._board, self._cell = walk, board, cell_px
        color = "green" if walk.verdict == VERDICT_OK else "red"
        self._banner = tk.Label(root, text=walk.verdict, fg="white", bg=color)
        self._banner.pack(fill="x")
        side = board.grid_size * cell_px
        self._canvas = tk.Canvas(root, width=side, height=side)
        self._canvas.pack()
        controls = tk.Frame(root)
        controls.pack(fill="x")
        tk.Button(controls, text="<", command=self._back).pack(side="left")
        tk.Button(controls, text=">", command=self._forward).pack(side="left")
        self._status = tk.Label(controls, text="", anchor="w")
        self._status.pack(side="left", fill="x", expand=True)
        self._redraw()

    def _back(self) -> None:
        self._walk.back()
        self._redraw()

    def _forward(self) -> None:
        self._walk.forward()
        self._redraw()

    def _display_row(self, row: int) -> int:
        if self._board.axis_origin_corner.startswith("bottom"):
            return self._board.grid_size - 1 - row
        return row

    def _redraw(self) -> None:
        if not len(self._walk):
            self._status.configure(text="no audited frames in this log")
            return
        frame, cell, origin = self._walk.current(), self._cell, self._board.axis_start_index
        self._canvas.delete("all")
        for row in range(self._board.grid_size):
            for col in range(self._board.grid_size):
                coord = (row + origin, col + origin)
                x, y = col * cell, self._display_row(row) * cell
                fill = "black" if coord in frame.barriers else "white"
                self._canvas.create_rectangle(x, y, x + cell, y + cell, fill=fill)
                for sender, position in frame.positions.items():
                    if position == coord:
                        self._canvas.create_text(
                            x + cell // 2, y + cell // 2, text=sender[0].upper()
                        )
        self._status.configure(text=f"step {frame.step} ({self._walk.index + 1}/{len(self._walk)})")


def show_replay(log_path: Path, constitution: Constitution, settings: GuiSettings) -> None:
    """Open the viewer over a log and block until the operator closes it."""
    walk = ReplayWalk.from_log(log_path)
    root = tk.Tk()
    root.title(f"copthief replay - {log_path.name}")
    ReplayWindow(root, walk, constitution.board.make_board(), settings.cell_px)
    root.mainloop()
