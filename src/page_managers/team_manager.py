"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import re
import streamlit as st
from annotated_text import annotated_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import (
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    GraphType,
    line_graph,
    multi_line_graph,
    plotly_chart,
    Queries,
    retrieve_team_list,
    retrieve_pit_scouting_data,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    colored_metric_with_two_values,
    populate_missing_data
)


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        # self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        queried_team = int(st.experimental_get_query_params().get("team_number", [0])[0]) or 4099
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(queried_team) if queried_team in team_list else 0
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        points_contributed_col, auto_cycle_col, teleop_col, misses_col = st.columns(4)
        iqr_col, algae_off_reef_col, climb_breakdown_col, disables_col = st.columns(4)

        # Metric for avg. points contributed
        with points_contributed_col:
            average_points_contributed = self.calculated_stats.average_points_contributed(
                team_number
            )
            points_contributed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_points_contributed(team)
            )
            colored_metric(
                "Average Points Contributed",
                round(average_points_contributed, 2),
                threshold=points_contributed_for_percentile
            )

        # Metric for average auto cycles
        with auto_cycle_col:
            average_auto_coral_l1_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_CORAL_L1
            )
            average_auto_coral_l2_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_CORAL_L2
            )
            average_auto_coral_l3_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_CORAL_L3
            )
            average_auto_coral_l4_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_CORAL_L4
            )
            average_auto_algae_barge_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_BARGE
            )
            average_auto_algae_processor_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_PROCESSOR
            )
            average_auto_coral_cycles = average_auto_coral_l1_cycles + average_auto_coral_l2_cycles + average_auto_coral_l3_cycles + average_auto_coral_l4_cycles
            average_auto_algae_cycles = average_auto_algae_barge_cycles + average_auto_algae_processor_cycles

            average_auto_coral_l1_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_CORAL_L1)
            )
            average_auto_coral_l2_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_CORAL_L2)
            )
            average_auto_coral_l3_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_CORAL_L3)
            )
            average_auto_coral_l4_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_CORAL_L4)
            )
            average_auto_algae_barge_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_BARGE)
            )
            average_auto_algae_processor_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_PROCESSOR)
            )

            average_auto_coral_cycles_for_percentile = (average_auto_coral_l1_cycles_for_percentile + average_auto_coral_l2_cycles_for_percentile + average_auto_coral_l3_cycles_for_percentile + average_auto_coral_l4_cycles_for_percentile)/4.0
            average_auto_algae_cycles_for_percentile = (average_auto_algae_processor_cycles_for_percentile + average_auto_algae_barge_cycles_for_percentile) / 2.0


            colored_metric_with_two_values(
                "Average Auto Cycles",
                "Coral / Algae",
                round(average_auto_coral_cycles, 2),
                round(average_auto_algae_cycles, 2),
                first_threshold=average_auto_coral_cycles_for_percentile,
                second_threshold=average_auto_algae_cycles_for_percentile
            )

        # Metric for average teleop coral cycles
        with teleop_col:
            average_teleop_algae_processor_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_PROCESSOR
            )
            average_teleop_algae_barge_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_BARGE
            )

            average_teleop_algae_processor_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_PROCESSOR)
            )
            average_teleop_algae_barge_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_BARGE)
            )
            average_teleop_coral_l1_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_CORAL_L1
            )
            average_teleop_coral_l2_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_CORAL_L2
            )
            average_teleop_coral_l3_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_CORAL_L3
            )
            average_teleop_coral_l4_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_CORAL_L4
            )
            average_teleop_coral_cycles = average_teleop_coral_l1_cycles + average_teleop_coral_l2_cycles + average_teleop_coral_l3_cycles + average_teleop_coral_l4_cycles

            average_teleop_coral_l1_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_CORAL_L1)
            )
            average_teleop_coral_l2_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_CORAL_L2)
            )
            average_teleop_coral_l3_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_CORAL_L3)
            )
            average_teleop_coral_l4_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_CORAL_L4)
            )
            average_teleop_coral_for_percentile = (average_teleop_coral_l1_for_percentile + average_teleop_coral_l2_for_percentile + average_teleop_coral_l3_for_percentile + average_teleop_coral_l4_for_percentile) / 4.0

            colored_metric_with_two_values(
                "Average Teleop Cycles",
                "Coral / Algae",
                round(average_teleop_coral_cycles, 2),
                round(average_teleop_algae_barge_cycles + average_teleop_algae_processor_cycles, 2),
                first_threshold=average_teleop_coral_for_percentile,
                second_threshold=average_teleop_algae_processor_for_percentile + average_teleop_algae_barge_for_percentile
            )

        # Metric for average algae teleop cycles
        with misses_col:
            average_auto_misses = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_CORAL_MISSES
            )
            average_teleop_misses = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_CORAL_MISSES
            )

            average_auto_misses_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_CORAL_MISSES)
            )
            average_teleop_misses_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_CORAL_MISSES)
            )

            colored_metric_with_two_values(
                "Average Misses",
                "Auto / Teleop",
                round(average_auto_misses, 2),
                round(average_teleop_misses, 2),
                first_threshold=average_auto_misses_for_percentile,
                second_threshold=average_teleop_misses_for_percentile,
                invert_threshold=True
            )

        # Metric for IQR of points contributed (consistency)
        with iqr_col:
            team_dataset = self.calculated_stats.points_contributed_by_match(
                team_number
            )
            iqr_of_points_contributed = self.calculated_stats.calculate_iqr(team_dataset)
            iqr_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.calculate_iqr(
                    self.points_contributed_by_match(team)
                )
            )

            colored_metric(
                "IQR of Points Contributed",
                iqr_of_points_contributed,
                threshold=iqr_for_percentile,
                invert_threshold=True
            )

        # Metric for ability to remove algae off the reef
        with algae_off_reef_col:
            average_algae_removal_value = self.calculated_stats.average_stat(
                team_number,
                Queries.TELEOP_ALGAE_REMOVAL,
                Criteria.BOOLEAN_CRITERIA
            )
            colored_metric(
                "Can robot remove algae off reef?",
                average_algae_removal_value,
                threshold=0.01,
                value_formatter=lambda value: "Yes" if value > 0 else "No"
            )

        # Metric for number of times robot climbed
        with climb_breakdown_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMBED_CAGE,
                Criteria.CLIMBING_CRITERIA
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.CLIMBED_CAGE, Criteria.CLIMBING_CRITERIA)
            )

            colored_metric(
                "# of Times Climbed",
                times_climbed,
                threshold=times_climbed_for_percentile,
            )

        # Metric for number of disables
        with disables_col:
            times_disabled = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.DISABLE,
                Criteria.BOOLEAN_CRITERIA
            )
            times_disabled_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.DISABLE, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Times Disabled",
                times_disabled,
                threshold=times_disabled_for_percentile,
                invert_threshold=True
            )

    def generate_autonomous_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType
    ) -> None:
        """Generates the autonomous graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: The type of graph to use for the graphs on said page (cycle contribution / point contributions).
        :return:
        """
        leaves_col, scoring_side_col = st.columns(2)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        with leaves_col:
            # Metric for how many times they left the starting zone
            times_left_starting_zone = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.LEFT_STARTING_ZONE,
                Criteria.BOOLEAN_CRITERIA
            )
            times_left_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.LEFT_STARTING_ZONE, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Leaves from the Starting Zone",
                times_left_starting_zone,
                threshold=times_left_for_percentile
            )

        with scoring_side_col:
            # Metric for how many times they went to the centerline for auto
            times_went_to_non_processor_side = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.SCORING_SIDE,
                {"Non-Processor Side": 1}
            )
            times_went_to_processor_side = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.SCORING_SIDE,
                {"Processor Side": 1}
            )

            times_went_to_non_processor_side_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.SCORING_SIDE, {"Non-Processor Side": 1})
            )
            times_went_to_processor_side_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.SCORING_SIDE, {"Processor Side": 1})
            )

            colored_metric_with_two_values(
                "# of Times Scored on Side",
                "Non-Processor Side / Processor Side",
                round(times_went_to_non_processor_side, 2),
                round(times_went_to_processor_side, 2),
                first_threshold=times_went_to_non_processor_side_percentile,
                second_threshold=times_went_to_processor_side_percentile
            )

        # Auto Speaker/amp over time graph
        coral_l1_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_CORAL_L1
        ) * (1 if using_cycle_contributions else 3)
        coral_l2_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_CORAL_L2
        ) * (1 if using_cycle_contributions else 4)
        coral_l3_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_CORAL_L3
        ) * (1 if using_cycle_contributions else 6)
        coral_l4_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_CORAL_L4
        ) * (1 if using_cycle_contributions else 7)

        algae_barge_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_BARGE
        ) * (1 if using_cycle_contributions else 4)
        algae_processor_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_PROCESSOR
        ) * (1 if using_cycle_contributions else 6)

        line_names_1 = [
            ("# of Coral L1 Cycles" if using_cycle_contributions else "# of Coral L1 Points"),
            ("# of Coral L2 Cycles" if using_cycle_contributions else "# of Coral L2 Points"),
            ("# of Coral L3 Cycles" if using_cycle_contributions else "# of Coral L3 Points"),
            ("# of Coral L4 Cycles" if using_cycle_contributions else "# of Coral L4 Points")
        ]

        line_names_2 = [
            ("# of Algae Net Cycles" if using_cycle_contributions else "# of Algae Net Points"),
            ("# of Algae Processor Cycles" if using_cycle_contributions else "# of Algae Processor Points")
        ]

        plotly_chart(
            multi_line_graph(
                range(len(coral_l1_cycles_by_match)),
                [coral_l1_cycles_by_match, coral_l2_cycles_by_match, coral_l3_cycles_by_match, coral_l4_cycles_by_match],
                x_axis_label="Match Index",
                y_axis_label=line_names_1,
                y_axis_title=f"# of Autonomous {'Cycles' if using_cycle_contributions else 'Points'}",
                title=f"Coral {'Cycles' if using_cycle_contributions else 'Points'} During Autonomous Over Time",
                color_map=dict(zip(line_names_1, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
            )
        )

        plotly_chart(
            multi_line_graph(
                range(len(algae_processor_cycles_by_match)),
                [algae_barge_cycles_by_match, algae_processor_cycles_by_match],
                x_axis_label="Match Index",
                y_axis_label=line_names_2,
                y_axis_title=f"# of Autonomous {'Cycles' if using_cycle_contributions else 'Points'}",
                title=f"Algae {'Cycles' if using_cycle_contributions else 'Points'} During Autonomous Over Time",
                color_map=dict(zip(line_names_2, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
            )
        )

    def generate_teleop_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType
    ) -> None:
        """Generates the teleop graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: The type of graph to use for the graphs on said page (cycle contribution / point contributions).
        :return:
        """
        coral_col, algae_col, climb_speed_col = st.columns(3)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        # Teleop coral over time graph
        with coral_col:
            coral_l1_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_CORAL_L1
            ) * (1 if using_cycle_contributions else 2)
            coral_l2_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_CORAL_L2
            ) * (1 if using_cycle_contributions else 3)
            coral_l3_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_CORAL_L3
            ) * (1 if using_cycle_contributions else 4)
            coral_l4_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_CORAL_L4
            ) * (1 if using_cycle_contributions else 5)
            line_names = [
                ("# of Coral L1 Cycles" if using_cycle_contributions else "# of Coral L1 Points"),
                ("# of Coral L2 Cycles" if using_cycle_contributions else "# of Coral L2 Points"),
                ("# of Coral L3 Cycles" if using_cycle_contributions else "# of Coral L3 Points"),
                ("# of Coral L4 Cycles" if using_cycle_contributions else "# of Coral L4 Points")
            ]

            plotly_chart(
                stacked_bar_graph(
                    range(len(coral_l1_cycles_by_match)),
                    [coral_l1_cycles_by_match, coral_l2_cycles_by_match, coral_l3_cycles_by_match, coral_l4_cycles_by_match],
                    x_axis_label="",
                    y_axis_label=line_names,
                    y_axis_title=f"# of Teleop {'Cycles' if using_cycle_contributions else 'Points'}",
                    title=f"Coral {'Cycles' if using_cycle_contributions else 'Points'} During Teleop Over Time",
                    color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
                )
            )

        # Teleop algae over time graph
        with algae_col:
            barge_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_BARGE
            ) * (1 if using_cycle_contributions else 4)
            processor_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_PROCESSOR
            ) * (1 if using_cycle_contributions else 6)

            line_names = [
                ("# of Algae Net Cycles" if using_cycle_contributions else "# of Algae Net Points"),
                ("# of Algae Processor Cycles" if using_cycle_contributions else "# of Algae Processor Points")
            ]

            plotly_chart(
                stacked_bar_graph(
                    range(len(barge_cycles_by_match)),
                    [barge_cycles_by_match, processor_cycles_by_match],
                    x_axis_label="",
                    y_axis_label=line_names,
                    y_axis_title=f"# of Teleop {'Cycles' if using_cycle_contributions else 'Points'}",
                    title=f"Algae {'Cycles' if using_cycle_contributions else 'Points'} During Teleop Over Time",
                    color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
                )
            )

        # Climb speed over time graph
        with climb_speed_col:
            slow_climbs = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMB_SPEED,
                {"Slow (>10 seconds)": 1}
            )
            average_climbs = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMB_SPEED,
                {"Average (5-10 seconds)": 1}
            )
            fast_climbs = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMB_SPEED,
                {"Fast (<5 seconds)": 1}
            )

            plotly_chart(
                bar_graph(
                    ["Slow Climbs", "Average Climbs", "Fast Climbs"],
                    [slow_climbs, average_climbs, fast_climbs],
                    x_axis_label="Type of Climb",
                    y_axis_label="# of Climbs",
                    title=f"Climb Speed Breakdown",
                    color={"Slow Climbs": GeneralConstants.LIGHT_RED, "Average Climbs": GeneralConstants.GOLD_GRADIENT[0], "Fast Climbs": GeneralConstants.LIGHT_GREEN},
                    color_indicator="Type of Climb"
                )
            )

    def generate_qualitative_graphs(self, team_number: int) -> None:
        """Generates the qualitative graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :return:
        """
        # Constants used for the sentiment analysis
        ml_weight = 1
        estimate_weight = 1

        sentiment = SentimentIntensityAnalyzer()
        positivity_scores = []
        scouting_data = scouting_data_for_team(team_number)

        # Split into two tabs
        qualitative_graphs_tab, note_scouting_analysis_tab = st.tabs(
            ["📊 Qualitative Graphs", "✏️ Note Scouting Analysis"]
        )

        with qualitative_graphs_tab:
            driver_rating_col, intake_defense_skill_col = st.columns(2)
            intake_speed_col, defense_skill_col = st.columns(2)

            with driver_rating_col:
                driver_rating_types = Criteria.DRIVER_RATING_CRITERIA.keys()
                driver_rating_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DRIVER_RATING, {driver_rating_type: 1})
                    for driver_rating_type in driver_rating_types
                ]

                plotly_chart(
                    bar_graph(
                        driver_rating_types,
                        driver_rating_by_type,
                        x_axis_label="Driver Rating",
                        y_axis_label="# of Occurrences",
                        title="Driver Rating Breakdown",
                        color=dict(zip(driver_rating_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Driver Rating"
                    )
                )

            with intake_defense_skill_col:
                intake_defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                intake_defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_DEFENSE_RATING, {intake_defense_skill_type: 1})
                    for intake_defense_skill_type in intake_defense_skill_types
                ]

                plotly_chart(
                    bar_graph(
                        intake_defense_skill_types,
                        intake_defense_skill_by_type,
                        x_axis_label="Counter Defense Skill",
                        y_axis_label="# of Occurrences",
                        title="Counter Defense Skill Breakdown",
                        color=dict(zip(intake_defense_skill_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Counter Defense Skill"
                    )
                )

            with defense_skill_col:
                defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DEFENSE_RATING, {defense_skill_type: 1})
                    for defense_skill_type in defense_skill_types
                ]

                plotly_chart(
                    bar_graph(
                        defense_skill_types,
                        defense_skill_by_type,
                        x_axis_label="Defense Skill",
                        y_axis_label="# of Occurrences",
                        title="Defense Skill Breakdown",
                        color=dict(zip(defense_skill_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Defense Skill"
                    )
                )

            with intake_speed_col:
                intake_speed_types = Criteria.INTAKE_SPEED_CRITERIA.keys()
                intake_speed_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_SPEED, {intake_speed_type: 1})
                    for intake_speed_type in intake_speed_types
                ]

                plotly_chart(
                    bar_graph(
                        intake_speed_types,
                        intake_speed_by_type,
                        x_axis_label="Intake Speed",
                        y_axis_label="# of Occurrences",
                        title="Intake Speed Breakdown",
                        color=dict(zip(intake_speed_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Intake Speed"
                    )
                )
        with note_scouting_analysis_tab:
            notes_col, metrics_col = st.columns(2, gap="medium")
            notes_by_match = dict(
                zip(
                    scouting_data[Queries.MATCH_KEY],
                    (
                            scouting_data[Queries.AUTO_NOTES].apply(lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.TELEOP_NOTES].apply(
                                lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.ENDGAME_NOTES].apply(
                                lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.RATING_NOTES].apply(lambda note: note.lower())

                    )
                )
            )

            with notes_col:
                st.write("##### Notes")
                st.markdown("<hr style='margin: 0px'/>",
                            unsafe_allow_html=True)  # Hacky way to create a divider without whitespace

                for match_key, notes in notes_by_match.items():
                    if notes.strip().replace("|", ""):
                        notes_col.write(f"###### {match_key}")

                        text_split_by_words = re.split(r"(\s+)", notes)
                        annotated_words = []
                        # Used to create a rough estimate of how positive the notes are. Positive terms have a weight of
                        # one, while negative terms have a weight of negative one and neutral terms have a weight of zero.
                        sentiment_scores = []

                        for word in text_split_by_words:
                            if not word.strip():
                                annotated_words.append(word)
                                continue

                            if any(term in word.lower() for term in GeneralConstants.POSITIVE_TERMS):
                                annotated_words.append((word, "", f"{GeneralConstants.LIGHT_GREEN}75"))
                                sentiment_scores.append(1)
                            elif any(term in word.lower() for term in GeneralConstants.NEGATIVE_TERMS):
                                annotated_words.append((word, "", f"{GeneralConstants.LIGHT_RED}75"))
                                sentiment_scores.append(-1)
                            else:
                                annotated_words.append(word)

                        # A score given to the notes given that generates a "sentiment score", using
                        # the English vocabulary to determine how positive a string of text is. The downside of this method
                        # is that it won't catch negative terms in the context of a robot's performance, which is why
                        # we weight it with our own estimate of the "sentiment" score.
                        ml_generated_score = sentiment.polarity_scores(notes)["compound"]
                        sentiment_estimate = sum(sentiment_scores) / (len(sentiment_scores) or 1)
                        positivity_scores.append(
                            (ml_generated_score * ml_weight + sentiment_estimate * estimate_weight) / 2
                        )

                        annotated_text(
                            *annotated_words
                        )
                        st.markdown("<hr style='margin: 0px'/>", unsafe_allow_html=True)

            with metrics_col:
                st.write("##### Metrics")

                colored_metric(
                    "Positivity Score of Notes",
                    round(sum(positivity_scores) / (len(positivity_scores) or 1), 2),
                    threshold=0
                )