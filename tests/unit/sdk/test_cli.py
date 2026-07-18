"""CLI entry (TODO M1-7): `run local-match` — one command, JSON out, sdk-only access."""

import json

import pytest

from copthief_core.sdk.cli import main


def test_run_local_match_prints_a_verified_result(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["run", "local-match", "--police-seed", "5", "--thief-seed", "6"])
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["outcome"] == "thief_survival"
    assert payload["audit_ok_police_side"] is True
    assert payload["audit_ok_thief_side"] is True
    assert payload["game_uid"]


def test_unknown_command_fails_loudly() -> None:
    with pytest.raises(SystemExit):
        main(["run", "teleport"])


def test_gui_flag_parses_and_defaults_off() -> None:
    # M4-2: --gui opens the live view on `peer` and `local-match`; default stays
    # headless so CI and scripts never touch a display stack.
    from copthief_core.sdk.cli import _parser

    parser = _parser()
    assert parser.parse_args(["run", "peer", "--role", "police", "--gui"]).gui is True
    assert parser.parse_args(["run", "local-match"]).gui is False
