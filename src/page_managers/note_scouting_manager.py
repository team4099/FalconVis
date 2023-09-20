"""Creates the `NoteScoutingManager` class used to set up the Note Scouting page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils import (
    bar_graph,
    box_plot,
    CalculatedQualitativeStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    GraphType,
    line_graph,
    plotly_chart,
    NoteScoutingQueries,
    retrieve_team_list,
    retrieve_pit_scouting_data,
    retrieve_note_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph
)


class NoteScoutingManager(PageManager):
    """The page manager for the `Note Scouting` page."""

    def __init__(self):
        self.calculated_stats = CalculatedQualitativeStats(
            retrieve_note_scouting_data()
        )

    def generate_team_input_section(self) -> int:
        """Retrieves the list of teams from the note scouting data and lets the user select a team.

        :return: A team number representing the selected team.
        """
        return st.selectbox(
            "Team Number",
            retrieve_team_list(from_note_scouting_data=True)
        )

    def generate_team_autonomous_graphs(self, team_number: int) -> None:
        """Generates the autonomous graphs based on the team selected surrounding the note scouting data.

        :param team_number: The team number selected to generate the graphs for.
        """
        average_cycles_col, times_engaged_col = st.columns(2)
        intaking_accuracy_col, obstacle_avoidance_col = st.columns(2)

        # Metric containing the average autonomous cycles
        with average_cycles_col:
            average_cycles = self.calculated_stats.average_cycles(
                team_number,
                NoteScoutingQueries.AUTO_GRID
            )
            average_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles(team, NoteScoutingQueries.AUTO_GRID)
            )

            colored_metric(
                "Average Auto Cycles",
                round(average_cycles, 2),
                threshold=average_cycles_for_percentile
            )

        # Metric containing the total number of times a team engaged.
        with times_engaged_col:
            times_engaged = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_ENGAGED,
                Criteria.BOOLEAN_CRITERIA
            )
            times_engaged_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_ENGAGED,
                    Criteria.BOOLEAN_CRITERIA
                )
            )

            colored_metric(
                "# of Times Engaged",
                times_engaged,
                threshold=times_engaged_for_percentile
            )

        # Metric containing the accuracy of the robot when it comes to intaking.
        with intaking_accuracy_col:
            auto_intaking_accuracy = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_INTAKE_ACCURACY,
                Criteria.BOOLEAN_CRITERIA
            ) / (self.calculated_stats.matches_played(team_number) or 1)

            auto_intaking_accuracy_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_INTAKE_ACCURACY,
                    Criteria.BOOLEAN_CRITERIA
                ) / (self.matches_played(team_number) or 1)
            )

            colored_metric(
                "Intaking Accuracy (%)",
                auto_intaking_accuracy,
                threshold=auto_intaking_accuracy_for_percentile,
                value_formatter=lambda value: f"{value:.1%}"
            )

        # Metric displaying the obstacle avoidance skills of the robot during autonomous.
        with obstacle_avoidance_col:
            average_obstacle_avoidance = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_DRIVING_SKILLS,
                Criteria.BOOLEAN_CRITERIA
            ) / (self.calculated_stats.matches_played(team_number) or 1) * 5
            average_obstacle_avoidance_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_DRIVING_SKILLS,
                    Criteria.BOOLEAN_CRITERIA
                ) / (self.matches_played(team_number) or 1) * 5
            )

            colored_metric(
                "Obstacle Avoidance Rating (1-5)",
                round(average_obstacle_avoidance, 1),
                threshold=average_obstacle_avoidance_for_percentile
            )