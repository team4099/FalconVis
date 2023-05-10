"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils.functions import retrieve_team_list


class EventManager(PageManager):
    """The page manager for the `Event` page."""

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return
