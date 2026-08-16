"""M13p2 interception positioning (ADR-0017) — ⚑ police repo.

The wire grades a landing against the thief's CURRENT cell (ADR-0016), so prediction
buys POSITIONING: value cop destinations by the probability that the thief's next
cell lands adjacent to us — the geometry from which the following turn's landing is
graded. `reply_distribution` spreads the posterior one thief-move under a motion
model; `adjacency_value` scores a cop destination against it.
"""

from copthief_core.domain.board import Board
from copthief_police.reply_forecast import adjacency_value, reply_distribution

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board(barriers: frozenset = frozenset()) -> Board:  # type: ignore[type-arg]
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def test_reply_distribution_spreads_one_thief_move() -> None:
    """A certain thief at (3,3): five legal replies, uniform mass 0.2 each."""
    board = make_board()
    replies = reply_distribution({(3, 3): 1.0}, board, MOVE_SET)
    assert replies == {
        (2, 3): 0.2,
        (4, 3): 0.2,
        (3, 2): 0.2,
        (3, 4): 0.2,
        (3, 3): 0.2,
    }


def test_reply_distribution_respects_walls() -> None:
    """A walled reply redistributes nothing — the move is illegal, not redirected."""
    board = make_board(frozenset({(2, 3)}))
    replies = reply_distribution({(3, 3): 1.0}, board, MOVE_SET)
    assert (2, 3) not in replies
    assert abs(sum(replies.values()) - 1.0) < 1e-9
    assert all(abs(v - 0.25) < 1e-9 for v in replies.values())


def test_adjacency_value_counts_mass_within_one_step() -> None:
    """Cop destination (4,4) vs a certain thief at (3,3): the replies adjacent to
    (4,4) are (4,3) and (3,4) — 0.4 of the reply mass. The thief's own cell (3,3)
    is distance 2, NOT adjacent."""
    board = make_board()
    replies = reply_distribution({(3, 3): 1.0}, board, MOVE_SET)
    assert abs(adjacency_value((4, 4), replies) - 0.4) < 1e-9


def test_adjacency_value_excludes_colocation() -> None:
    """Mass that steps ONTO the cop's destination is not adjacency — a co-located
    thief cannot be landed on (M13: co-location is not a capture state), so it
    contributes nothing to next-turn convertibility."""
    board = make_board()
    replies = reply_distribution({(3, 3): 1.0}, board, MOVE_SET)
    # Cop destination (3,3) itself: replies adjacent to it are the four ring cells
    # it can be re-entered from; the STAY mass AT (3,3) is co-location, excluded.
    assert abs(adjacency_value((3, 3), replies) - 0.8) < 1e-9


def test_a_dominant_intercept_weight_picks_the_adjacency_maximizing_move() -> None:
    """Property pin: with w_intercept overpowering every other term, the brain's
    chosen move maximizes reply-adjacency among the legal moves — and at the
    default 0.0 the existing decision pins (test_police_brain) hold unchanged."""
    from copthief_core.domain.belief import BeliefFilter
    from copthief_core.strategy.brains import Observation
    from copthief_police.brain import PoliceBrain

    board = make_board(frozenset({(0, 2)}))
    belief = BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=(0, 3),
        center_intensity=0.9,
        decay=0.1,
        smell_trust=4.0,
        hint_trust=1.0,
    )
    obs = Observation(
        board=board,
        position=(2, 2),
        move_set=MOVE_SET,
        role="police",
        step=5,
        barriers_used=14,
        max_barriers=14,
    )
    brain = PoliceBrain(seed=1, options={"w_intercept": 10000.0, "endgame_enabled": 0.0})
    decision = brain.decide(obs, belief)
    replies = reply_distribution(belief.probs(), board, MOVE_SET)
    chosen_dest = board.apply_move(obs.position, decision.move)
    best = max(
        adjacency_value(board.apply_move(obs.position, m), replies)
        for m in ("N", "S", "E", "W", "STAY")
        if not board.is_blocked(board.apply_move(obs.position, m))
    )
    assert abs(adjacency_value(chosen_dest, replies) - best) < 1e-9
