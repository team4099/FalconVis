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


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.pit_scouting_data = retrieve_pit_scouting_data()

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
        :param type_of_graph: The type of graphs to display (cycle contributions / point contributions).
        """
        combined_teams = red_alliance + blue_alliance
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS
        color_sequence = ["#781212", "#163ba1"]  # Bright red  # Bright blue

        structure_breakdown_col, auto_cycles_col = st.columns(2)
        teleop_cycles_col, cumulative_cycles_col = st.columns(2)

        # Breaks down where the different teams scored among the six teams
        with structure_breakdown_col:
            structure_breakdown = [
                [
                    self.calculated_stats.cycles_by_structure_per_match(
                        team, structures
                    ).sum()
                    for team in combined_teams
                ]
                for structures in (
                    (Queries.AUTO_AMP, Queries.TELEOP_AMP),
                    (Queries.AUTO_SPEAKER, Queries.TELEOP_SPEAKER),
                    Queries.TELEOP_TRAP
                )
            ]

            plotly_chart(
                stacked_bar_graph(
                    combined_teams,
                    structure_breakdown,
                    "Teams",
                    ["# of Amp Cycles", "# of Speaker Cycles", "# of Trap Cycles"],
                    "Total Cycles Scored into Structures",
                    title="Structure Breakdown",
                    color_map={
                        "# of Amp Cycles": GeneralConstants.GOLD_GRADIENT[0],
                        "# of Speaker Cycles": GeneralConstants.GOLD_GRADIENT[1],
                        "# of Trap Cycles": GeneralConstants.GOLD_GRADIENT[2]
                    },
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Breaks down cycles/point contributions among both alliances in Autonomous.
        with auto_cycles_col:
            auto_alliance_distributions = []

            for alliance in (red_alliance, blue_alliance):
                cycles_in_alliance = [
                    (
                        self.calculated_stats.cycles_by_match(team, Queries.AUTO)
                        if display_cycle_contributions
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.AUTO
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
                        "Notes Scored"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Notes During Autonomous (N={len(auto_alliance_distributions[0])})"
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
                        self.calculated_stats.cycles_by_match(team, Queries.TELEOP)
                        if display_cycle_contributions
                        else self.calculated_stats.points_contributed_by_match(
                            team, Queries.TELEOP
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
                        "Notes Scored"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Notes During Teleop (N={len(teleop_alliance_distributions[0])})"
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
                        "Notes Scored"
                        if display_cycle_contributions
                        else "Points Contributed"
                    ),
                    title=(
                        f"Notes During Auto + Teleop (N={len(cumulative_alliance_distributions[0])})"
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
        fastest_cycler_col, second_fastest_cycler_col, slowest_cycler_col, reaches_coop_col = st.columns(4)

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

        # Colored metric displaying the chance of reaching the co-op bonus (1 amp cycle in 45 seconds + auto)
        with reaches_coop_col:
            colored_metric(
                "Chance of Co-Op Bonus",
                f"{self.calculated_stats.chance_of_coop_bonus(team_numbers):.0%}",
                background_color=color_gradient[3],
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

        best_auto_config_col, auto_cycles_breakdown_col, centerline_auto_col = st.columns(3)

        # Best auto configuration graph
        with best_auto_config_col:
            if display_cycle_contributions:
                best_autos_by_team = sorted(
                    [
                        (team_number, self.calculated_stats.cycles_by_match(team_number, Queries.AUTO).max())
                        for team_number in team_numbers
                    ],
                    key=lambda pair: pair[1],
                    reverse=True
                )
            else:
                best_autos_by_team = sorted(
                    [
                        (
                        team_number, self.calculated_stats.points_contributed_by_match(team_number, Queries.AUTO).max())
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
                        "# of Cycles in Auto"
                        if display_cycle_contributions
                        else "# of Points in Auto"
                    ),
                    title="Best Auto Configuration",
                    color=color_gradient
                )
            )

        # Auto cycle breakdown graph
        with auto_cycles_breakdown_col:
            if display_cycle_contributions:
                average_speaker_cycles_by_team = [
                    self.calculated_stats.average_cycles_for_structure(team, Queries.AUTO_SPEAKER)
                    for team in team_numbers
                ]
                average_amp_cycles_by_team = [
                    self.calculated_stats.average_cycles_for_structure(team, Queries.AUTO_AMP)
                    for team in team_numbers
                ]
            else:
                average_speaker_cycles_by_team = [
                    self.calculated_stats.average_cycles_for_structure(team, Queries.AUTO_SPEAKER) * 5
                    for team in team_numbers
                ]
                average_amp_cycles_by_team = [
                    self.calculated_stats.average_cycles_for_structure(team, Queries.AUTO_AMP) * 2
                    for team in team_numbers
                ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [average_speaker_cycles_by_team, average_amp_cycles_by_team],
                    "Teams",
                    [
                        ("Avg. Speaker Cycles" if display_cycle_contributions else "Avg. Speaker Points"),
                        ("Avg. Amp Cycles" if display_cycle_contributions else "Avg. Amp Points")
                    ],
                    ("Total Auto Cycles" if display_cycle_contributions else "Total Auto Points"),
                    title="Auto Scoring Breakdown",
                    color_map={
                        ("Avg. Speaker Cycles" if display_cycle_contributions else "Avg. Speaker Points"): color_gradient[1],
                        ("Avg. Amp Cycles" if display_cycle_contributions else "Avg. Amp Points"): color_gradient[2]
                    }
                ).update_layout(xaxis={"categoryorder": "total descending"})
            )

        # Number of times they intook from the centerline by team
        with centerline_auto_col:
            autos_in_centerline_by_team = [
                self.calculated_stats.cumulative_stat(
                    team,
                    Queries.AUTO_USED_CENTERLINE,
                    Criteria.BOOLEAN_CRITERIA
                )
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    autos_in_centerline_by_team,
                    x_axis_label="Teams",
                    y_axis_label="# of Centerline Autos Achieved",
                    title="Centerline Autos Achieved By Team",
                    color=color_gradient[-1]
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
        :param type_of_graph: The type of graph to make (cycle contributions/point contributions).
        :param color_gradient: The color gradient to use for graphs, depending on the alliance.
        :return:
        """
        teams_data = [scouting_data_for_team(team) for team in team_numbers]
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        speaker_cycles_over_time_col, amp_periods_over_time_col = st.columns(2, gap="large")
        climb_breakdown_by_team_col, climb_speed_by_team = st.columns(2, gap="large")
        passing_shot_by_team_col = st.columns(1, gap="large")

        short_gradient = [
            GeneralConstants.LIGHT_RED,
            GeneralConstants.RED_TO_GREEN_GRADIENT[2],
            GeneralConstants.LIGHT_GREEN
        ]

        # Display the teleop speaker cycles of each team over time
        with speaker_cycles_over_time_col:
            cycles_by_team = [
                self.calculated_stats.cycles_by_structure_per_match(team, Queries.TELEOP_SPEAKER) *
                (
                    1 if display_cycle_contributions else 2
                )
                for team in team_numbers
            ]
            best_teams = sorted(zip(team_numbers, cycles_by_team), key=lambda pair: pair[1].mean())
            color_map = {
                pair[0]: color
                for pair, color in zip(best_teams, short_gradient)
            }

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
                        "Teleop Speaker Cycles Over Time"
                        if display_cycle_contributions
                        else "Points Contributed in the Speaker Over Time"
                    ),
                    color_map=color_map
                )
            )

        # Display the teleop speaker cycles of each team over time
        with amp_periods_over_time_col:
            amp_periods_by_team = [
                self.calculated_stats.potential_amplification_periods_by_match(team)
                for team in team_numbers
            ]
            best_teams = sorted(zip(team_numbers, amp_periods_by_team), key=lambda pair: pair[1].mean())
            color_map = {
                pair[0]: color
                for pair, color in zip(best_teams, short_gradient)
            }

            plotly_chart(
                multi_line_graph(
                    *populate_missing_data(amp_periods_by_team),
                    x_axis_label="Match Index",
                    y_axis_label=team_numbers,
                    y_axis_title="# of Potential Amplification Periods",
                    title="Potential Amplification Periods Produced by Alliance",
                    color_map=color_map
                )
            )

        with climb_breakdown_by_team_col:
            harmonized_climbs_by_team = [
                team_data[Queries.HARMONIZED_ON_CHAIN].sum() 
                for team_data in teams_data
            ]
            normal_climbs_by_team = [
                team_data[Queries.CLIMBED_CHAIN].sum() - harmonized_climbs
                for team_data, harmonized_climbs in zip(teams_data, harmonized_climbs_by_team)
            ]

            plotly_chart(
                stacked_bar_graph(
                    team_numbers,
                    [normal_climbs_by_team, harmonized_climbs_by_team],
                    x_axis_label="Teams",
                    y_axis_label=["Normal Climbs", "Harmonized Climbs"],
                    y_axis_title="# of Climb Types",
                    title="Climbs by Team",
                    color_map={"Normal Climbs": color_gradient[0], "Harmonized Climbs": color_gradient[1]}
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

        with passing_shot_by_team_col:
            passing_shots_by_team = [
                self.calculated_stats.passing_shots_by_match(team)
                for team in team_numbers
            ]
            color_map = {
                pair[0]: color
                for pair, color in zip(best_teams, short_gradient)
            }

            plotly_chart(
                multi_line_graph(
                    *populate_missing_data(amp_periods_by_team),
                    x_axis_label="Match Index",
                    y_axis_label=team_numbers,
                    y_axis_title="# of Cycles",
                    title="Potential Passing Cycles by Alliance",
                    color_map=color_map
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
        driver_rating_by_team_col, defense_rating_by_team_col, disables_by_team_col = st.columns(3)

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
        
        with defense_rating_by_team_col:
            defense_rating_by_team = [
                self.calculated_stats.average_defense_skill(team)
                for team in team_numbers
            ]

            plotly_chart(
                bar_graph(
                    team_numbers,
                    defense_rating_by_team,
                    x_axis_label="Teams",
                    y_axis_label="Defense Rating (1-5)",
                    title="Average Defense Rating by Team",
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
