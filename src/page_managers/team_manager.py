"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import streamlit as st

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import (
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    colored_metric_with_two_values,
    Criteria,
    GeneralConstants,
    GraphType,
    line_graph,
    plotly_chart,
    Queries,
    retrieve_team_list,
    retrieve_pit_scouting_data,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph
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
        return st.selectbox(
            "Team Number",
            retrieve_team_list()
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
            average_teleop_cycles = self.calculated_stats.average_cycles(
                team_number,
                Queries.TELEOP
            )
            teleop_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles(team, Queries.TELEOP)
            )
            colored_metric(
                "Average Teleop Cycles",
                round(average_teleop_cycles, 2),
                threshold=teleop_cycles_for_percentile
            )

        # TODO: the next 3 metrics are likely wrong
        # Metric for ability to score trap
        with trap_ability_col:
            trap_ability = self.calculated_stats.average_stat(
                team_number,
                Queries.TELEOP_TRAP,
                Criteria.BOOLEAN_CRITERIA
            )
            colored_metric(
                "Able To Score Trap",
                "Yes" if trap_ability > 0 else "No",
            )

        # Metric for total times climbed
        with times_climbed_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMBED_CHAIN,
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.CLIMBED_CHAIN)
            )
            colored_metric(
                "Times Climbed",
                times_climbed,
                threshold=times_climbed_for_percentile
            )

        # Metric for ability to harmonize
        with harmonize_ability_col:
            harmonize_ability = self.calculated_stats.average_stat(
                team_number,
                Queries.HARMONIZED_ON_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            colored_metric(
                "Able To Harmonize",
                "Yes" if harmonize_ability > 0 else "No"
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
        team_data = scouting_data_for_team(team_number)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        # TODO: Add autonomous graphs

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
        team_data = scouting_data_for_team(team_number)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        # TODO: Add teleop graphs
