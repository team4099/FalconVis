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
        auto_speaker_points = team_data[Queries.AUTO_SPEAKER].apply(lambda cycle: cycle * 5)
        auto_amp_points = team_data[Queries.AUTO_AMP].apply(lambda cycle: cycle * 2)
        auto_leave_points = team_data[Queries.LEFT_STARTING_ZONE].apply(
            lambda left_starting_zone: Criteria.BOOLEAN_CRITERIA[left_starting_zone]
        )
        total_auto_points = auto_speaker_points + auto_amp_points + auto_leave_points

        # Teleop calculations
        teleop_speaker_points = team_data[Queries.TELEOP_SPEAKER].apply(lambda cycle: cycle * 2)
        teleop_amp_points = team_data[Queries.TELEOP_AMP]
        total_teleop_points = teleop_speaker_points + teleop_amp_points

        # Endgame (stage) calculations
        park_points = team_data[Queries.PARKED_UNDER_STAGE].apply(
            lambda parking_state: Criteria.BOOLEAN_CRITERIA[parking_state]
        )
        climb_points = team_data[Queries.CLIMBED_CHAIN].apply(
            lambda climbing_state: Criteria.BOOLEAN_CRITERIA[climbing_state] * 3
        )
        harmony_points = team_data[Queries.HARMONIZED_ON_CHAIN].apply(
            lambda harmonized: Criteria.BOOLEAN_CRITERIA[harmonized] * 2
        )
        trap_points = team_data[Queries.TELEOP_TRAP].apply(lambda cycle: cycle * 5)
        total_endgame_points = park_points + climb_points + harmony_points + trap_points

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

    # Cycle calculation methods
    @_convert_to_float_from_numpy_type
    def average_cycles(self, team_number: int, mode: str = None) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param mode: The mode to calculate said cycles for (Auto/Teleop)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        if mode is not None:
            return self.cycles_by_match(team_number, mode).mean()
        else:
            return (self.cycles_by_match(team_number, Queries.AUTO) + self.cycles_by_match(team_number, Queries.TELEOP)).mean()

    @_convert_to_float_from_numpy_type
    def average_passing_cycles(self, team_number) -> float:
        """Calculates the average passing cycles for a team

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :return: A float representing the average cycles for said team in the mode specified."""

        return self.cycles_by_match(team_number, Queries.TELEOP_PASSING).mean()

    @_convert_to_float_from_numpy_type
    def average_cycles_for_structure(self, team_number: int, structure: str) -> float:
        """Calculates the average cycles for a team for a structure (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param structure: The structure to return cycles for (AutoSpeaker/AutoAmp/TeleopSpeaker/TeleopAmp/TeleopTrap)
        :return: A float representing the average cycles for said team in the structure specified.
        """
        return self.cycles_by_structure_per_match(team_number, structure).mean()

    def average_potential_amplification_periods(self, team_number: int) -> float:
        """Returns the potential amplification periods a team is capable of by match.

        The following custom graphs are supported with this function:
        - Bar graph

        The amplification periods that a team is capable of is decided by their auto + teleop amp cycles divided by two
        :param team_number: The team to determine the potential amplification periods for.
        """
        return self.potential_amplification_periods_by_match(team_number).mean()

    def cycles_by_match(self, team_number: int, mode: str = None) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by match for.
        :param mode: The mode to return cycles by match for (Auto/Teleop)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        if mode == Queries.AUTO:
            return team_data[Queries.AUTO_SPEAKER] + team_data[Queries.AUTO_AMP]
        elif mode == Queries.TELEOP:
            return team_data[Queries.TELEOP_SPEAKER] + team_data[Queries.TELEOP_AMP] + team_data[Queries.TELEOP_TRAP]
        else:
            return (
                team_data[Queries.AUTO_SPEAKER] + team_data[Queries.AUTO_AMP]
                + team_data[Queries.TELEOP_SPEAKER] + team_data[Queries.TELEOP_AMP] + team_data[Queries.TELEOP_TRAP]
            )

    def passing_shots_by_match(self, team_number: int) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by match for.
        :param mode: The mode to return cycles by match for (Auto/Teleop)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        return team_data[Queries.TELEOP_PASSING]

    def cycles_by_structure_per_match(self, team_number: int, structure: str | tuple) -> Series:
        """Returns the cycles for a certain structure (auto speaker, auto amp, etc.) in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by height per match for.
        :param structure: The structure to return cycles for (AutoSpeaker/AutoAmp/TeleopSpeaker/TeleopAmp/TeleopTrap)
        :return: A series containing the cycles per match for the structure specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        if isinstance(structure, tuple):
            return reduce(lambda x, y: x + y, [team_data[struct] for struct in structure])
        else:
            return team_data[structure]

    def potential_amplification_periods_by_match(self, team_number: int) -> Series:
        """Returns the potential amplification periods a team is capable of by match.

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        The amplification periods that a team is capable of is decided by their auto + teleop amp cycles divided by two
        :param team_number: The team to determine the potential amplification periods for.
        """
        return self.cycles_by_structure_per_match(team_number, (Queries.AUTO_AMP, Queries.TELEOP_AMP)) // 2

    # Alliance-wide methods
    @_convert_to_float_from_numpy_type
    def average_coop_bonus_rate(self, team_number: int) -> float:
        """Returns the average rate (%) that the coopertition bonus is reached by an alliance (average method).
        (ignore)

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team to calculate the average coop bonus rate for.
        :return: A float representing the % rate of the alliance reaching the coopertition bonus.
        """
        return self.reaches_coop_bonus_by_match(team_number).astype(int).mean()

    def reaches_coop_bonus_by_match(self, team_number: int) -> Series:
        """Returns whether three teams within an alliance are able to reach the coopertition bonus within the first
        45 seconds of a match by match. (ignore)

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team to determine the coop bonus rate by match for.
        :return: Whether or not the alliance would reach the coopertition bonus requirement of one amp cycle in 45 sec.
        """
        auto_amp_sufficient = self.cycles_by_structure_per_match(
            team_number, Queries.AUTO_AMP
        ).apply(lambda total_auto_amp: total_auto_amp >= 1)
        teleop_amp_sufficient = (
            self.cycles_by_structure_per_match(team_number, Queries.TELEOP_AMP)
        ).apply(lambda total_teleop_amp: total_teleop_amp >= 1)

        return auto_amp_sufficient | teleop_amp_sufficient

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
    def average_feeding_cycles_without_full_field(self, team_number: int) -> float:
        """Returns the average feeding cycles without matches where they ran full field cycles."""
        team_scouting_data = scouting_data_for_team(team_number, self.data)
        passing_cycles = team_scouting_data[team_scouting_data[Queries.TELEOP_PASSING] != 0][Queries.TELEOP_PASSING]
        return (passing_cycles.mean()) if not passing_cycles.empty else 0

    @_convert_to_float_from_numpy_type
    def average_defense_rating(self, team_number: int) -> float:
        """Returns a series of data representing the team's defense rating

        :param team_number: The team to find defense data for.
        :return: A series with the teams defense data.
        """

        return scouting_data_for_team(team_number, self.data)[Queries.DRIVER_RATING].apply(
            lambda driver_rating: Criteria.BASIC_RATING_CRITERIA.get(driver_rating, float("nan"))
        )

    @_convert_to_float_from_numpy_type
    def average_defense_time(self, team_number: int) -> float:
        """Returns the average defense time of a team

        :param team_number: The team to determine the defense time for.
        :return: A float representing the average defense time of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DEFENSE_TIME].apply(
            lambda defense_time: Criteria.DEFENSE_TIME_CRITERIA.get(defense_time, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_defense_skill(self, team_number: int) -> float:
        """Returns the average defense skill of a team.

        :param team_number: The team to determine the defense skill for.
        :return: A float representing the average defense skill of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DEFENSE_SKILL].apply(
            lambda defense_skill: Criteria.BASIC_RATING_CRITERIA.get(defense_skill, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_counter_defense_skill(self, team_number: int) -> float:
        """Returns the average counter defense skill (ability to swerve past defense) of a team.

        :param team_number: The team to determine the counter defense skill for.
        :return: A float representing the average counter defense skill of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.COUNTER_DEFENSE_SKIll].apply(
            lambda counter_defense_skill: Criteria.BASIC_RATING_CRITERIA.get(counter_defense_skill, float("nan"))
        ).mean()
    
    def drivetrain_width_by_team(self, team_number: int) -> float:
        """Returns a float representing the teams drivetrain width

        :param team_number: The team to find disable data for.
        :return: A float with the team drivtrain width in inches
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
    def chance_of_coop_bonus(self, alliance: list[int]) -> float:
        """Determines the chance of the coop bonus using all possible permutations with an alliance.

        :param alliance: The three teams on the alliance.
        """
        coop_by_match = [self.reaches_coop_bonus_by_match(team) for team in alliance]
        possible_coop_combos = self.cartesian_product(*coop_by_match)
        return len([combo for combo in possible_coop_combos if any(combo)]) / len(possible_coop_combos)

    def chance_of_bonuses(self, alliance: list[int]) -> tuple[float, float, float]:
        """Determines the chance of the coopertition bonus, the melody bonus and the ensemble bonus using all possible permutations with an alliance.

        :param alliance: The three teams on the alliance.
        """
        chance_of_coop = self.chance_of_coop_bonus(alliance)
        cycles_for_alliance = [self.cycles_by_match(team) for team in alliance]

        # Melody RP calculations
        possible_cycle_combos = self.cartesian_product(*cycles_for_alliance, reduce_with_sum=True)
        chance_of_reaching_21_cycles = (
            len([combo for combo in possible_cycle_combos if combo >= 21]) / len(possible_cycle_combos)
        )
        chance_of_reaching_25_cycles = (
            len([combo for combo in possible_cycle_combos if combo >= 25]) / len(possible_cycle_combos)
        )

        # Ensemble RP calculations
        endgame_points_by_team = [self.points_contributed_by_match(team, Queries.ENDGAME) for team in alliance]
        possible_endgame_combos = self.cartesian_product(*endgame_points_by_team, reduce_with_sum=True)
        chance_of_reaching_10_points = (
            len([combo for combo in possible_endgame_combos if combo >= 10]) / len(possible_endgame_combos)
        )

        ability_to_climb_by_team = [True in self.stat_per_match(team, Queries.CLIMBED_CHAIN) for team in alliance]

        if ability_to_climb_by_team.count(True) >= 2:  # If teams can climb
            chance_of_ensemble_rp = chance_of_reaching_10_points
        else:
            chance_of_ensemble_rp = 0  # No chance that they can get the RP even if 10 points can be reached.

        return (
            chance_of_coop,
            chance_of_reaching_21_cycles * (1 - chance_of_coop) + chance_of_reaching_25_cycles * chance_of_coop,
            chance_of_ensemble_rp
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
