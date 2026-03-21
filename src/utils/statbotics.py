"""Utility functions for fetching and caching Statbotics EPA data."""

import json
import os
from datetime import datetime

import requests
import streamlit as st

from .constants import EventSpecificConstants, GeneralConstants

__all__ = [
    "retrieve_statbotics_data",
    "get_team_statbotics",
    "statbotics_quantile",
]

_STATBOTICS_BASE_URL = "https://api.statbotics.io/v3"
_CACHE_PATH = f"./src/data/statbotics_{EventSpecificConstants.EVENT_CODE}.json"


def _fetch_from_api() -> dict[str, dict]:
    """Fetches EPA data for every team at the event from the Statbotics API.

    :return: A dict mapping team number strings to their EPA breakdown dicts.
    :raises requests.HTTPError: If the API returns a non-2xx response.
    """
    response = requests.get(
        f"{_STATBOTICS_BASE_URL}/team_events",
        params={"event": EventSpecificConstants.EVENT_CODE, "limit": 100},
        timeout=10,
    )
    response.raise_for_status()

    teams: dict[str, dict] = {}
    for entry in response.json():
        team_num = str(entry["team"])
        epa = entry.get("epa", {})
        bd = epa.get("breakdown", {})

        def _safe(val) -> float:
            return round(float(val), 2) if val is not None else 0.0

        teleop_fuel  = _safe(bd.get("teleop_fuel"))
        endgame_fuel = _safe(bd.get("endgame_fuel"))
        raw_sd = epa.get("total_points", {}).get("sd")
        teams[team_num] = {
            "total_epa":            _safe(epa.get("total_points", {}).get("mean")),
            "total_epa_sd":         _safe(raw_sd) if raw_sd else 10.0,
            "auto_fuel":            _safe(bd.get("auto_fuel")),
            "teleop_endgame_fuel":  round(teleop_fuel + endgame_fuel, 2),
            "tower_points":         _safe(bd.get("endgame_tower")),
        }

    return teams


@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE * 4)
def retrieve_statbotics_data() -> dict[str, dict]:
    """Retrieves Statbotics EPA data for all teams at the current event.

    When a network connection is available the data is fetched from the
    Statbotics API and persisted to a local JSON cache so it remains
    accessible offline.  If the API is unreachable the cached file is
    used as a fallback.

    :return: A dict mapping team number strings to their EPA breakdown dicts.
             Returns an empty dict if neither the API nor the cache is available.
    """
    try:
        teams = _fetch_from_api()
        os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
        with open(_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump({"last_updated": datetime.now().isoformat(), "teams": teams}, f, indent=2)
        return teams
    except Exception:
        try:
            with open(_CACHE_PATH, encoding="utf-8") as f:
                return json.load(f)["teams"]
        except Exception:
            return {}


def get_team_statbotics(team_number: int) -> dict:
    """Returns the Statbotics EPA dict for a single team.

    :param team_number: The FRC team number.
    :return: A dict with EPA fields, or an empty dict if no data is available.
    """
    return retrieve_statbotics_data().get(str(team_number), {})


def statbotics_quantile(field: str, q: float = 0.5) -> float:
    """Computes a quantile across all teams for a given Statbotics field.

    :param field: The key in each team's EPA breakdown dict.
    :param q: Quantile level between 0.0 and 1.0.
    :return: The quantile value, or 0.0 if no data is available.
    """
    values = sorted(
        v[field]
        for v in retrieve_statbotics_data().values()
        if field in v and v[field] is not None
    )
    if not values:
        return 0.0
    idx = min(int(len(values) * q), len(values) - 1)
    return values[idx]
