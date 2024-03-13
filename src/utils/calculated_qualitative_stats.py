"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from pandas import DataFrame

from .base_calculated_stats import BaseCalculatedStats

__all__ = ["CalculatedQualitativeStats"]


class CalculatedQualitativeStats(BaseCalculatedStats):
    """Utility class for calculating qualitative statistics derived from note scouting in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)
