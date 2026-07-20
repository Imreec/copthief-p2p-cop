"""The locked-model registry (ADR-0004 v2 item 5; kit SPEC §7).

Two properties matter here and nowhere else: our declared hash equals the KIT's pin
byte-for-byte (otherwise the lock is a private ritual, not an interop artifact), and a
registration that contradicts the signed constitution is refused before it can be
declared (otherwise we announce physics we do not play).
"""

import json
from pathlib import Path
from typing import Any

import pytest

from copthief_core.shared.config_model import PheromoneParams
from copthief_core.shared.locked_models import (
    SCENT_MODEL,
    LockedModelError,
    LockedModelRegistry,
    assert_agrees_with,
    load_locked_models,
    lock_decision,
)

REGISTRY = load_locked_models(Path("config/locked_models.json"))
KIT = json.loads(
    (Path("tests/conformance/vectors/locked_model.json")).read_text(encoding="utf-8")
)
SHIPPED = PheromoneParams(center_intensity=0.9, decay=0.1, grid_size=5, min_center_intensity=0.5)


def _kit_entry(name: str) -> dict[str, Any]:
    return next(r for r in KIT["registered"] if r["doc"]["name"] == name)


def test_every_committed_registration_hashes_to_the_kit_pin() -> None:
    """The whole point: our bytes and the kit's bytes are the same bytes."""
    for entry in KIT["registered"]:
        doc = entry["doc"]
        assert REGISTRY.hash(doc["family"], doc["name"]) == entry["sha256"], doc["name"]


def test_alons_re_emitted_lock_hash_is_the_one_we_declare() -> None:
    """Cross-team pin: anrbj666's re-emitted `934c220d…` == the kit registry pin."""
    assert REGISTRY.hash(SCENT_MODEL, "multiplicative_book_v1") == _kit_entry(
        "multiplicative_book_v1"
    )["sha256"]


def test_the_declared_key_is_the_family_suffixed_form() -> None:
    assert LockedModelRegistry.declared_key(SCENT_MODEL) == "scent_model_sha256"


def test_an_unregistered_name_is_refused_not_silently_skipped() -> None:
    with pytest.raises(LockedModelError, match="no registration"):
        REGISTRY.doc(SCENT_MODEL, "gaussian_fitted_v9")


def test_a_registry_without_a_version_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "locked_models.json"
    path.write_text(json.dumps({"models": {}}), encoding="utf-8")
    with pytest.raises(LockedModelError, match="carries no version"):
        load_locked_models(path)


def test_both_shipped_scent_registrations_agree_with_the_signed_constitution() -> None:
    for name in ("subtractive_chebyshev_v1", "multiplicative_book_v1"):
        assert_agrees_with(REGISTRY.doc(SCENT_MODEL, name), SHIPPED)


def test_a_registration_that_contradicts_the_signed_terms_is_refused() -> None:
    """A changed pheromone value IS a different model; it must earn a new registration
    rather than ride the old hash."""
    drifted = PheromoneParams(
        center_intensity=0.9, decay=0.2, grid_size=5, min_center_intensity=0.5
    )
    with pytest.raises(LockedModelError, match="disagrees with the signed constitution"):
        assert_agrees_with(REGISTRY.doc(SCENT_MODEL, "subtractive_chebyshev_v1"), drifted)


def test_the_refusal_rule_reproduces_the_kit_truth_table() -> None:
    """Five rows, and only ONE of them refuses (kit SPEC §7; ADR-0004 v2 decision 3)."""
    for row in KIT["refusal_rule"]:
        assert lock_decision(row["ours"], row["theirs"]) == row["decision"], row["note"]


def test_omission_is_never_refusal_in_either_direction() -> None:
    """A lock that fail-fasts on silence cannot start a game against the reference peer."""
    ours = REGISTRY.hash(SCENT_MODEL, "subtractive_chebyshev_v1")
    assert lock_decision(ours, None) == "play"
    assert lock_decision(None, ours) == "play"
    assert lock_decision(None, None) == "play"
