"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from typing import Callable

import numpy as np
from numpy import percentile
from pandas import DataFrame, Series

from .functions import retrieve_team_list


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