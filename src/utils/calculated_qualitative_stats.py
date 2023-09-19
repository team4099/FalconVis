"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from typing import Callable
from pandas import DataFrame, Series

from .base_calculated_stats import BaseCalculatedStats
from .functions import scouting_data_for_team, retrieve_team_list

__all__ = ["CalculatedQualitativeStats"]


class CalculatedQualitativeStats(BaseCalculatedStats):
    """Utility class for calculating qualitative statistics derived from note scouting in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # General methods
    def cycles_by_match(self, team_number: int, type_of_grid: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match.

        :param team_number: The team number to calculate the cycles by match for.
        :param type_of_grid: The mode to return cycles by match for (AutoGrid/TeleopGrid)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[type_of_grid]

    # Average-calculating methods
    def average_cycles(self, team_number: int, type_of_grid: str) -> float:
        """Returns the average cycles for a certain mode (autonomous/teleop) in a match.

        :param team_number: The team number to calculate the cycles by match for.
        :param type_of_grid: The mode to return cycles by match for (AutoGrid/TeleopGrid)
        :return: A float representing the average cycles put up per match.
        """
        return self.cycles_by_match(team_number, type_of_grid).mean()
