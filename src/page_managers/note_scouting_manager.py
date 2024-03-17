"""Creates the `PicklistManager` class used to set up the Picklist page and its table."""

import streamlit as st

from .page_manager import PageManager
from utils import (
    bar_graph,
    CalculatedQualitativeStats,
    Criteria,
    GeneralConstants,
    plotly_chart,
    Queries,
    retrieve_note_scouting_data,
    retrieve_team_list
)


class NoteScoutingManager(PageManager):
    """The manager for the Note Scouting page."""

    def __init__(self):
        self._data = retrieve_note_scouting_data()
        self.calculated_stats = CalculatedQualitativeStats(self._data)

    def generate_input_section(self) -> int:    
        """Creates the input section for the `Note Scouting` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list(self._data)),
            index=team_list.index(4099) if 4099 in team_list else 0
        )

    def generate_ratings(self, team_number: int) -> None:
        """Generates the Ratings page for the `Note Scouting` page."""

        amp_align_col, scoring_speed_col, intaking_speed_col = st.columns(3)

        with amp_align_col:
            amp_align_types = Criteria.AMP_ALIGNING_SPEED_CRITERIA.keys()
            amp_align_by_type = [
                self.calculated_stats.cumulative_stat(team_number, Queries.AMP_ALIGNING_SPEED, {amp_align_type: 1})
                for amp_align_type in amp_align_types
            ]

            plotly_chart(
                bar_graph(
                    amp_align_types,
                    amp_align_by_type,
                    x_axis_label="Amp Aligning Speed",
                    y_axis_label="# of Occurrences",
                    title="How fast are they at aligning on the amp?",
                    color=dict(zip(amp_align_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Amp Aligning Speed"
                )
            )

        with scoring_speed_col:
            scoring_speed_types = Criteria.SCORING_SPEED_CRITERIA.keys()
            scoring_speed_by_type = [
                self.calculated_stats.cumulative_stat(team_number, Queries.SCORING_SPEED, {scoring_speed_type: 1})
                for scoring_speed_type in scoring_speed_types
            ]

            plotly_chart(
                bar_graph(
                    scoring_speed_types,
                    scoring_speed_by_type,
                    x_axis_label="Scoring Speed",
                    y_axis_label="# of Occurrences",
                    title="How fast was their scoring mechanism?",
                    color=dict(zip(scoring_speed_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-2])),
                    color_indicator="Scoring Speed"
                )
            )

        with intaking_speed_col:
            intaking_speed_types = Criteria.INTAKING_SPEED_CRITERIA.keys()
            intaking_speed_by_type = [
                self.calculated_stats.cumulative_stat(
                    team_number,
                    Queries.INTAKING_SPEED,
                    {intaking_speed_type: 1}
                )
                for intaking_speed_type in intaking_speed_types
            ]

            plotly_chart(
                bar_graph(
                    intaking_speed_types,
                    intaking_speed_by_type,
                    x_axis_label="Intaking Speed",
                    y_axis_label="# of Occurrences",
                    title="How fast were they at intaking notes?",
                    color=dict(zip(intaking_speed_types, GeneralConstants.SHORT_RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Intaking Speed"
                )
            )
