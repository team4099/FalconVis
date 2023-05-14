"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils import CalculatedStats, Queries, retrieve_team_list, retrieve_scouting_data


class EventManager(PageManager):
    """The page manager for the `Event` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return
