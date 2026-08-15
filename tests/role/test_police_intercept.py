"""M12 intercept — the cop hunts where the thief WILL be, not where it was.

The 08-14 best2934 forensics: our capture claims trailed their thief's true cell by
exactly one step for 20+ consecutive steps in all three cop games — 11-12
adjacencies and two literal co-locations, zero conversions. The scent posterior is
accurate but lagged, so against any mover the argmax is yesterday's cell. These
tests pin the momentum advance that closes it, and that the shipped stream is
byte-identical while the knob is off.
"""

from pathlib import Path

from copthief_core.shared.config import load_all
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.referee_setup import referee_belief
from copthief_police.brain import PoliceBrain
from copthief_police.intercept import advanced_probs, drift

CONSTITUTION, PRIVATE, _ = load_all(Path("config"), counted=False)
TRUST = PRIVATE.smell_trust_weight


def _observation(board: object, position: tuple[int, int], **kw: object) -> Observation:
    return Observation(
        board=board,  # type: ignore[arg-type]
        position=position,
        move_set=CONSTITUTION.movement.move_set,
        role="police",
        step=int(kw.pop("step", 1)),
        survival_threshold=int(kw.pop("survival_threshold", 35)),
        max_moves=int(kw.pop("max_moves", 35)),
        barriers_used=int(kw.pop("barriers_used", 0)),
        max_barriers=int(kw.pop("max_barriers", 14)),
    )


def _delta_belief(cell: tuple[int, int]) -> object:
    return referee_belief(CONSTITUTION, start=cell, smell_trust=TRUST)


def test_drift_is_only_a_unit_orthogonal_step() -> None:
    """A peak that jumped is noise, not momentum; a parked peak carries none."""
    assert drift((3, 3), (3, 4)) == (0, 1)
    assert drift((3, 3), (2, 3)) == (-1, 0)
    assert drift((3, 3), (3, 3)) is None
    assert drift((3, 3), (5, 3)) is None
    assert drift((3, 3), (2, 4)) is None


def test_advanced_mass_stops_at_walls_and_edges() -> None:
    """Shifted mass lands only on open cells; blocked or off-board mass stays put."""
    board = CONSTITUTION.board.make_board().with_barrier((3, 5))
    shifted = advanced_probs({(3, 4): 0.6, (3, 6): 0.4}, (0, 1), board)
    assert shifted == {(3, 4): 0.6, (3, 6): 0.4}  # wall ahead / board edge ahead
    open_board = CONSTITUTION.board.make_board()
    assert advanced_probs({(3, 4): 1.0}, (0, 1), open_board) == {(3, 5): 1.0}


def test_the_default_stream_ignores_momentum_entirely() -> None:
    """`intercept_enabled` defaults 0.0: two brains, one with the knob explicitly off,
    must agree move-for-move across a sequence where the peak visibly drifts."""
    board = CONSTITUTION.board.make_board()
    plain = PoliceBrain(seed=7)
    pinned = PoliceBrain(seed=7, options={"intercept_enabled": 0.0})
    for step, peak in ((1, (3, 3)), (2, (3, 4)), (3, (3, 5))):
        belief = _delta_belief(peak)
        observation = _observation(board, (6, 6), step=step)
        assert plain.decide(observation, belief) == pinned.decide(observation, belief)


def test_armed_intercept_commits_onto_the_running_thiefs_next_cell() -> None:
    """THE conversion the forensics demanded: the peak ran (3,2)->(3,3)->(3,4)
    eastward — two consistent drifts — so the true cell is (3,5); the armed cop
    standing at (3,6) steps W onto it even at a commit bar its lagged posterior
    could never clear. The disarmed cop cannot commit there (its mass sits on
    yesterday's cell)."""
    board = CONSTITUTION.board.make_board()
    armed = PoliceBrain(seed=7, options={"intercept_enabled": 1.0, "p_commit": 0.9})
    armed.decide(_observation(board, (3, 6), step=1), _delta_belief((3, 2)))
    armed.decide(_observation(board, (3, 6), step=2), _delta_belief((3, 3)))
    decision = armed.decide(_observation(board, (3, 6), step=3), _delta_belief((3, 4)))
    assert decision.barrier is None
    assert decision.move == "W"


def test_one_drift_alone_is_not_momentum() -> None:
    """Persistence gate (the pool-dip fix): a single observed step is noise against
    an erratic evader — the advance fires only after the SAME unit drift twice in
    a row, so a zigzagging peak leaves the posterior untouched. Verified through
    the tracker directly: E then E fires east; E then N fires nothing."""
    from copthief_police.intercept import InterceptTracker

    board = CONSTITUTION.board.make_board()
    steady = InterceptTracker()
    steady.observe(1, (3, 2), {(3, 2): 1.0}, board)
    steady.observe(2, (3, 3), {(3, 3): 1.0}, board)
    assert steady.observe(3, (3, 4), {(3, 4): 1.0}, board) == {(3, 5): 1.0}
    zigzag = InterceptTracker()
    zigzag.observe(1, (3, 2), {(3, 2): 1.0}, board)
    zigzag.observe(2, (3, 3), {(3, 3): 1.0}, board)
    assert zigzag.observe(3, (2, 3), {(2, 3): 1.0}, board) == {(2, 3): 1.0}


def test_intercept_is_stable_when_the_same_step_is_decided_twice() -> None:
    """The degrade path re-enters `_pick_move` within one turn; the drift estimate
    must not consume itself (same step in => same answer out)."""
    board = CONSTITUTION.board.make_board()
    brain = PoliceBrain(seed=7, options={"intercept_enabled": 1.0, "p_commit": 0.9})
    brain.decide(_observation(board, (3, 6), step=1), _delta_belief((3, 2)))
    brain.decide(_observation(board, (3, 6), step=2), _delta_belief((3, 3)))
    belief = _delta_belief((3, 4))
    first = brain.decide(_observation(board, (3, 6), step=3), belief)
    second = brain.decide(_observation(board, (3, 6), step=3), belief)
    assert first == second
