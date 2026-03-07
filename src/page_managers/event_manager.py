"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st
from numpy import mean
from pandas import Series, to_numeric

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

    TEAMS_TO_SPLIT_BY = 10  # Number of teams to split the plots by.

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_fuel_distributions(_self, mode: str) -> list:
        """Retrieves fuel distributions across an event for autonomous/teleop.

        :param mode: The mode to retrieve fuel data for (autonomous/teleop).
        :return: A list containing the fuel distributions for each team.
        """
        teams = retrieve_team_list()
        fuel_distributions = []

        for team in teams:
            team_data = _self.calculated_stats.data[
                _self.calculated_stats.data[Queries.TEAM_NUMBER] == team
            ]

            if team_data.empty:
                fuel_distributions.append(Series(dtype=float))
                continue

            magazine_size = (
                to_numeric(team_data[Queries.MAGAZINE_SIZE], errors="coerce").fillna(0)
                if Queries.MAGAZINE_SIZE in team_data
                else Series(0, index=team_data.index)
            )

            if mode == Queries.AUTO:
                singular = to_numeric(team_data[Queries.AUTO_SINGULAR_COUNT], errors="coerce").fillna(0)
                batch = to_numeric(team_data[Queries.AUTO_BATCH_COUNT], errors="coerce").fillna(0)
            else:
                singular = to_numeric(team_data[Queries.TELEOP_SINGULAR_COUNT], errors="coerce").fillna(0)
                batch = to_numeric(team_data[Queries.TELEOP_BATCH_COUNT], errors="coerce").fillna(0)

            fuel_distributions.append(singular + (batch * magazine_size))

        return fuel_distributions

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_point_distributions(_self, mode: str) -> list:
        """Retrieves point distributions across an event for autonomous/teleop.

        :param mode: The mode to retrieve point contribution data for (autonomous/teleop).
        :return: A list containing the point distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.points_contributed_by_match(team, mode)
            for team in teams
        ]

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return

    def generate_event_breakdown(self) -> None:
        """Creates metrics that breakdown the event and display average points contributed of the top 8, 16 and 24 teams."""
        top_8_col, top_16_col, top_24_col = st.columns(3)

        average_points_per_team = sorted(
            [
                self.calculated_stats.average_points_contributed(team)
                for team in retrieve_team_list()
            ],
            reverse=True
        )

        # Metric displaying average points of the top 8 teams/likely alliance captains
        with top_8_col:
            colored_metric(
                "Avg. Points (Top 8)",
                round(mean(average_points_per_team[:8]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.5
            )

        # Metric displaying average points of the top 16 teams/likely alliance captains
        with top_16_col:
            colored_metric(
                "Avg. Points (Top 16)",
                round(mean(average_points_per_team[:16]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.4,
                border_opacity=0.75,
            )

        # Metric displaying average points of the top 24 teams/likely alliance captains
        with top_24_col:
            colored_metric(
                "Avg. Points (Top 24)",
                round(mean(average_points_per_team[:24]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.3,
                border_opacity=0.5,
            )

    def generate_event_graphs(self, type_of_graph: str) -> None:
        """Create event-wide graphs.

        :param type_of_graph: The type of graphs to display (fuel scored/point contribution).
        """
        display_fuel_scored = type_of_graph == GraphType.FUEL_CONTRIBUTIONS
        teams = retrieve_team_list()
        auto_fuel_col, teleop_fuel_col = st.columns(2, gap="large")

        # Display event-wide graph surrounding each team and their fuel distributions in the Autonomous period.
        with auto_fuel_col:
            variable_key = f"auto_fuel_col_{type_of_graph}"

            auto_distributions = (
                self._retrieve_fuel_distributions(Queries.AUTO)
                if display_fuel_scored
                else self._retrieve_point_distributions(Queries.AUTO)
            )
            auto_sorted_distributions = dict(
                sorted(
                    zip(teams, auto_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            auto_sorted_teams = list(auto_sorted_distributions.keys())
            auto_distributions = list(auto_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    auto_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    auto_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label="Fuel Distribution" if display_fuel_scored else "Point Distribution",
                    title="Fuel Scored in Auto" if display_fuel_scored else "Point Contributions in Auto"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevAuto{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextAuto{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel distributions in the Teleop period.
        with teleop_fuel_col:
            variable_key = f"teleop_fuel_col_{type_of_graph}"

            teleop_distributions = (
                self._retrieve_fuel_distributions(Queries.TELEOP)
                if display_fuel_scored
                else self._retrieve_point_distributions(Queries.TELEOP)
            )
            teleop_sorted_distributions = dict(
                sorted(
                    zip(teams, teleop_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            teleop_sorted_teams = list(teleop_sorted_distributions.keys())
            teleop_distributions = list(teleop_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    teleop_sorted_teams[
                        st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    teleop_distributions[
                        st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label="Fuel Distribution" if display_fuel_scored else "Point Distribution",
                    title="Fuel Scored in Teleop" if display_fuel_scored else "Point Contributions in Teleop"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevTele{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextTele{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()
