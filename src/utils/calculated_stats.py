"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from pandas import DataFrame, Series

from .base_calculated_stats import BaseCalculatedStats
from .constants import Criteria, Queries
from .functions import scouting_data_for_team

__all__ = ["CalculatedStats"]


class CalculatedStats(BaseCalculatedStats):
    """Utility class for calculating statistics in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # Point contribution methods
    def average_points_contributed(self, team_number: int) -> float:
        """Returns the average points contributed by a team.

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average points contributed for.
        """
        return self.points_contributed_by_match(team_number).mean()

    def points_contributed_by_match(self, team_number: int, mode: str = "") -> Series:
        """Returns the points contributed by match for a team.

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the points contributed over the matches they played.
        :param mode: The mode for average points contributed (auto/teleop).
        :return: A Series containing the points contributed by said team per match.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        auto_points = (
            team_data[Queries.AUTO_UPPER_HUB] * 4
            + team_data[Queries.AUTO_LOWER_HUB] * 2
            + team_data[Queries.TAXIED] * 2
        )
        teleop_points = (
            team_data[Queries.TELEOP_UPPER_HUB] * 2
            + team_data[Queries.TELEOP_LOWER_HUB]
        )
        endgame_points = Criteria.ENDGAME_POINTAGE[team_data[Queries.FINAL_CLIMB_TYPE]]

        if mode == Queries.AUTO:
            return auto_points
        elif mode == Queries.TELEOP:
            return teleop_points

        return (
            auto_points
            + teleop_points
            + endgame_points
        )

    # Cycle calculation methods
    def average_cycles(self, team_number: int, mode: str) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param mode: The mode to calculate said cycles for (autonomous/teleop)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        return self.cycles_by_match(team_number, mode).mean()

    def average_cycles_for_height(self, team_number: int, mode: str, height: str) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param mode: The mode to calculate said cycles for (auto/teleop)
        :param height: The height to return cycles by match for (H/M/L)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        return self.cycles_by_height_per_match(team_number, mode, height).mean()

    def cycles_by_match(self, team_number: int, mode: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by match for.
        :param mode: The mode to return cycles by match for (auto/teleop)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        if mode == Queries.AUTO:
            return team_data[Queries.AUTO_UPPER_HUB] + team_data[Queries.AUTO_LOWER_HUB]
        else:
            return team_data[Queries.TELEOP_UPPER_HUB] + team_data[Queries.TELEOP_LOWER_HUB]

    def cycles_by_height_per_match(self, team_number: int, mode: str, height: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) and height in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by height per match for.
        :param mode: The mode to return cycles by match for (auto/teleop)
        :param height: The height to return cycles by match for (Upper/lower hub)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        if mode == Queries.AUTO:
            height_to_query = {
                Queries.UPPER_HUB: Queries.AUTO_UPPER_HUB,
                Queries.LOWER_HUB: Queries.AUTO_LOWER_HUB
            }
            return team_data[height_to_query[height]]
        else:
            height_to_query = {
                Queries.UPPER_HUB: Queries.TELEOP_UPPER_HUB,
                Queries.LOWER_HUB: Queries.TELEOP_LOWER_HUB
            }
            return team_data[height_to_query[height]]

    def climb_type_occurrences(self, team_number: int) -> list:
        """Returns the different occurrences of each climb type (Low/Mid/High/Traversal) for a team."""
        team_data = scouting_data_for_team(team_number, self.data)
        return [len(team_data[team_data[Queries.FINAL_CLIMB_TYPE] == climb_type]) for climb_type in Queries.CLIMB_TYPES]

