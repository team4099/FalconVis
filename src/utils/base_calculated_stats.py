"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from typing import Callable

import numpy as np
from numpy import percentile
from pandas import DataFrame, Series

from .functions import scouting_data_for_team, retrieve_team_list


class BaseCalculatedStats:
    """Base class defining methods that are used across both quantitative and qualitative calculated stats implementations."""

    def __init__(self, data: DataFrame):
        self.data = data

    # Percentile methods
    def quantile_stat(self, quantile: float, predicate: Callable) -> float:
        """Calculates a scalar value for a percentile of a dataset.

        Used for comparisons between teams (eg passing in 0.5 will return the median).

        :param quantile: Quantile used to find the scalar value at.
        :param predicate: Predicate called per team in the scouting data to create the dataset (self and team number must be arguments).
        :return: A float representing the scalar value for a percentile of a dataset.
        """
        dataset = [predicate(self, team) for team in retrieve_team_list(self.data)]
        return percentile(dataset, quantile * 100)

    # General methods
    def average_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> float:
        """Calculates the average statistic for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "average statistic".
        """
        return self.stat_per_match(team_number, stat, criteria).mean()

    def cumulative_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> int:
        """Calculates a cumulative stat for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "cumulative statistic".
        """
        return self.stat_per_match(team_number, stat, criteria).sum()

    def matches_played(self, team_number: int) -> int:
        """Returns the number of matches a team played."""
        return len(scouting_data_for_team(team_number, self.data))

    def stat_per_match(self, team_number: int, stat: str, criteria: dict | None = None) -> Series:
        """Calculates a statistic over time as specified for a team.

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A series representing the statistic for the team for each match.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[stat].apply(
            lambda datum: criteria.get(datum, 0) if criteria is not None else datum
        )

    def calculate_iqr(self, dataset: Series) -> float:
        """Calculates the IQR of a dataset (75th percentile - 25th percentile).

        :param dataset: The dataset to calculate the IQR for.
        :return: A float representing the IQR.
        """
        return percentile(dataset, 75) - percentile(dataset, 25)

    def cartesian_product(
            self,
            dataset_x: list,
            dataset_y: list,
            dataset_z: list,
            reduce_with_sum: bool = False
    ) -> np.ndarray:
        """Creates a cartesian product (permutations of each element in the three datasets).

        :param dataset_x: A dataset containing x values.
        :param dataset_y: A dataset containing y values.
        :param dataset_z: A dataset containing z values.
        :param reduce_with_sum: Whether or not to add up the cartesian product for each tuple yielded.
        :return: A list containing the cartesian products or the sum of it if `reduce_with_sum` is True.
        """
        return np.array([
            (x + y + z if reduce_with_sum else (x, y, z))
            for x in dataset_x for y in dataset_y for z in dataset_z
        ])
