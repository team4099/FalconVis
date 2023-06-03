"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import numpy as np
import streamlit as st
from scipy.integrate import quad
from scipy.stats import norm

from .page_manager import PageManager
from utils import (
    alliance_breakdown,
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    GeneralConstants,
    GraphType,
    multi_line_graph,
    plotly_chart,
    Queries,
    retrieve_match_schedule,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team,
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
        match_schedule = retrieve_match_schedule()

        # Create columns to make the input section more structured.
        filter_teams_col, match_selector_col = st.columns(2)

        filter_by_team_number = str(
            filter_teams_col.selectbox(
                "Filter Matches by Team Number",
                ["—"] + retrieve_team_list()
            )
        )

        if filter_by_team_number != "—":
            # Filter through matches where the selected team plays in.
            match_schedule = match_schedule[
                match_schedule["red_alliance"].apply(
                    lambda alliance: ",".join(map(str, alliance))
                ).str.contains(filter_by_team_number)
                | match_schedule["blue_alliance"].apply(
                    lambda alliance: ",".join(map(str, alliance))
                ).str.contains(filter_by_team_number)
            ]

        match_chosen = match_selector_col.selectbox(
            "Choose Match",
            match_schedule["match_key"]
        )
        match_info = match_schedule[
            match_schedule["match_key"] == match_chosen
        ]

        return [
            *match_info["red_alliance"],
            *match_info["blue_alliance"]
        ]

    def generate_match_prediction_dashboard(
        self,
        red_alliance: list[int],
        blue_alliance: list[int]
    ) -> None:
        """Generates metrics for match predictions (Red vs. Blue Tab).

        :param red_alliance: A list of three integers, each integer representing a team on the Red Alliance
        :param blue_alliance: A list of three integers, each integer representing a team on the Blue Alliance.
        """
        chance_of_winning_col, = st.columns(1)
        predicted_red_score_col, red_alliance_breakdown_col = st.columns(2)
        predicted_blue_score_col, blue_alliance_breakdown_col = st.columns(2)

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

        # Alliance breakdowns by team
        with red_alliance_breakdown_col:
            average_points_contributed = [
                round(np.mean(team_distribution), 1) for team_distribution in red_alliance_points
            ]

            best_to_defend = sorted(
                [
                    (
                        team,
                        average_points_contributed[idx],
                        scouting_data_for_team(team)["DriverRating"].mean()
                    ) for idx, team in enumerate(red_alliance)
                ],
                key=lambda info: (info[1] / info[2], 5 - info[2])
            )[-1][0]

            alliance_breakdown(
                red_alliance,
                average_points_contributed,
                best_to_defend,
                Queries.RED_ALLIANCE
            )

        with blue_alliance_breakdown_col:
            average_points_contributed = [
                round(np.mean(team_distribution), 1) for team_distribution in blue_alliance_points
            ]
            best_to_defend = sorted(
                [
                    (
                        team,
                        average_points_contributed[idx],
                        scouting_data_for_team(team)["DriverRating"].mean()
                    ) for idx, team in enumerate(blue_alliance)
                ],
                key=lambda info: (info[1] / info[2], 5 - info[2])
            )[-1][0]

            alliance_breakdown(
                blue_alliance,
                average_points_contributed,
                best_to_defend,
                Queries.BLUE_ALLIANCE
            )

    def generate_match_prediction_graphs(
        self,
        red_alliance: list[int],
        blue_alliance: list[int],
        type_of_graph: str
    ) -> None:
        """Generate graphs for match prediction (Red vs. Blue tab).

        :param red_alliance: A list of three integers, each integer representing a team on the Red Alliance
        :param blue_alliance: A list of three integers, each integer representing a team on the Blue Alliance.
        :param type_of_graph: The type of graphs to display (cycle contributions / point contributions).
        """
        combined_teams = red_alliance + blue_alliance
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS
        color_sequence = [
            "#781212",  # Bright red
            "#163ba1"  # Bright blue
        ]

        game_piece_breakdown_col, auto_cycles_col = st.columns(2)
        teleop_cycles_col, cumulative_cycles_col = st.columns(2)

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

            plotly_chart(
                stacked_bar_graph(
                    combined_teams,
                    game_piece_breakdown,
                    "Teams",
                    ["Total # of Cones Scored", "Total # of Cubes Scored"],
                    "Total Game Pieces Scored",
                    title="Game Piece Breakdown",
                    color_map={
                        "Total # of Cones Scored": GeneralConstants.CONE_COLOR,  # Cone color
                        "Total # of Cubes Scored": GeneralConstants.CUBE_COLOR  # Cube color
                    }
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Breaks down cycles/point contributions among both alliances in Autonomous.
        with auto_cycles_col:
            auto_alliance_distributions = []

            for alliance in (red_alliance, blue_alliance):
                cycles_in_alliance = [
                    (
                        self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID)
                        if display_cycle_contributions
                        else self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID)
                    )
                    for team in alliance
                ]
                auto_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(*cycles_in_alliance, reduce_with_sum=True)
                )

            plotly_chart(
                box_plot(
                    ["Red Alliance", "Blue Alliance"],
                    auto_alliance_distributions,
                    y_axis_label=(
                        "Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Cycles During Autonomous (N={len(auto_alliance_distributions[0])})"
                        if display_cycle_contributions
                        else f"Points Contributed During Autonomous (N={len(auto_alliance_distributions[0])})"
                    ),
                    color_sequence=color_sequence
                )
            )

        # Breaks down cycles/point contributions among both alliances in Teleop.
        with teleop_cycles_col:
            teleop_alliance_distributions = []

            for alliance in (red_alliance, blue_alliance):
                cycles_in_alliance = [
                    (
                        self.calculated_stats.cycles_by_match(team, Queries.TELEOP_GRID)
                        if display_cycle_contributions
                        else self.calculated_stats.points_contributed_by_match(team, Queries.TELEOP_GRID)
                    )
                    for team in alliance
                ]
                teleop_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(*cycles_in_alliance, reduce_with_sum=True)
                )

            plotly_chart(
                box_plot(
                    ["Red Alliance", "Blue Alliance"],
                    teleop_alliance_distributions,
                    y_axis_label=(
                        "Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Cycles During Teleop (N={len(teleop_alliance_distributions[0])})"
                        if display_cycle_contributions
                        else f"Points Contributed During Teleop (N={len(teleop_alliance_distributions[0])})"
                    ),
                    color_sequence=color_sequence
                )
            )

        # Show cumulative cycles/point contributions (auto and teleop)
        with cumulative_cycles_col:
            cumulative_alliance_distributions = [
                auto_distribution + teleop_distribution
                for auto_distribution, teleop_distribution in zip(
                    auto_alliance_distributions, teleop_alliance_distributions
                )
            ]

            plotly_chart(
                box_plot(
                    ["Red Alliance", "Blue Alliance"],
                    cumulative_alliance_distributions,
                    y_axis_label=(
                        "Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Cycles During Auto + Teleop (N={len(cumulative_alliance_distributions[0])})"
                        if display_cycle_contributions
                        else f"Points Contributed During Auto + Teleop (N={len(cumulative_alliance_distributions[0])})"
                    ),
                    color_sequence=color_sequence
                )
            )
            
    def generate_graphs(self, team_numbers: list, display_points: bool = False) -> None:
        """Generates the graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :return:
        """
        
        teams_data = [scouting_data_for_team(team) for team in team_numbers]

        
        auto_graphs_tab, teleop_graphs_tab, endgame_graphs_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop", "🧗 Endgame"]
        )

        # Autonomous graphs
        with auto_graphs_tab:
            st.write("#### Autonomous")

            # Graph for auto cycles over time
            auto_cycles_over_time_per_team = [self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID) if display_points else self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID) for team in team_numbers]

            st.plotly_chart(
                multi_line_graph(
                    x=teams_data[0][Queries.MATCH_KEY],
                    y=auto_cycles_over_time_per_team,
                    x_axis_label="Match Key",
                    y_axis_label=team_numbers,
                    y_axis_title= "Auto Point Total" if display_points else "# of Auto Cycles"
                ),
                use_container_width=True
            )

            auto_cycles_cone_vs_cube_col, auto_cycles_by_level_col = st.columns(2)

            with auto_cycles_cone_vs_cube_col:
                auto_cycles_cone_vs_cube = [[self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.AUTO_CONES).mean() for team in team_numbers], [self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.AUTO_CUBES).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=auto_cycles_cone_vs_cube,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "Cones","Cubes"
                        ],
                        y_axis_title="Auto Cones vs Cubes",
                    ),use_container_width=True
                )

            with auto_cycles_by_level_col:
                auto_cycles_by_level = [[self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.HIGH).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.MID).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.LOW).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=auto_cycles_by_level,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "High","Mid", "Low"
                        ],
                        y_axis_title="Auto Game Pieces by Level",
                    ),use_container_width=True
                )

            # Graph for auto charge station psuccess_rate
            auto_engage_success_rate_per_team = [[self.calculated_stats.auto_engage_success_rate(team), self.calculated_stats.auto_total_attempted_charge(team), self.calculated_stats.auto_total_successful_charge(team)] for team in team_numbers]

            st.plotly_chart(
                    bar_graph(
                        x=team_numbers,
                        y=auto_engage_success_rate_per_team,
                        x_axis_label="Teams",
                        y_axis_label="Auto Engage Success Rate",
                        hover_data=["Attempts", "Successful Engages"]
                    ),use_container_width=True
                )
            

        # Teleop + endgame graphs
        with teleop_graphs_tab:
            st.write("#### Teleop")

            # Graph for teleop cycles over time
            teleop_cycles_over_time_per_team =  [self.calculated_stats.points_contributed_by_match(team, Queries.TELEOP_GRID) if display_points else self.calculated_stats.cycles_by_match(team, Queries.TELEOP_GRID) for team in team_numbers]

            st.plotly_chart(multi_line_graph(
                    x=teams_data[0][Queries.MATCH_KEY],
                    y=teleop_cycles_over_time_per_team,
                    x_axis_label="Match Key",
                    y_axis_label=team_numbers,
                    y_axis_title="Teleop Point Total" if display_points else "# of Teleop Cycles"
                    ),
                    use_container_width=True
            )
                

            teleop_cycles_cone_vs_cube_col, teleop_cycles_by_level_col = st.columns(2)

            with teleop_cycles_cone_vs_cube_col:
                teleop_cycles_cone_vs_cube = [[self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.TELEOP_CONES).mean() for team in team_numbers], [self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.TELEOP_CUBES).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=teleop_cycles_cone_vs_cube,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "Cones","Cubes"
                        ],
                        y_axis_title="Teleop Cones vs Cubes",
                    ), use_container_width=True
                )
            
            with teleop_cycles_by_level_col:
                teleop_cycles_by_level = [[self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.HIGH).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.MID).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.LOW).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=teleop_cycles_by_level,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "High","Mid", "Low"
                        ],
                        y_axis_title="Teleop Game Pieces by Level",
                    ), use_container_width=True
                )
            

        with endgame_graphs_tab:
            st.write("#### Endgame")
