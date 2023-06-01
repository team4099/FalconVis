"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st
from numpy import mean

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    colored_metric,
    GeneralConstants,
    Queries, 
    retrieve_team_list, 
    retrieve_scouting_data
)


class EventManager(PageManager):
    """The page manager for the `Event` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return
    
    def generate_event_breakdown(self) -> None:
        """Creates metrics that breakdown the events and display the average cycles of the top 8, 16 and 24 teams."""
        top_8_col, top_16_col, top_24_col = st.columns(3)
        
        average_cycles_per_team = sorted(
            [
                self.calculated_stats.average_cycles(team)
                for team in retrieve_team_list()
            ],
            reverse=True
        )
        
        # Metric displaying the average cycles of the top 8 teams/likely alliance captains
        with top_8_col:
            colored_metric(
                "Avg. Cycles (Top 8)",
                mean(average_cycles_per_team[:8]),
                background_color=GeneralConstants.TEAM_GOLD,
                opacity=0.5
            )

        # Metric displaying the average cycles of the top 16 teams/likely alliance captains
        with top_16_col:
            colored_metric(
                "Avg. Cycles (Top 16)",
                mean(average_cycles_per_team[:16]),
                background_color=GeneralConstants.TEAM_GOLD,
                opacity=0.5
            )
        
        # Metric displaying the average cycles of the top 24 teams/likely alliance captains
        with top_24_col:
            colored_metric(
                "Avg. Cycles (Top 24)",
                mean(average_cycles_per_team[:24]),
                background_color=GeneralConstants.TEAM_GOLD,
                opacity=0.5
            )

