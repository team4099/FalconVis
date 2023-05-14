"""Defines utility functions that are later used in FalconVis."""

from pandas import DataFrame
from requests import get
import streamlit as st

from .constants import EventSpecificConstants, GeneralConstants

__all__ = [
    "retrieve_team_list",
    "retrieve_scouting_data",
    "scouting_data_for_team"
]


@st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
def retrieve_scouting_data() -> DataFrame:
    """Retrieves the latest scouting data from team4099/ScoutingAppData on GitHub based on the current event.

    :return: A dataframe containing the scouting data from an event.
    """
    return DataFrame.from_dict(
        get(EventSpecificConstants.URL).json()
    )


def scouting_data_for_team(team_number: int, scouting_data: DataFrame | None = None) -> DataFrame:
    """Retrieves the submissions within the scouting data for a certain team.

    :param team_number: The number of the team to retrieve the submissions for.
    :param scouting_data: An optional argument allowing the user to pass in the scouting data if already retrieved.
    :return: A dataframe containing th submissions within the scouting data for the team passed in.
    """
    if scouting_data is None:
        scouting_data = retrieve_scouting_data()

    return scouting_data[
        scouting_data["TeamNumber"] == team_number
    ]


def retrieve_team_list() -> list:
    """Retrieves the team list at the current event via the scouting data.

    :return: A list containing the teams at the current event.
    """
    scouting_data = retrieve_scouting_data()
    return sorted(
        set(
            scouting_data["TeamNumber"]
        )
    )
