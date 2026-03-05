"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import numpy as np
import streamlit as st
from pandas import to_numeric
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


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        # self.pit_scouting_data = retrieve_pit_scouting_data()
    
    def _fuel_by_match(self, team_number: int, mode: str = ""):
        team_data = scouting_data_for_team(team_number, self.calculated_stats.data)
        magazine_size = to_numeric(team_data[Queries.MAGAZINE_SIZE]).fillna(0)
        auto_fuel = (
            to_numeric(team_data[Queries.AUTO_SINGULAR_COUNT]).fillna(0)
            + to_numeric(team_data[Queries.AUTO_BATCH_COUNT]).fillna(0) * magazine_size
        )
        teleop_fuel = (
            to_numeric(team_data[Queries.TELEOP_SINGULAR_COUNT]).fillna(0)
            + to_numeric(team_data[Queries.TELEOP_BATCH_COUNT]).fillna(0) * magazine_size
        )
        if mode == Queries.AUTO:
            return auto_fuel
        if mode == Queries.TELEOP:
            return teleop_fuel
        return auto_fuel + teleop_fuel

    def _average_fuel(self, team_number: int, mode: str = ""):
        return self._fuel_by_match(team_number, mode).mean()

    def _fuel_index(self, team_number: int) -> float:
        counter_defense_skill = self.calculated_stats.average_counter_defense_skill(team_number)
        return 0 if np.isnan(counter_defense_skill) else counter_defense_skill

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
                        self.calculated_stats.average_driver_rating(team),
                        self.calculated_stats.average_counter_defense_skill(team)
                    )
                    for idx, team in enumerate(red_alliance)
                ],
                key=lambda info: info[1] / info[2],
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
                        self.calculated_stats.average_driver_rating(team),
                        self.calculated_stats.average_counter_defense_skill(team)
                    )
                    for idx, team in enumerate(blue_alliance)
                ],
                key=lambda info: info[1] / info[2],
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
        :param type_of_graph: The type of graphs to display (fuel contributions / point contributions).
        """
        combined_teams = red_alliance + blue_alliance
        display_fuel_contributions = type_of_graph == GraphType.FUEL_CONTRIBUTIONS
        color_sequence = ["#781212", "#163ba1"]  # Bright red  # Bright blue

        structure_breakdown_col, auto_fuel_col = st.columns(2)
        teleop_fuel_col, cumulative_fuel_col = st.columns(2)

        # Breaks down where the different teams scored among the six teams
        with structure_breakdown_col:
            structure_breakdown = [
                [
                    self._fuel_by_match(team).sum()
                    for team in combined_teams
                ]
            ]

            plotly_chart(
                stacked_bar_graph(
                    combined_teams,
                    structure_breakdown,
                    "Teams",
                    ["# of Total Fuel"],
                    "Total Fuel Scored",
                    title="Structure Breakdown",
                    color_map={
                        "# of Total Fuel": GeneralConstants.GOLD_GRADIENT[0],
                    },
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Breaks down fuel/point contributions among both alliances in Autonomous.
        with auto_fuel_col:
            auto_alliance_distributions = []

            for alliance in (red_alliance, blue_alliance):
                fuel_in_alliance = [
                    (
                        self._fuel_by_match(team, Queries.AUTO)
                        if display_fuel_contributions
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.AUTO
                        )
                    )
                    for team in alliance
                ]
                auto_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(
                        *fuel_in_alliance, reduce_with_sum=True
                    )
                )

            plotly_chart(
                box_plot(
                    ["Red Alliance", "Blue Alliance"],
                    auto_alliance_distributions,
                    y_axis_label=(
                        "Fuel Scored"
                        if display_fuel_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Fuel During Autonomous (N={len(auto_alliance_distributions[0])})"
                        if display_fuel_contributions
                        else f"Points Contributed During Autonomous (N={len(auto_alliance_distributions[0])})"
                    ),
                    color_sequence=color_sequence,
                )
            )

        # Breaks down fuel/point contributions among both alliances in Teleop.
        with teleop_fuel_col:
            teleop_alliance_distributions = []

            for alliance in (red_alliance, blue_alliance):
                fuel_in_alliance = [
                    (
                        self._fuel_by_match(team, Queries.TELEOP)
                        if display_fuel_contributions
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.TELEOP
                        )
                    )
                    for team in alliance
                ]
                teleop_alliance_distributions.append(
                    self.calculated_stats.cartesian_product(
                        *fuel_in_alliance, reduce_with_sum=True
                    )
                )

            plotly_chart(
                box_plot(
                    ["Red Alliance", "Blue Alliance"],
                    teleop_alliance_distributions,
                    y_axis_label=(
                        "Fuel Scored"
                        if display_fuel_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Fuel During Teleop (N={len(teleop_alliance_distributions[0])})"
                        if display_fuel_contributions
                        else f"Points Contributed During Teleop (N={len(teleop_alliance_distributions[0])})"
                    ),
                    color_sequence=color_sequence,
                )
            )

        # Show cumulative fuel/point contributions (auto and teleop)
        with cumulative_fuel_col:
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
                        "Fuel Scored"
                        if display_fuel_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Fuel During Auto + Teleop (N={len(cumulative_alliance_distributions[0])})"
                        if display_fuel_contributions
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
        highest_fuel_index_col, second_highest_fuel_index_col, lowest_fuel_index_col = st.columns(3)

        fuel_index_rankings = sorted(
            {
                team: self._fuel_index(team) for team in team_numbers
            }.items(),
            key=lambda pair: pair[1],
            reverse=True
        )

        # Colored metric displaying the highest fuel index in the alliance.
        with highest_fuel_index_col:
            colored_metric(
                "Highest Fuel Index",
                fuel_index_rankings[0][0],
                background_color=color_gradient[0],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the second highest fuel index in the alliance.
        with second_highest_fuel_index_col:
            colored_metric(
                "Second Highest Fuel Index",
                fuel_index_rankings[1][0],
                background_color=color_gradient[1],
                opacity=0.4,
                border_opacity=0.9
            )

        # Colored metric displaying the lowest fuel index in the alliance.
        with lowest_fuel_index_col:
            colored_metric(
                "Lowest Fuel Index",
                fuel_index_rankings[2][0],
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
        :param type_of_graph: The type of graph to make (fuel contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        display_fuel_contributions = type_of_graph == GraphType.FUEL_CONTRIBUTIONS

        best_auto_config_col, auto_fuel_breakdown_col = st.columns(2)


        # Best auto configuration graph
        with best_auto_config_col:
            if display_fuel_contributions:
                best_autos_by_team = sorted(
                    [
                        (team_number, self._fuel_by_match(team_number, Queries.AUTO).max())
                        for team_number in team_numbers
                    ],
                    key=lambda pair: pair[1],
                    reverse=True
                )
            else:
                best_autos_by_team = sorted(
                    [
                        (
                            team_number,
                            self.calculated_stats.points_contributed_by_match(team_number, Queries.AUTO).max())
                        for team_number in team_numbers
                    ],
                    key=lambda pair: pair[1],
                    reverse=True
                )

            plotly_chart(
                bar_graph(
                    [pair[0] for pair in best_autos_by_team],
                    [pair[1] for pair in best_autos_by_team],
                    x_axis_label="Teams",
                    y_axis_label=(
                        "# of Fuel in Auto"
                        if display_fuel_contributions
                        else "# of Points in Auto"
                    ),
                    title="Best Auto Configuration",
                    color=color_gradient
                )
            )

        # Auto fuel breakdown graph
        with auto_fuel_breakdown_col:
            if display_fuel_contributions:
                average_auto_fuel_by_team = [
                    self._average_fuel(team, Queries.AUTO)
                    for team in team_numbers
                ]
            else:
                average_auto_fuel_by_team = [
                    self._average_fuel(team, Queries.AUTO)
                    for team in team_numbers
                ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [average_auto_fuel_by_team],
                    "Teams",
                    [
                        ("Avg. Auto Fuel" if display_fuel_contributions else "Avg. Auto Points"),
                    ],
                    ("Total Auto Fuel" if display_fuel_contributions else "Total Auto Points"),
                    title="Auto Scoring Breakdown",
                    color_map={
                        ("Avg. Auto Fuel" if display_fuel_contributions else "Avg. Auto Points"):
                            color_gradient[0],
                    }
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )


    def generate_teleop_graphs(
            self,
            team_numbers: list[int],
            type_of_graph: str,
            color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: The type of graph to make (fuel contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        teams_data = [scouting_data_for_team(team) for team in team_numbers]
        display_fuel_contributions = type_of_graph == GraphType.FUEL_CONTRIBUTIONS

        st.write("## ⭕ Fuel")
        (fuel_over_time_col,) = st.columns(1, gap="small")

        st.divider()
        st.write("## ⛓️ Endgame")
        climb_breakdown_by_team_col, climb_speed_by_team = st.columns(2, gap="large")

        short_gradient = [
            GeneralConstants.LIGHT_RED,
            GeneralConstants.RED_TO_GREEN_GRADIENT[2],
            GeneralConstants.LIGHT_GREEN
        ]

        # Display the teleop fuel of each team over time.
        with fuel_over_time_col:
            fuel_by_team = [
                self._fuel_by_match(team, Queries.TELEOP)
                for team in team_numbers
            ]
            best_teams = sorted(zip(team_numbers, fuel_by_team), key=lambda pair: pair[1].mean())
            color_map = {
                pair[0]: color
                for pair, color in zip(best_teams, short_gradient)
            }

            plotly_chart(
                multi_line_graph(
                    *populate_missing_data(fuel_by_team),
                    x_axis_label="Match Index",
                    y_axis_label=team_numbers,
                    y_axis_title=(
                        "# of Fuel Scored"
                        if display_fuel_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        "Teleop Fuel Over Time"
                        if display_fuel_contributions
                        else "Points Contributed through Teleop Fuel Over Time"
                    ),
                    color_map=color_map
                )
            )

        with climb_breakdown_by_team_col:
            climb_levels = [
                level
                for level in Criteria.CLIMBING_CRITERIA
                if level != "None"
            ]
            climbs_by_level = [
                [
                    (team_data[Queries.TELEOP_CLIMB] == level).sum()
                    for team_data in teams_data
                ]
                for level in climb_levels
            ]
            climb_level_labels = [
                f"Level {Criteria.CLIMBING_CRITERIA[level]} Climbs"
                for level in climb_levels
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    climbs_by_level,
                    x_axis_label="Teams",
                    y_axis_label=climb_level_labels,
                    y_axis_title="# of Climbs by Level",
                    title="Climbs by Team",
                    color_map={
                        label: color
                        for label, color in zip(climb_level_labels, GeneralConstants.LEVEL_GRADIENT)
                    }
                )
            )

        with climb_speed_by_team:
            slow_climbs = [
                (team_data[Queries.CLIMB_SPEED] == "Slow").sum()
                for team_data in teams_data
            ]

            fast_climbs = [
                (team_data[Queries.CLIMB_SPEED] == "Fast").sum()
                for team_data in teams_data
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [slow_climbs, fast_climbs],
                    x_axis_label="Teams",
                    y_axis_label=["Slow Climbs", "Fast Climbs"],
                    y_axis_title="# of Climb Speeds",
                    title="Climb Speeds by Team",
                    color_map={"Slow Climbs": GeneralConstants.LIGHT_RED, "Fast Climbs": GeneralConstants.LIGHT_GREEN}
                )
            )

    def generate_qualitative_graphs(
            self,
            team_numbers: list[int],
            color_gradient: list[str]
    ):
        """Generates the qualitative graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        driver_rating_by_team_col, counter_defense_rating_by_team_col, disables_by_team_col = st.columns(3)

        with driver_rating_by_team_col:
            driver_rating_by_team = [
                self.calculated_stats.average_driver_rating(team)
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    driver_rating_by_team,
                    x_axis_label="Teams",
                    y_axis_label="Driver Rating (1-5)",
                    title="Average Driver Rating by Team",
                    color=color_gradient[0]
                )
            )

        with counter_defense_rating_by_team_col:
            counter_defense_rating_by_team = [
                self.calculated_stats.average_counter_defense_skill(team)
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    counter_defense_rating_by_team,
                    x_axis_label="Teams",
                    y_axis_label="Intake Defense Rating (1-5)",
                    title="Average Intake Defense Rating by Team",
                    color=color_gradient[1]
                )
            )

        with disables_by_team_col:
            disables_by_team = [
                self.calculated_stats.cumulative_stat(team, Queries.DISABLE, Criteria.BOOLEAN_CRITERIA)
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    disables_by_team,
                    x_axis_label="Teams",
                    y_axis_label="Disables",
                    title="Disables by Team",
                    color=color_gradient[2]
                )
            )
