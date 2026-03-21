"""File that contains the class which calculates statistics for a team/event/for other purposes."""
from __future__ import annotations

from functools import reduce
from typing import Callable

import numpy as np
from numpy import percentile
from pandas import DataFrame, Series, isna, to_numeric
from scipy.integrate import quad
from scipy.stats import norm


from .base_calculated_stats import BaseCalculatedStats
from .constants import Criteria, Queries
from .functions import _convert_to_float_from_numpy_type, scouting_data_for_team, retrieve_team_list
from .statbotics import get_team_statbotics

__all__ = ["CalculatedStats"]


class CalculatedStats(BaseCalculatedStats):
    """Utility class for calculating statistics in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # --- Rating methods ---

    @_convert_to_float_from_numpy_type
    def average_driver_rating(self, team_number: int) -> float:
        """Returns the average driver rating (1–5 scale) of a team.

        :param team_number: The team to determine the driver rating for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DRIVER_RATING].apply(
            lambda v: Criteria.DRIVER_RATING_CRITERIA.get(v, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_intake_speed_rating(self, team_number: int) -> float:
        """Returns the average intake speed rating (1–5) of a team.

        :param team_number: The team to determine the intake speed rating for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.INTAKE_SPEED].apply(
            lambda v: Criteria.INTAKE_SPEED_CRITERIA.get(v, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_defense_rating(self, team_number: int) -> float:
        """Returns the average defense rating (1–5) of a team.

        :param team_number: The team to find defense data for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DEFENSE_RATING].apply(
            lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_counter_defense_skill(self, team_number: int) -> float:
        """Returns the average counter-defense skill (intake defense rating, 1–5) of a team.

        :param team_number: The team to determine the counter defense skill for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.INTAKE_DEFENSE_RATING].apply(
            lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_throughput_speed(self, team_number: int) -> float:
        """Returns the average throughput speed rating (1–5) of a team.

        :param team_number: The team to determine the throughput for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.THROUGHPUT_SPEED].apply(
            lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, float("nan"))
        ).mean()

    @_convert_to_float_from_numpy_type
    def average_shooter_defense_skill(self, team_number: int) -> float:
        """Returns the average shooter defense skill (1–5) of a team.

        :param team_number: The team to determine the shooter defense skill for.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.SHOOTER_DEFENSE_RATING].apply(
            lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, float("nan"))
        ).mean()

    # --- Rate/count methods ---

    @_convert_to_float_from_numpy_type
    def auto_climb_rate(self, team_number: int) -> float:
        """Returns the fraction of matches in which a team climbed during auto (0–1).

        :param team_number: The team to compute the auto climb rate for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        if team_data.empty:
            return 0.0
        values = team_data[Queries.AUTO_CLIMB].apply(
            lambda v: Criteria.BOOLEAN_CRITERIA.get(v, 0)
        )
        return float(values.mean())

    @_convert_to_float_from_numpy_type
    def teleop_climb_rate(self, team_number: int) -> float:
        """Returns the fraction of matches in which a team performed any teleop climb (0–1).

        :param team_number: The team to compute the teleop climb rate for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        if team_data.empty:
            return 0.0
        values = team_data[Queries.TELEOP_CLIMB].apply(
            lambda v: 0 if v in (None, "No climb") else 1
        )
        return float(values.mean())

    @_convert_to_float_from_numpy_type
    def disabled_rate(self, team_number: int) -> float:
        """Returns the fraction of matches in which a team was disabled (0–1).

        :param team_number: The team to compute the disabled rate for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        if team_data.empty:
            return 0.0
        values = team_data[Queries.DISABLE].apply(
            lambda v: Criteria.BOOLEAN_CRITERIA.get(v, 0)
        )
        return float(values.mean())

    @_convert_to_float_from_numpy_type
    def shoot_on_the_move_rate(self, team_number: int) -> float:
        """Returns the fraction of matches in which a team shot on the move (0–1).

        :param team_number: The team to compute the shoot-on-the-move rate for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        if team_data.empty:
            return 0.0
        values = team_data[Queries.SHOOT_ON_THE_MOVE].apply(
            lambda v: Criteria.BOOLEAN_CRITERIA.get(v, 0)
        )
        return float(values.mean())

    # --- Composite scoring proxy (used for win probability) ---

    def composite_score_by_match(self, team_number: int) -> Series:
        """Returns a numeric proxy score per match derived from qualitative ratings.

        Combines driver rating, throughput speed, intake speed, and climb level into a
        single normalised composite that can be used for relative win-probability estimation.

        :param team_number: The team to compute the composite score for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        if team_data.empty:
            return Series(dtype=float)

        driver = team_data[Queries.DRIVER_RATING].apply(
            lambda v: Criteria.DRIVER_RATING_CRITERIA.get(v, 3.0)
        )
        throughput = team_data[Queries.THROUGHPUT_SPEED].apply(
            lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, 3.0)
        )
        intake = team_data[Queries.INTAKE_SPEED].apply(
            lambda v: Criteria.INTAKE_SPEED_CRITERIA.get(v, 3.0)
        )
        climb = team_data[Queries.TELEOP_CLIMB].apply(
            lambda v: Criteria.CLIMBING_CRITERIA.get(v, 0) * 2.0
        )
        auto_climb = team_data[Queries.AUTO_CLIMB].apply(
            lambda v: Criteria.BOOLEAN_CRITERIA.get(v, 0) * 3.0
        )

        return (driver * 2 + throughput * 3 + intake * 1 + climb + auto_climb).reset_index(drop=True)

    # --- Percentile methods ---

    def quantile_stat(self, quantile: float, predicate: Callable) -> float:
        """Calculates a scalar value for a percentile of a dataset.

        Used for comparisons between teams (e.g. passing 0.5 returns the median).

        :param quantile: Quantile used to find the scalar value at.
        :param predicate: Predicate called per team (self and team number must be arguments).
        """
        dataset = [predicate(self, team) for team in retrieve_team_list()]
        return percentile(dataset, quantile * 100)

    # --- General stat methods ---

    @_convert_to_float_from_numpy_type
    def average_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> float:
        """Calculates the average statistic for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        """
        return self.stat_per_match(team_number, stat, criteria).mean()

    @_convert_to_float_from_numpy_type
    def cumulative_stat(self, team_number: int, stat: str, criteria: dict | None = None) -> int:
        """Calculates a cumulative stat for a team (wrapper around `stat_per_match`).

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        """
        return self.stat_per_match(team_number, stat, criteria).sum()

    def stat_per_match(self, team_number: int, stat: str, criteria: dict | None = None) -> Series:
        """Calculates a statistic over time as specified for a team.

        :param team_number: The team number to calculate said statistic for.
        :param stat: The field within the scouting data that corresponds to the desired statistic.
        :param criteria: An optional criteria used to determine what the weightage of the statistic is.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[stat].apply(
            lambda datum: criteria.get(datum, 0) if criteria is not None else datum
        )

    def driving_index(self, team_number: int) -> float:
        """Returns a composite driving quality index (throughput × counter-defense) for a team.

        - Used for custom graphs with three teams.
        - Used for custom graphs with a full event.

        :param team_number: The team number to calculate a driving index for.
        """
        throughput = self.average_throughput_speed(team_number)
        counter_defense = self.average_counter_defense_skill(team_number)
        if isna(throughput) or isna(counter_defense):
            return 0.0
        return float(throughput * counter_defense)

    # --- Bonus RP estimation (qualitative proxy) ---

    def chance_of_bonuses(self, alliance: list[int]) -> tuple[float, float, float]:
        """Estimates bonus RP chances from qualitative data.

        Since the dataset has no quantitative scores, returns simplified estimates:
        - Scoring RP proxy: average of throughput ratings across alliance / 5
        - Supercharged RP proxy: 0 (insufficient data to estimate)
        - Traversal RP proxy: average teleop climb rate across alliance

        :param alliance: The three teams on the alliance.
        """
        throughput_rates = [self.average_throughput_speed(team) for team in alliance]
        avg_throughput = sum(t for t in throughput_rates if not (t != t)) / max(len(throughput_rates), 1)
        chance_scoring_rp = min(avg_throughput / 5.0, 1.0)

        climb_rates = [self.teleop_climb_rate(team) for team in alliance]
        avg_climb_rate = sum(climb_rates) / max(len(climb_rates), 1)

        return (chance_scoring_rp, 0.0, avg_climb_rate)

    # --- Win probability (Statbotics EPA-based) ---

    def chance_of_winning(self, alliance_one: list[int], alliance_two: list[int]) -> tuple:
        """Returns the estimated win probability between two alliances.

        Uses Statbotics EPA mean and standard deviation per team to model each
        alliance's score as a normal distribution, then integrates to find the
        probability that alliance one outscores alliance two.  Falls back to the
        qualitative composite proxy when no Statbotics data is available.

        :param alliance_one: Three-team list for alliance one (red).
        :param alliance_two: Three-team list for alliance two (blue).
        """
        def _epa_stats(team: int) -> tuple[float, float]:
            data = get_team_statbotics(team)
            mean = float(data.get("total_epa") or 0)
            sd   = float(data.get("total_epa_sd") or 0)
            return mean, sd

        a1_stats = [_epa_stats(t) for t in alliance_one]
        a2_stats = [_epa_stats(t) for t in alliance_two]

        if all(m == 0 for m, _ in a1_stats + a2_stats):
            # No Statbotics data — fall back to qualitative composite scores
            a1_series = [self.composite_score_by_match(t) for t in alliance_one]
            a2_series = [self.composite_score_by_match(t) for t in alliance_two]
            alliance_one_mean = sum(float(np.mean(s)) for s in a1_series if len(s))
            alliance_two_mean = sum(float(np.mean(s)) for s in a2_series if len(s))
            alliance_one_std  = sum(float(np.std(s)) ** 2 for s in a1_series) ** 0.5
            alliance_two_std  = sum(float(np.std(s)) ** 2 for s in a2_series) ** 0.5
        else:
            alliance_one_mean = sum(m for m, _ in a1_stats)
            alliance_two_mean = sum(m for m, _ in a2_stats)

            def _sd(mean: float, sd: float) -> float:
                # If API returned a valid SD use it; otherwise estimate ~15% of mean
                return sd if sd > 0 else max(abs(mean) * 0.15, 5.0)

            alliance_one_std = sum(_sd(m, s) ** 2 for m, s in a1_stats) ** 0.5
            alliance_two_std = sum(_sd(m, s) ** 2 for m, s in a2_stats) ** 0.5

        compared_mean = alliance_one_mean - alliance_two_mean
        compared_std  = (alliance_one_std ** 2 + alliance_two_std ** 2) ** 0.5

        if not compared_std and compared_mean:
            compared_std = abs(compared_mean)
        elif not compared_std:
            compared_std = 0.5

        dist = norm(loc=compared_mean, scale=compared_std)
        odds_of_one_winning = quad(lambda x: dist.pdf(x), 0, np.inf)[0]
        odds_of_two_winning = quad(lambda x: dist.pdf(x), -np.inf, 0)[0]

        return odds_of_one_winning, odds_of_two_winning, alliance_one_mean, alliance_two_mean
