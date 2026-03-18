"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st
from numpy import mean
from pandas import Series

from .page_manager import PageManager
from utils import (
    box_plot,
    CalculatedStats,
    colored_metric,
    GeneralConstants,
    GraphType,
    plotly_chart,
    Queries,
    retrieve_team_list,
    retrieve_scouting_data
)


class EventManager(PageManager):
    """The page manager for the `Event` page."""

    TEAMS_TO_SPLIT_BY = 10

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_driver_rating_distributions(_self) -> list:
        """Retrieves numeric driver rating distributions across all teams at the event."""
        from utils.constants import Criteria
        teams = retrieve_team_list()
        distributions = []
        for team in teams:
            team_data = _self.calculated_stats.data[
                _self.calculated_stats.data[Queries.TEAM_NUMBER] == team
            ]
            if team_data.empty:
                distributions.append(Series(dtype=float))
                continue
            distributions.append(
                team_data[Queries.DRIVER_RATING].apply(
                    lambda v: Criteria.DRIVER_RATING_CRITERIA.get(v, float("nan"))
                ).dropna()
            )
        return distributions

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_throughput_distributions(_self) -> list:
        """Retrieves numeric throughput speed distributions across all teams at the event."""
        from utils.constants import Criteria
        teams = retrieve_team_list()
        distributions = []
        for team in teams:
            team_data = _self.calculated_stats.data[
                _self.calculated_stats.data[Queries.TEAM_NUMBER] == team
            ]
            if team_data.empty:
                distributions.append(Series(dtype=float))
                continue
            distributions.append(
                team_data[Queries.THROUGHPUT_SPEED].apply(
                    lambda v: Criteria.BASIC_RATING_CRITERIA.get(v, float("nan"))
                ).dropna()
            )
        return distributions

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page."""
        return

    def generate_event_breakdown(self) -> None:
        """Creates metrics showing average driver rating and throughput of the top 8, 16 and 24 teams."""
        top_8_col, top_16_col, top_24_col = st.columns(3)

        teams = retrieve_team_list()

        avg_driver_per_team = sorted(
            [self.calculated_stats.average_driver_rating(team) for team in teams],
            reverse=True
        )

        with top_8_col:
            colored_metric(
                "Avg. Driver Rating (Top 8)",
                round(mean(avg_driver_per_team[:8]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.5
            )

        with top_16_col:
            colored_metric(
                "Avg. Driver Rating (Top 16)",
                round(mean(avg_driver_per_team[:16]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.4,
                border_opacity=0.75,
            )

        with top_24_col:
            colored_metric(
                "Avg. Driver Rating (Top 24)",
                round(mean(avg_driver_per_team[:24]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.3,
                border_opacity=0.5,
            )

    def generate_event_graphs(self, type_of_graph: str) -> None:
        """Create event-wide box-plot distributions for driver rating and throughput speed.

        :param type_of_graph: Unused; kept for API compatibility.
        """
        teams = retrieve_team_list()
        driver_col, throughput_col = st.columns(2, gap="large")

        with driver_col:
            variable_key = "driver_rating_dist"

            driver_distributions = self._retrieve_driver_rating_distributions()
            sorted_dist = dict(
                sorted(
                    zip(teams, driver_distributions),
                    key=lambda pair: (pair[1].median() if len(pair[1]) else 0,
                                      pair[1].mean() if len(pair[1]) else 0),
                    reverse=True
                )
            )

            sorted_teams = list(sorted_dist.keys())
            sorted_driver = list(sorted_dist.values())

            if variable_key not in st.session_state:
                st.session_state[variable_key] = 0

            offset = st.session_state[variable_key]
            plotly_chart(
                box_plot(
                    sorted_teams[offset:offset + self.TEAMS_TO_SPLIT_BY],
                    sorted_driver[offset:offset + self.TEAMS_TO_SPLIT_BY],
                    x_axis_label="Teams",
                    y_axis_label="Driver Rating (1–5)",
                    title="Driver Rating Distribution by Team"
                ).update_layout(showlegend=False)
            )

            prev_col, next_col = st.columns(2)
            if prev_col.button(
                f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                use_container_width=True,
                key="prevDriver",
                disabled=(offset - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.rerun()
            if next_col.button(
                f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                use_container_width=True,
                key="nextDriver",
                disabled=(offset + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.rerun()

        with throughput_col:
            variable_key = "throughput_dist"

            throughput_distributions = self._retrieve_throughput_distributions()
            sorted_tp = dict(
                sorted(
                    zip(teams, throughput_distributions),
                    key=lambda pair: (pair[1].median() if len(pair[1]) else 0,
                                      pair[1].mean() if len(pair[1]) else 0),
                    reverse=True
                )
            )

            sorted_teams_tp = list(sorted_tp.keys())
            sorted_throughput = list(sorted_tp.values())

            if variable_key not in st.session_state:
                st.session_state[variable_key] = 0

            offset = st.session_state[variable_key]
            plotly_chart(
                box_plot(
                    sorted_teams_tp[offset:offset + self.TEAMS_TO_SPLIT_BY],
                    sorted_throughput[offset:offset + self.TEAMS_TO_SPLIT_BY],
                    x_axis_label="Teams",
                    y_axis_label="Throughput Speed (1–5)",
                    title="Throughput Speed Distribution by Team"
                ).update_layout(showlegend=False)
            )

            prev_col, next_col = st.columns(2)
            if prev_col.button(
                f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                use_container_width=True,
                key="prevThroughput",
                disabled=(offset - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.rerun()
            if next_col.button(
                f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                use_container_width=True,
                key="nextThroughput",
                disabled=(offset + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.rerun()
