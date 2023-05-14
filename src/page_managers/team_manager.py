"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import streamlit as st

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import CalculatedStats, Queries, retrieve_team_list, retrieve_scouting_data


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        return st.selectbox(
            "Team Number",
            retrieve_team_list()
        )

    def generate_metrics(self, team_number: int, quartile: float) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        :param quartile: The quartile to use per-metric for comparisons between a team and the xth-percentile.
        """
        points_contributed_col, auto_cycle_col, teleop_cycle_col, mobility_col = st.columns(4)

        # Metric for avg. points contributed
        with points_contributed_col:
            average_points_contributed = self.calculated_stats.average_points_contributed(
                team_number
            )
            points_contributed_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_points_contributed(team)
            )
            st.metric(
                "Average Points Contributed",
                round(average_points_contributed, 2),
                round(average_points_contributed - points_contributed_for_percentile, 2)
            )

        # Metric for average auto cycles
        with auto_cycle_col:
            average_auto_cycles = self.calculated_stats.average_cycles(
                team_number,
                Queries.AUTO_GRID
            )
            auto_cycles_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_cycles(team, Queries.AUTO_GRID)
            )
            st.metric(
                "Average Auto Cycles",
                round(average_auto_cycles, 2),
                round(average_auto_cycles - auto_cycles_for_percentile, 2)
            )

        # Metric for average teleop cycles
        with teleop_cycle_col:
            average_teleop_cycles = self.calculated_stats.average_cycles(
                team_number,
                Queries.TELEOP_GRID
            )
            teleop_cycles_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_cycles(team, Queries.TELEOP_GRID)
            )
            st.metric(
                "Average Teleop Cycles",
                round(average_teleop_cycles, 2),
                round(average_teleop_cycles - teleop_cycles_for_percentile, 2)
            )

        # Metric for avg. mobility (%)
        with mobility_col:
            average_mobility = self.calculated_stats.average_stat(
                team_number,
                Queries.LEFT_COMMUNITY,
                Queries.MOBILITY_CRITERIA
            )
            mobility_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_stat(
                    team,
                    Queries.LEFT_COMMUNITY,
                    Queries.MOBILITY_CRITERIA
                )
            )

            st.metric(
                "Average Mobility (%)",
                f"{round(average_mobility, 2):.1%}",
                f"{round(average_mobility - mobility_for_percentile, 2):.1%}"
            )
