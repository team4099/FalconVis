import pandas as pd
import streamlit as st
from .page_manager import PageManager
from src.utils import (
    CalculatedStats,
    Queries,
    retrieve_scouting_data,
    retrieve_match_schedule,
    retrieve_match_data,
    retrieve_match_data_raw,
    Criteria
)
from pandas import DataFrame

load_dotenv()


class MatchAccuracyManager(PageManager):

    def __init__(self):
        self.calulated_stats = CalculatedStats(retrieve_scouting_data())
        self.raw_scouting_data = retrieve_scouting_data()
        self.match_schedule = retrieve_match_schedule()
        self.match_data = retrieve_match_data()

    def generate_input_section(self) -> str:
        """Generates the input section of the `Scouting Accuracy` page.

        Provides a text box for the user to input a custom string value.

        :return: Returns the string entered by the user.
        """

        return st.text_input(
            "Search a match string",
            placeholder="Type here..."
        )

    def generate_match_accuracy_table(self, match: str) -> DataFrame:
        matchData = retrieve_match_data_raw()

        accuracy = {
            "Match": [],
            "# of Scouters": [],
            "Accuracy": [],
            "# of Red Scouters": [],
            "Red Accuracy (%)": [],
            "# of Blue Scouters": [],
            "Blue Accuracy (%)": [],
        }

        for index, row in self.match_data.iterrows():
            match_key = row["match_key"]
            red_alliance = row["red_alliance"]
            blue_alliance = row["blue_alliance"]

            # Rojo Alianza
            team_list = red_alliance.split(",")
            for match in matchData:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    red_total_score = match["score_breakdown"]["red"]["totalPoints"]
                    red_foul_score = match["score_breakdown"]["red"]["foulPoints"]
                    red_calc_score = red_total_score - red_foul_score
                    break

            if red_calc_score is None:
                continue
            red_scouted_score = 0
            scout_count_r = 0
            for team_key in team_list:
                scouting_team_filter = self.raw_scouting_data[
                    self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)
                    ].reset_index(drop=True)

                match_indices = scouting_team_filter.index[
                    scouting_team_filter[Queries.MATCH_KEY] == match_key
                    ].tolist()

                if len(match_indices) > 0:
                    idx = match_indices[0]
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    red_scouted_score += points_per_match[idx]
                    scout_name = scouting_team_filter.iloc[idx][Queries.SCOUT_ID]
                    if (scout_name):
                        scout_count_r+=1

            red_accuracy = (1 - abs((red_scouted_score - red_calc_score) / red_calc_score)) * 100

            # Azul Alianza
            bteam_list = blue_alliance.split(",")
            for match in matchData:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    blue_total_score = match["score_breakdown"]["blue"]["totalPoints"]
                    blue_foul_score = match["score_breakdown"]["blue"]["foulPoints"]
                    blue_calc_score = blue_total_score - blue_foul_score
                    break

            if blue_calc_score is None:
                continue
            blue_scouted_score = 0
            scout_count_b = 0
            for team_key in team_list:
                scouting_team_filter = self.raw_scouting_data[
                    self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)
                    ].reset_index(drop=True)

                match_indices = scouting_team_filter.index[
                    scouting_team_filter[Queries.MATCH_KEY] == match_key
                    ].tolist()

                if len(match_indices) > 0:
                    idx = match_indices[0]
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    blue_scouted_score += points_per_match[idx]
                    scout_name = scouting_team_filter.iloc[idx][Queries.SCOUT_ID]
                    if (scout_name):
                        scout_count_b += 1

            blue_accuracy = (1 - abs((blue_scouted_score - blue_calc_score) / blue_calc_score)) * 100
            total_scouts = scout_count_r + scout_count_b

            overall_acc = (red_accuracy + blue_accuracy) / 2
            accuracy["Match"].append(match_key)
            accuracy["# of Scouters"].append(total_scouts)
            accuracy["Accuracy"].append(overall_acc)
            accuracy["# of Red Scouters"].append(scout_count_r)
            accuracy["Red Accuracy (%)"].append(red_accuracy)
            accuracy["# of Blue Scouters"].append(scout_count_b)
            accuracy["Blue Accuracy (%)"].append(blue_accuracy)

            accuracy.sort(key = lambda row: int(row["Match"][2:]))
            return pd.DataFrame(accuracy)