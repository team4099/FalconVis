"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""
import re

import streamlit as st

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    GraphType,
    line_graph,
    plotly_chart,
    Queries,
    retrieve_team_list,
    retrieve_pit_scouting_data,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph
)


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        return st.selectbox(
            "Team Number",
            retrieve_team_list()
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        # What we'll be working on this workshop (SP10)

    def generate_teleop_graphs(self, team_number: int) -> None:
        """Creates the teleop graphs for the `Teams` page.

        :param team_number: The team number to calculate the teleop graphs for.
        """
        # What we'll be working on the next workshop (SP11)

    
