"""Creates the `MatchAccuracyManager` class used to set up the Match Accuracy page and generate its table."""
import pandas as pd
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


class MatchAccuracyManager(PageManager):
    """The match accuracy page manager for the `Match Accuracy` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.raw_scouting_data = retrieve_scouting_data()
        self.match_schedule = retrieve_match_schedule()
        self.match_data = retrieve_match_data()

    def generate_accuracy_table(self) -> DataFrame:
        """Generates the match accuracy table for all matches."""
        accuracy_rows = []
        headers = {"X-TBA-Auth-Key": os.getenv("HEADERS")}

        with st.spinner("Calculating match accuracy..."):
            for index, row in self.match_data.iterrows():
                match_key = row["match_key"]
                red_alliance = row["red_alliance"]
                blue_alliance = row["blue_alliance"]

                # --- Red Alliance ---
                red_team_list = red_alliance.split(",")
                red_tba_matches = requests.get(
                    f"https://www.thebluealliance.com/api/v3/team/frc{red_team_list[0]}/event/{EventSpecificConstants.EVENT_CODE}/matches",
                    headers=headers
                ).json()

                red_calculated_score = None
                for match in red_tba_matches:
                    if (match["comp_level"] + str(match["match_number"])) == match_key:
                        red_total_score = match["score_breakdown"]["red"]["totalPoints"]
                        red_foul_score = match["score_breakdown"]["red"]["foulPoints"]
                        red_calculated_score = red_total_score - red_foul_score
                        break

                if red_calculated_score is None:
                    continue  # skip if match not found

                red_scouting_alliance_score = 0
                scouters_names_r = []

                for team_key in red_team_list:
                    scouting_team_filter = self.raw_scouting_data[
                        self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)
                    ].reset_index(drop=True)

                    match_indices = scouting_team_filter.index[
                        scouting_team_filter[Queries.MATCH_KEY] == match_key
                    ].tolist()

                    if len(match_indices) > 0:
                        idx = match_indices[0]
                        points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                        red_scouting_alliance_score += points_per_match[idx]
                        scout_name = scouting_team_filter.iloc[idx][Queries.SCOUT_ID]
                        scouters_names_r.append(scout_name.title().replace(" ", ""))

                red_accuracy = (1 - abs((red_scouting_alliance_score - red_calculated_score) / red_calculated_score)) * 100

                # --- Blue Alliance ---
                blue_team_list = blue_alliance.split(",")
                blue_tba_matches = requests.get(
                    f"https://www.thebluealliance.com/api/v3/team/frc{blue_team_list[0]}/event/{EventSpecificConstants.EVENT_CODE}/matches",
                    headers=headers
                ).json()

                blue_calculated_score = None
                for match in blue_tba_matches:
                    if (match["comp_level"] + str(match["match_number"])) == match_key:
                        blue_total_score = match["score_breakdown"]["blue"]["totalPoints"]
                        blue_foul_score = match["score_breakdown"]["blue"]["foulPoints"]
                        blue_calculated_score = blue_total_score - blue_foul_score
                        break

                if blue_calculated_score is None:
                    continue  # skip if match not found

                blue_scouting_alliance_score = 0
                scouters_names_b = []

                for team_key in blue_team_list:
                    scouting_team_filter = self.raw_scouting_data[
                        self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)
                    ].reset_index(drop=True)

                    match_indices = scouting_team_filter.index[
                        scouting_team_filter[Queries.MATCH_KEY] == match_key
                    ].tolist()

                    if len(match_indices) > 0:
                        idx = match_indices[0]
                        points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                        blue_scouting_alliance_score += points_per_match[idx]
                        scout_name = scouting_team_filter.iloc[idx][Queries.SCOUT_ID]
                        scouters_names_b.append(scout_name.title().replace(" ", ""))

                blue_accuracy = (1 - abs((blue_scouting_alliance_score - blue_calculated_score) / blue_calculated_score)) * 100

                total_scouts = len(set(scouters_names_r + scouters_names_b))
                average_accuracy = round((red_accuracy + blue_accuracy) / 2, 2)

                accuracy_rows.append({
                    "Match": match_key,
                    "# of Scouters": total_scouts,
                    "Accuracy (%)": f"{average_accuracy}%"
                })

        df = pd.DataFrame(accuracy_rows)
        return df
