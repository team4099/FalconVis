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
        auto_coral_l1_points = team_data[Queries.AUTO_CORAL_L1].apply(lambda cycle: cycle * 3)
        auto_coral_l2_points = team_data[Queries.AUTO_CORAL_L2].apply(lambda cycle: cycle * 4)
        auto_coral_l3_points = team_data[Queries.AUTO_CORAL_L3].apply(lambda cycle: cycle * 6)
        auto_coral_l4_points = team_data[Queries.AUTO_CORAL_L4].apply(lambda cycle: cycle * 7)
        auto_barge_points = team_data[Queries.AUTO_BARGE].apply(lambda cycle: cycle * 4)
        auto_processor_points = team_data[Queries.AUTO_PROCESSOR].apply(lambda cycle: cycle * 6)
        auto_leave_points = team_data[Queries.LEFT_STARTING_ZONE].apply(
            lambda left_starting_zone: Criteria.BOOLEAN_CRITERIA[left_starting_zone] * 3
        )
        total_auto_points = auto_coral_l1_points + auto_coral_l2_points + auto_coral_l3_points + auto_coral_l4_points + auto_barge_points + auto_processor_points + auto_leave_points
        # Teleop calculations
        teleop_coral_l1_points = team_data[Queries.TELEOP_CORAL_L1].apply(lambda cycle: cycle * 2)
        teleop_coral_l2_points = team_data[Queries.TELEOP_CORAL_L2].apply(lambda cycle: cycle * 3)
        teleop_coral_l3_points = team_data[Queries.TELEOP_CORAL_L3].apply(lambda cycle: cycle * 4)
        teleop_coral_l4_points = team_data[Queries.TELEOP_CORAL_L4].apply(lambda cycle: cycle * 5)
        teleop_barge_points = team_data[Queries.TELEOP_BARGE].apply(lambda cycle: cycle * 4)
        teleop_processor_points = team_data[Queries.TELEOP_PROCESSOR].apply(lambda cycle: cycle * 6)
        total_teleop_points = teleop_coral_l1_points + teleop_coral_l2_points + teleop_coral_l3_points + teleop_coral_l4_points + teleop_barge_points + teleop_processor_points

        # Endgame (stage) calculations
        park_points = team_data[Queries.PARKED_UNDER_BARGE].apply(
            lambda parking_state: Criteria.BOOLEAN_CRITERIA[parking_state]
        )
        climb_points = team_data[Queries.CLIMBED_CAGE].apply(
            lambda climbing_state: Criteria.CLIMBING_POINTAGE[climbing_state]
        )
       
        total_endgame_points = park_points + climb_points 

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
    def average_cycles_for_structure(self, team_number: int, structure: str) -> float:
        """Calculates the average cycles for a team for a structure (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param structure: The structure to return cycles for (AutoSpeaker/AutoAmp/TeleopSpeaker/TeleopAmp/TeleopTrap)
        :return: A float representing the average cycles for said team in the structure specified.
        """
        return self.cycles_by_structure_per_match(team_number, structure).mean()

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
            return team_data[Queries.AUTO_CORAL_L1] + team_data[Queries.AUTO_CORAL_L2]+ team_data[Queries.AUTO_CORAL_L3] + team_data[Queries.AUTO_CORAL_L4] + team_data[Queries.AUTO_BARGE] + team_data[Queries.AUTO_PROCESSOR]
        elif mode == Queries.AUTO_CORAL:
            return team_data[Queries.AUTO_CORAL_L1] + team_data[Queries.AUTO_CORAL_L2]+ team_data[Queries.AUTO_CORAL_L3] + team_data[Queries.AUTO_CORAL_L4]
        elif mode == Queries.TELEOP:
            return team_data[Queries.TELEOP_CORAL_L1] + team_data[Queries.TELEOP_CORAL_L2] + team_data[Queries.TELEOP_CORAL_L3] + team_data[Queries.TELEOP_CORAL_L4] + team_data[Queries.TELEOP_BARGE] + team_data[Queries.TELEOP_PROCESSOR]
        elif mode == Queries.CORAL_L1:
            return team_data[Queries.TELEOP_CORAL_L1] + team_data[Queries.AUTO_CORAL_L1]
        elif mode == Queries.CORAL_L2:
            return team_data[Queries.TELEOP_CORAL_L2] + team_data[Queries.AUTO_CORAL_L2]
        elif mode == Queries.CORAL_L3:
            return team_data[Queries.TELEOP_CORAL_L3] + team_data[Queries.AUTO_CORAL_L3]
        elif mode == Queries.CORAL_L4:
            return team_data[Queries.TELEOP_CORAL_L4] + team_data[Queries.AUTO_CORAL_L4]
        else:
            return (
                team_data[Queries.AUTO_CORAL_L1] + team_data[Queries.AUTO_CORAL_L2]+ team_data[Queries.AUTO_CORAL_L3] + team_data[Queries.AUTO_CORAL_L4] + team_data[Queries.AUTO_BARGE] + team_data[Queries.AUTO_PROCESSOR]
                + team_data[Queries.TELEOP_CORAL_L1] + team_data[Queries.TELEOP_CORAL_L2] + team_data[Queries.TELEOP_CORAL_L3] + team_data[Queries.TELEOP_CORAL_L4] + team_data[Queries.TELEOP_BARGE] + team_data[Queries.TELEOP_PROCESSOR]
            )

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
        auto_processor_sufficient = self.cycles_by_structure_per_match(
            team_number, Queries.AUTO_PROCESSOR
        )
        teleop_processor_sufficient = (
            self.cycles_by_structure_per_match(team_number, Queries.TELEOP_PROCESSOR)
        )

        return auto_processor_sufficient + teleop_processor_sufficient >= 2

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
        """Determines the chance of the coopertition bonus, the auto bonus, coral bonus, and the barge bonus using all possible permutations with an alliance.

        :param alliance: The three teams on the alliance.
        """
        chance_of_coop = self.chance_of_coop_bonus(alliance)
        cycles_for_alliance = [self.cycles_by_match(team) for team in alliance]        
        # Auto RP calculations
        Auto_Coral_Cycles_by_Team = [self.cycles_by_match(team, Queries.AUTO_CORAL) for team in alliance]
        possible_cycle_combos = self.cartesian_product(*Auto_Coral_Cycles_by_Team, reduce_with_sum=True)
        chance_of_reaching_1_cycles = (
            len([combo for combo in possible_cycle_combos if combo >= 1]) / len(possible_cycle_combos)
        )
        Robot_Left_Starting_Zone =[True in self.stat_per_match(team, Queries.LEFT_STARTING_ZONE) for team in alliance]
        if Robot_Left_Starting_Zone.count(True) == 3:  # If teams can climb
            chance_of_auto_rp = chance_of_reaching_1_cycles
        else:
            chance_of_auto_rp = 0  # No chance that they can get the RP even if 14 points can be reached.

        # Coral RP calculations
        Coral_L1_Cycles_by_Team = [self.cycles_by_match(team, Queries.CORAL_L1) for team in alliance]
        Coral_L2_Cycles_by_Team = [self.cycles_by_match(team, Queries.CORAL_L2) for team in alliance]
        Coral_L3_Cycles_by_Team = [self.cycles_by_match(team, Queries.CORAL_L3) for team in alliance]
        Coral_L4_Cycles_by_Team = [self.cycles_by_match(team, Queries.CORAL_L4) for team in alliance]
        possible_coral_L1_cycles = self.cartesian_product(*Coral_L1_Cycles_by_Team, reduce_with_sum=True)
        possible_coral_L2_cycles = self.cartesian_product(*Coral_L2_Cycles_by_Team, reduce_with_sum=True)
        possible_coral_L3_cycles = self.cartesian_product(*Coral_L3_Cycles_by_Team, reduce_with_sum=True)
        possible_coral_L4_cycles = self.cartesian_product(*Coral_L4_Cycles_by_Team, reduce_with_sum=True)
        chance_of_reaching_5_cycles_L1 = (
            len([combo for combo in possible_coral_L1_cycles if combo >= 5]) / len(possible_coral_L1_cycles)
        )
        chance_of_reaching_5_cycles_L2 = (
            len([combo for combo in possible_coral_L2_cycles if combo >= 5]) / len(possible_coral_L2_cycles)
        )
        chance_of_reaching_5_cycles_L3 = (
            len([combo for combo in possible_coral_L3_cycles if combo >= 5]) / len(possible_coral_L3_cycles)
        )
        chance_of_reaching_5_cycles_L4 = (
            len([combo for combo in possible_coral_L4_cycles if combo >= 5]) / len(possible_coral_L4_cycles)
        )
        chance_of_reaching_5_cycles_for_each_level = (
            chance_of_reaching_5_cycles_L1 * chance_of_reaching_5_cycles_L2 * chance_of_reaching_5_cycles_L3 * chance_of_reaching_5_cycles_L4
        )
        chance_of_reaching_5_cycles_for_3_levels = (

            1 - (1 - chance_of_reaching_5_cycles_for_each_level) ** 3
        )     
        # Barge RP calculations
        endgame_points_by_team = [self.points_contributed_by_match(team, Queries.ENDGAME) for team in alliance]
        possible_endgame_combos = self.cartesian_product(*endgame_points_by_team, reduce_with_sum=True)
        chance_of_barge_rp = (
            len([combo for combo in possible_endgame_combos if combo >= 14]) / len(possible_endgame_combos)
        )
        return (
            chance_of_coop,
            chance_of_reaching_5_cycles_for_each_level * (1 - chance_of_coop) + chance_of_reaching_5_cycles_for_3_levels * chance_of_coop,
            chance_of_barge_rp,
            chance_of_auto_rp
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
