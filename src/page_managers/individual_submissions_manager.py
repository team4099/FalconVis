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

    def display_autonomous_data(self, submission: DataFrame) -> None:
        """Displays the autonomous data in an individual submission.

        :param submission: The individual submission for a certain team.
        """
        auto_grid_col, auto_info_col_1, auto_info_col_2 = st.columns(3)

        with auto_grid_col:
            display_grid(
                Queries.AUTO_GRID,
                submission[Queries.ALLIANCE].iloc[0],
                submission[Queries.AUTO_GRID].iloc[0].split("|")
            )

        # Split metrics into two different columns to make it easier to read
        with auto_info_col_1:
            colored_metric(
                "Charge Station State",
                submission[Queries.AUTO_CHARGING_STATE].iloc[0],
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

            colored_metric(
                "Did They Attempt to Engage?",
                "Yes" if submission[Queries.AUTO_ENGAGE_ATTEMPTED].iloc[0] == "Engage" else "No",
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

        with auto_info_col_2:
            colored_metric(
                "Game Pieces Missed",
                submission[Queries.AUTO_MISSED].iloc[0],
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

            colored_metric(
                "Did They Leave the Community?",
                "Yes" if submission[Queries.LEFT_COMMUNITY].iloc[0] else "No",
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

    def display_teleop_data(self, submission: DataFrame) -> None:
        """Displays the teleop data in an individual submission.

        :param submission: The individual submission for a certain team.
        """
        teleop_grid_col, teleop_info_col_1, teleop_info_col_2 = st.columns(3)

        with teleop_grid_col:
            display_grid(
                Queries.TELEOP_GRID,
                submission[Queries.ALLIANCE].iloc[0],
                submission[Queries.TELEOP_GRID].iloc[0].split("|")
            )

        # Split metrics into two different columns to make it easier to read
        with teleop_info_col_1:
            colored_metric(
                "Final Charging Station State",
                submission[Queries.ENDGAME_FINAL_CHARGE].iloc[0],
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

            colored_metric(
                "Game Pieces Missed",
                submission[Queries.TELEOP_MISSED].iloc[0],
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

        with teleop_info_col_2:
            colored_metric(
                "Did They Disable?",
                "Yes" if submission[Queries.DISABLE].iloc[0] else "No",
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )

            colored_metric(
                "Were They Tippy?",
                "Yes" if submission[Queries.TIPPY].iloc[0] else "No",
                opacity=0.5,
                background_color=GeneralConstants.PRIMARY_COLOR
            )
