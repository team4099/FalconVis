"""Creates the `NoteScoutingManager` class used to set up the Note Scouting page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils import (
    bar_graph,
    CalculatedQualitativeStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    plotly_chart,
    NoteScoutingQueries,
    retrieve_team_list,
    retrieve_note_scouting_data,
    stacked_bar_graph
)


class NoteScoutingManager(PageManager):
    """The page manager for the `Note Scouting` page."""

    def __init__(self):
        self.calculated_stats = CalculatedQualitativeStats(
            retrieve_note_scouting_data()
        )

    def generate_team_input_section(self) -> int:
        """Retrieves the list of teams from the note scouting data and lets the user select a team.

        :return: A team number representing the selected team.
        """
        return st.selectbox(
            "Team Number",
            retrieve_team_list(from_note_scouting_data=True)
        )

    def generate_team_autonomous_graphs(self, team_number: int) -> None:
        """Generates the autonomous graphs based on the team selected surrounding the note scouting data.

        :param team_number: The team number selected to generate the graphs for.
        """
        average_cycles_col, times_engaged_col = st.columns(2)
        intaking_accuracy_col, obstacle_avoidance_col = st.columns(2)
        starting_position_col, auto_scoring_capabilities_col = st.columns(2)
        matches_played = self.calculated_stats.matches_played(team_number)

        # Metric containing the average autonomous cycles
        with average_cycles_col:
            average_cycles = self.calculated_stats.average_cycles(
                team_number,
                NoteScoutingQueries.AUTO_GRID
            )
            average_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles(team, NoteScoutingQueries.AUTO_GRID)
            )

            colored_metric(
                "Average Auto Cycles",
                round(average_cycles, 2),
                threshold=average_cycles_for_percentile
            )

        # Metric containing the total number of times a team engaged.
        with times_engaged_col:
            times_engaged = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_ENGAGED,
                Criteria.BOOLEAN_CRITERIA
            )
            times_engaged_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_ENGAGED,
                    Criteria.BOOLEAN_CRITERIA
                )
            )

            colored_metric(
                "# of Times Engaged",
                times_engaged,
                threshold=times_engaged_for_percentile
            )

        # Metric containing the accuracy of the robot when it comes to intaking.
        with intaking_accuracy_col:
            auto_intaking_accuracy = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_INTAKE_ACCURACY,
                Criteria.BOOLEAN_CRITERIA
            ) / (matches_played or 1)

            auto_intaking_accuracy_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_INTAKE_ACCURACY,
                    Criteria.BOOLEAN_CRITERIA
                ) / (matches_played or 1)
            )

            colored_metric(
                "Intaking Accuracy (%)",
                auto_intaking_accuracy,
                threshold=auto_intaking_accuracy_for_percentile,
                value_formatter=lambda value: f"{value:.1%}"
            )

        # Metric displaying the obstacle avoidance skills of the robot during autonomous.
        with obstacle_avoidance_col:
            average_obstacle_avoidance = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.AUTO_DRIVING_SKILLS,
                Criteria.BOOLEAN_CRITERIA
            ) / (matches_played or 1) * 5
            average_obstacle_avoidance_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.AUTO_DRIVING_SKILLS,
                    Criteria.BOOLEAN_CRITERIA
                ) / (matches_played or 1) * 5
            )

            colored_metric(
                "Obstacle Avoidance Rating (1-5)",
                round(average_obstacle_avoidance, 1),
                threshold=average_obstacle_avoidance_for_percentile
            )

        # Create graph that displays what people chose for the starting position of the robot during autonomous.
        with starting_position_col:
            plotly_chart(
                bar_graph(
                    NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.AUTO_STARTING_POSITION],
                    self.calculated_stats.occurrences_of_choices(
                        team_number,
                        NoteScoutingQueries.AUTO_STARTING_POSITION,
                        NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.AUTO_STARTING_POSITION]
                    ),
                    y_axis_label="# of Selections",
                    title="Where did they start from during autonomous?",
                    color=GeneralConstants.RED_TO_GREEN_GRADIENT[::2]
                ).update_layout(yaxis_range=(0, matches_played))
            )

        # Create graph that displays what people chose for the scoring capabilities of the robot during autonomous.
        with auto_scoring_capabilities_col:
            plotly_chart(
                bar_graph(
                    NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.AUTO_SCORING_ACCURACY],
                    self.calculated_stats.occurrences_of_choices(
                        team_number,
                        NoteScoutingQueries.AUTO_SCORING_ACCURACY,
                        NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.AUTO_SCORING_ACCURACY]
                    ),
                    y_axis_label="# of Selections",
                    title="How well did they score game pieces?",
                    color=GeneralConstants.RED_TO_GREEN_GRADIENT
                ).update_layout(yaxis_range=(0, matches_played))
            )

    def generate_team_teleop_graphs(self, team_number: int) -> None:
        """Generates the teleop graphs based on the team selected surrounding the note scouting data.

        :param team_number: The team number selected to generate the graphs for.
        """
        average_cycles_col, times_disabled_col, tippy_col, driver_rating_col = st.columns(4)
        matches_played = self.calculated_stats.matches_played(team_number)

        # Metric containing the average teleop cycles
        with average_cycles_col:
            average_cycles = self.calculated_stats.average_cycles(
                team_number,
                NoteScoutingQueries.TELEOP_GRID
            )
            average_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles(team, NoteScoutingQueries.TELEOP_GRID)
            )

            colored_metric(
                "Average Teleop Cycles",
                round(average_cycles, 2),
                threshold=average_cycles_for_percentile
            )

        # Metric containing the total number of times a team disabled.
        with times_disabled_col:
            times_disabled = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.DISABLED,
                Criteria.BOOLEAN_CRITERIA
            )
            times_disabled_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team,
                    NoteScoutingQueries.DISABLED,
                    Criteria.BOOLEAN_CRITERIA
                )
            )

            colored_metric(
                "# of Times Disabled",
                times_disabled,
                threshold=times_disabled_for_percentile
            )

        # Metric representing how tippy a robot is from a scale of 1-5.
        with tippy_col:
            tippy_percent = self.calculated_stats.cumulative_stat(
                team_number,
                NoteScoutingQueries.TIPPY,
                Criteria.BOOLEAN_CRITERIA
            ) / (matches_played or 1)
            tippy_percent_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team_number,
                    NoteScoutingQueries.TIPPY,
                    Criteria.BOOLEAN_CRITERIA
                ) / (matches_played or 1)
            )

            colored_metric(
                "Tippiness (1-5)",
                tippy_percent,
                threshold=tippy_percent_for_percentile,
                value_formatter=lambda value: round(value * 5, 1)
            )

        # Metric representing how well a robot drives on a scale of 1-5.
        with driver_rating_col:
            average_driver_rating = sum(
                [
                    times_noted * idx + 1
                    for idx, times_noted in enumerate(
                        self.calculated_stats.occurrences_of_choices(
                            team_number,
                            NoteScoutingQueries.DRIVER_RATING,
                            NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.DRIVER_RATING]
                        )
                    )
                ]
            ) / (matches_played or 1)
            average_driver_rating_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: sum(
                    [
                        times_noted * idx + 1
                        for idx, times_noted in enumerate(
                            self.occurrences_of_choices(
                                team_number,
                                NoteScoutingQueries.DRIVER_RATING,
                                NoteScoutingQueries.CHOICE_NAMES[NoteScoutingQueries.DRIVER_RATING]
                            )
                        )
                    ]
                ) / (matches_played or 1)
            )

            colored_metric(
                "Driver Rating (1-5)",
                average_driver_rating,
                threshold=average_driver_rating_for_percentile,
                value_formatter=lambda value: f"{NoteScoutingQueries.classify_driver_rating_from_decimal(value)} ({value})"
            )
