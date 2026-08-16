"""PoliceBrain behavior pins (TODO M5-2; PRD_police_brain §5) — ⚑ police repo only.

Expectimax over the truncated belief + capture-commit + determinism. The brain reads
the belief through its public surface, proposes through the Decision seam, and every
knob arrives via options (data-table defaults, config overrides — AppFTable pattern).
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation, make_brain
from copthief_core.strategy.region import path_length
from copthief_police.brain import PoliceBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board(barriers: frozenset = frozenset()) -> Board:  # type: ignore[type-arg]
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def make_belief(board: Board, opponent_at: tuple[int, int]) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=opponent_at,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=4.0,
        hint_trust=1.0,
    )


def observation(
    board: Board,
    position: tuple[int, int],
    *,
    step: int = 1,
    barriers_used: int = 0,
    max_barriers: int = 14,
) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="police",
        step=step,
        barriers_used=barriers_used,
        max_barriers=max_barriers,
    )


def test_capture_commit_steps_onto_a_certain_adjacent_cell() -> None:
    board = make_board()
    belief = make_belief(board, (3, 4))  # certain: the thief is due east
    decision = PoliceBrain(seed=1).decide(observation(board, (3, 3)), belief)
    assert decision.barrier is None
    assert decision.move == "E"  # step onto the mass; the claim rides free (SQ2)


def test_closes_distance_toward_a_certain_far_target() -> None:
    board = make_board()
    belief = make_belief(board, (6, 6))
    decision = PoliceBrain(seed=1).decide(observation(board, (0, 0)), belief)
    assert decision.move in {"S", "E"}


def test_refuses_the_pocket_seal_that_locks_us_out() -> None:
    """⚠ EXPECTATION REVERSED at M7-49; the original is preserved in the body below.

    This test used to assert `decision.barrier == (5, 5)` — "graph surgery: one wall
    seals the region". Measured against the 2026-08-08 friendly, that is a LOSING move
    and the original expectation was wrong.

    Row 6 is sealed from row 5 except the entrance at (5, 5), and the thief is at (6, 0).
    Walling (5, 5) does cut its region to seven cells — and leaves `path_length(cop,
    thief) is None`, so the cop can never enter. A thief with seven cells and no pursuer
    simply runs out the clock: the "seal" converts a hunt into a guaranteed survival.
    Leaving the entrance open keeps a seven-step route into a ONE-WIDE corridor, which
    is the best terrain a pursuer can ask for.

    This is not hypothetical. Our cop played the same shape in friendly g03: it walled
    (5,6) to complete a two-cell pocket around their camping thief, sealed itself out,
    and then stood at (4,5) playing STAY for sixteen turns with eleven barriers unspent.
    """
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))  # far end of the pocket
    decision = PoliceBrain(seed=1).decide(
        observation(board, (4, 5), barriers_used=len(walls)), belief
    )
    assert decision.barrier != (5, 5)
    if decision.barrier is not None:
        assert path_length(board.with_barrier(decision.barrier), (4, 5), (6, 0), MOVE_SET)


def test_never_walls_with_quota_spent() -> None:
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))
    decision = PoliceBrain(seed=1).decide(
        observation(board, (4, 5), barriers_used=14, max_barriers=14), belief
    )
    assert decision.barrier is None


def test_barrier_threshold_option_disables_surgery() -> None:
    walls = frozenset({(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)})
    board = make_board(barriers=walls)
    belief = make_belief(board, (6, 0))
    brain = PoliceBrain(seed=1, options={"barrier_gain_threshold": 1e9})
    decision = brain.decide(observation(board, (4, 5), barriers_used=len(walls)), belief)
    assert decision.barrier is None  # the config knob really governs the policy


def test_decisions_are_deterministic_and_always_legal() -> None:
    board = make_board(barriers=frozenset({(2, 3), (3, 2)}))
    belief = make_belief(board, (0, 6))
    for _ in range(2):
        first = PoliceBrain(seed=7).decide(observation(board, (3, 3)), belief)
        again = PoliceBrain(seed=7).decide(observation(board, (3, 3)), belief)
        assert first == again
    assert first.move in MOVE_SET


def test_factory_builds_the_dotted_spec() -> None:
    brain = make_brain("copthief_police.brain:PoliceBrain", seed=3)
    assert isinstance(brain, PoliceBrain)


# -- M13 (ADR-0016): the brain prices its own landing --------------------------------------


def test_commit_decision_carries_the_hunted_posteriors_confidence() -> None:
    """The claim gate's input is the SAME posterior the brain hunted — a certain
    adjacent thief commits with confidence ~1.0 on the landing cell."""
    board = make_board()
    belief = make_belief(board, (3, 4))
    decision = PoliceBrain(seed=1).decide(observation(board, (3, 3)), belief)
    assert decision.move == "E"
    assert decision.landing_confidence is not None
    assert decision.landing_confidence > 0.9


def test_expectimax_moves_price_their_landing_from_the_same_posterior() -> None:
    """A far target: the landing cell holds ~none of the posterior, and the decision
    says so — the gate can stay honest about non-capture steps."""
    board = make_board()
    belief = make_belief(board, (6, 6))
    decision = PoliceBrain(seed=1).decide(observation(board, (0, 0)), belief)
    assert decision.landing_confidence is not None
    assert decision.landing_confidence < 0.1


def test_parity_bonus_prices_even_distance_and_nothing_else() -> None:
    """M13 (ADR-0016): w_parity adds exactly its weight at even Manhattan distance,
    zero at odd — and 0.0 (the default) is the shipped stream byte-identical."""
    from copthief_police.features import leaf_value, resolve_options

    board = make_board()
    base = resolve_options({})
    armed = resolve_options({"w_parity": 2.0})
    even = ((0, 0), (2, 0))  # distance 2
    odd = ((0, 0), (1, 0))  # distance 1
    for (cop, thief), expected_delta in ((even, 2.0), (odd, 0.0)):
        plain = leaf_value(board, cop, thief, MOVE_SET, base, {})
        priced = leaf_value(board, cop, thief, MOVE_SET, armed, {})
        assert priced == plain + expected_delta
