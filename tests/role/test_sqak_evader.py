"""uoh-sqak rewritten-evader arm pins (M7-48) — ⚑ police repo, opponent model only.

Pins what the arm exists to model: their FIELDED values (not class defaults), the ROOM
objective that replaced distance-maximising, and the two tie-break behaviours their own
commit says were load-bearing — seeded randomness, and never standing still on a tie.
"""

from copthief_core.domain.belief import BeliefFilter
from copthief_core.domain.board import Board
from copthief_core.strategy.brains import Observation
from copthief_police.sqak_evader import EVADER_DEFAULTS, SqakEvaderThiefBrain

MOVE_SET = ("N", "S", "E", "W", "STAY")


def make_board(barriers: frozenset = frozenset()) -> Board:  # type: ignore[type-arg]
    return Board(grid_size=7, axis_origin_corner="top-left", axis_start_index=0, barriers=barriers)


def make_belief(board: Board, cop_at: tuple[int, int]) -> BeliefFilter:
    return BeliefFilter(
        board=board,
        move_set=MOVE_SET,
        start=cop_at,
        center_intensity=0.9,
        decay=0.1,
        smell_trust=4.0,
        hint_trust=0.0,
    )


def observation(board: Board, position: tuple[int, int], *, step: int = 1) -> Observation:
    return Observation(
        board=board,
        position=position,
        move_set=MOVE_SET,
        role="thief",
        step=step,
        max_barriers=14,
        survival_threshold=35,
        max_moves=35,
    )


def test_the_fielded_weights_are_the_ones_they_play() -> None:
    """config/thief/game.toml [strategy] @ 1ca9d23 — NOT the class defaults.

    `w_exits` is 1.0 there against a class default of 0.3 (their comment: "measured:
    0.3 -> 1.0 doubles survival"), and `w_risk` is 1.0 against a default of 3.0.
    """
    assert EVADER_DEFAULTS["w_exits"] == 1.0
    assert EVADER_DEFAULTS["w_risk"] == 1.0
    assert EVADER_DEFAULTS["w_dist"] == 1.0
    assert EVADER_DEFAULTS["w_reach"] == 0.15


def test_it_leaves_a_corner_rather_than_camping_in_it() -> None:
    """The whole point of their rewrite: the old brain parked at (6,6) and was sealed."""
    board = make_board()
    brain = SqakEvaderThiefBrain(seed=1)
    move = brain.pick_move(observation(board, (6, 6)), make_belief(board, (3, 3)))
    assert move != "STAY"


def test_the_rewrite_fixed_parking_not_corner_seeking() -> None:
    """Worth knowing before we tune a cop against it: on an OPEN board their new
    objective still rates the far corner highest. `w_dist` and `w_exits` are both 1.0,
    so twelve cells of distance beat two lost exits (21.35 against 19.35, from (0,0)).
    What the rewrite changed is that the thief no longer STANDS there — the tie-break
    drops STAY — so the cop no longer gets free tempo to seal a two-exit cell.
    """
    board = make_board()
    brain = SqakEvaderThiefBrain(seed=1)
    corner = brain._score(board, (6, 6), (0, 0), MOVE_SET)
    open_ground = brain._score(board, (4, 4), (0, 0), MOVE_SET)
    assert corner > open_ground


def test_room_wins_once_walls_make_the_corner_small() -> None:
    """The reachability term is what their commit message is about: a corner cut down
    to a pocket stops being attractive, however far away it is."""
    board = make_board(frozenset({(5, 6), (6, 5)}))
    brain = SqakEvaderThiefBrain(seed=1)
    pocket = brain._score(board, (6, 6), (0, 0), MOVE_SET)
    open_ground = brain._score(board, (4, 4), (0, 0), MOVE_SET)
    assert open_ground > pocket


def test_the_adjacent_cell_penalty_bites() -> None:
    board = make_board()
    brain = SqakEvaderThiefBrain(seed=1)
    opts = {**EVADER_DEFAULTS}
    touching = brain._score(board, (3, 3), (3, 4), MOVE_SET)
    clear = brain._score(board, (3, 3), (3, 5), MOVE_SET)
    assert clear - touching > opts["w_risk"]  # the risk term plus the lost distance


def test_a_walled_in_thief_still_answers(  ) -> None:
    """No legal move must degrade to STAY, never raise — the arm plays a full series."""
    board = make_board(frozenset({(0, 1), (1, 0)}))
    brain = SqakEvaderThiefBrain(seed=1)
    assert brain.pick_move(observation(board, (0, 0)), make_belief(board, (6, 6))) == "STAY"


def test_the_tie_break_is_seeded_not_fixed() -> None:
    """Their runtime seeds it `Random(play.seed + sub_game_number)`, so a series draws a
    different stream per sub-game: their THIEF is not deterministic, only their cop is."""
    board = make_board()
    belief = make_belief(board, (0, 0))
    draws = {
        SqakEvaderThiefBrain(seed=seed).pick_move(observation(board, (3, 3)), belief)
        for seed in range(24)
    }
    assert len(draws) > 1
