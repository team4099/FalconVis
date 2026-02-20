"""File that contains the class which calculates statistics for a team/event/for other purposes."""
from __future__ import annotations

from functools import reduce
from typing import Callable

import numpy as np
from numpy import percentile
from pandas import DataFrame, Series, isna
from scipy.integrate import quad
from scipy.stats import norm


from .base_calculated_stats import BaseCalculatedStats
from .constants import Criteria, Queries
from .functions import _convert_to_float_from_numpy_type, scouting_data_for_team, retrieve_team_list, retrieve_pit_scouting_data

__all__ = ["CalculatedStats"]


class CalculatedStats(BaseCalculatedStats):
    """Utility class for calculating statistics in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # Point contribution methods
    @_convert_to_float_from_numpy_type
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
        :param mode: Optional argument defining which mode to return the total points for (Auto/Teleop)
        :return: A Series containing the points contributed by said team per match.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        # Autonomous calculations
        auto_singular_ball_points = team_data[Queries.AUTO_SINUGLAR_COUNT].apply(lambda cycle: cycle)
        auto_batch_points = (team_data[Queries.AUTO_BATCH_COUNT]*team_data[Queries.MAGAZINE_SIZE])
        auto_climb_points = Criteria.BOOLEAN_CRITERIA[team_data[Queries.AUTO_CLIMB]] *15

        total_auto_points = auto_singular_ball_points + auto_batch_points + auto_climb_points

        # Teleop calculations
        teleop_singular_ball_points = team_data[Queries.TELEOP_SINUGLAR_COUNT].apply(lambda cycle: cycle)
        teleop_batch_points = team_data[Queries.TELEOP_BATCH_COUNT].apply(lambda cycle: cycle)

        total_teleop_points = teleop_singular_ball_points + teleop_batch_points

        # Endgame (stage) calculations
        climb_points = team_data[Queries.TELEOP_CLIMB].apply(lambda cycle: cycle)
       
        total_endgame_points = climb_points

        if mode == Queries.AUTO:
            return total_auto_points
        elif mode == Queries.TELEOP:
            return total_teleop_points
        elif mode == Queries.ENDGAME:
            return total_endgame_points

        return (
            total_auto_points
            + total_teleop_points
            + total_endgame_points
        )

    # Rating methods
    @_convert_to_float_from_numpy_type
    def average_driver_rating(self, team_number: int) -> float:
        """Returns the average driver rating of a team.

        :param team_number: The team to determine the driver rating for.
        :return: A float representing the average driver rating of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DRIVER_RATING].apply(
            lambda driver_rating: Criteria.DRIVER_RATING_CRITERIA.get(driver_rating, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_intake_speed_rating(self, team_number: int) -> float:
        """Returns the average intake speed rating of a team.

        :param team_number: The team to determine the intake speed rating for.
        :return: A float representing the average intake speed rating of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.INTAKE_SPEED].apply(
            lambda intake_speed: Criteria.INTAKE_SPEED_CRITERIA.get(intake_speed, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_defense_rating(self, team_number: int) -> float:
        """Returns a series of data representing the team's defense rating

        :param team_number: The team to find defense data for.
        :return: A series with the teams defense data.
        """

        return scouting_data_for_team(team_number, self.data)[Queries.DEFENSE_RATING].apply(
            lambda defense_rating: Criteria.BASIC_RATING_CRITERIA.get(defense_rating, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_counter_defense_skill(self, team_number: int) -> float:
        """Returns the average counter defense skill (ability to swerve past defense) of a team.

        :param team_number: The team to determine the counter defense skill for.
        :return: A float representing the average counter defense skill of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.INTAKE_DEFENSE_RATING].apply(
            lambda counter_defense_skill: Criteria.BASIC_RATING_CRITERIA.get(counter_defense_skill, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
        def average_throughput_speed(self, team_number: int) -> float:
            """Returns the average throughput (fuel shot per second) of a team.

            :param team_number: The team to determine the throughput for.
            :return: A float representing the average throughput of said team.
            """
            return scouting_data_for_team(team_number, self.data)[Queries.THROUGHPUT_SPEED].apply(
                lambda throughput_speed: Criteria.BASIC_RATING_CRITERIA.get(throughput_speed, float("nan"))
            ).mean()

    @_convert_to_float_from_numpy_type
            def average_shooter_defense_skill(self, team_number: int) -> float:
                """Returns the average shooter defense skill (ability to shoot while being defended against) of a team.

                :param team_number: The team to determine the shooter defense skill for.
                :return: A float representing the average shooter defense skill of said team.
                """
                return scouting_data_for_team(team_number, self.data)[Queries.SHOOTER_DEFENSE_RATING].apply(
                    lambda shooter_defense_skill: Criteria.BASIC_RATING_CRITERIA.get(shooter_defense_skill, float("nan"))
                ).mean()
    
    def drivetrain_width_by_team(self, team_number: int) -> float:
        """Returns a float representing the teams drivetrain width

        :param team_number: The team to find disable data for.
        :return: A float with the team drivetrain width in inches
        """
        pit_scouting_data = retrieve_pit_scouting_data()
        return pit_scouting_data[
                            pit_scouting_data["Team Number"] == team_number
                        ].iloc[0]["Drivetrain Width"]

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
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[stat].apply(
            lambda datum: criteria.get(datum, 0) if criteria is not None else datum
        )

    def driving_index(self, team_number: int) -> float:
        """Determines how fast a team is based on multiplying their teleop cycles by their counter defense rating

        - Used for custom graphs with three teams.
        - Used for custom graphs with a full event.

        :param team_number: The team number to calculate a driving index for.
        """
        counter_defense_skill = self.average_counter_defense_skill(team_number)
        return (
            self.average_cycles(team_number, Queries.TELEOP)
            * 0 if isna(counter_defense_skill) else counter_defense_skill
        )

    # Methods for ranking simulation
    def chance_of_bonuses(self, alliance: list[int]) -> tuple[float, float, float]:
        """Determines the chance of the coopertition bonus, the auto bonus, coral bonus, and the barge bonus using all possible permutations with an alliance.

        :param alliance: The three teams on the alliance.
        """

        Points_by_Team = team_data[Queries.AUTO_SINUGLAR_COUNT].apply(lambda cycle: cycle)+ team_data[Queries.AUTO_BATCH_COUNT].apply(lambda cycle: cycle)+team_data[Queries.TELEOP_SINUGLAR_COUNT].apply(lambda cycle: cycle)+team_data[Queries.TELEOP_BATCH_COUNT].apply(lambda cycle: cycle)
        possible_points = self.cartesian_product(*Points_by_team, reduce_with_sum=True)
        chance_of_energized_rp = (
            len([combo for combo in possible_points if combo >= 100]) / len(possible_points)
        )
        chance_of_supercharged_rp = (
                    len([combo for combo in possible_points if combo >= 360]) / len(possible_points)
                )
        # Endgame RP calculations
        traversal_points_by_team =Criteria.BOOLEAN_CRITERIA[team_data[Queries.AUTO_CLIMB]] * 15 + Criteria.BOOLEAN_CRITERIA[team_data[Queries.TELEOP_CLIMB]]
        possible_traversal_combos = self.cartesian_product(*traversal_points_by_team, reduce_with_sum=True)
        chance_of_traversal_rp = (
            len([combo for combo in possible_traversal_combos if combo >= 50) / len(possible_traversal_combos)
        )
        return (
            chance_of_energized_rp,
            chance_of_supercharged_rp,
            chance_of_traversal_rp

        )
        
    def chance_of_winning(self, alliance_one: list[int], alliance_two: list[int]) -> tuple:
        """Returns the chance of winning between two alliances using integrals."""
        alliance_one_points = [
            self.points_contributed_by_match(team)
            for team in alliance_one
        ]
        alliance_two_points = [
            self.points_contributed_by_match(team)
            for team in alliance_two
        ]

        # Calculate mean and standard deviation of the point distribution of the red alliance.
        alliance_one_std = (
                sum(
                    [
                        np.std(team_distribution) ** 2
                        for team_distribution in alliance_one_points
                    ]
                )
                ** 0.5
        )
        alliance_one_mean = sum(
            [
                np.mean(team_distribution)
                for team_distribution in alliance_one_points
            ]
        )

        # Calculate mean and standard deviation of the point distribution of the blue alliance.
        alliance_two_std = (
                sum(
                    [
                        np.std(team_distribution) ** 2
                        for team_distribution in alliance_two_points
                    ]
                )
                ** 0.5
        )
        alliance_two_mean = sum(
            [
                np.mean(team_distribution)
                for team_distribution in alliance_two_points
            ]
        )

        # Calculate mean and standard deviation of the point distribution of red alliance - blue alliance
        compared_std = (alliance_one_std ** 2 + alliance_two_std ** 2) ** 0.5
        compared_mean = alliance_one_mean - alliance_two_mean

        # Use sentinel value if there isn't enough of a distribution yet to determine standard deviation.
        if not compared_std and compared_mean:
            compared_std = abs(compared_mean)
        elif not compared_std:
            compared_std = 0.5

        compared_distribution = norm(loc=compared_mean, scale=compared_std)

        # Calculate odds of red/blue winning using integrals.
        odds_of_red_winning = quad(
            lambda x: compared_distribution.pdf(x), 0, np.inf
        )[0]
        odds_of_blue_winning = quad(
            lambda x: compared_distribution.pdf(x), -np.inf, 0
        )[0]

        return odds_of_red_winning, odds_of_blue_winning, alliance_one_mean, alliance_two_mean
