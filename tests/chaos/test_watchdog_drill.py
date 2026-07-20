"""Chaos drill — the stalled loop (PLAN §10; FR-8): watchdog, threaded, for real.

A loop that stops beating is never a silent freeze: within the (tiny, real-time)
budget the thread persists the snapshot and fires the shutdown callback; a loop
that keeps beating is never disturbed.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from copthief_core.peer.watchdog import Watchdog


def test_drill_stalled_loop_persists_and_shuts_down(tmp_path: Path) -> None:
    stalls: list[str] = []
    dog = Watchdog(
        timeout_sec=0.15,
        io_timeout_sec=3.0,
        snapshot=lambda: {"role": "police", "steps_sealed": 4},
        persist_path=tmp_path / "state_uid.json",
        on_stall=stalls.append,
    )
    dog.start(poll_interval=0.02)
    try:
        dog.beat()
        deadline = time.time() + 3.0
        while not dog.fired and time.time() < deadline:
            time.sleep(0.02)  # the loop has stalled: no more beats
    finally:
        dog.stop()
    assert dog.fired is True
    assert len(stalls) == 1
    assert json.loads((tmp_path / "state_uid.json").read_text(encoding="utf-8")) == {
        "role": "police",
        "steps_sealed": 4,
    }


def test_drill_beating_loop_is_never_disturbed(tmp_path: Path) -> None:
    stalls: list[str] = []
    dog = Watchdog(
        timeout_sec=0.2,
        io_timeout_sec=3.0,
        snapshot=dict,
        persist_path=tmp_path / "state_uid.json",
        on_stall=stalls.append,
    )
    dog.start(poll_interval=0.02)
    try:
        for _ in range(10):
            dog.beat()
            time.sleep(0.03)  # well inside the budget every time
    finally:
        dog.stop()
    assert dog.fired is False
    assert stalls == []
    assert not (tmp_path / "state_uid.json").exists()
