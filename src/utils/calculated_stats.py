"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from statistics import mean
from typing import Callable

from numpy import percentile
from pandas import DataFrame, Series

from .constants import Queries
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
        return mean(
            self.points_contributed_by_match(team)
        )

    def points_contributed_by_match(self, team: int) -> list[int]:
        """Returns the points contributed by match for a team.

        :param team: The team number to calculate the points contributed over the matches they played.
        :return: A list containing the points contributed by said team per match.
        """
        team_data = scouting_data_for_team(team, self.data).to_dict(orient="records")
        points_contributed = []

        for submission in team_data:
            auto_points = sum([
                Queries.AUTO_GRID_POINTAGE[game_piece[1]]
                for game_piece in submission[Queries.AUTO_GRID].split("|")
                if game_piece
            ])
            auto_points += Queries.MOBILITY_CRITERIA[
                submission[Queries.LEFT_COMMUNITY]
            ] * 3
            auto_points += Queries.AUTO_CHARGE_POINTAGE.get(
                submission[Queries.AUTO_CHARGING_STATE],
                0
            )

            teleop_points = sum([
                Queries.TELEOP_GRID_POINTAGE[game_piece[1]]
                for game_piece in submission[Queries.TELEOP_GRID].split("|")
                if game_piece
            ])

            endgame_points = Queries.ENDGAME_POINTAGE.get(
                submission[Queries.ENDGAME_FINAL_CHARGE],
                0
            )

            points_contributed.append(auto_points + teleop_points + endgame_points)

        return points_contributed

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
    def average_stat(self, team: int, stat: str, criteria: dict) -> float:
        """Calculates the average statistic for a team (wrapper around `stat_per_match`).

        :param team: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: A criteria used to determine what the weightage of the statistic is.
        :return: A float representing the "average statistic".
        """
        return self.stat_per_match(team, stat, criteria).mean()

    def stat_per_match(self, team: int, stat: str, criteria: dict) -> Series:
        """Calculates a statistic over time as specified for a team.

        :param team: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: A criteria used to determine what the weightage of the statistic is.
        :return: A series representing the statistic for the team for each match.
        """
        team_data = scouting_data_for_team(team, self.data)
        return team_data[stat].apply(
            lambda datum: criteria[datum]
        )
