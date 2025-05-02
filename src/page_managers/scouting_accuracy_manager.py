"""Creates the `ScoutingAccuracyManager` class used to set up the Scouting Accuracy page and generate its table."""
import streamlit as st
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    EventSpecificConstants,
    retrieve_scouting_data,
    retrieve_match_schedule,
    retrieve_match_data
)
import requests


class ScoutingAccuracyManager(PageManager):
    """The scouting accuracy page manager for the `Scouting Accuracy` page."""
    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.raw_scouting_data = retrieve_scouting_data()
        self.match_schedule = retrieve_match_schedule()
        self.match_data = retrieve_match_data()


    def generate_input_section(self) -> str:
        """Generates the input section of the `Scouting Accuracy` page.

        Provides a text box for the user to input a custom string value.

        :return: Returns the string entered by the user.
        """

        return st.text_input(
            "Enter the name of the member",
            placeholder="Type here..."
        )

    def generate_accuracy_table(self, member_name):
        """Generates the scouting accuracy table for the `Scouting Accuracy` page."""
        headers = {
            "X-TBA-Auth-Key": "6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"
        }

        for index, row in self.match_data.iterrows():
            match_key = row["match_key"]
            red_alliance = row["red_alliance"]
            blue_alliance = row["blue_alliance"]
            red_alliance_score = row["red_score"]
            blue_alliance_score = row["blue_score"]
            # TODO: Fix team key issue since it is not getting the correct key
            for team_key in red_alliance.split(","):
                matches = requests.get(f"https://www.thebluealliance.com/api/v3/team/{team_key}/event/{EventSpecificConstants.EVENT_CODE}/matches", headers=headers).json()
                print(team_key)
                print(matches)

            break
