"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st
from numpy import mean

from .page_manager import PageManager
from utils import (
    box_plot,
    CalculatedStats,
    colored_metric,
    GeneralConstants,
    GraphType,
    plotly_chart,
    Queries, 
    retrieve_team_list, 
    retrieve_scouting_data
)


class EventManager(PageManager):
    """The page manager for the `Event` page."""

    TEAMS_TO_SPLIT_BY = 10  # Number of teams to split the plots by.

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return
    
    def generate_event_breakdown(self) -> None:
        """Creates metrics that breakdown the events and display the average cycles of the top 8, 16 and 24 teams."""
