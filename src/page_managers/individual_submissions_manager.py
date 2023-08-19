import streamlit as st
from pandas import DataFrame

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    colored_metric,
    display_grid,
    GeneralConstants,
    retrieve_scouting_data,
    retrieve_team_list,
    scouting_data_for_team,
    Queries
)


class IndividualSubmissionsManager(PageManager):
    """The page manager for the `Individual Submissions` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team to view their individual submissions.

        :return: The team number selected to view the individual submissions for.
        """
        team_number = st.selectbox(
            "Team Number",
            retrieve_team_list()
        )

        # Create the drop down to choose the individual submission
        scouting_data = scouting_data_for_team(team_number)
        if not (query_parameters := st.experimental_get_query_params()):
            match_key = st.selectbox(
                "Match",
                scouting_data[Queries.MATCH_KEY]
            )
        else:
            match_key = st.selectbox(
                "Match",
                scouting_data[Queries.MATCH_KEY],
                index=list(scouting_data[Queries.MATCH_KEY]).index(query_parameters["match_key"][0])
            )

        return scouting_data[
            scouting_data[Queries.MATCH_KEY] == match_key
        ]

    def display_miscellaneous_data(self, submission: DataFrame) -> None:
        """Displays the miscellaneous data in an individual submission like the scout name, driver station, etc.

        :param submission: The individual submission for a certain team.
        """
        scout_col, alliance_col = st.columns(2)

        with scout_col:
            colored_metric(
                "Scout Name",
                submission[Queries.SCOUT_ID].iloc[0].title(),
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

        with alliance_col:
            colored_metric(
                "Alliance",
                f"{submission[Queries.ALLIANCE].iloc[0].title()} {submission[Queries.DRIVER_STATION].iloc[0]}",
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )
