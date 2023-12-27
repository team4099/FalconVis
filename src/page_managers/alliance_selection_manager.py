"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import numpy as np
import streamlit as st
from scipy.integrate import quad
from scipy.stats import norm

from .page_manager import PageManager
from utils import (
    alliance_breakdown,
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    GraphType,
    multi_line_graph,
    plotly_chart,
    populate_missing_data,
    Queries,
    retrieve_match_schedule,
    retrieve_pit_scouting_data,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    win_percentages,
)


class AllianceSelectionManager(PageManager):
    """The page manager for the `Alliance Selection` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Alliance Selection` page.

        Creates 3 dropdowns to choose teams

        :return: List with 3 choices
        """
        team_list = retrieve_team_list()

        # Create the different dropdowns to choose the three teams for Red Alliance.
        team_1_col, team_2_col, team_3_col = st.columns(3)
        team_1 = team_1_col.selectbox(
            "Team 1",
            team_list,
            index=0
        )
        team_2 = team_2_col.selectbox(
            "Team 2",
            team_list,
            index=1
        )
        team_3 = team_3_col.selectbox(
            "Team 3",
            team_list,
            index=2
        )

        return [team_1, team_2, team_3]

    def generate_alliance_dashboard(self, team_numbers: list[int], color_gradient: list[str]) -> None:
        """Generates an alliance dashboard in the `Match` page.

        :param team_numbers: The teams to generate the alliance dashboard for.
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
    
    def generate_drivetrain_dashboard(self, team_numbers: list[int], color_gradient: list[str]) -> None:
        """Generates an drivetrain dashboard in the `Alliance Selection` page.

        :param team_numbers: The teams to generate the drivetrain dashboard for.
        :param color_gradient: The color gradient to use for graphs.
        :return:
        """

    def generate_autonomous_graphs(
        self,
        team_numbers: list[int],
        type_of_graph: str,
        color_gradient: list[str]
    ) -> None:
        """Generates the autonomous graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """

    def generate_teleop_graphs(
        self,
        team_numbers: list[int],
        type_of_graph: str,
        color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """

    
    def generate_rating_graphs(
        self,
        team_numbers: list[int],
        color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """


    