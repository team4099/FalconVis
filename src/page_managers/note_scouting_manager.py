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
        average_cycles_col, _ = st.columns(2)

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
