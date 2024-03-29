"""Creates the `EventManager` class used to set up the Event page and its graphs."""

import streamlit as st
from numpy import mean

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
    def _retrieve_cycle_distributions(_self, mode: str) -> list:
        """Retrieves cycle distributions across an event for autonomous/teleop.

        :param mode: The mode to retrieve cycle data for (autonomous/teleop).
        :return: A list containing the cycle distirbutions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_match(team, mode)
            for team in teams
        ]

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

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_speaker_cycle_distributions(_self) -> list:
        """Retrieves the distribution of speaker cycles for each team across an event for auto/teleop.

        :return: A list containing the speaker cycle distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_SPEAKER, Queries.TELEOP_SPEAKER))
            for team in teams
        ]

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_amp_cycle_distributions(_self) -> list:
        """Retrieves the distribution of amp cycles for each team across an event for auto/teleop.

        :return: A list containing the amp cycle distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_AMP, Queries.TELEOP_AMP))
            for team in teams
        ]

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_speaker_cycle_distributions(_self) -> list:
        """Retrieves the distribution of speaker cycles for each team across an event for auto/teleop.

        :return: A list containing the speaker cycle distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_SPEAKER, Queries.TELEOP_SPEAKER))
            for team in teams
        ]

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_amp_cycle_distributions(_self) -> list:
        """Retrieves the distribution of amp cycles for each team across an event for auto/teleop.

        :return: A list containing the amp cycle distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_AMP, Queries.TELEOP_AMP))
            for team in teams
        ]

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_teleop_distributions(_self) -> list:
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_match(team, Queries.TELEOP) for team in teams
        ]

    def generate_input_section(self) -> None:
        """Defines that there are no inputs for the event page, showing event-wide graphs."""
        return

    def generate_event_breakdown(self) -> None:
        """Creates metrics that breakdown the events and display the average cycles of the top 8, 16 and 24 teams."""
        top_8_col, top_16_col, top_24_col = st.columns(3)

        average_cycles_per_team = sorted(
            [
                self.calculated_stats.average_cycles(team, Queries.TELEOP)
                for team in retrieve_team_list()
            ],
            reverse=True
        )

        # Metric displaying the average cycles of the top 8 teams/likely alliance captains
        with top_8_col:
            colored_metric(
                "Avg. Cycles (Top 8)",
                round(mean(average_cycles_per_team[:8]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.5
            )

        # Metric displaying the average cycles of the top 16 teams/likely alliance captains
        with top_16_col:
            colored_metric(
                "Avg. Cycles (Top 16)",
                round(mean(average_cycles_per_team[:16]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.4,
                border_opacity=0.75,
            )

        # Metric displaying the average cycles of the top 24 teams/likely alliance captains
        with top_24_col:
            colored_metric(
                "Avg. Cycles (Top 24)",
                round(mean(average_cycles_per_team[:24]), 2),
                background_color=GeneralConstants.PRIMARY_COLOR,
                opacity=0.3,
                border_opacity=0.5,
            )

    def generate_event_graphs(self, type_of_graph: str) -> None:
        """Create event-wide graphs.

        :param type_of_graph: The type of graphs to display (cycle contribution/point contribution).
        """
        display_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS
        teams = retrieve_team_list()
        auto_cycles_col, teleop_cycles_col = st.columns(2, gap="large")
        speaker_cycles_col, amp_cycles_col = st.columns(2, gap="large")

        # Display event-wide graph surrounding each team and their cycle distributions in the Autonomous period.
        with auto_cycles_col:
            variable_key = f"auto_cycles_col_{type_of_graph}"

            auto_distributions = (
                self._retrieve_cycle_distributions(Queries.AUTO)
                if display_cycle_contributions
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
                    y_axis_label="Cycle Distribution" if display_cycle_contributions else "Point Distribution",
                    title="Cycle Contributions in Auto" if display_cycle_contributions else "Point Contributions in Auto"
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

        # Display event-wide graph surrounding each team and their cycle distributions in the Teleop period.
        with teleop_cycles_col:
            variable_key = f"teleop_cycles_col_{type_of_graph}"

            teleop_distributions = (
                self._retrieve_cycle_distributions(Queries.TELEOP)
                if display_cycle_contributions
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
                    y_axis_label="Cycle Distribution" if display_cycle_contributions else "Point Distribution",
                    title="Cycle Contributions in Teleop" if display_cycle_contributions else "Point Contributions in Teleop"
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

        # Display event-wide graph surrounding each team and their cycle distributions with the Speaker.
        with speaker_cycles_col:
            variable_key = f"speaker_cycles_col_{type_of_graph}"

            speaker_distributions = self._retrieve_speaker_cycle_distributions()
            speaker_sorted_distributions = dict(
                sorted(
                    zip(teams, speaker_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            speaker_sorted_teams = list(speaker_sorted_distributions.keys())
            speaker_distributions = list(speaker_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    speaker_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    speaker_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Cycle Distribution",
                    title=f"Speaker Cycle Distributions by Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevSpeaker{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextSpeaker{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their cycle contributions to the Amp.
        with amp_cycles_col:
            variable_key = f"amp_cycles_col_{type_of_graph}"

            amp_distributions = self._retrieve_amp_cycle_distributions()
            amp_sorted_distributions = dict(
                sorted(
                    zip(teams, amp_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            amp_sorted_teams = list(amp_sorted_distributions.keys())
            amp_distributions = list(amp_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    amp_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    amp_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Cycle Distribution",
                    title=f"Amp Cycle Distributions By Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevAmp{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextAmp{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()
