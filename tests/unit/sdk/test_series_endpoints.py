"""Where the opponent listens, per sub-game (M7-11).

Two topologies exist in the league and both are real: the reference runs a whole
series as ONE process at ONE address, while Alon's team serves TWO role-split
services, each owning half the sub-games (his committed `league_series.py`). A
driver that dials one URL for all six games is wrong half the time against the
second shape — so the mapping from "their role this sub-game" to "the URL we
dial" is a pure, pinned decision, not an inline default.
"""

from __future__ import annotations

import pytest

from copthief_core.sdk.series_endpoints import SeriesEndpoints, resolve_endpoints

POLICE_URL = "https://cop-mcp.example.test/mcp"
THIEF_URL = "https://thief-mcp.example.test/mcp"
ONE_URL = "https://peer.example.test/mcp"


def test_one_address_serves_both_roles() -> None:
    endpoints = resolve_endpoints(single=ONE_URL)
    assert endpoints.for_opponent_role("police") == ONE_URL
    assert endpoints.for_opponent_role("thief") == ONE_URL


def test_role_split_addresses_dial_by_their_role_that_game() -> None:
    endpoints = resolve_endpoints(police_url=POLICE_URL, thief_url=THIEF_URL)
    assert endpoints.for_opponent_role("police") == POLICE_URL
    assert endpoints.for_opponent_role("thief") == THIEF_URL


def test_mixing_single_and_split_addresses_is_refused() -> None:
    """An operator who typed both meant one of them; guessing which loses a series."""
    with pytest.raises(ValueError, match="either ONE"):
        resolve_endpoints(single=ONE_URL, police_url=POLICE_URL, thief_url=THIEF_URL)


def test_half_a_split_pair_is_refused_naming_the_missing_half() -> None:
    with pytest.raises(ValueError, match="thief"):
        resolve_endpoints(police_url=POLICE_URL)


def test_no_address_at_all_is_refused() -> None:
    with pytest.raises(ValueError, match="no opponent address"):
        resolve_endpoints()


def test_blank_strings_count_as_absent() -> None:
    """The config default for `opponent_url` is "" — a blank must never be dialed."""
    endpoints = resolve_endpoints(single="", police_url=POLICE_URL, thief_url=THIEF_URL)
    assert endpoints.for_opponent_role("police") == POLICE_URL


def test_an_unknown_role_is_refused() -> None:
    endpoints = SeriesEndpoints(police_url=POLICE_URL, thief_url=THIEF_URL)
    with pytest.raises(ValueError, match="unknown role"):
        endpoints.for_opponent_role("cop")
