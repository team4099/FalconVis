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
    retrieve_pit_scouting_data,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    win_percentages,
)


class AllianceSelectionManager(PageManager):
    """The page manager for the `Alliance Selection` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Alliance Selection` page.

        Creates 3 dropdowns to choose teams

        :return: List with 3 choices
        :return: List with 3 choices
        """
        team_list = retrieve_team_list()

        # Create the different dropdowns to choose the three teams for Red Alliance.
        team_1_col, team_2_col, team_3_col = st.columns(3)
        team_1 = team_1_col.selectbox(
            "Team 1",
            team_list,
            index=0
        )
        team_2 = team_2_col.selectbox(
            "Team 2",
            team_list,
            index=1
        )
        team_3 = team_3_col.selectbox(
            "Team 3",
            team_list,
            index=2
        )

        return [team_1, team_2, team_3]

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
    
    def generate_drivetrain_dashboard(self, team_numbers: list[int], color_gradient: list[str]) -> None:
        """Generates an drivetrain dashboard in the `Alliance Selection` page.

        :param team_numbers: The teams to generate the drivetrain dashboard for.
        :param color_gradient: The color gradient to use for graphs.
        :return:
        """

        team1_col, team2_col, team3_col = st.columns(3)

        drivetrain_data = [
            (
                self.pit_scouting_data[
                    self.pit_scouting_data["Team Number"] == team
                ].iloc[0]["Drivetrain"]
                if self.pit_scouting_data is not None
                else "—"
            )
            for team in team_numbers
        ]

        # Colored metric displaying the fastest cycler in the alliance
        with team1_col:
            colored_metric(
                "Team " + str(team_numbers[0]) + " Drivetrain",
                drivetrain_data[0],
                background_color=color_gradient[0],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the second fastest cycler in the alliance
        with team2_col:
            colored_metric(
                "Team " + str(team_numbers[1]) + " Drivetrain",
                drivetrain_data[1],
                background_color=color_gradient[1],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the slowest cycler in the alliance
        with team3_col:
            colored_metric(
                "Team " + str(team_numbers[2]) + " Drivetrain",
                drivetrain_data[2],
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
            average_auto_cycles_by_team = [
                (
                    self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID)
                    if display_cycle_contributions
                    else self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID)
                ).mean()
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    average_auto_cycles_by_team,
                    x_axis_label="Teams",
                    y_axis_label=(
                        "Cycles in Auto"
                        if display_cycle_contributions
                        else "Points Scored in Auto"
                    ),
                    title="Average Auto Contribution",
                    color=color_gradient[1]
                )
            )

        # Determine the accuracy of teams when it comes to engaging onto the charge station
        with auto_engage_stats_col:
            successful_engages_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_ENGAGE_SUCCESSFUL,
                    Criteria.BOOLEAN_CRITERIA
                )
                for team in team_numbers
            ]
            missed_attempts_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_ENGAGE_ATTEMPTED,
                    Criteria.BOOLEAN_CRITERIA
                ) - successful_engages_by_team[idx]
                for idx, team in enumerate(team_numbers)
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [missed_attempts_by_team, successful_engages_by_team],
                    x_axis_label="Teams",
                    y_axis_label=["# of Missed Engages", "# of Engages"],
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
                            GeneralConstants.LEVEL_GRADIENT
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
                self.calculated_stats.teleop_cycles_by_game_piece_per_match(
                    team,
                    Queries.CONE
                ).sum()
                for team in team_numbers
            ]
            cubes_scored_by_team = [
                self.calculated_stats.teleop_cycles_by_game_piece_per_match(
                    team,
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
    
    def generate_rating_graphs(
        self,
        team_numbers: list[int],
        color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """

        disables_col, drivetrain_width_col = st.columns(2)
        driver_rating_col, = st.columns(1)

        with driver_rating_col:
            driver_ratings = [
                self.calculated_stats.average_driver_rating(team) for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    driver_ratings,
                    x_axis_label="Teams",
                    y_axis_label="Driver Rating",
                    title="Driver Rating",
                    color=color_gradient[1]
                )
            )

        with disables_col:
            disables_by_team = [
                    self.calculated_stats.disables_by_team(team) for team in team_numbers
                ]

            plotly_chart(
                    multi_line_graph(
                        *populate_missing_data(disables_by_team),
                        x_axis_label="Match Index",
                        y_axis_label=team_numbers,
                        y_axis_title="Disabled",
                        title=(
                            "Disables Over Time"
                        ),
                        color_map=dict(zip(team_numbers, color_gradient))
                    )
                )
        
        with drivetrain_width_col:
            drivetrain_widths = [
                self.calculated_stats.drivetrain_width_by_team(team) for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    drivetrain_widths,
                    x_axis_label="Teams",
                    y_axis_label="Drivetrain Width",
                    title="Drivetrain Width",
                    color=color_gradient[1]
                )
            )

    