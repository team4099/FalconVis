"""Creates the `MatchManager` class used to set up the Match page and its graphs."""
from random import randrange

import numpy as np
import streamlit as st
from scipy.integrate import quad
from scipy.stats import norm

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    colored_metric,
    GeneralConstants,
    Queries,
    retrieve_team_list,
    retrieve_scouting_data,
    stacked_bar_graph,
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
        red_alliance_form, blue_alliance_form = st.columns(2, gap="medium")

        # Create the different dropdowns to choose the three teams for Red Alliance.
        with red_alliance_form:
            red_1_col, red_2_col, red_3_col = st.columns(3)
            red_1 = red_1_col.selectbox(
                ":red[Red 1]",
                team_list,
                index=0
            )
            red_2 = red_2_col.selectbox(
                ":red[Red 2]",
                team_list,
                index=1
            )
            red_3 = red_3_col.selectbox(
                ":red[Red 3]",
                team_list,
                index=2
            )

        # Create the different dropdowns to choose the three teams for Blue Alliance.
        with blue_alliance_form:
            blue_1_col, blue_2_col, blue_3_col = st.columns(3)
            blue_1 = blue_1_col.selectbox(
                ":blue[Blue 1]",
                team_list,
                index=3
            )
            blue_2 = blue_2_col.selectbox(
                ":blue[Blue 2]",
                team_list,
                index=4
            )
            blue_3 = blue_3_col.selectbox(
                ":blue[Blue 3]",
                team_list,
                index=5
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
        combined_teams = red_alliance + blue_alliance

        chance_of_winning_col, = st.columns(1)
        predicted_red_score_col, predicted_blue_score_col = st.columns(2)
        cycle_contribution_breakdown_tab, point_contribution_breakdown_tab = st.tabs(
            ["📈 Cycle Contribution Breakdown", "🧮 Point Contribution Breakdown"]
        )

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

            # Use sentinel value if there isn't enough of a distribution yet to determine standard deviation.
            if not compared_std and compared_mean:
                compared_std = abs(compared_mean)
            elif not compared_std:
                compared_std = 0.5

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
            colored_metric(
                "Predicted Score (Red)",
                int(
                    red_alliance_mean * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    )
                ),
                background_color=GeneralConstants.DARK_RED,
                opacity=0.5
            )

        with predicted_blue_score_col:
            colored_metric(
                "Predicted Score (Blue)",
                int(
                    blue_alliance_mean * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    )
                ),
                background_color=GeneralConstants.DARK_BLUE,
                opacity=0.5
            )

        # Creates graphs breaking down cycles among teams
        with cycle_contribution_breakdown_tab:
            game_piece_breakdown_col, _ = st.columns(2)

            # Breaks down game pieces between cones/cubes among the six teams
            with game_piece_breakdown_col:
                game_piece_breakdown = [
                    [
                        self.calculated_stats.cycles_by_game_piece_per_match(
                            team,
                            Queries.TELEOP_GRID,
                            game_piece
                        ).sum()
                        for team in combined_teams
                    ]
                    for game_piece in (Queries.CONE, Queries.CUBE)
                ]

                st.plotly_chart(
                    stacked_bar_graph(
                        combined_teams,
                        game_piece_breakdown,
                        "Teams",
                        ["Total # of Cones Scored", "Total # of Cubes Scored"],
                        title="Game Piece Breakdown",
                        color_map={
                            "Total # of Cones Scored": GeneralConstants.CONE_COLOR,  # Cone color
                            "Total # of Cubes Scored": GeneralConstants.CUBE_COLOR  # Cube color
                        }
                    ).update_layout(xaxis={"categoryorder": "total descending"}),
                    use_container_width=True
                )
