"""Referee games under a selected scent model + per-side feeds (M7-14).

Two doors the counted-series prep needs: the whole referee world (both trails, both
observation models) can run `multiplicative_book_v1`, and the two sides' information
structures can differ (the claim-reading counter is thief-side lag-1 truth while our
cop stays hidden-info). Determinism pins ride along — the arena's reproducibility
contract must survive both doors.
"""

from pathlib import Path

from copthief_core.shared.config import load_all
from copthief_core.shared.locked_models import build_scent_model
from copthief_core.strategy.brains import make_brain
from copthief_core.strategy.info_feed import TruthFeed
from copthief_core.strategy.referee import play_referee_game

CONSTITUTION, PRIVATE, _ = load_all(Path("config"), counted=False)
BOOK = build_scent_model(
    PRIVATE.locked_models, "multiplicative_book_v1", CONSTITUTION.pheromones
)
SEEDS = range(1, 9)


def _series(scent_model: object = None, thief_feed: object = None) -> list[tuple[str, int]]:
    results = []
    for seed in SEEDS:
        game = play_referee_game(
            CONSTITUTION,
            police_brain=make_brain("greedy-manhattan", seed=2 * seed),
            thief_brain=make_brain("greedy-manhattan", seed=2 * seed + 1),
            smell_trust=PRIVATE.smell_trust_weight,
            seed=seed,
            scent_model=scent_model,  # type: ignore[arg-type]
            thief_belief_feed=thief_feed,  # type: ignore[arg-type]
        )
        results.append((game.outcome.value, game.steps))
    return results


def test_book_model_games_are_deterministic() -> None:
    assert _series(scent_model=BOOK) == _series(scent_model=BOOK)


def test_the_selected_model_reaches_behavior() -> None:
    """If the book physics never changes a single game across eight seeds, the door
    is decorative — the M3-8 belief measurements say the two models disagree hard."""
    assert _series(scent_model=BOOK) != _series()


def test_the_thief_feed_can_differ_from_the_police_feed() -> None:
    """Thief on full information, cop still hidden — the asymmetric shape the
    trap-aware-evader measurement needs (the wire-shape balance study proved full
    info flips evader behavior, so at least one of eight games must move)."""
    truth = TruthFeed(CONSTITUTION, smell_trust=PRIVATE.smell_trust_weight)
    assert _series(thief_feed=truth) != _series()
    assert _series(thief_feed=truth) == _series(thief_feed=truth)
