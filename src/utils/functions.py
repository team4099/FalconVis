"""Defines utility functions that are later used in FalconVis."""
from io import StringIO
from re import search
from typing import Any

import streamlit as st
from pandas import DataFrame, read_csv
from requests import get
from tbapy import TBA

from .constants import EventSpecificConstants, GeneralConstants, Queries

__all__ = [
    "populate_missing_data",
    "retrieve_match_schedule",
    "retrieve_pit_scouting_data",
    "retrieve_note_scouting_data",
    "retrieve_team_list",
    "retrieve_scouting_data",
    "scouting_data_for_team"
]


def populate_missing_data(distributions: list[list], sentinel: Any = None) -> tuple[range, list]:
    """Populates missing data points when plotting multiple distributions.

    :param distributions: A list containing different distributions that are to be populated.
    :param sentinel: The value to append to distributions with missing data points (in this case, None).
    :return: A range showing the length of the distribution and a list where all the distributions have equal lengths.
    """
    max_data_points = len(max(distributions, key=len))

    # Populate missing data points with None
    return (
        range(max_data_points),
        [
            list(distribution) + [sentinel] * (max_data_points - len(distribution))
            for distribution in distributions
        ]
    )


@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
def retrieve_scouting_data() -> DataFrame:
    """Retrieves the latest scouting data from team4099/ScoutingAppData on GitHub based on the current event.

    :return: A dataframe containing the scouting data from an event.
    """
    scouting_data = DataFrame.from_dict(
        get(EventSpecificConstants.URL).json()
    )
    scouting_data[Queries.MATCH_NUMBER] = scouting_data[Queries.MATCH_KEY].apply(
        lambda match_key: int(search(r"\d+", match_key).group(0))
    )

    return scouting_data.sort_values(by=Queries.MATCH_NUMBER).reset_index(drop=True)


@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
def retrieve_note_scouting_data() -> DataFrame:
    """Retrieves the latest note scouting data from team4099/ScoutingAppData on GitHub based on the current event.

    :return: A dataframe containing the scouting data from an event.
    """
    scouting_data = DataFrame.from_dict(
        get(EventSpecificConstants.NOTE_SCOUTING_URL).json()
    )
    scouting_data[Queries.MATCH_NUMBER] = scouting_data[Queries.MATCH_KEY].apply(
        lambda match_key: int(search(r"\d+", match_key).group(0))
    )

    return scouting_data.sort_values(by=Queries.MATCH_NUMBER).reset_index(drop=True)


@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
def retrieve_pit_scouting_data() -> DataFrame | None:
    """Retrieves the latest pit scouting data from team4099/ScoutingAppData on GitHub based on the current event.

    :return: A dataframe containing the scouting data from an event.
    """
    response = get(EventSpecificConstants.PIT_SCOUTING_URL)

    if response.status_code == 200:
        return read_csv(
            StringIO(response.text)
        )


# Cache for longer because match schedule is relatively constant.
@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE * 4)
def retrieve_match_schedule() -> DataFrame:
    """Retrieves the match schedule for the current event using TBA."""
    tba_instance = TBA(
        auth_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"  # For testing purposes
    )
    match_levels_to_order = {"qm": 0, "sf": 1, "f": 2}

    event_matches = sorted(
        tba_instance.event_matches(EventSpecificConstants.EVENT_CODE),
        key=lambda match_info: (match_levels_to_order[match_info["comp_level"]], match_info["match_number"])
    )

    return DataFrame.from_dict(
        [
            {
                "match_key": match["key"].replace(f"{EventSpecificConstants.EVENT_CODE}_", ""),
                "red_alliance": [int(team[3:]) for team in match["alliances"]["red"]["team_keys"]],
                "blue_alliance": [int(team[3:]) for team in match["alliances"]["blue"]["team_keys"]]
            }
            for match in event_matches
        ]
    )


def scouting_data_for_team(
    team_number: int,
    scouting_data: DataFrame | None = None,
    from_note_scouting_data: bool = False
) -> DataFrame:
    """Retrieves the submissions within the scouting data for a certain team.

    :param team_number: The number of the team to retrieve the submissions for.
    :param scouting_data: An optional argument allowing the user to pass in the scouting data if already retrieved.
    :param from_note_scouting_data: A flag representing whether to pull from the note scouting data.
    :return: A dataframe containing th submissions within the scouting data for the team passed in.
    """
    if scouting_data is None:
        scouting_data = retrieve_note_scouting_data() if from_note_scouting_data else retrieve_scouting_data()

    return scouting_data[
        scouting_data["TeamNumber"] == team_number
    ]


def retrieve_team_list(scouting_data: DataFrame | None = None, from_note_scouting_data: bool = False) -> list:
    """Retrieves the team list at the current event via the scouting data.

    :param scouting_data: An optional argument allowing the user to pass in the scouting data if already retrieved.
    :param from_note_scouting_data: A flag representing whether to pull from the note scouting data.
    :return: A list containing the teams at the current event.
    """
    if scouting_data is None:
        scouting_data = retrieve_note_scouting_data() if from_note_scouting_data else retrieve_scouting_data()

    # Filter out empty team numbers
    scouting_data = scouting_data[scouting_data["TeamNumber"] != ""]

    return sorted(
        set(
            scouting_data["TeamNumber"]
        )
    )

