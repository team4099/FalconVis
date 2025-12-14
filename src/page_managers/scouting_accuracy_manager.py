"""Creates the `ScoutingAccuracyManager` class used to set up the Scouting Accuracy page and generate its table."""
import pandas as pd
import streamlit as st
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    Queries,
    retrieve_scouting_data,
    retrieve_match_schedule,
    retrieve_match_data,
    retrieve_match_data_raw,
    Criteria
)
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
    
    #Method to create table sorted by scouter
    def generate_scouting_accuracy_table(self, member_name: str) -> DataFrame:
        """Generates the scouting accuracy table for the `Scouting Accuracy` page."""

        accuracy_dict = {
            'ScoutersNames': [],
            'CumulativeAccuracy': [],
            'AutoAccuracy': [],
            'TeleopAccuracy': [],
            'EndgameAccuracy': [],
            'NumberOfScoutedMatches': []
        }

        matches = retrieve_match_data_raw()

        for index, row in self.match_data.iterrows():
            match_key = row["match_key"]
            red_alliance = row["red_alliance"]
            blue_alliance = row["blue_alliance"]

            # Red alliance score from TBA
            team_list = red_alliance.split(",")
            for match in matches:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    red_total_score = match["score_breakdown"]["red"]["totalPoints"]
                    red_foul_score = match["score_breakdown"]["red"]["foulPoints"]
                    red_auto_score = match["score_breakdown"]["red"]["autoPoints"]
                    red_teleop_score = match["score_breakdown"]["red"]["teleopPoints"]
                    red_endgame_score = match["score_breakdown"]["red"]["endGameBargePoints"]
                    red_calculated_score = red_total_score - red_foul_score
                    break

            red_scouting_alliance_score = 0
            red_scouting_auto_score = 0
            red_scouting_teleop_score = 0
            red_scouting_endgame_score = 0

            scouters_names_list_r = []

            for team_key in team_list:
                scouting_team_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)]
                scouting_team_filter = scouting_team_filter.reset_index(drop=True)
                match_index_list = scouting_team_filter.index[scouting_team_filter[Queries.MATCH_KEY] == match_key].tolist()
                if len(match_index_list) != 0:
                    match_index = match_index_list[0]

                    # Auto Accuracy Retrieval
                    auto_coral_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L1).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L2).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L3).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L4).values
                    ]
                    for i in range(len(auto_coral_per_match)):
                        red_scouting_auto_score += auto_coral_per_match[i][match_index] * Criteria.AUTO_CORAL_POINTAGE[i + 1]
                    auto_algae_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_BARGE).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_PROCESSOR).values
                    ]
                    for i in range(len(auto_algae_per_match)):
                        red_scouting_auto_score += auto_algae_per_match[i][match_index] * Criteria.ALGAE_POINTAGE[i + 1]
                    leave_points = self.calculated_stats.stat_per_match(int(team_key), Queries.LEFT_STARTING_ZONE, Criteria.BOOLEAN_CRITERIA).values
                    red_scouting_auto_score += (leave_points[match_index] * 2)

                    # Teleop Accuracy Retrieval
                    teleop_coral_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L1).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L2).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L3).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L4).values
                    ]
                    for i in range(len(teleop_coral_per_match)):
                        red_scouting_teleop_score += teleop_coral_per_match[i][match_index] * Criteria.TELEOP_CORAL_POINTAGE[i + 1]
                    teleop_algae_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_BARGE).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_PROCESSOR).values
                    ]
                    for i in range(len(teleop_algae_per_match)):
                        red_scouting_teleop_score += teleop_algae_per_match[i][match_index] * Criteria.ALGAE_POINTAGE[i + 1]

                    # Endgame Accuracy Retrieval
                    park_points = self.calculated_stats.stat_per_match(int(team_key), Queries.PARKED_UNDER_BARGE, Criteria.BOOLEAN_CRITERIA).values
                    climb_points = self.calculated_stats.stat_per_match(int(team_key), Queries.CLIMBED_CAGE, Criteria.CLIMBING_POINTAGE).values
                    red_scouting_endgame_score = park_points[match_index] * 2 + climb_points[match_index]

                    # Cumulative Accuracy Retrieval
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    red_scouting_alliance_score += points_per_match[match_index]

                    scout_name = scouting_team_filter.iloc[match_index][Queries.SCOUT_ID]
                    scouters_names_list_r.append(scout_name.title().replace(" ", ""))

                    # Red alliance accuracy
                    if red_calculated_score == 0:
                        if red_scouting_alliance_score == 0:
                            red_alliance_accuracy = 100.0
                        else:
                            red_alliance_accuracy = 0.0
                    else:
                        red_alliance_accuracy = (1 - abs((red_scouting_alliance_score - red_calculated_score) / red_calculated_score)) * 100
                    # red auto accuracy
                    if red_auto_score == 0:
                        if red_scouting_auto_score == 0:
                            red_auto_accuracy = 100.0
                        else:
                            red_auto_accuracy = 0.0
                    else:
                        red_auto_accuracy = (1 - abs((red_scouting_auto_score - red_auto_score) / red_auto_score)) * 100
                    # red teleop accuracy
                    if red_teleop_score == 0:
                        if red_scouting_teleop_score == 0:
                            red_teleop_accuracy = 100.0
                        else:
                            red_teleop_accuracy = 0.0
                    else:
                        red_teleop_accuracy = (1 - abs((red_scouting_teleop_score - red_teleop_score) / red_teleop_score)) * 100
                    # red endgame accuracy
                    if red_endgame_score == 0:
                        if red_scouting_endgame_score == 0:
                            red_endgame_accuracy = 100.0
                        else:
                            red_endgame_accuracy = 0.0
                    else:
                        red_endgame_accuracy = (1 - abs((red_scouting_endgame_score - red_endgame_score) / red_endgame_score)) * 100

            scouters_names = ", ".join(scouters_names_list_r)

            if member_name.replace(" ", "").lower() in scouters_names.replace(" ", "").lower():
                if scouters_names not in accuracy_dict['ScoutersNames']:
                    accuracy_dict['ScoutersNames'].append(scouters_names)
                    accuracy_dict['CumulativeAccuracy'].append(red_alliance_accuracy)
                    accuracy_dict['AutoAccuracy'].append(red_auto_accuracy)
                    accuracy_dict['TeleopAccuracy'].append(red_teleop_accuracy)
                    accuracy_dict['EndgameAccuracy'].append(red_endgame_accuracy)
                    accuracy_dict['NumberOfScoutedMatches'].append(1)
                else:
                    accuracy_scouts_index = accuracy_dict['ScoutersNames'].index(scouters_names)
                    accuracy_dict['CumulativeAccuracy'][accuracy_scouts_index] += red_alliance_accuracy
                    accuracy_dict['AutoAccuracy'][accuracy_scouts_index] += red_auto_accuracy
                    accuracy_dict['TeleopAccuracy'][accuracy_scouts_index] += red_teleop_accuracy
                    accuracy_dict['EndgameAccuracy'][accuracy_scouts_index] += red_endgame_accuracy
                    accuracy_dict['NumberOfScoutedMatches'][accuracy_scouts_index] += 1

            # Blue Alliance score from TBA
            for match in matches:
                if (match["comp_level"] + str(match["match_number"])) == match_key:
                    blue_total_score = match["score_breakdown"]["blue"]["totalPoints"]
                    blue_foul_score = match["score_breakdown"]["blue"]["foulPoints"]
                    blue_auto_score = match["score_breakdown"]["blue"]["autoPoints"]
                    blue_teleop_score = match["score_breakdown"]["blue"]["teleopPoints"]
                    blue_endgame_score = match["score_breakdown"]["blue"]["endGameBargePoints"]
                    blue_calculated_score = blue_total_score - blue_foul_score
                    break

            blue_scouting_alliance_score = 0
            blue_scouting_auto_score = 0
            blue_scouting_teleop_score = 0
            blue_scouting_endgame_score = 0

            scouters_names_list_b = []

            for team_key in blue_alliance.split(","):
                scouting_team_filter = self.raw_scouting_data[self.raw_scouting_data[Queries.TEAM_NUMBER] == int(team_key)]
                scouting_team_filter = scouting_team_filter.reset_index(drop=True)
                match_index_list = scouting_team_filter.index[scouting_team_filter[Queries.MATCH_KEY] == match_key].tolist()
                if len(match_index_list) != 0:
                    match_index = match_index_list[0]

                    # Auto Accuracy Retrieval
                    auto_coral_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L1).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L2).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L3).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_CORAL_L4).values
                    ]
                    for i in range(len(auto_coral_per_match)):
                        blue_scouting_auto_score += auto_coral_per_match[i][match_index] * Criteria.AUTO_CORAL_POINTAGE[i + 1]
                    algae_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_BARGE).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.AUTO_PROCESSOR).values
                    ]
                    for i in range(len(algae_per_match)):
                        blue_scouting_auto_score += algae_per_match[i][match_index] * Criteria.ALGAE_POINTAGE[i + 1]
                    leave_points = self.calculated_stats.stat_per_match(int(team_key), Queries.LEFT_STARTING_ZONE, Criteria.BOOLEAN_CRITERIA).values
                    blue_scouting_auto_score += (leave_points[match_index] * 2)

                    # Teleop Accuracy Retrieval
                    teleop_coral_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L1).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L2).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L3).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_CORAL_L4).values
                    ]
                    for i in range(len(teleop_coral_per_match)):
                        blue_scouting_teleop_score += teleop_coral_per_match[i][match_index] * Criteria.TELEOP_CORAL_POINTAGE[i + 1]
                    teleop_algae_per_match = [
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_BARGE).values,
                        self.calculated_stats.cycles_by_structure_per_match(int(team_key), Queries.TELEOP_PROCESSOR).values
                    ]
                    for i in range(len(teleop_algae_per_match)):
                        blue_scouting_teleop_score += teleop_algae_per_match[i][match_index] * Criteria.ALGAE_POINTAGE[i + 1]

                    # Endgame Accuracy Retrieval
                    park_points = self.calculated_stats.stat_per_match(int(team_key), Queries.PARKED_UNDER_BARGE, Criteria.BOOLEAN_CRITERIA).values
                    climb_points = self.calculated_stats.stat_per_match(int(team_key), Queries.CLIMBED_CAGE, Criteria.CLIMBING_POINTAGE).values
                    blue_scouting_endgame_score = park_points[match_index] * 2 + climb_points[match_index]

                    # Cumulative Accuracy Retrieval
                    points_per_match = self.calculated_stats.points_contributed_by_match(int(team_key)).values
                    blue_scouting_alliance_score += points_per_match[match_index]

                    scout_name = scouting_team_filter.iloc[match_index][Queries.SCOUT_ID]
                    scouters_names_list_b.append(scout_name.title().replace(" ", ""))

                self.calculated_stats.points_contributed_by_match(team_key)
                blue_scouting_alliance_score += self.calculated_stats.points_contributed_by_match(team_key).sum()

                # blue alliance accuracy
                if blue_calculated_score == 0:
                    if blue_scouting_alliance_score == 0:
                        blue_alliance_accuracy = 100.0
                    else:
                        blue_alliance_accuracy = 0.0
                else:
                    blue_alliance_accuracy = (1 - abs((blue_scouting_alliance_score - blue_calculated_score) / blue_calculated_score)) * 100
                # blue auto accuracy
                if blue_auto_score == 0:
                    if blue_scouting_auto_score == 0:
                        blue_auto_accuracy = 100.0
                    else:
                        blue_auto_accuracy = 0.0
                else:
                    blue_auto_accuracy = (1 - abs((blue_scouting_auto_score - blue_auto_score) / blue_auto_score)) * 100
                # blue teleop accuracy
                if blue_teleop_score == 0:
                    if blue_scouting_teleop_score == 0:
                        blue_teleop_accuracy = 100.0
                    else:
                        blue_teleop_accuracy = 0.0
                else:
                    blue_teleop_accuracy = (1 - abs((blue_scouting_teleop_score - blue_teleop_score) / blue_teleop_score)) * 100
                # blue endgame accuracy
                if blue_endgame_score == 0:
                    if blue_scouting_endgame_score == 0:
                        blue_endgame_accuracy = 100.0
                    else:
                        blue_endgame_accuracy = 0.0
                else:
                    blue_endgame_accuracy = (1 - abs((blue_scouting_endgame_score - blue_endgame_score) / blue_endgame_score)) * 100

            scouters_names = ", ".join(scouters_names_list_b)

            if member_name.replace(" ", "").lower() in scouters_names.lower():
                if scouters_names not in accuracy_dict['ScoutersNames']:
                    accuracy_dict['ScoutersNames'].append(scouters_names)
                    accuracy_dict['CumulativeAccuracy'].append(blue_alliance_accuracy)
                    accuracy_dict['AutoAccuracy'].append(blue_auto_accuracy)
                    accuracy_dict['TeleopAccuracy'].append(blue_teleop_accuracy)
                    accuracy_dict['EndgameAccuracy'].append(blue_endgame_accuracy)
                    accuracy_dict['NumberOfScoutedMatches'].append(1)
                else:
                    accuracy_scouts_index = accuracy_dict['ScoutersNames'].index(scouters_names)
                    accuracy_dict['CumulativeAccuracy'][accuracy_scouts_index] += blue_alliance_accuracy
                    accuracy_dict['AutoAccuracy'][accuracy_scouts_index] += blue_auto_accuracy
                    accuracy_dict['TeleopAccuracy'][accuracy_scouts_index] += blue_teleop_accuracy
                    accuracy_dict['EndgameAccuracy'][accuracy_scouts_index] += blue_endgame_accuracy
                    accuracy_dict['NumberOfScoutedMatches'][accuracy_scouts_index] += 1

        df = pd.DataFrame(data={
            'Scouters': accuracy_dict['ScoutersNames'],
            'Average Accuracy %': [round(accuracy_dict['CumulativeAccuracy'][scouter_set]/accuracy_dict['NumberOfScoutedMatches'][scouter_set], 2) for scouter_set in range(len(accuracy_dict['NumberOfScoutedMatches']))],
            'Average Auto Accuracy %': [round(accuracy_dict['AutoAccuracy'][scouter_set]/accuracy_dict['NumberOfScoutedMatches'][scouter_set], 2) for scouter_set in range(len(accuracy_dict['NumberOfScoutedMatches']))],
            'Average Teleop Accuracy %': [round(accuracy_dict['TeleopAccuracy'][scouter_set]/accuracy_dict['NumberOfScoutedMatches'][scouter_set], 2) for scouter_set in range(len(accuracy_dict['NumberOfScoutedMatches']))],
            'Average Endgame Accuracy %': [round(accuracy_dict['EndgameAccuracy'][scouter_set]/accuracy_dict['NumberOfScoutedMatches'][scouter_set], 2) for scouter_set in range(len(accuracy_dict['NumberOfScoutedMatches']))],
            'NumberOfScoutedMatches': accuracy_dict['NumberOfScoutedMatches']
        })

        return df
    #Method to create table sorted by match
    def generate_match_accuracy_table(self) -> DataFrame:
        """Generates the match accuracy table for all matches."""
        accuracy_rows = []
        matches = retrieve_match_data_raw()

        with st.spinner("Calculating match accuracy..."):
            for index, row in self.match_data.iterrows():
                match_key = row["match_key"]
                red_alliance = row["red_alliance"]
                blue_alliance = row["blue_alliance"]

                # --- Red Alliance ---
                red_team_list = red_alliance.split(",")

                red_calculated_score = None
                for match in matches:
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

                blue_calculated_score = None
                for match in matches:
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
                    "Accuracy (%)": f"{average_accuracy}%",
                    "# of Red Scouters": len(scouters_names_r),
                    "Red Accuracy (%)": f"{round(red_accuracy, 2)}%",
                    "# of Blue Scouters": len(scouters_names_b),
                    "Blue Accuracy (%)": f"{round(blue_accuracy, 2)}%"
                })

        accuracy_rows.sort(key = lambda row: int(row["Match"][2:]))
        df = pd.DataFrame(accuracy_rows)
        return df
