"""Creates the `RankingSimulatorManager` class used to set up the Ranking Simulator page and its table."""
from collections import defaultdict

import streamlit as st
from numpy import logical_and
from pandas import DataFrame

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    retrieve_match_data,
    retrieve_match_schedule,
    retrieve_scouting_data,
    retrieve_team_list
)


class RankingSimulatorManager(PageManager):
    """The ranking simulator page manager for the `Ranking Simulator` page."""
    MATCHES_TO_START_FROM = 12

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.matches_played = retrieve_match_data()

    def generate_input_section(self) -> str:
        """Generates the input section of the `Ranking Simulator` page."""
        if (
            not self.matches_played.empty
            and (last_match_played := self.matches_played["match_number"].max()) >= self.MATCHES_TO_START_FROM
        ):
            return st.slider("Match Number to Simulate From", self.MATCHES_TO_START_FROM, last_match_played)

        return st.exception(
            ValueError(
                f"Come back to the simulator once at least {self.MATCHES_TO_START_FROM} matches have been played!"
            )
        )

    def _generate_rankings(self, to_match: int) -> DataFrame:
        """Generates the rankings for a team given the matches that are specified."""
        rankings = []
        for team in retrieve_team_list():
            red_match_data_for_team = self.matches_played[
                logical_and(
                    self.matches_played["red_alliance"].str.contains(str(team)),
                    self.matches_played["match_number"] <= to_match
                )
            ]
            blue_match_data_for_team = self.matches_played[
                logical_and(
                    self.matches_played["blue_alliance"].str.contains(str(team)),
                    self.matches_played["match_number"] <= to_match
                )
            ]

            matches_played = len(red_match_data_for_team) + len(blue_match_data_for_team)
            average_rps = (
                red_match_data_for_team["red_alliance_rp"].sum() + blue_match_data_for_team["blue_alliance_rp"].sum()
            ) / matches_played
            average_coop = (
                red_match_data_for_team["reached_coop"].sum() + blue_match_data_for_team["reached_coop"].sum()
            ) / matches_played
            average_match_score = (
                red_match_data_for_team["red_score"].sum() + blue_match_data_for_team["blue_score"].sum()
            ) / matches_played
            rankings.append((team, average_rps, average_coop, average_match_score, matches_played))  # Sort orders

        return DataFrame(
            sorted(rankings, key=lambda ranking: ranking[1:-1], reverse=True),
            columns=("team", "rp", "coop", "match_score", "matches_played")
        )

    def generate_simulated_rankings(self, to_match: int) -> None:
        """Generates the simulated rankings up to the match number requested."""
        rankings = self._generate_rankings(to_match)
        match_schedule = retrieve_match_schedule()
        simulated_rankings = defaultdict(lambda: [[], [], [], 0])

        teams = retrieve_team_list()
        progress_bar = st.progress(0, text="Crunching the simulations...")

        for idx, team in enumerate(teams, start=1):
            matches_for_team = match_schedule[
                match_schedule["red_alliance"]
                    .apply(lambda alliance: ",".join(map(str, alliance)))
                    .str.contains(str(team))
                | match_schedule["blue_alliance"]
                    .apply(lambda alliance: ",".join(map(str, alliance)))
                    .str.contains(str(team))
            ]
            matches_left_for_team = matches_for_team[
                matches_for_team["match_key"].apply(
                    lambda key: int(key.replace("qm", "").replace("sf", "").replace("f", "").replace("m1", "").replace("m2", "").replace("m3", ""))
                ) >= to_match
            ][matches_for_team["match_key"].str.contains("qm")]

            for _, row in matches_left_for_team.iterrows():
                alliance = row["red_alliance"] if team in row["red_alliance"] else row["blue_alliance"]
                opposing_alliance = row["blue_alliance"] if team in row["red_alliance"] else row["red_alliance"]

                chance_of_coop, chance_of_melody, chance_of_ensemble = self.calculated_stats.chance_of_bonuses(alliance)
                chance_of_winning, _, score, __ = self.calculated_stats.chance_of_winning(alliance, opposing_alliance)

                total_rps = chance_of_melody + chance_of_ensemble + chance_of_winning * 2
                simulated_rankings[team][0].append(total_rps)
                simulated_rankings[team][1].append(chance_of_coop)
                simulated_rankings[team][2].append(score)
                simulated_rankings[team][3] += 1

            progress_bar.progress(idx / len(teams), "Crunching the simulations...")

        new_rankings = []

        # Calculate new rankings with simulated rankings.
        for team in teams:
            _, rps, avg_coop, avg_match_score, matches_played = rankings[rankings["team"] == team].iloc[0]
            total_matches_played = matches_played + simulated_rankings[team][3]
            total_avg_rp = (rps * matches_played + sum(simulated_rankings[team][0])) / total_matches_played
            total_avg_coop = (avg_coop * matches_played + sum(simulated_rankings[team][1])) / total_matches_played
            total_avg_score = (avg_match_score * matches_played + sum(simulated_rankings[team][2])) / total_matches_played
            new_rankings.append((team, total_avg_rp, total_avg_coop, total_avg_score))

        ranking_df = DataFrame(
            sorted(new_rankings, key=lambda ranking: ranking[1:], reverse=True),
            columns=("Team", "Average Ranking Points", "Average Coopertition", "Average Match Score")
        )
        st.table(ranking_df.applymap(lambda value: f"{value:.2f}" if isinstance(value, float) else value))