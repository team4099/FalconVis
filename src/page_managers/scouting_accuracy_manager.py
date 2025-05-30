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
import os
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()


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

    def generate_accuracy_table(self, member_name) -> DataFrame:
        """Generates the scouting accuracy table for the `Scouting Accuracy` page."""
        for index, row in self.match_data.iterrows():
            match_key = row["match_key"]
            red_alliance = row["red_alliance"]
            blue_alliance = row["blue_alliance"]
            headers = {
                "X-TBA-Auth-Key": os.getenv("HEADERS")
            }

            scouting_match_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.MATCH_KEY] == match_key]

            # Red alliance score from TBA
            team_list = red_alliance.split(",")
            red_tba_matches = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_list[0]}/event/{EventSpecificConstants.EVENT_CODE}/matches", headers=headers).json()
            for match in red_tba_matches:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    red_total_score = match["score_breakdown"]["red"]["totalPoints"]
                    red_foul_score = match["score_breakdown"]["red"]["foulPoints"]
                    red_calculated_score = red_total_score - red_foul_score
                    break

            red_scouting_alliance_score = 0

            for team_key in team_list:
                scouting_team_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)]
                scouting_team_filter = scouting_team_filter.reset_index(drop=True)
                match_index_list = scouting_team_filter.index[scouting_team_filter[Queries.MATCH_KEY] == match_key].tolist()
                if len(match_index_list) != 0:
                    match_index = match_index_list[0]
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    red_scouting_alliance_score += points_per_match[match_index]

            red_alliance_accuracy = (red_scouting_alliance_score-red_calculated_score)/red_calculated_score


            # Blue Alliance score from TBA
            team_list = blue_alliance.split(",")
            blue_tba_matches = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_list[0]}/event/{EventSpecificConstants.EVENT_CODE}/matches", headers=headers).json()
            for match in blue_tba_matches:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    blue_total_score = match["score_breakdown"]["blue"]["totalPoints"]
                    blue_foul_score = match["score_breakdown"]["blue"]["foulPoints"]
                    blue_calculated_score = blue_total_score - blue_foul_score
                    break

            blue_scouting_alliance_score = 0

            for team_key in blue_alliance.split(","):
                scouting_team_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)]
                scouting_team_filter = scouting_team_filter.reset_index(drop=True)
                match_index_list = scouting_team_filter.index[scouting_team_filter[Queries.MATCH_KEY] == match_key].tolist()
                if len(match_index_list) != 0:
                    match_index = match_index_list[0]
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    blue_scouting_alliance_score += points_per_match[match_index]
                self.calculated_stats.points_contributed_by_match(team_key)
                blue_scouting_alliance_score += self.calculated_stats.points_contributed_by_match(team_key).sum()

            blue_alliance_accuracy = (blue_scouting_alliance_score-blue_calculated_score)/blue_calculated_score
