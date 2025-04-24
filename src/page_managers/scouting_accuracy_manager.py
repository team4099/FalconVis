"""Creates the `ScoutingAccuracyManager` class used to set up the Scouting Accuracy page and generate its table."""
import falcon_alliance
import streamlit as st

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    EventSpecificConstants,
    retrieve_scouting_data,
    retrieve_match_schedule,
    retrieve_match_data
)


class ScoutingAccuracyManager(PageManager):
    """The scouting accuracy page manager for the `Scouting Accuracy` page."""
    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.match_data = retrieve_match_data()
        self.match_schedule = retrieve_match_schedule()

        # Setting up FalconAlliance (our connection to TBA)
        # TODO: Figure out issue where getting API client causes a current event loop issue
        self.api_client = falcon_alliance.ApiClient(
            api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"
        )

    def generate_input_section(self) -> str:
        """Generates the input section of the `Ranking Simulator` page."""
        # TODO: Fill in input sections later
        return

    def generate_accuracy_table(self):
        """Generates the scouting accuracy table for the `Scouting Accuracy` page."""
        print(len(self.match_schedule))
