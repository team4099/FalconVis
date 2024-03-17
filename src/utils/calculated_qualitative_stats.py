"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from pandas import DataFrame, Series

from .base_calculated_stats import BaseCalculatedStats
from .functions import _convert_to_float_from_numpy_type, note_scouting_data_for_team

__all__ = ["CalculatedQualitativeStats"]


class CalculatedQualitativeStats(BaseCalculatedStats):
    """Utility class for calculating qualitative statistics derived from note scouting in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # General methods
    @_convert_to_float_from_numpy_type
    def average_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> float:
        """Calculates the average statistic for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "average statistic".
        """
        return self.stat_per_match(team_number, stat, criteria).mean()

    @_convert_to_float_from_numpy_type
    def cumulative_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> int:
        """Calculates a cumulative stat for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "cumulative statistic".
        """
        return self.stat_per_match(team_number, stat, criteria).sum()

    def stat_per_match(self, team_number: int, stat: str, criteria: dict | None = None) -> Series:
        """Calculates a statistic over time as specified for a team.

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A series representing the statistic for the team for each match.
        """
        team_data = note_scouting_data_for_team(team_number, self.data)
        return team_data[stat].apply(
            lambda datum: criteria.get(datum, 0) if criteria is not None else datum
        )
