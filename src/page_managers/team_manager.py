"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import streamlit as st

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils.functions import retrieve_team_list


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        return st.selectbox(
            "Team Number",
            retrieve_team_list()
        )

    def generate_metrics(self, quartile: float) -> None:
        """Creates the metrics for the `Teams` page.

        :param quartile: The quartile to use per-metric for comparisons between a team and the xth-percentile.
        """
