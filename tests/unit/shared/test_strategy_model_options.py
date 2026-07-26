"""Per-model strategy weights (M7-15): `[strategy.<role>.<scent_model>]` overlays.

The M7-14 gate comparison proved the tuned vectors are PHYSICS-SPECIFIC (the book-v1
winner loses the reference table and vice versa), so deployment must follow the
selected model. These pin the mechanism: the base `[strategy.<role>]` table stays
authoritative, a sub-table named after a scent model overlays it ONLY when that
model is the selected one, and configs without sub-tables parse exactly as before.
"""

from pathlib import Path

from copthief_core.shared.private_config import load_private_settings

BASE_TOML = (Path("config") / "game.toml").read_text(encoding="utf-8")
PER_MODEL = """
[strategy.police.multiplicative_book_v1]
w_budget = 0.0
w_distance = 9.9
"""


def _load(tmp_path: Path, toml_text: str) -> object:
    (tmp_path / "locked_models.json").write_bytes(
        (Path("config") / "locked_models.json").read_bytes()
    )
    path = tmp_path / "game.toml"
    path.write_text(toml_text, encoding="utf-8")
    return load_private_settings(path)


def test_a_per_model_sub_table_overlays_only_under_its_model(tmp_path: Path) -> None:
    text = BASE_TOML.replace('model = "subtractive_chebyshev_v1"', 'model = "multiplicative_book_v1"')
    private = _load(tmp_path, text + PER_MODEL)
    options = private.strategy_options("police")
    assert options["w_budget"] == 0.0  # the overlay
    assert options["w_distance"] == 9.9  # the overlay
    assert options["p_commit"] == 0.2  # the base table survives underneath


def test_the_sub_table_is_inert_under_a_different_model(tmp_path: Path) -> None:
    private = _load(tmp_path, BASE_TOML + PER_MODEL)  # shipped default model
    options = private.strategy_options("police")
    assert options["w_budget"] == 1.7277  # the base GA value, not the overlay
    assert options["w_distance"] == 3.8875


def test_a_config_without_sub_tables_parses_exactly_as_before(tmp_path: Path) -> None:
    private = _load(tmp_path, BASE_TOML)
    assert private.strategy_options("police") == private.police_options
    assert private.strategy_options("thief") == private.thief_options
