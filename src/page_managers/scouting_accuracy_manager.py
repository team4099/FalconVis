"""Creates the `ScoutingAccuracyManager` class used to set up the Scouting Accuracy page and generate its table."""
import streamlit as st
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    EventSpecificConstants,
    Queries,
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
            print(red_alliance)
            blue_alliance = row["blue_alliance"]
            red_alliance_score = row["red_score"]
            blue_alliance_score = row["blue_score"]

            scouting_match_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.MATCH_KEY] == match_key]

            # TODO: Figure out if there's a better way to do this than just iterating through the list
            for team_key in red_alliance.split(","):
                red_tba_matches = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_key}/event/{EventSpecificConstants.EVENT_CODE}/matches", headers=headers).json()
                for match in red_tba_matches:
                    if (match["comp_level"] + str(match["match_number"])) == match_key:
                        red_total_score = match["score_breakdown"]["red"]["totalPoints"]
                        red_foul_score = match["score_breakdown"]["red"]["foulPoints"]
                        red_adjust_score = match["score_breakdown"]["red"]["adjustPoints"]
                        red_calculated_score = red_total_score - red_foul_score - red_adjust_score
                        print(red_calculated_score)
                        break

                scouting_team_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)]
                scouting_team_filter = scouting_team_filter.reset_index(drop=True)
                match_index_list = scouting_team_filter.index[scouting_team_filter[Queries.MATCH_KEY] == match_key].tolist()
                if len(match_index_list) != 0:
                    match_index = match_index_list[0]
                    print(match_index)

            for team_key in blue_alliance.split(","):
                blue_tba_matches = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_key}/event/{EventSpecificConstants.EVENT_CODE}/matches", headers=headers).json()
