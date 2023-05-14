"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from typing import Callable

from numpy import percentile
from pandas import DataFrame, Series

from .constants import Criteria, Queries
from .functions import scouting_data_for_team, retrieve_team_list

__all__ = ["CalculatedStats"]


class CalculatedStats:
    """Utility class for calculating statistics in an event."""

    def __init__(self, data: DataFrame):
        self.data = data

    # Point contribution methods
    def average_points_contributed(self, team: int) -> float:
        """Returns the average points contributed by a team.

        :param team: The team number to calculate the average points contributed for.
        """
        return self.points_contributed_by_match(team).mean()

    def points_contributed_by_match(self, team: int) -> Series:
        """Returns the points contributed by match for a team.

        :param team: The team number to calculate the points contributed over the matches they played.
        :return: A Series containing the points contributed by said team per match.
        """
        team_data = scouting_data_for_team(team, self.data)

        auto_grid_points = team_data[Queries.AUTO_GRID].apply(
            lambda grid_data: sum([
                Criteria.AUTO_GRID_POINTAGE[game_piece[1]]
                for game_piece in grid_data.split("|")
                if game_piece
            ])
        )
        auto_mobility_points = team_data[Queries.LEFT_COMMUNITY].apply(
            lambda left_community: Criteria.MOBILITY_CRITERIA[left_community] * 3
        )

        teleop_grid_points = team_data[Queries.TELEOP_GRID].apply(
            lambda grid_data: sum([
                Criteria.TELEOP_GRID_POINTAGE[game_piece[1]]
                for game_piece in grid_data.split("|")
                if game_piece
            ])
        )

        endgame_points = team_data[Queries.ENDGAME_FINAL_CHARGE].apply(
            lambda charging_state: Criteria.ENDGAME_POINTAGE.get(charging_state, 0)
        )

        return auto_grid_points + auto_mobility_points + teleop_grid_points + endgame_points

    # Cycle calculation methods
    def average_cycles(self, team: int, type_of_grid: str) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        :param team: The team number to calculate the average cycles for.
        :param type_of_grid: The mode to calculate said cycles for (autonomous/teleop)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        return self.cycles_by_match(team, type_of_grid).mean()

    def cycles_by_match(self, team: int, type_of_grid: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match

        :param team: The team number to calculate the cycles by match for.
        :param type_of_grid: The mode to return cycles by match for (autonomous/teleop).
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team, self.data)
        return team_data[type_of_grid].apply(
            lambda grid_data: len(grid_data.split("|"))
        ).mean()

    # Accuracy methods
    def average_auto_accuracy(self, team_number: int) -> float:
        """Returns the average auto accuracy of a team (wrapper around `auto_accuracy_by_match`).

        :param team_number: The team to determine the average auto accuracy for.
        :return: A float representing a percentage of the average auto accuracy of said team.
        """
        return self.auto_accuracy_by_match(team_number).mean()

    def auto_accuracy_by_match(self, team_number: int) -> Series:
        """Returns the auto accuracy of a team by match.

        :param team_number: The team to determine the auto accuracy per match for.
        :return: A series containing the auto accuracy by match for said team.
        """
        auto_missed_by_match = self.stat_per_match(
            team_number,
            Queries.AUTO_MISSED
        )
        auto_cycles_by_match = self.cycles_by_match(
            team_number,
            Queries.AUTO_GRID
        ) + auto_missed_by_match  # Adding auto missed in order to get an accurate % (2 scored + 1 missed = 33%)
        return 1 - (auto_missed_by_match / auto_cycles_by_match)

    # Percentile methods
    def quantile_stat(self, quantile: float, predicate: Callable) -> float:
        """Calculates a scalar value for a percentile of a dataset.

        Used for comparisons between teams (eg passing in 0.5 will return the median).

        :param quantile: Quantile used to find the scalar value at.
        :param predicate: Predicate called per team in the scouting data to create the dataset (self and team number must be arguments).
        :return: A float representing the scalar value for a percentile of a dataset.
        """
        dataset = [predicate(self, team) for team in retrieve_team_list()]
        return percentile(dataset, quantile * 100)

    # General methods
    def average_stat(self, team: int, stat: str, criteria: dict | None = None) -> float:
        """Calculates the average statistic for a team (wrapper around `stat_per_match`).

        :param team: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional riteria used to determine what the weightage of the statistic is.
        :return: A float representing the "average statistic".
        """
        return self.stat_per_match(team, stat, criteria).mean()

    def cumulative_stat(self, team: int, stat: str, criteria: dict | None = None) -> int:
        """Calculates a cumulative stat for a team (wrapper around `stat_per_match`).

        :param team: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "cumulative statistic".
        """
        return self.stat_per_match(team, stat, criteria).sum()

    def stat_per_match(self, team: int, stat: str, criteria: dict | None = None) -> Series:
        """Calculates a statistic over time as specified for a team.

        :param team: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        :return: A series representing the statistic for the team for each match.
        """
        team_data = scouting_data_for_team(team, self.data)
        return team_data[stat].apply(
            lambda datum: criteria.get(datum, 0) if criteria is not None else datum
        )

    def calculate_iqr(self, dataset: Series) -> float:
        """Calculates the IQR of a dataset (75th percentile - 25th percentile).

        :param dataset: The dataset to calculate the IQR for.
        :return: A float representing the IQR.
        """
        return percentile(dataset, 75) - percentile(dataset, 25)