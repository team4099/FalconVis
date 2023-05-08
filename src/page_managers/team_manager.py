"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils.functions import retrieve_team_list


class TeamManager(PageManager):
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
