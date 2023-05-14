"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import plotly.express as px
import streamlit as st

from .contains_graphs import ContainsGraphs
from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    create_df,
    Criteria,
    GeneralConstants,
    Queries,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team
)


class TeamManager(PageManager, ContainsGraphs, ContainsMetrics):
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
        iqr_col, auto_engage_col, auto_engage_accuracy_col, auto_accuracy_col = st.columns(4)

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
                f"{round(average_points_contributed - points_contributed_for_percentile, 2)} pts"
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
                f"{round(average_auto_cycles - auto_cycles_for_percentile, 2)} cycles"
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
                f"{round(average_teleop_cycles - teleop_cycles_for_percentile, 2)} cycles"
            )

        # Metric for avg. mobility (%)
        with mobility_col:
            average_mobility = self.calculated_stats.average_stat(
                team_number,
                Queries.LEFT_COMMUNITY,
                Criteria.MOBILITY_CRITERIA
            )
            mobility_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_stat(
                    team,
                    Queries.LEFT_COMMUNITY,
                    Criteria.MOBILITY_CRITERIA
                )
            )

            st.metric(
                "Average Mobility (%)",
                f"{round(average_mobility, 2):.1%}",
                f"{round(average_mobility - mobility_for_percentile, 2):.1%}"
            )

        # Metric for IQR of points contributed (consistency)
        with iqr_col:
            team_dataset = self.calculated_stats.points_contributed_by_match(
                team_number
            )
            iqr_of_points_contributed = self.calculated_stats.calculate_iqr(team_dataset)
            iqr_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.calculate_iqr(
                    self.points_contributed_by_match(team)
                )
            )

            st.metric(
                "IQR of Points Contributed (Consistency)",
                iqr_of_points_contributed,
                f"{round(iqr_of_points_contributed - iqr_for_percentile, 2)} pts",
                delta_color="inverse"
            )

        # Metric for total auto engage attempts
        with auto_engage_col:
            total_auto_engage_attempts = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.AUTO_ENGAGE_ATTEMPTED,
                Criteria.AUTO_ATTEMPT_CRITERIA
            )
            auto_engage_attempts_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.cumulative_stat(
                    team,
                    Queries.AUTO_ENGAGE_ATTEMPTED,
                    Criteria.AUTO_ATTEMPT_CRITERIA
                )
            )

            st.metric(
                "Auto Engage Attempts",
                total_auto_engage_attempts,
                f"{round(total_auto_engage_attempts - auto_engage_attempts_for_percentile, 2)} attempts"
            )

        # Metric for auto engage accuracy
        with auto_engage_accuracy_col:
            total_successful_engages = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.AUTO_CHARGING_STATE,
                Criteria.SUCCESSFUL_ENGAGE_CRITERIA
            )
            auto_engage_accuracy = (
                total_successful_engages / total_auto_engage_attempts
                if total_auto_engage_attempts
                else None
            )

            st.metric(
                "Auto Engage Accuracy",
                (
                    f"{auto_engage_accuracy:.1%}"
                    if auto_engage_accuracy is not None
                    else auto_engage_accuracy
                )
            )

        # Metric for average auto accuracy by match
        with auto_accuracy_col:
            average_auto_accuracy = self.calculated_stats.average_auto_accuracy(team_number)
            auto_accuracy_for_percentile = self.calculated_stats.quantile_stat(
                quartile,
                lambda self, team: self.average_auto_accuracy(team)
            )

            st.metric(
                "Average Auto Accuracy (%)",
                f"{average_auto_accuracy:.1%}",
                f"{round(average_auto_accuracy - auto_accuracy_for_percentile, 2):.1%}"
            )

    def generate_graphs(self, team_number: int) -> None:
        """Generates the graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :return:
        """
        team_data = scouting_data_for_team(team_number)

        # Autonomous graphs
        with st.container():
            st.write("#### Autonomous Graphs")

            auto_cycles_over_time_col, _ = st.columns(2)

            # Grpah for auto cycles over time
            with auto_cycles_over_time_col:
                auto_cycles_over_time = self.calculated_stats.cycles_by_match(team_number, Queries.AUTO_GRID)
                auto_cycles_df = create_df(
                    team_data[Queries.MATCH_KEY],
                    auto_cycles_over_time,
                    x_axis_label="Match Key",
                    y_axis_label="# of Auto Cycles"
                )

                st.plotly_chart(
                    px.line(
                        auto_cycles_df,
                        x="Match Key",
                        y="# of Auto Cycles",
                        title="Auto Cycles Over Time"
                    ).update_traces(
                        line_color=GeneralConstants.PRIMARY_COLOR
                    )
                )

        # Teleop + endgame graphs
        with st.container():
            st.write("#### Teleop + Endgame Graphs")

            teleop_cycles_over_time_col, _ = st.columns(2)

            # Graph for teleop cycles over time
            with teleop_cycles_over_time_col:
                teleop_cycles_over_time = self.calculated_stats.cycles_by_match(team_number, Queries.TELEOP_GRID)
                teleop_cycles_df = create_df(
                    team_data[Queries.MATCH_KEY],
                    teleop_cycles_over_time,
                    x_axis_label="Match Key",
                    y_axis_label="# of Teleop Cycles"
                )

                st.plotly_chart(
                    px.line(
                        teleop_cycles_df,
                        x="Match Key",
                        y="# of Teleop Cycles",
                        title="Teleop Cycles Over Time"
                    ).update_traces(
                        line_color=GeneralConstants.PRIMARY_COLOR
                    )
                )
