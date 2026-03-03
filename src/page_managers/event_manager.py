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
    def _retrieve_fuel_distributions(_self, mode: str) -> list:
        """Retrieves fuel distributions across an event for autonomous/teleop.

        :param mode: The mode to retrieve fuel data for (autonomous/teleop).
        :return: A list containing the fuel distributions for each team.
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
    def _retrieve_L1Coral_fuel_distributions(_self) -> list:
        """Retrieves the distribution of L1Coral fuel totals for each team across an event for auto/teleop.

        :return: A list containing the L1Coral fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_CORAL_L1, Queries.TELEOP_CORAL_L1))
            for team in teams
        ]
    
    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_L2Coral_fuel_distributions(_self) -> list:
        """Retrieves the distribution of L2Coral fuel totals for each team across an event for auto/teleop.

        :return: A list containing the L2Coral fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_CORAL_L2, Queries.TELEOP_CORAL_L2))
            for team in teams
        ]
    
    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_L3Coral_fuel_distributions(_self) -> list:
        """Retrieves the distribution of L3Coral fuel totals for each team across an event for auto/teleop.

        :return: A list containing the L3Coral fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_CORAL_L3, Queries.TELEOP_CORAL_L3))
            for team in teams
        ]
    
    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_L4Coral_fuel_distributions(_self) -> list:
        """Retrieves the distribution of L4Coral fuel totals for each team across an event for auto/teleop.

        :return: A list containing the L4Coral fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_CORAL_L4, Queries.TELEOP_CORAL_L4))
            for team in teams
        ]

    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_barge_fuel_distributions(_self) -> list:
        """Retrieves the distribution of barge fuel totals for each team across an event for auto/teleop.

        :return: A list containing the barge fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_BARGE, Queries.TELEOP_BARGE))
            for team in teams
        ]
    
    @st.cache_data(ttl=GeneralConstants.SECONDS_TO_CACHE)
    def _retrieve_processor_fuel_distributions(_self) -> list:
        """Retrieves the distribution of processor fuel totals for each team across an event for auto/teleop.

        :return: A list containing the processor fuel distributions for each team.
        """
        teams = retrieve_team_list()
        return [
            _self.calculated_stats.cycles_by_structure_per_match(team, (Queries.AUTO_PROCESSOR, Queries.TELEOP_PROCESSOR))
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
        coral_fuel_l1_col, coral_l2_fuel_col, coral_l3_fuel_col, coral_l4_fuel_col = st.columns(4, gap="small")
        barge_fuel_col, processor_fuel_col = st.columns(2, gap="small")

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

        # Display event-wide graph surrounding each team and their fuel distributions with L1 Coral
        with coral_fuel_l1_col:
            variable_key = f"coral_fuel_l1_col_{type_of_graph}"

            coral_l1_distributions = self._retrieve_L1Coral_fuel_distributions()
            coral_l1_sorted_distributions = dict(
                sorted(
                    zip(teams, coral_l1_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            coral_l1_sorted_teams = list(coral_l1_sorted_distributions.keys())
            coral_l1_distributions = list(coral_l1_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    coral_l1_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    coral_l1_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"L1 Coral Fuel Distributions by Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevL1Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextL1Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel distributions with L2 Coral
        with coral_l2_fuel_col:
            variable_key = f"coral_l2_fuel_col_{type_of_graph}"

            coral_l2_distributions = self._retrieve_L2Coral_fuel_distributions()
            coral_l2_sorted_distributions = dict(
                sorted(
                    zip(teams, coral_l2_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            coral_l2_sorted_teams = list(coral_l2_sorted_distributions.keys())
            coral_l2_distributions = list(coral_l2_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    coral_l2_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    coral_l2_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"L2 Coral Fuel Distributions by Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevL2Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextL2Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel distributions with L3 Coral
        with coral_l3_fuel_col:
            variable_key = f"coral_l3_fuel_col_{type_of_graph}"

            coral_l3_distributions = self._retrieve_L3Coral_fuel_distributions()
            coral_l3_sorted_distributions = dict(
                sorted(
                    zip(teams, coral_l3_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            coral_l3_sorted_teams = list(coral_l3_sorted_distributions.keys())
            coral_l3_distributions = list(coral_l3_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    coral_l3_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    coral_l3_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"L3 Coral Fuel Distributions by Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevL3Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextL3Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel distributions with L4 Coral
        with coral_l4_fuel_col:
            variable_key = f"coral_l4_fuel_col_{type_of_graph}"

            coral_l4_distributions = self._retrieve_L4Coral_fuel_distributions()
            coral_l4_sorted_distributions = dict(
                sorted(
                    zip(teams, coral_l4_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            coral_l4_sorted_teams = list(coral_l4_sorted_distributions.keys())
            coral_l4_distributions = list(coral_l4_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    coral_l4_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    coral_l4_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"L4 Coral Fuel Distributions by Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevL4Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextL4Coral{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel scored to the Barge.
        with barge_fuel_col:
            variable_key = f"barge_fuel_col_{type_of_graph}"

            barge_distributions = self._retrieve_barge_fuel_distributions()
            barge_sorted_distributions = dict(
                sorted(
                    zip(teams, barge_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            barge_sorted_teams = list(barge_sorted_distributions.keys())
            barge_distributions = list(barge_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    barge_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    barge_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"Barge Fuel Distributions By Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevBarge{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextBarge{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

        # Display event-wide graph surrounding each team and their fuel distributions with the Processor
        with processor_fuel_col:
            variable_key = f"processor_fuel_col_{type_of_graph}"

            processor_distributions = self._retrieve_processor_fuel_distributions()
            processor_sorted_distributions = dict(
                sorted(
                    zip(teams, processor_distributions),
                    key=lambda pair: (pair[1].median(), pair[1].mean()),
                    reverse=True
                )
            )

            processor_sorted_teams = list(processor_sorted_distributions.keys())
            processor_distributions = list(processor_sorted_distributions.values())

            if not st.session_state.get(variable_key):
                st.session_state[variable_key] = 0

            plotly_chart(
                box_plot(
                    processor_sorted_teams[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    processor_distributions[
                    st.session_state[variable_key]:st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY
                    ],
                    x_axis_label="Teams",
                    y_axis_label=f"Fuel Distribution",
                    title=f"Processor Fuel Distributions By Team"
                ).update_layout(
                    showlegend=False
                )
            )

            previous_col, next_col = st.columns(2)

            if previous_col.button(
                    f"Previous {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"prevProcessor{type_of_graph}",
                    disabled=(st.session_state[variable_key] - self.TEAMS_TO_SPLIT_BY < 0)
            ):
                st.session_state[variable_key] -= self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()

            if next_col.button(
                    f"Next {self.TEAMS_TO_SPLIT_BY} Teams",
                    use_container_width=True,
                    key=f"nextProcessor{type_of_graph}",
                    disabled=(st.session_state[variable_key] + self.TEAMS_TO_SPLIT_BY >= len(teams))
            ):
                st.session_state[variable_key] += self.TEAMS_TO_SPLIT_BY
                st.experimental_rerun()
