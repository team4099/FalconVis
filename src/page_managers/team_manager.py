"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import streamlit as st

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
        self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        queried_team = int(st.experimental_get_query_params().get("team_number", [0])[0])
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(queried_team) if queried_team in team_list else 0
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        points_contributed_col, drivetrain_col, auto_cycle_col, teleop_cycle_col = st.columns(4)
        iqr_col, trap_ability_col, times_climbed_col, harmonize_ability_col = st.columns(4)

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

        # Metric for drivetrain
        with drivetrain_col:
            try:
                drivetrain = self.pit_scouting_data[
                    self.pit_scouting_data["Team Number"] == team_number
                ].iloc[0]["Drivetrain"].split("/")[0]  # The splitting at / is used to shorten the drivetrain type.
            except (IndexError, TypeError):
                drivetrain = "—"

            colored_metric(
                "Drivetrain Type",
                drivetrain,
                background_color="#052e16",
                opacity=0.5
            )

        # Metric for average auto cycles
        with auto_cycle_col:
            average_auto_speaker_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_SPEAKER
            )
            average_auto_amp_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_AMP
            )
            average_auto_speaker_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_SPEAKER)
            )
            average_auto_amp_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_AMP)
            )

            colored_metric_with_two_values(
                "Average Auto Cycles",
                "Speaker / Amp",
                round(average_auto_speaker_cycles, 2),
                round(average_auto_amp_cycles, 2),
                first_threshold=average_auto_speaker_cycles_for_percentile,
                second_threshold=average_auto_amp_cycles_for_percentile
            )

        # Metric for average teleop cycles
        with teleop_cycle_col:
            average_teleop_speaker_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_SPEAKER
            )
            average_teleop_amp_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_AMP
            )
            average_teleop_speaker_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_SPEAKER)
            )
            average_teleop_amp_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_AMP)
            )

            colored_metric_with_two_values(
                "Average Teleop Cycles",
                "Speaker / Amp",
                round(average_teleop_speaker_cycles, 2),
                round(average_teleop_amp_cycles, 2),
                first_threshold=average_teleop_speaker_cycles_for_percentile,
                second_threshold=average_teleop_amp_cycles_for_percentile
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

        # Metric for ability to score trap
        with trap_ability_col:
            average_trap_cycles = self.calculated_stats.average_stat(
                team_number,
                Queries.TELEOP_TRAP,
                Criteria.BOOLEAN_CRITERIA
            )
            colored_metric(
                "Can they score in the trap?",
                average_trap_cycles,
                threshold=0.01,
                value_formatter=lambda value: "Yes" if value > 0 else "No"
            )

        # Metric for total times climbed
        with times_climbed_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMBED_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.CLIMBED_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )
            colored_metric(
                "# of Times Climbed",
                times_climbed,
                threshold=times_climbed_for_percentile
            )

        # Metric for ability to harmonize
        with harmonize_ability_col:
            times_harmonized = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.HARMONIZED_ON_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_harmonized_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.HARMONIZED_ON_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Times Harmonized",
                times_harmonized,
                threshold=times_harmonized_for_percentile
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
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

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

        # Auto Speaker/amp over time graph
        speaker_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_SPEAKER
        ) * (1 if using_cycle_contributions else 5)
        amp_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_AMP
        ) * (1 if using_cycle_contributions else 2)
        line_names = [
            ("# of Speaker Cycles" if using_cycle_contributions else "# of Speaker Points"),
            ("# of Amp Cycles" if using_cycle_contributions else "# of Amp Points")
        ]

        plotly_chart(
            multi_line_graph(
                range(len(speaker_cycles_by_match)),
                [speaker_cycles_by_match, amp_cycles_by_match],
                x_axis_label="Match Index",
                y_axis_label=line_names,
                y_axis_title=f"# of Autonomous {'Cycles' if using_cycle_contributions else 'Points'}",
                title=f"Speaker/Amp {'Cycles' if using_cycle_contributions else 'Points'} During Autonomous Over Time",
                color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
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
        times_climbed_col, times_harmonized_col = st.columns(2)
        speaker_amp_col, climb_speed_col = st.columns(2)


        team_data = scouting_data_for_team(team_number)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        # Teleop Speaker/amp over time graph
        with speaker_amp_col:
            speaker_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_SPEAKER
            ) * (1 if using_cycle_contributions else 5)
            amp_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_AMP
            ) * (1 if using_cycle_contributions else 2)
            line_names = [
                ("# of Speaker Cycles" if using_cycle_contributions else "# of Speaker Points"),
                ("# of Amp Cycles" if using_cycle_contributions else "# of Amp Points")
            ]

            plotly_chart(
                multi_line_graph(
                    range(len(speaker_cycles_by_match)),
                    [speaker_cycles_by_match, amp_cycles_by_match],
                    x_axis_label="Match Index",
                    y_axis_label=line_names,
                    y_axis_title=f"# of Teleop {'Cycles' if using_cycle_contributions else 'Points'}",
                    title=f"Speaker/Amp {'Cycles' if using_cycle_contributions else 'Points'} During Teleop Over Time",
                    color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
                )
            )

        # Metric for times climbed
        with times_climbed_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMBED_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.CLIMBED_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Times Climbed",
                times_climbed,
                threshold=times_climbed_for_percentile
            )

        # Metric for harmonized
        with times_harmonized_col:
            times_harmonized = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.HARMONIZED_ON_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_harmonized_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.HARMONIZED_ON_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Times Harmonized",
                times_harmonized,
                threshold=times_harmonized_for_percentile
            )

        # Climb speed over time graph
        with climb_speed_col:
            climb_speed_by_match = self.calculated_stats.stat_per_match(
                team_number,
                Queries.CLIMB_SPEED
            )

            plotly_chart(
                line_graph(
                    range(len(climb_speed_by_match)),
                    climb_speed_by_match,
                    x_axis_label="Match Index",
                    y_axis_label="Climb Speed",
                    title=f"Climb Speed Over Time",
                )
            )

    def generate_qualitative_graphs(
            self,
            team_number: int,
    ) -> None:
        """Generates the teleop graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :return:
        """
        driver_rating_col, defense_skill_col, disables_col = st.columns(3)

        with driver_rating_col:
            driver_rating_by_match = self.calculated_stats.stat_per_match(team_number, Queries.DRIVER_RATING)

            plotly_chart(
                line_graph(
                    range(len(driver_rating_by_match)),
                    driver_rating_by_match,
                    x_axis_label="Match Key",
                    y_axis_label="Driver Rating (1-5)",
                    title="Driver Rating Over Time",
                )
            )

        with defense_skill_col:
            defense_skill_by_match = self.calculated_stats.stat_per_match(team_number, Queries.DEFENSE_SKILL)

            plotly_chart(
                line_graph(
                    range(len(defense_skill_by_match)),
                    defense_skill_by_match,
                    x_axis_label="Match Key",
                    y_axis_label="Defense Skill (1-5)",
                    title="Defense Skill Over Time",
                )
            )

        with disables_col:
            disables_by_match = self.calculated_stats.stat_per_match(team_number, Queries.DISABLE)

            plotly_chart(
                line_graph(
                    range(len(disables_by_match)),
                    disables_by_match,
                    x_axis_label="Match Key",
                    y_axis_label="Disables",
                    title="Disables by Match",
                )
            )