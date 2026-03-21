"""Creates the `PicklistManager` class used to set up the Picklist page and its table."""

import os
from functools import partial

import streamlit as st
from dotenv import load_dotenv
from notion_client import Client
from notion_client.helpers import get_id
from pandas import DataFrame, notna

from .page_manager import PageManager
from utils import CalculatedStats, Criteria, EventSpecificConstants, Queries, retrieve_scouting_data, retrieve_team_list

load_dotenv()


class PicklistManager(PageManager):
    """The page manager for the `Picklist` page."""
    TRUNCATE_AT_DIGIT = 2

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.teams = retrieve_team_list()
        self.client = Client(auth=os.getenv("NOTION_TOKEN"))

        self.requested_stats = {
            "Avg. Driver Rating (1–5)": self.calculated_stats.average_driver_rating,
            "Avg. Throughput Speed (1–5)": self.calculated_stats.average_throughput_speed,
            "Avg. Intake Speed (1–5)": self.calculated_stats.average_intake_speed_rating,
            "Avg. Defense Rating (1–5)": self.calculated_stats.average_defense_rating,
            "Avg. Counter Defense (1–5)": self.calculated_stats.average_counter_defense_skill,
            "Avg. Shooter Defense (1–5)": self.calculated_stats.average_shooter_defense_skill,
            "Teleop Climb Rate": self.calculated_stats.teleop_climb_rate,
            "Auto Climb Rate": self.calculated_stats.auto_climb_rate,
            "Disabled Rate": self.calculated_stats.disabled_rate,
            "Shoot-on-the-Move Rate": self.calculated_stats.shoot_on_the_move_rate,
        }

    def generate_input_section(self) -> list[str]:
        """Creates a multiselect box for choosing picklist fields.

        :return: The list of chosen stat names.
        """
        return st.multiselect(
            "Picklist Fields",
            list(self.requested_stats.keys()),
            default=list(self.requested_stats.keys())[0]
        )

    def generate_picklist(self, stats_requested: list[str]) -> DataFrame:
        """Generates the picklist containing the requested statistics per team.

        :param stats_requested: The names of the statistics to include.
        """
        requested_picklist = [
            {
                "Team Number": f"FRC {team}"
            } | {
                stat_name: round(self.requested_stats[stat_name](team), self.TRUNCATE_AT_DIGIT)
                for stat_name in stats_requested
            }
            for team in self.teams
        ]
        return DataFrame.from_dict(requested_picklist)

    def write_to_notion(self, dataframe: DataFrame) -> None:
        """Writes the picklist to a Notion database.

        :param dataframe: The dataframe containing all the statistics of each team.
        """
        properties = {
            "Team Name": {"title": {}}
        } | {
            column: {"number": {}} for column in dataframe.columns if column != "Team Number"
        }
        icon = {"type": "emoji", "emoji": "🗒️"}
        self.client.databases.update(
            database_id=(db_id := get_id(EventSpecificConstants.PICKLIST_URL)),
            properties=properties,
            icon=icon
        )

        percentile_75 = self.calculated_stats.quantile_stat(
            0.75, lambda self_, team: self_.average_driver_rating(team)
        )
        percentile_50 = self.calculated_stats.quantile_stat(
            0.5, lambda self_, team: self_.average_driver_rating(team)
        )
        percentile_25 = self.calculated_stats.quantile_stat(
            0.25, lambda self_, team: self_.average_driver_rating(team)
        )

        for _, row in dataframe.iterrows():
            team_name = row["Team Number"]
            query_page = self.client.databases.query(
                database_id=db_id,
                filter={
                    "property": "Team Name",
                    "title": {"contains": team_name}
                }
            )
            team_number = int(team_name.split()[1])
            team_driver = self.calculated_stats.average_driver_rating(team_number)

            if team_driver > percentile_75:
                emoji = "🔵"
            elif percentile_50 <= team_driver < percentile_75:
                emoji = "🟢"
            elif percentile_25 <= team_driver < percentile_50:
                emoji = "🟠"
            else:
                emoji = "🔴"

            auto_notes = self.calculated_stats.stat_per_match(team_number, Queries.AUTO_NOTES)
            teleop_notes = self.calculated_stats.stat_per_match(team_number, Queries.TELEOP_NOTES)
            rating_notes = self.calculated_stats.stat_per_match(team_number, Queries.RATING_NOTES)

            def _notes_block(heading: str, notes_series) -> list:
                notes_list = [n for n in notes_series if n]
                if not notes_list:
                    return []
                return [
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"text": {"content": heading, "link": None}}],
                            "color": "default",
                            "is_toggleable": False
                        }
                    }
                ] + [
                    {
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": note, "link": None}}]
                        }
                    }
                    for note in notes_list
                ]

            children = (
                [{
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": f"Notes of {team_name}", "link": None}}],
                        "icon": {"emoji": "📝"},
                        "color": "default"
                    }
                }]
                + _notes_block("Autonomous Notes", auto_notes)
                + _notes_block("Teleop Notes", teleop_notes)
                + _notes_block("Rating Notes", rating_notes)
            )

            page_props = {
                column: {
                    "number": data if notna(
                        data := dataframe[dataframe["Team Number"] == team_name][column].tolist()[0]
                    ) else 0
                }
                for column in dataframe.columns if column != "Team Number"
            } | {
                "Team Name": {"id": "title", "title": [{"text": {"content": team_name}}]},
            }

            if not query_page["results"]:
                self.client.pages.create(
                    database_id=db_id,
                    icon={"type": "emoji", "emoji": emoji},
                    parent={"type": "database_id", "database_id": db_id},
                    properties=page_props,
                    children=children
                )
            else:
                self.client.pages.update(
                    page_id=query_page["results"][0]["id"],
                    icon={"type": "emoji", "emoji": emoji},
                    parent={"type": "database_id", "database_id": db_id},
                    properties=page_props
                )
