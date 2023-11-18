"""Creates the `CustomGraphsManager` class used to set up the Custom Graph page and generate its data."""

import inspect
import re
from typing import Callable

import streamlit as st

from .page_manager import PageManager
from utils import (
    CalculatedStats,
    graphing,
    plotly_chart,
    populate_missing_data,
    Queries,
    retrieve_scouting_data,
    retrieve_team_list,
    scouting_data_for_team
)


class CustomGraphsManager(PageManager):
    """The page manager for the `Custom Graphs` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> list[list, list, Callable, str]:
        """Creates the input section for the `Custom Graphs` page.

        Creates tabs to choose what data to display in the graph.
        Creates a dropdown to choose a stat (the y-data) before letting you input the parameters.

        :return: Returns a list containing the x axis, the y axis, the graph type, and the statistic name.
        """
        team_list = retrieve_team_list()

        names_to_methods = {
            name.replace("_", " ").capitalize(): method
            for name, method in inspect.getmembers(self.calculated_stats, predicate=inspect.ismethod)
            if not name.startswith("__")
        }

        st.write("#### 📈 Data to Display")

        data_to_display = st.radio(
            "Choose the data you want to display:",
            ("One Team's Data", "Three Teams' Data", "Full Event's Data")
        )
        data_for_team = data_to_display == "One Team's Data"
        data_for_three_teams = data_to_display == "Three Teams' Data"
        data_for_event = data_to_display == "Full Event's Data"

        # Set the keyword to look for in docstrings
        if data_for_team:
            keyword_in_docstring = Queries.ONE_TEAM_KEYWORD
        elif data_for_three_teams:
            keyword_in_docstring = Queries.THREE_TEAMS_KEYWORD
        else:
            keyword_in_docstring = Queries.FULL_EVENT_KEYWORD

        # Graph type input section
        st.write("#### 📊 Type of Graph")

        # Get all graphing functions and filter out the ones that support the type of graph.
        graph_types = {
            name.replace("_", " ").capitalize(): member
            for name, member in inspect.getmembers(graphing, predicate=inspect.isfunction)
            if member.__doc__ and keyword_in_docstring in member.__doc__
        }

        graph_name = st.selectbox("Type of Graph", list(graph_types.keys()))
        graph_selected = graph_types[graph_name]

        # X-axis input section.
        if data_for_team:
            st.write("#### ↔️ X Axis")

            teams_selected = [st.selectbox("Team to Graph", team_list)]
        elif data_for_three_teams:
            st.write("#### ↔️ X Axis")

            team1_col, team2_col, team3_col = st.columns(3)
            teams_selected = [
                team1_col.selectbox("Team 1", team_list),
                team2_col.selectbox("Team 2", team_list),
                team3_col.selectbox("Team 3", team_list)
            ]
        elif data_for_event:
            teams_selected = team_list

        # Filter out methods based on if they support the type of graph.
        names_to_methods_filtered = {
            name: method for name, method in names_to_methods.items()
            if graph_name in method.__doc__
        }

        # Y-axis input section
        st.write("#### ↕️ Y-Axis")

        stat_selected = st.selectbox("Statistic to Graph", list(names_to_methods_filtered.keys()))
        method_to_use = names_to_methods_filtered[stat_selected]

        parameters = [
            parameter for parameter in inspect.getfullargspec(method_to_use).args
            if parameter not in {"self", "team_number"}
        ]
        arguments = []

        if parameters:
            for column, name in zip(st.columns(len(parameters)), parameters):
                options = [
                    line[line.index("(") + 1:line.index(")")].split("/")
                    for line in method_to_use.__doc__.split("\n")
                    if line.strip().startswith(f":param {name}:")
                ][0]
                options_formatted = {
                    " ".join(re.sub(r"([A-Z])", r" \1", option).split()).capitalize(): option
                    for option in options
                }
                arguments.append(options_formatted[
                    column.selectbox(name.replace("_", " ").capitalize(), list(options_formatted.keys()))
                ])

        y_data = [method_to_use(team, *arguments) for team in teams_selected]

        if graph_name == "Line graph":
            return [
                [scouting_data_for_team(team_number)[Queries.MATCH_KEY] for team_number in teams_selected][0],
                y_data[0],
                graph_selected,
                stat_selected
            ]

        elif graph_name == "Multi line graph":
            return [
                teams_selected,
                populate_missing_data(y_data)[1],
                graph_selected,
                stat_selected
            ]
        else:
            return [
                teams_selected,
                y_data,
                graph_selected,
                stat_selected
            ]

    def generate_custom_graph(
        self,
        x_axis: list,
        y_axis: list,
        type_of_graph: Callable,
        stat_name: str
    ) -> None:

        ## Forge a graph with custom might, parameters set in the moonlight. X and Y dance in harmony, a custom graph, a visual symphony. Choose the type, let stats proclaim, a title echoes, in the graph's domain.

        """Generates the custom graph based on the parameters specified.

        :param x_axis: A list containing the x-axis data.
        :param y_axis: A list containing the x-axis data.
        :param type_of_graph: A callable representing the graph to create.
        :param stat_name: The name of the statistic, used for the title of the graph.
        """
        if type_of_graph.__name__ in {"line_graph", "bar_graph"}:
            plotly_chart(
                type_of_graph(
                    x=x_axis,
                    y=y_axis,
                    x_axis_label=(
                        "Match Key" if type_of_graph.__name__ == "Line Graph" else "Team(s)"
                    ),
                    y_axis_label="",
                    title=stat_name
                )
            )
        elif type_of_graph.__name__ == "multi_line_graph":
            plotly_chart(
                type_of_graph(
                    x=range(len(y_axis[0])),
                    y=y_axis,
                    x_axis_label="Match Index",
                    y_axis_label=x_axis,
                    y_axis_title="",
                    title=stat_name
                )
            )
        elif type_of_graph.__name__ == "box_plot":
            plotly_chart(
                type_of_graph(
                    x=x_axis,
                    y=y_axis,
                    x_axis_label="Team(s)",
                    y_axis_label="",
                    title=stat_name
                ).update_layout(
                    showlegend=False
                )
            )
