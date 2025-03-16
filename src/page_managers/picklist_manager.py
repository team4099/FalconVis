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
    TRUNCATE_AT_DIGIT = 2  # Round the decimal to two places

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.teams = retrieve_team_list()
        self.client = Client(auth=os.getenv("NOTION_TOKEN"))

        # Requested stats is used to define the stats wanted in the picklist generation.
        self.requested_stats = {
            "Average Points Contributed": self.calculated_stats.average_points_contributed,
            "Average Auto Cycles": partial(
                self.calculated_stats.average_cycles,
                mode=Queries.AUTO
            ),
            "Average Teleop Cycles": partial(
                self.calculated_stats.average_cycles,
                mode=Queries.TELEOP
            ),
            "Average Coral Cycles": partial(
                self.calculated_stats.average_cycles_for_structure,
                structure=(Queries.AUTO_CORAL_L1, Queries.AUTO_CORAL_L2, Queries.AUTO_CORAL_L3, Queries.AUTO_CORAL_L4,
                           Queries.TELEOP_CORAL_L1, Queries.TELEOP_CORAL_L2, Queries.TELEOP_CORAL_L3, Queries.TELEOP_CORAL_L4)
            ),
            "Average Algae Cycles": partial(
                self.calculated_stats.average_cycles_for_structure,
                structure=(Queries.AUTO_BARGE, Queries.AUTO_PROCESSOR,
                           Queries.TELEOP_BARGE, Queries.TELEOP_PROCESSOR)
            ),
            "Average Misses": partial(
                self.calculated_stats.average_cycles_for_structure,
                structure=(Queries.AUTO_CORAL_MISSES, Queries.TELEOP_CORAL_MISSES)
            ),
            "# of Times Climbed": partial(
                self.calculated_stats.cumulative_stat,
                stat=Queries.CLIMBED_CAGE,
                criteria=Criteria.CLIMBING_CRITERIA
            ),
            "# of Disables": partial(
                self.calculated_stats.cumulative_stat,
                stat=Queries.DISABLE,
                criteria=Criteria.BOOLEAN_CRITERIA
            ),
            "Average Driver Rating": self.calculated_stats.average_driver_rating,
            "Average Counter Defense Skill": self.calculated_stats.average_counter_defense_skill,
            "Average Defense Skill": self.calculated_stats.average_defense_rating,
            "Average Intake Speed": self.calculated_stats.average_intake_speed,

        }

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Picklist` page.

        Creates a multiselect box to choose the different fields for the picklist table.

        :return: Returns a list containing the different fields chosen.
        """
        return st.multiselect(
            "Picklist Fields",
            self.requested_stats.keys(),
            default=list(self.requested_stats.keys())[0]
        )

    def generate_picklist(self, stats_requested: list[str]) -> DataFrame:
        """Generates the picklist containing the statistics requested and the team number.

        :param stats_requested: The name of the statistics requested (matches the keys in `self.requested_stats`
        """
        requested_picklist = [
            {
                "Team Number": f"FRC {team}"  # We make it a string because otherwise Notion won't recognize the value.
            } | {
                stat_name: round(self.requested_stats[stat_name](team), self.TRUNCATE_AT_DIGIT)
                for stat_name in stats_requested
            }
            for team in self.teams
        ]
        return DataFrame.from_dict(requested_picklist)

    def write_to_notion(self, dataframe: DataFrame) -> None:
        """Writes to a Notion picklist entered by the user in the constants file.

        :param dataframe: The dataframe containing all the statistics of each team.
        :return:
        """
        # Generate Notion Database first
        properties = {
            "Team Name": {"title": {}}
        } | {
            column: {"number": {}} for column in dataframe.columns if column != "Team Number"
        }
        icon = {"type": "emoji", "emoji": "🗒️"}
        self.client.databases.update(
            database_id=(db_id := get_id(EventSpecificConstants.PICKLIST_URL)), properties=properties, icon=icon
        )

        # Find percentiles across all teams
        percentile_75 = self.calculated_stats.quantile_stat(
            0.75,
            lambda self_, team: self_.average_cycles(team)
        )
        percentile_50 = self.calculated_stats.quantile_stat(
            0.5,
            lambda self_, team: self_.average_cycles(team)
        )
        percentile_25 = self.calculated_stats.quantile_stat(
            0.25,
            lambda self_, team: self_.average_cycles(team)
        )

        for _, row in dataframe.iterrows():
            team_name = row["Team Number"]
            query_page = self.client.databases.query(
                database_id=db_id,
                filter={
                    "property": "Team Name",
                    "title": {
                        "contains": team_name,
                    },
                }
            )
            # Based off of the percentile between all their stats
            team_number = int(team_name.split()[1])
            team_cycles = self.calculated_stats.average_cycles(team_number)

            if team_cycles > percentile_75:
                emoji = "🔵"
            elif percentile_50 <= team_cycles < percentile_75:
                emoji = "🟢"
            elif percentile_25 <= team_cycles < percentile_50:
                emoji = "🟠"
            else:
                emoji = "🔴"

            autonomous_notes = self.calculated_stats.stat_per_match(team_number, Queries.AUTO_NOTES)

            if not autonomous_notes.empty and any(note for note in autonomous_notes):
                autonomous_block = [
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": "Autonomous Notes",
                                        "link": None
                                    }
                                }
                            ],
                            "color": "default",
                            "is_toggleable": False
                        }
                    }
                ] + [
                    {
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": note,
                                        "link": None
                                    }
                                }
                            ]
                        }
                    }
                    for note in autonomous_notes if note
                ]
            else:
                autonomous_block = []

            teleop_notes = self.calculated_stats.stat_per_match(team_number, Queries.TELEOP_NOTES)

            if not teleop_notes.empty and any(note for note in teleop_notes):
                teleop_block = [
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": "Teleop Notes",
                                        "link": None
                                    }
                                }
                            ],
                            "color": "default",
                            "is_toggleable": False
                        }
                    }
                ] + [
                    {
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": note,
                                        "link": None
                                    }
                                }
                            ]
                        }
                    }
                    for note in teleop_notes if note
                ]
            else:
                teleop_block = []

            endgame_notes = self.calculated_stats.stat_per_match(team_number, Queries.ENDGAME_NOTES)
            if not endgame_notes.empty and any(note for note in endgame_notes):
                endgame_block = [
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": "Endgame Notes",
                                        "link": None
                                    }
                                }
                            ],
                            "color": "default",
                            "is_toggleable": False
                        }
                    }
                ] + [
                    {
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": note,
                                        "link": None
                                    }
                                }
                            ]
                        }
                    }
                    for note in endgame_notes if note
                ]
            else:
                endgame_block = []

            # No page created yet.
            if not query_page["results"]:
                self.client.pages.create(
                    database_id=db_id,
                    icon={"type": "emoji", "emoji": emoji},
                    parent={"type": "database_id", "database_id": db_id},
                    properties={
                        column: {
                            "number": data if notna(data := dataframe[dataframe["Team Number"] == team_name][column].tolist()[0]) else 0
                        } for column in dataframe.columns if column != "Team Number"
                    } | {
                        "Team Name": {"id": "title", "title": [{"text": {"content": team_name}}]},
                    },
                    children=[
                        {
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": f"Notes of {team_name}",
                                            "link": None
                                        }
                                    }
                                ],
                                "icon": {
                                    "emoji": "📝"
                                },
                                "color": "default"
                            }
                        }
                    ] + autonomous_block + teleop_block + endgame_block
                )
            # Page already created
            else:
                self.client.pages.update(
                    page_id=query_page["results"][0]["id"],
                    icon={"type": "emoji", "emoji": emoji},
                    parent={"type": "database_id", "database_id": db_id},
                    properties={
                       column: {
                           "number": data if notna(data := dataframe[dataframe["Team Number"] == team_name][column].tolist()[0]) else 0
                       } for column in dataframe.columns if column != "Team Number"
                    } | {
                       "Team Name": {"id": "title", "title": [{"text": {"content": team_name}}]},
                    }
                )
