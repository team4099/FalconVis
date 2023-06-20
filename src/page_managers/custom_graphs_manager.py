"""Creates the `CustomGraphsManager` class used to set up the Custom Graph page and generate its data."""

import inspect

import streamlit as st

from .page_manager import PageManager
from utils import CalculatedStats, GeneralConstants, Queries, retrieve_scouting_data, retrieve_team_list


class CustomGraphsManager(PageManager):
    """The page manager for the `Custom Graphs` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> list[list, list] | None:
        """Creates the input section for the `Custom Graphs` page.

        Creates tabs to choose what data to display in the graph.
        Creates a dropdown to choose a stat (the y-data) before letting you input the parameters.

        :return: Returns a list containing the x and y data.
        """
        team_list = retrieve_team_list()

        names_to_methods = {
            name.replace("_", " ").capitalize(): method
            for name, method in inspect.getmembers(self.calculated_stats, predicate=inspect.ismethod)
            if not name.startswith("__")
        }

        st.write("#### 📈 Data to Display")

        one_team_col, three_teams_col, full_event_col = st.columns(3)
        (
            st.session_state["data_for_team"],
            st.session_state["data_for_three_teams"],
            st.session_state["data_for_event"]
        ) = (
            one_team_col.button("One Team's Data", use_container_width=True),
            three_teams_col.button("Three Teams' Data", use_container_width=True),
            full_event_col.button("Full Event's Data", use_container_width=True)
        )
        data_for_team, data_for_three_teams, data_for_event = (
            st.session_state["data_for_team"],
            st.session_state["data_for_three_teams"],
            st.session_state["data_for_event"]
        )

        # X-axis input section.
        if data_for_team:
            st.write("#### ↔️ X Axis")

            teams_selected = [st.selectbox("Team to Graph", team_list)]
            keyword_in_docstring = Queries.ONE_TEAM_KEYWORD
        elif data_for_three_teams:
            st.write("#### ↔️ X Axis")

            team1_col, team2_col, team3_col = st.columns(3)
            teams_selected = [
                team1_col.selectbox("Team 1", team_list),
                team2_col.selectbox("Team 2", team_list),
                team3_col.selectbox("Team 3", team_list)
            ]
            keyword_in_docstring = Queries.THREE_TEAMS_KEYWORD
        elif data_for_event:
            teams_selected = team_list
            keyword_in_docstring = Queries.FULL_EVENT_KEYWORD
        else:
            return

        # Filter out methods based on if they support the type of data being graphed.
        names_to_methods_filtered = {
            name: method for name, method in names_to_methods.items()
            if keyword_in_docstring in method.__doc__
        }

        # Y-axis input section
        st.write("#### ↕️ Y-Axis")

        stat_selected = st.selectbox("Statistic to Graph", list(names_to_methods_filtered.keys()), index=1)
        parameters = [
            parameter for parameter in inspect.getfullargspec(names_to_methods_filtered[stat_selected]).args
            if parameter not in {"self", "team_number"}
        ]
        print(parameters)

        if parameters:
            for column, name in zip(st.columns(len(parameters)), parameters):
                column.text_input(name.replace("_", " ").capitalize())
