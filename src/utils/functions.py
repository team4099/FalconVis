"""Defines utility functions that are later used in FalconVis."""
from re import search

from pandas import DataFrame
from requests import get
import streamlit as st

from .constants import EventSpecificConstants, GeneralConstants, Queries

__all__ = [
    "create_df",
    "retrieve_team_list",
    "retrieve_scouting_data",
    "scouting_data_for_team"
]


def create_df(
        x_axis: list,
        y_axis: list,
        x_axis_label: str = "x",
        y_axis_label: str = "y"
) -> DataFrame:
    """Creates a DF where every element in x_axis and every element in y_axis is mapped to each other in a DataFrame.

    :param x_axis: Sequence representing elements in the desired X axis.
    :param y_axis: Sequence representing elements in the desired Y axis.
    :param x_axis_label: Optional label for desired X axis (header for X axis).
    :param y_axis_label: Optional label for desired Y axis (header for Y axis).
    :return: A DataFrame where the headers are `x_axis_label` and `y_axis_label` and each element in `x_axis` is mapped to one in `y_axis`.
    """
    return DataFrame.from_dict(
        [
            {
                x_axis_label: x,
                y_axis_label: y
            } for x, y in zip(x_axis, y_axis)
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
