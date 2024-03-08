"""Creates the `PicklistManager` class used to set up the Picklist page and its table."""

import streamlit as st

from .page_manager import PageManager
from utils import CalculatedStats, Criteria, EventSpecificConstants, Queries, retrieve_scouting_data, retrieve_team_list


class NoteScoutingManager(PageManager):
    """The manager for the Note Scouting page."""

    def generate_input_section(self) -> int:    
        """Creates the input section for the `Note Scouting` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(4099)
        )