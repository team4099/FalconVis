"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import numpy as np
import streamlit as st
from scipy.integrate import quad
from scipy.stats import norm

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    GeneralConstants,
    Queries,
    retrieve_team_list,
    retrieve_scouting_data,
    win_percentages
)


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Match` page.

        Creates six dropdowns to choose teams for each alliance separately.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        team_list = retrieve_team_list()

        # Create the separate columns for submitting teams.
        red_alliance_form, blue_alliance_form = st.beta_columns(2, gap="medium")

        # Create the different dropdowns to choose the three teams for Red Alliance.
        with red_alliance_form:
            red_1_col, red_2_col, red_3_col = st.beta_columns(3)
            red_1 = red_1_col.selectbox(
                ":red[Red 1]",
                team_list
            )
            red_2 = red_2_col.selectbox(
                ":red[Red 2]",
                team_list
            )
            red_3 = red_3_col.selectbox(
                ":red[Red 3]",
                team_list
            )

        # Create the different dropdowns to choose the three teams for Blue Alliance.
        with blue_alliance_form:
            blue_1_col, blue_2_col, blue_3_col = st.columns(3)
            blue_1 = blue_1_col.selectbox(
                ":blue[Blue 1]",
                team_list
            )
            blue_2 = blue_2_col.selectbox(
                ":blue[Blue 2]",
                team_list
            )
            blue_3 = blue_3_col.selectbox(
                ":blue[Blue 3]",
                team_list
            )

        return [
            [red_1, red_2, red_3],
            [blue_1, blue_2, blue_3]
        ]

    def generate_match_predictions(
        self,
        red_alliance: list[int],
        blue_alliance: list[int]
    ) -> None:
        """Generates graphs and metrics for match predictions (Red vs. Blue Tab).

        :param red_alliance: A list of three integers, each integer representing a team on the Red Alliance
        :param blue_alliance: A list of three integers, each integer representing a team on the Blue Alliance.
        """
        chance_of_winning_col, = st.columns(1)
        predicted_red_score_col, predicted_blue_score_col = st.columns(2)

        # Calculates each alliance's chance of winning.
        with chance_of_winning_col:
            red_alliance_points = [
                self.calculated_stats.points_contributed_by_match(team)
                for team in red_alliance
            ]
            blue_alliance_points = [
                self.calculated_stats.points_contributed_by_match(team)
                for team in blue_alliance
            ]

            # Calculate mean and standard deviation of the point distribution of the red alliance.
            red_alliance_std = sum([
                np.std(team_distribution) ** 2
                for team_distribution in red_alliance_points
            ]) ** 0.5
            red_alliance_mean = sum([
                np.mean(team_distribution)
                for team_distribution in red_alliance_points
            ])

            # Calculate mean and standard deviation of the point distribution of the blue alliance.
            blue_alliance_std = sum([
                np.std(team_distribution) ** 2
                for team_distribution in blue_alliance_points
            ]) ** 0.5
            blue_alliance_mean = sum([
                np.mean(team_distribution)
                for team_distribution in blue_alliance_points
            ])

            # Calculate mean and standard deviation of the point distribution of red alliance - blue alliance
            compared_std = (red_alliance_std ** 2 + blue_alliance_std ** 2) ** 0.5
            compared_mean = red_alliance_mean - blue_alliance_mean
            compared_distribution = norm(loc=compared_mean, scale=compared_std)

            # Calculate odds of red/blue winning using integrals.
            odds_of_red_winning = quad(
                lambda x: compared_distribution.pdf(x),
                0,
                np.inf
            )[0]
            odds_of_blue_winning = quad(
                lambda x: compared_distribution.pdf(x),
                -np.inf,
                0
            )[0]

            # Create the stacked bar comparing the odds of the red alliance and blue alliance winning.
            win_percentages(red_odds=odds_of_red_winning, blue_odds=odds_of_blue_winning)

        # Calculates the predicted scores for each alliance
        with predicted_red_score_col:
            st.metric(
                "Predicted Score (:red[Red Alliance])",
                int(
                    red_alliance_mean * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    )
                )
            )

        with predicted_blue_score_col:
            st.metric(
                "Predicted Score (:blue[Blue Alliance])",
                int(
                    blue_alliance_mean * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    )
                )
            )
