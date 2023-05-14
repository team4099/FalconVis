"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils import CalculatedStats, Queries, retrieve_team_list, retrieve_scouting_data


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Match` page.

        Creates six dropdowns to choose teams for each alliance separately.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        team_list = retrieve_team_list()

        # Create the separate columns for submitting teams.
        red_alliance_form, blue_alliance_form = st.columns(2, gap="medium")

        # Create the different dropdowns to choose the three teams for Red Alliance.
        with red_alliance_form:
            red_1_col, red_2_col, red_3_col = st.columns(3)
            red_1 = red_1_col.selectbox(
                ":red[Red 1]",
                team_list
            )
            red_2 = red_2_col.selectbox(
                ":red[Red 2]",
                team_list
            )
            red_3 = red_3_col.selectbox(
                ":red[Red 3]",
                team_list
            )

        # Create the different dropdowns to choose the three teams for Blue Alliance.
        with blue_alliance_form:
            blue_1_col, blue_2_col, blue_3_col = st.columns(3)
            blue_1 = blue_1_col.selectbox(
                ":blue[Blue 1]",
                team_list
            )
            blue_2 = blue_2_col.selectbox(
                ":blue[Blue 2]",
                team_list
            )
            blue_3 = blue_3_col.selectbox(
                ":blue[Blue 3]",
                team_list
            )

        return [
            [red_1, red_2, red_3],
            [blue_1, blue_2, blue_3]
        ]
