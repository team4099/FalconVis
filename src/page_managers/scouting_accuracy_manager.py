"""Creates the `ScoutingAccuracyManager` class used to set up the Scouting Coverage page."""
import pandas as pd
import streamlit as st
from .page_manager import PageManager
from utils import (
    CalculatedStats,
    Queries,
    retrieve_scouting_data,
)
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()


class ScoutingAccuracyManager(PageManager):
    """Page manager for the `Scouting Coverage` page.

    Since the current dataset is qualitative-only, this page shows scouting
    coverage statistics (matches scouted per person, teams covered) rather than
    numerical accuracy against TBA scores.
    """

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())
        self.raw_scouting_data = retrieve_scouting_data()

    def generate_input_section(self) -> str:
        """Provides a text input for filtering by scouter name.

        :return: The scout name entered by the user (empty string shows all).
        """
        return st.text_input(
            "Filter by scouter name (leave blank to see all)",
            placeholder="e.g. Nikhil"
        )

    def generate_scouting_accuracy_table(self, member_name: str) -> DataFrame:
        """Generates a per-scouter coverage breakdown.

        Shows how many matches each scouter covered, which teams they scouted,
        and how many unique teams they observed.

        :param member_name: Optional filter — only rows whose ScoutId contains this string are shown.
        :return: A DataFrame summarising each scouter's coverage.
        """
        data = self.raw_scouting_data.copy()

        if member_name.strip():
            data = data[
                data[Queries.SCOUT_ID].str.lower().str.contains(member_name.strip().lower(), na=False)
            ]

        if data.empty:
            return DataFrame(columns=["Scouter", "Matches Scouted", "Unique Teams", "Teams Scouted"])

        rows = []
        for scout_id, group in data.groupby(Queries.SCOUT_ID):
            teams = sorted(group[Queries.TEAM_NUMBER].unique().tolist())
            rows.append({
                "Scouter": scout_id,
                "Matches Scouted": len(group),
                "Unique Teams": len(teams),
                "Teams Scouted": ", ".join(str(t) for t in teams),
            })

        return DataFrame(rows).sort_values("Matches Scouted", ascending=False).reset_index(drop=True)

    def generate_match_accuracy_table(self) -> DataFrame:
        """Generates a per-match coverage breakdown showing which teams were scouted in each match.

        :return: A DataFrame with one row per match and scouting coverage info.
        """
        data = self.raw_scouting_data.copy()

        rows = []
        for match_key, group in data.groupby(Queries.MATCH_KEY):
            num = group[Queries.MATCH_NUMBER].iloc[0] if Queries.MATCH_NUMBER in group.columns else None
            teams = sorted(group[Queries.TEAM_NUMBER].unique().tolist())
            scouts = sorted(group[Queries.SCOUT_ID].unique().tolist())
            rows.append({
                "Match": match_key,
                "Match #": num,
                "Teams Scouted": len(teams),
                "Team Numbers": ", ".join(str(t) for t in teams),
                "Scouters": ", ".join(scouts),
            })

        if not rows:
            return DataFrame()

        df = DataFrame(rows)
        if "Match #" in df.columns and df["Match #"].notna().any():
            df = df.sort_values("Match #").reset_index(drop=True)
        return df.drop(columns=["Match #"], errors="ignore")
