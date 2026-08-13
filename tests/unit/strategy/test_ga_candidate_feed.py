"""The GA evolves UNDER the information structure the candidate will field (M11 part 2).

Every armed brain we deploy reads a configured feed (the live evader and cop run
the sharp fresh-peak tier), but GA fitness always ran the CANDIDATE on the
hidden default — knobs harvested under blur it will not play with. The
`candidate_feed` door closes that: run-level, defaulting to None (the
historical behavior, so no committed GA artifact is invalidated).

Role-blind: nothing here names this repo's brain or its shipped values.
"""

from pathlib import Path

from copthief_core.shared.config import load_all
from copthief_core.strategy.genetic.fitness import opponent_fitness
from copthief_core.strategy.genetic.runs import GaConfig, load_ga_config
from copthief_core.strategy.scenarios import scenario_suite

CONSTITUTION, PRIVATE, _LIMITS = load_all(Path("config"), counted=False)
SHIPPED = load_ga_config(Path("config") / "ga.json")


def test_candidate_feed_defaults_to_the_historical_hidden_run() -> None:
    assert SHIPPED.candidate_feed is None


def _chaser_config(candidate_feed: str | None) -> GaConfig:
    """A belief-chasing cop as the candidate: what it knows is what it catches."""
    fields = {k: getattr(SHIPPED, k) for k in SHIPPED.__dataclass_fields__}
    fields.update(
        role="police",
        brain="greedy-manhattan",
        opponent="random",
        opponent_options={},
        opponent_feed=None,
        opponent_pool=(),
        candidate_feed=candidate_feed,
    )
    return GaConfig(**fields)


def _fitness(candidate_feed: str | None) -> float:
    scenarios = scenario_suite(CONSTITUTION, seeds=[1, 2, 3, 4, 5, 6, 7, 8], min_separation=4)
    return opponent_fitness(
        _chaser_config(candidate_feed),
        CONSTITUTION,
        smell_trust=PRIVATE.smell_trust_weight,
        scenarios=scenarios,
        candidate_options={},
        opponent={"spec": "random"},
        locked_models=PRIVATE.locked_models,
    )


def test_fitness_runs_under_the_candidates_feed() -> None:
    """A truth-fed chaser sees the true cell and must convert at least as often
    as the blurred one — and on this suite, strictly more (non-vacuous pin)."""
    truth = _fitness("truth")
    hidden = _fitness(None)
    assert truth >= hidden
    assert truth > hidden  # the door demonstrably changes what fitness measures
