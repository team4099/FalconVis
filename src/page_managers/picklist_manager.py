"""Creates the `PicklistManager` class used to set up the Picklist page and its table."""

from functools import partial

import streamlit as st
from pandas import DataFrame

from .page_manager import PageManager
from utils import CalculatedStats, Queries, retrieve_scouting_data, retrieve_team_list


class PicklistManager(PageManager):
    """The page manager for the `Picklist` page."""
    TRUNCATE_AT_DIGIT = 2  # Round the decimal to two places

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.teams = retrieve_team_list()

        # Requested stats is used to define the stats wanted in the picklist generation.
        self.requested_stats = {
            "Average Auto Cycles": partial(
                self.calculated_stats.average_cycles,
                mode=Queries.AUTO
            ),
            "Average Teleop Cycles": partial(
                self.calculated_stats.average_cycles,
                mode=Queries.TELEOP
            )
        }  # TODO: Add more stats here later

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Picklist` page.

        Creates a multiselect box to choose the different fields for the picklist table.

        :return: Returns a list containing the different fields chosen.
        """
        return st.multiselect(
            "Picklist Fields",
            self.requested_stats.keys(),
            default=list(self.requested_stats.keys())[0]
        )

    def generate_picklist(self, stats_requested: list[str]) -> DataFrame:
        """Generates the picklist containing the statistics requested and the team number.

        :param stats_requested: The name of the statistics requested (matches the keys in `self.requested_stats`
        """
        requested_picklist = [
            {
                "Team Number": f"FRC {team}"  # We make it a string because otherwise Notion won't recognize the value.
            } | {
                stat_name: round(self.requested_stats[stat_name](team), self.TRUNCATE_AT_DIGIT)
                for stat_name in stats_requested
            }
            for team in self.teams
        ]
        return DataFrame.from_dict(requested_picklist)
