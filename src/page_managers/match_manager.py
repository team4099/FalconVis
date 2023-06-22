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
    Criteria,
    GeneralConstants,
    GraphType,
    multi_line_graph,
    plotly_chart,
    populate_missing_data,
    Queries,
    retrieve_match_schedule,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    win_percentages,
)


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Match` page.

        Creates a dropdown to choose a match for and a dropdown to filter matches that a team played in.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        match_schedule = retrieve_match_schedule()

        # Create columns to make the input section more structured.
        filter_teams_col, match_selector_col = st.columns(2)

        filter_by_team_number = str(
            filter_teams_col.selectbox(
                "Filter Matches by Team Number", ["—"] + retrieve_team_list()
            )
        )

        if filter_by_team_number != "—":
            # Filter through matches where the selected team plays in.
            match_schedule = match_schedule[
                match_schedule["red_alliance"]
                .apply(lambda alliance: ",".join(map(str, alliance)))
                .str.contains(filter_by_team_number)
                | match_schedule["blue_alliance"]
                .apply(lambda alliance: ",".join(map(str, alliance)))
                .str.contains(filter_by_team_number)
            ]

        match_chosen = match_selector_col.selectbox(
            "Choose Match", match_schedule["match_key"]
        )
        match_info = match_schedule[match_schedule["match_key"] == match_chosen]

        return [*match_info["red_alliance"], *match_info["blue_alliance"]]

    def generate_hypothetical_input_section(self) -> list[list, list]:
        """Creates the input section for the `Hypothetical Match` page.

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

    def generate_match_prediction_dashboard(
        self, red_alliance: list[int], blue_alliance: list[int]
    ) -> None:
        """Generates metrics for match predictions (Red vs. Blue Tab).

        :param red_alliance: A list of three integers, each integer representing a team on the Red Alliance
        :param blue_alliance: A list of three integers, each integer representing a team on the Blue Alliance.
        """
        (chance_of_winning_col,) = st.columns(1)
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
            red_alliance_std = (
                sum(
                    [
                        np.std(team_distribution) ** 2
                        for team_distribution in red_alliance_points
                    ]
                )
                ** 0.5
            )
            red_alliance_mean = sum(
                [
                    np.mean(team_distribution)
                    for team_distribution in red_alliance_points
                ]
            )

            # Calculate mean and standard deviation of the point distribution of the blue alliance.
            blue_alliance_std = (
                sum(
                    [
                        np.std(team_distribution) ** 2
                        for team_distribution in blue_alliance_points
                    ]
                )
                ** 0.5
            )
            blue_alliance_mean = sum(
                [
                    np.mean(team_distribution)
                    for team_distribution in blue_alliance_points
                ]
            )

            # Calculate mean and standard deviation of the point distribution of red alliance - blue alliance
            compared_std = (red_alliance_std**2 + blue_alliance_std**2) ** 0.5
            compared_mean = red_alliance_mean - blue_alliance_mean

            # Use sentinel value if there isn't enough of a distribution yet to determine standard deviation.
            if not compared_std and compared_mean:
                compared_std = abs(compared_mean)
            elif not compared_std:
                compared_std = 0.5

            compared_distribution = norm(loc=compared_mean, scale=compared_std)

            # Calculate odds of red/blue winning using integrals.
            odds_of_red_winning = quad(
                lambda x: compared_distribution.pdf(x), 0, np.inf
            )[0]
            odds_of_blue_winning = quad(
                lambda x: compared_distribution.pdf(x), -np.inf, 0
            )[0]

            # Create the stacked bar comparing the odds of the red alliance and blue alliance winning.
            win_percentages(
                red_odds=odds_of_red_winning, blue_odds=odds_of_blue_winning
            )

        # Calculates the predicted scores for each alliance
        with predicted_red_score_col:
            colored_metric(
                "Predicted Score (Red)",
                round(
                    red_alliance_mean
                    * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    ),
                    1
                ),
                background_color=GeneralConstants.DARK_RED,
                opacity=0.5,
            )

        with predicted_blue_score_col:
            colored_metric(
                "Predicted Score (Blue)",
                round(
                    blue_alliance_mean
                    * (
                        GeneralConstants.AVERAGE_FOUL_RATE
                        if GeneralConstants.AVERAGE_FOUL_RATE
                        else 1
                    ),
                    1
                ),
                background_color=GeneralConstants.DARK_BLUE,
                opacity=0.5,
            )

        # Alliance breakdowns by team
        with red_alliance_breakdown_col:
            average_points_contributed = [
                round(np.mean(team_distribution), 1)
                for team_distribution in red_alliance_points
            ]

            best_to_defend = sorted(
                [
                    (
                        team,
                        average_points_contributed[idx],
                        scouting_data_for_team(team)["DriverRating"].mean(),
                    )
                    for idx, team in enumerate(red_alliance)
                ],
                key=lambda info: (info[1] / info[2], 5 - info[2]),
            )[-1][0]

            alliance_breakdown(
                red_alliance,
                average_points_contributed,
                best_to_defend,
                Queries.RED_ALLIANCE,
            )

        with blue_alliance_breakdown_col:
            average_points_contributed = [
                round(np.mean(team_distribution), 1)
                for team_distribution in blue_alliance_points
            ]
            best_to_defend = sorted(
                [
                    (
                        team,
                        average_points_contributed[idx],
                        scouting_data_for_team(team)["DriverRating"].mean(),
                    )
                    for idx, team in enumerate(blue_alliance)
                ],
                key=lambda info: (info[1] / info[2], 5 - info[2]),
            )[-1][0]

            alliance_breakdown(
                blue_alliance,
                average_points_contributed,
                best_to_defend,
                Queries.BLUE_ALLIANCE,
            )

    def generate_match_prediction_graphs(
        self, red_alliance: list[int], blue_alliance: list[int], type_of_graph: str
    ) -> None:
        """Generate graphs for match prediction (Red vs. Blue tab).

        :param red_alliance: A list of three integers, each integer representing a team on the Red Alliance
        :param blue_alliance: A list of three integers, each integer representing a team on the Blue Alliance.
        :param type_of_graph: The type of graphs to display (cycle contributions / point contributions).
        """
        combined_teams = red_alliance + blue_alliance
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS
        color_sequence = ["#781212", "#163ba1"]  # Bright red  # Bright blue

        game_piece_breakdown_col, auto_cycles_col = st.columns(2)
        teleop_cycles_col, cumulative_cycles_col = st.columns(2)

        # Breaks down game pieces between cones/cubes among the six teams
        with game_piece_breakdown_col:
            game_piece_breakdown = [
                [
                    self.calculated_stats.cycles_by_game_piece_per_match(
                        team, Queries.TELEOP_GRID, game_piece
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
                        "Total # of Cubes Scored": GeneralConstants.CUBE_COLOR,  # Cube color
                    },
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
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.AUTO_GRID
                        )
                    )
                    for team in alliance
                ]
                auto_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(
                        *cycles_in_alliance, reduce_with_sum=True
                    )
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
                    color_sequence=color_sequence,
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
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.TELEOP_GRID
                        )
                    )
                    for team in alliance
                ]
                teleop_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(
                        *cycles_in_alliance, reduce_with_sum=True
                    )
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
                    color_sequence=color_sequence,
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
                    color_sequence=color_sequence,
                )
            )

    def generate_alliance_dashboard(self, team_numbers: list[int], color_gradient: list[str]) -> None:
        """Generates an alliance dashboard in the `Match` page.

        :param team_numbers: The teams to generate the alliance dashboard for.
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        fastest_cycler_col, second_fastest_cycler_col, slowest_cycler_col = st.columns(3)

        fastest_cyclers = sorted(
            {
                team: self.calculated_stats.driving_index(team) for team in team_numbers
            }.items(),
            key=lambda pair: pair[1],
            reverse=True
        )

        # Colored metric displaying the fastest cycler in the alliance
        with fastest_cycler_col:
            colored_metric(
                "Fastest Cycler",
                fastest_cyclers[0][0],
                background_color=color_gradient[0],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the second fastest cycler in the alliance
        with second_fastest_cycler_col:
            colored_metric(
                "Second Fastest Cycler",
                fastest_cyclers[1][0],
                background_color=color_gradient[1],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the slowest cycler in the alliance
        with slowest_cycler_col:
            colored_metric(
                "Slowest Cycler",
                fastest_cyclers[2][0],
                background_color=color_gradient[2],
                opacity=0.4,
                border_opacity=0.9
            )

    def generate_autonomous_graphs(
        self,
        team_numbers: list[int],
        type_of_graph: str,
        color_gradient: list[str]
    ) -> None:
        """Generates the autonomous graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        auto_configuration_col, auto_engage_stats_col = st.columns(2)
        auto_cycle_distribution_col, auto_cycles_over_time = st.columns(2)

        # Determine the best auto configuration for an alliance.
        with auto_configuration_col:
            teams_sorted_by_point_contribution = dict(
                sorted(
                    {
                        team: (
                            self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID)
                            if display_cycle_contributions
                            else self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID)
                        )
                        for team in team_numbers
                    }.items(),
                    key=lambda pair: pair[1].max(),
                    reverse=True
                )
            )

            # Y values of plot
            points_by_grid = {}
            full_grid = [Queries.LEFT, Queries.COOP, Queries.RIGHT]
            grids_occupied = set()

            for team, point_contributions in teams_sorted_by_point_contribution.items():
                grid_placements = self.calculated_stats.classify_autos_by_match(team)
                autos_sorted = sorted(
                    zip(point_contributions, grid_placements),
                    key=lambda pair: pair[0],
                    reverse=True
                )

                for auto_pointage, grid in autos_sorted:
                    if grid not in grids_occupied:
                        points_by_grid[team] = (auto_pointage, grid)
                        grids_occupied.add(grid)
                        break
                else:
                    # Add a placeholder in the worst-case scenario
                    placeholder_grid = next(iter(set(full_grid).difference(grids_occupied)))
                    points_by_grid[team] = (point_contributions.max(), placeholder_grid)
                    grids_occupied.add(placeholder_grid)

            # Sort points by grid in order to go from left to right (left, coop, right).
            points_by_grid = dict(
                sorted(
                    points_by_grid.items(),
                    key=lambda pair: full_grid.index(pair[1][1])
                )
            )

            plotly_chart(
                bar_graph(
                    list(points_by_grid.keys()),
                    [value[0] for value in points_by_grid.values()],
                    x_axis_label="Teams (Left, Coop, Right)",
                    y_axis_label=(
                        "Cycles in Auto"
                        if display_cycle_contributions
                        else "Points Scored in Auto"
                    ),
                    title="Best Auto Configuration",
                    color=color_gradient[1]
                )
            )

        # Determine the accuracy of teams when it comes to engaging onto the charge station
        with auto_engage_stats_col:
            successful_engages_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_CHARGING_STATE,
                    Criteria.SUCCESSFUL_ENGAGE_CRITERIA
                )
                for team in team_numbers
            ]
            successful_docks_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_CHARGING_STATE,
                    Criteria.SUCCESSFUL_DOCK_CRITERIA
                )
                for team in team_numbers
            ]
            missed_attempts_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_ENGAGE_ATTEMPTED,
                    Criteria.AUTO_ATTEMPT_CRITERIA
                ) - successful_docks_by_team[idx] - successful_engages_by_team[idx]
                for idx, team in enumerate(team_numbers)
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [missed_attempts_by_team, successful_docks_by_team, successful_engages_by_team],
                    x_axis_label="Teams",
                    y_axis_label=["# of Missed Engages", "# of Docks", "# of Engages"],
                    y_axis_title="",
                    color_map=dict(
                        zip(
                            ["# of Missed Engages", "# of Docks", "# of Engages"],
                            color_gradient
                        )
                    ),
                    title="Auto Engage Stats"
                )
            )

        # Box plot showing the distribution of cycles
        with auto_cycle_distribution_col:
            cycles_by_team = [
                (
                    self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID)
                    if display_cycle_contributions
                    else self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID)
                )
                for team in team_numbers
            ]

            plotly_chart(
                box_plot(
                    team_numbers,
                    cycles_by_team,
                    x_axis_label="Teams",
                    y_axis_label=(
                        "# of Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        "Distribution of Auto Cycles"
                        if display_cycle_contributions
                        else "Distribution of Points Contributed During Auto"
                    ),
                    show_underlying_data=True,
                    color_sequence=color_gradient
                )
            )

        # Plot cycles over time
        with auto_cycles_over_time:
            cycles_by_team = [
                (
                    self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID)
                    if display_cycle_contributions
                    else self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID)
                )
                for team in team_numbers
            ]

            plotly_chart(
                multi_line_graph(
                    *populate_missing_data(cycles_by_team),
                    x_axis_label="Match Index",
                    y_axis_label=team_numbers,
                    y_axis_title=(
                        "# of Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        "Auto Cycles Over Time"
                        if display_cycle_contributions
                        else "Points Contributed in Auto Over Time"
                    ),
                    color_map=dict(zip(team_numbers, color_gradient))
                )
            )

    def generate_teleop_graphs(
        self,
        team_numbers: list[int],
        type_of_graph: str,
        color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        teleop_cycles_by_level_col, teleop_game_piece_breakdown_col = st.columns(2)
        teleop_cycles_over_time_col, teleop_cycles_distribution_col = st.columns(2)

        # Graph the teleop cycles per team by level (High/Mid/Low)
        with teleop_cycles_by_level_col:
            cycles_by_height = []

            for height in (Queries.HIGH, Queries.MID, Queries.LOW):
                cycles_by_height.append([
                    self.calculated_stats.average_cycles_for_height(
                        team,
                        Queries.TELEOP_GRID,
                        height
                    ) * (1 if display_cycle_contributions else Criteria.TELEOP_GRID_POINTAGE[height])
                    for team in team_numbers
                ])

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    cycles_by_height,
                    x_axis_label="Teams",
                    y_axis_label=["High", "Mid", "Low"],
                    y_axis_title="",
                    color_map=dict(
                        zip(
                            ["High", "Mid", "Low"],
                            color_gradient
                        )
                    ),
                    title=(
                        "Average Cycles by Height"
                        if display_cycle_contributions
                        else "Average Points Contributed by Height"
                    )
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Graph the breakdown of game pieces by each team
        with teleop_game_piece_breakdown_col:
            cones_scored_by_team = [
                self.calculated_stats.cycles_by_game_piece_per_match(
                    team,
                    Queries.TELEOP_GRID,
                    Queries.CONE
                ).sum()
                for team in team_numbers
            ]
            cubes_scored_by_team = [
                self.calculated_stats.cycles_by_game_piece_per_match(
                    team,
                    Queries.TELEOP_GRID,
                    Queries.CUBE
                ).sum()
                for team in team_numbers
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [cones_scored_by_team, cubes_scored_by_team],
                    x_axis_label="Teams",
                    y_axis_label=["Total # of Cones Scored", "Total # of Cubes Scored"],
                    y_axis_title="",
                    color_map=dict(
                        zip(
                            ["Total # of Cones Scored", "Total # of Cubes Scored"],
                            [GeneralConstants.CONE_COLOR, GeneralConstants.CUBE_COLOR]
                        )
                    ),
                    title="Game Piece Breakdown by Team"
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Box plot showing the distribution of cycles
        with teleop_cycles_distribution_col:
            cycles_by_team = [
                (
                    self.calculated_stats.cycles_by_match(team, Queries.TELEOP_GRID)
                    if display_cycle_contributions
                    else self.calculated_stats.points_contributed_by_match(team, Queries.TELEOP_GRID)
                )
                for team in team_numbers
            ]

            plotly_chart(
                box_plot(
                    team_numbers,
                    cycles_by_team,
                    x_axis_label="Teams",
                    y_axis_label=(
                        "# of Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        "Distribution of Teleop Cycles"
                        if display_cycle_contributions
                        else "Distribution of Points Contributed During Teleop"
                    ),
                    show_underlying_data=True,
                    color_sequence=color_gradient
                )
            )

        # Plot cycles over time
        with teleop_cycles_over_time_col:
            cycles_by_team = [
                (
                    self.calculated_stats.cycles_by_match(team, Queries.TELEOP_GRID)
                    if display_cycle_contributions
                    else self.calculated_stats.points_contributed_by_match(team, Queries.TELEOP_GRID)
                )
                for team in team_numbers
            ]

            plotly_chart(
                multi_line_graph(
                    *populate_missing_data(cycles_by_team),
                    x_axis_label="Match Index",
                    y_axis_label=team_numbers,
                    y_axis_title=(
                        "# of Cycles"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        "Teleop Cycles Over Time"
                        if display_cycle_contributions
                        else "Points Contributed in Teleop Over Time"
                    ),
                    color_map=dict(zip(team_numbers, color_gradient))
                )
            )
