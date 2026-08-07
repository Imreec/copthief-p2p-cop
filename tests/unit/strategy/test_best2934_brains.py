"""best2934 opponent arms (M7-45) — the arena stand-ins for our second counted opponent.

Modelled from their PUBLISHED brains (github.com/Krayz1a/best2934-cop, MIT, (c) 2026
Tomer Levy / Eyal Koloshi / Alon Issman), same practice as M7-14's `belief-evader` for
anrbj666. Each test pins the ONE behaviour that distinguishes their policy from the
baselines we already field, because an arm that plays like `greedy-manhattan` measures
nothing about them.
"""

from pathlib import Path

from copthief_core.shared.config import load_all
from copthief_core.strategy.best2934_brains import Best2934CopBrain, Best2934ThiefBrain
from copthief_core.strategy.brains import Observation
from copthief_core.strategy.referee_setup import referee_belief

CONSTITUTION, PRIVATE, _ = load_all(Path("config"), counted=False)
TRUST = PRIVATE.smell_trust_weight


def _observation(board: object, position: tuple[int, int], role: str, **kw: object) -> Observation:
    return Observation(
        board=board,  # type: ignore[arg-type]
        position=position,
        move_set=CONSTITUTION.movement.move_set,
        role=role,
        step=int(kw.pop("step", 1)),
        survival_threshold=int(kw.pop("survival_threshold", 0)),
        barriers_used=int(kw.pop("barriers_used", 0)),
        max_barriers=int(kw.pop("max_barriers", 0)),
    )


def _delta_belief(cell: tuple[int, int]) -> object:
    return referee_belief(CONSTITUTION, start=cell, smell_trust=TRUST)


# --------------------------------------------------------------------- their thief


def test_the_thief_refuses_a_cell_adjacent_to_the_believed_cop() -> None:
    """Their ADJACENCY_PENALTY (6.0) dominates every other term: a destination within
    one step of the belief peak is close to fatal and is never chosen while a legal
    alternative exists. This is the term our cop's approach has to defeat."""
    board = CONSTITUTION.board.make_board()
    brain = Best2934ThiefBrain(seed=1)
    move = brain.pick_move(_observation(board, (3, 3), "thief"), _delta_belief((3, 5)))
    dest = board.apply_move((3, 3), move)
    assert abs(dest[0] - 3) + abs(dest[1] - 5) > 1


def test_the_thief_prefers_open_space_over_raw_distance() -> None:
    """AREA_WEIGHT is the point of their design: fleeing into a pocket is what a
    barrier-building cop wants. With the two directions tied on distance, the one
    that keeps more board reachable wins — the opposite of a pure distance-maximiser."""
    board = CONSTITUTION.board.make_board()
    for cell in ((0, 2), (1, 2), (2, 2)):  # wall off the top-left corner pocket
        board = board.with_barrier(cell)
    brain = Best2934ThiefBrain(seed=1)
    move = brain.pick_move(_observation(board, (1, 1), "thief"), _delta_belief((5, 1)))
    assert move != "N"  # N drives deeper into the sealed pocket


def test_the_thief_switches_to_pure_distance_in_the_endgame() -> None:
    """Inside ENDGAME_WINDOW (4) of the survival threshold they drop the area term to
    0.05 and double distance: with two steps left, not being adjacent is all that
    counts. Same board and belief as the area test, opposite preference."""
    board = CONSTITUTION.board.make_board()
    brain = Best2934ThiefBrain(seed=1)
    early = brain.pick_move(
        _observation(board, (3, 3), "thief", step=1, survival_threshold=35), _delta_belief((3, 1))
    )
    late = brain.pick_move(
        _observation(board, (3, 3), "thief", step=33, survival_threshold=35), _delta_belief((3, 1))
    )
    assert late == "S"  # straight away from the cop, area disregarded
    assert early in {"S", "E", "W"}


def test_the_thief_is_penalised_for_standing_still() -> None:
    """IDLE_PENALTY (1.0): camping saturates their own scent field and paints a target."""
    board = CONSTITUTION.board.make_board()
    brain = Best2934ThiefBrain(seed=1)
    move = brain.pick_move(_observation(board, (3, 3), "thief"), _delta_belief((3, 1)))
    assert move != "STAY"


# ----------------------------------------------------------------------- their cop


def test_the_cop_closes_on_the_belief_peak() -> None:
    """Their movement term is greedy descent on belief-weighted distance."""
    board = CONSTITUTION.board.make_board()
    brain = Best2934CopBrain(seed=1)
    move = brain.pick_move(_observation(board, (3, 3), "police"), _delta_belief((3, 6)))
    assert move == "S"


def test_the_cop_does_not_wall_beyond_its_engage_range() -> None:
    """THE fielded parameter, and the one that makes them dangerous or harmless:
    `barrier_engage_range` was tuned 4 -> 1 on their own sweep (capture 1.000 at range
    1, 0.000 at range 3). Beyond it a wall costs a turn of movement for nothing, so
    they move instead. At distance 3 the decision must be a move, never a barrier."""
    board = CONSTITUTION.board.make_board()
    brain = Best2934CopBrain(seed=1, options={"barrier_engage_range": 1})
    decision = brain.decide(
        _observation(board, (3, 3), "police", max_barriers=14), _delta_belief((3, 6))
    )
    assert decision.barrier is None


def test_the_cop_seals_at_contact_range() -> None:
    """Inside the engage range a barrier that shrinks the thief's reachable area by at
    least `barrier_min_gain` is worth the turn. This is the rule-46 enclosure capture
    that won both of their live sub-games against gal-roy1."""
    board = CONSTITUTION.board.make_board()
    for cell in ((0, 1), (1, 1)):  # thief in the top-left pocket, one mouth left at (2,0)
        board = board.with_barrier(cell)
    brain = Best2934CopBrain(seed=1, options={"barrier_engage_range": 1})
    decision = brain.decide(
        _observation(board, (1, 0), "police", max_barriers=14), _delta_belief((0, 0))
    )
    assert decision.barrier is not None
    assert decision.move == "STAY"


def test_the_cop_holds_its_endgame_reserve() -> None:
    """BARRIER_ENDGAME_RESERVE (3): with the quota nearly spent they only wall for a
    squeeze they can finish (distance <= 2), so a marginal seal is declined."""
    board = CONSTITUTION.board.make_board()
    for cell in ((0, 1), (1, 1)):
        board = board.with_barrier(cell)
    brain = Best2934CopBrain(seed=1, options={"barrier_engage_range": 1})
    decision = brain.decide(
        _observation(board, (1, 0), "police", barriers_used=12, max_barriers=14),
        _delta_belief((0, 0)),
    )
    assert decision.barrier is not None  # distance 1 <= 2, still inside the squeeze
