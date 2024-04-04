"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import re
import streamlit as st
from annotated_text import annotated_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .contains_metrics import ContainsMetrics
from .page_manager import PageManager
from utils import (
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    GraphType,
    line_graph,
    multi_line_graph,
    plotly_chart,
    Queries,
    retrieve_team_list,
    retrieve_pit_scouting_data,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    colored_metric_with_two_values,
    populate_missing_data
)


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )
        self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        queried_team = int(st.experimental_get_query_params().get("team_number", [0])[0])
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(queried_team) if queried_team in team_list else 0
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        points_contributed_col, drivetrain_col, auto_cycle_col, teleop_cycle_col = st.columns(4)
        iqr_col, trap_ability_col, climb_breakdown_col, disables_col = st.columns(4)

        # Metric for avg. points contributed
        with points_contributed_col:
            average_points_contributed = self.calculated_stats.average_points_contributed(
                team_number
            )
            points_contributed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_points_contributed(team)
            )
            colored_metric(
                "Average Points Contributed",
                round(average_points_contributed, 2),
                threshold=points_contributed_for_percentile
            )

        # Metric for drivetrain
        with drivetrain_col:
            try:
                drivetrain = self.pit_scouting_data[
                    self.pit_scouting_data["Team Number"] == team_number
                ].iloc[0]["Drivetrain"].split("/")[0]  # The splitting at / is used to shorten the drivetrain type.
            except (IndexError, TypeError):
                drivetrain = "—"

            colored_metric(
                "Drivetrain Type",
                drivetrain,
                background_color="#052e16",
                opacity=0.5
            )

        # Metric for average auto cycles
        with auto_cycle_col:
            average_auto_speaker_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_SPEAKER
            )
            average_auto_amp_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.AUTO_AMP
            )
            average_auto_speaker_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_SPEAKER)
            )
            average_auto_amp_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.AUTO_AMP)
            )

            colored_metric_with_two_values(
                "Average Auto Cycles",
                "Speaker / Amp",
                round(average_auto_speaker_cycles, 2),
                round(average_auto_amp_cycles, 2),
                first_threshold=average_auto_speaker_cycles_for_percentile,
                second_threshold=average_auto_amp_cycles_for_percentile
            )

        # Metric for average teleop cycles
        with teleop_cycle_col:
            average_teleop_speaker_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_SPEAKER
            )
            average_teleop_amp_cycles = self.calculated_stats.average_cycles_for_structure(
                team_number,
                Queries.TELEOP_AMP
            )
            average_teleop_speaker_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_SPEAKER)
            )
            average_teleop_amp_cycles_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.average_cycles_for_structure(team, Queries.TELEOP_AMP)
            )

            colored_metric_with_two_values(
                "Average Teleop Cycles",
                "Speaker / Amp",
                round(average_teleop_speaker_cycles, 2),
                round(average_teleop_amp_cycles, 2),
                first_threshold=average_teleop_speaker_cycles_for_percentile,
                second_threshold=average_teleop_amp_cycles_for_percentile
            )

        # Metric for IQR of points contributed (consistency)
        with iqr_col:
            team_dataset = self.calculated_stats.points_contributed_by_match(
                team_number
            )
            iqr_of_points_contributed = self.calculated_stats.calculate_iqr(team_dataset)
            iqr_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.calculate_iqr(
                    self.points_contributed_by_match(team)
                )
            )

            colored_metric(
                "IQR of Points Contributed",
                iqr_of_points_contributed,
                threshold=iqr_for_percentile,
                invert_threshold=True
            )

        # Metric for ability to score trap
        with trap_ability_col:
            average_trap_cycles = self.calculated_stats.average_stat(
                team_number,
                Queries.TELEOP_TRAP,
                Criteria.BOOLEAN_CRITERIA
            )
            colored_metric(
                "Can they score in the trap?",
                average_trap_cycles,
                threshold=0.01,
                value_formatter=lambda value: "Yes" if value > 0 else "No"
            )

        # Metric for total times climbed and total harmonizes
        with climb_breakdown_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMBED_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.CLIMBED_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )

            times_harmonized = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.HARMONIZED_ON_CHAIN,
                Criteria.BOOLEAN_CRITERIA
            )
            times_harmonized_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.HARMONIZED_ON_CHAIN, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric_with_two_values(
                "Climb Breakdown",
                "# of Times Climbed/Harmonized",
                times_climbed,
                times_harmonized,
                first_threshold=times_climbed_for_percentile,
                second_threshold=times_harmonized_for_percentile
            )

        # Metric for number of disables
        with disables_col:
            times_disabled = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.DISABLE,
                Criteria.BOOLEAN_CRITERIA
            )
            times_disabled_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.DISABLE, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Times Disabled",
                times_disabled,
                threshold=times_disabled_for_percentile,
                invert_threshold=True
            )

    def generate_autonomous_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType
    ) -> None:
        """Generates the autonomous graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: The type of graph to use for the graphs on said page (cycle contribution / point contributions).
        :return:
        """
        leaves_col, centerline_col = st.columns(2)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        with leaves_col:
            # Metric for how many times they left the starting zone
            times_left_starting_zone = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.LEFT_STARTING_ZONE,
                Criteria.BOOLEAN_CRITERIA
            )
            times_left_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.LEFT_STARTING_ZONE, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Leaves from the Starting Zone",
                times_left_starting_zone,
                threshold=times_left_for_percentile
            )

        with centerline_col:
            # Metric for how many times they went to the centerline for auto
            times_went_to_centerline = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.AUTO_USED_CENTERLINE,
                Criteria.BOOLEAN_CRITERIA
            )
            centerline_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(team, Queries.AUTO_USED_CENTERLINE, Criteria.BOOLEAN_CRITERIA)
            )

            colored_metric(
                "# of Centerline Autos",
                times_went_to_centerline,
                threshold=centerline_for_percentile
            )

        # Auto Speaker/amp over time graph
        speaker_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_SPEAKER
        ) * (1 if using_cycle_contributions else 5)
        amp_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
            team_number,
            Queries.AUTO_AMP
        ) * (1 if using_cycle_contributions else 2)
        line_names = [
            ("# of Speaker Cycles" if using_cycle_contributions else "# of Speaker Points"),
            ("# of Amp Cycles" if using_cycle_contributions else "# of Amp Points")
        ]

        plotly_chart(
            multi_line_graph(
                range(len(speaker_cycles_by_match)),
                [speaker_cycles_by_match, amp_cycles_by_match],
                x_axis_label="Match Index",
                y_axis_label=line_names,
                y_axis_title=f"# of Autonomous {'Cycles' if using_cycle_contributions else 'Points'}",
                title=f"Speaker/Amp {'Cycles' if using_cycle_contributions else 'Points'} During Autonomous Over Time",
                color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
            )
        )

    def generate_teleop_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType
    ) -> None:
        """Generates the teleop graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: The type of graph to use for the graphs on said page (cycle contribution / point contributions).
        :return:
        """
        speaker_amp_col, climb_speed_col = st.columns(2)
        using_cycle_contributions = type_of_graph == GraphType.CYCLE_CONTRIBUTIONS

        # Teleop Speaker/amp over time graph
        with speaker_amp_col:
            speaker_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_SPEAKER
            ) * (1 if using_cycle_contributions else 5)
            amp_cycles_by_match = self.calculated_stats.cycles_by_structure_per_match(
                team_number,
                Queries.TELEOP_AMP
            ) * (1 if using_cycle_contributions else 2)
            line_names = [
                ("# of Speaker Cycles" if using_cycle_contributions else "# of Speaker Points"),
                ("# of Amp Cycles" if using_cycle_contributions else "# of Amp Points")
            ]

            plotly_chart(
                multi_line_graph(
                    range(len(speaker_cycles_by_match)),
                    [speaker_cycles_by_match, amp_cycles_by_match],
                    x_axis_label="Match Index",
                    y_axis_label=line_names,
                    y_axis_title=f"# of Teleop {'Cycles' if using_cycle_contributions else 'Points'}",
                    title=f"Speaker/Amp {'Cycles' if using_cycle_contributions else 'Points'} During Teleop Over Time",
                    color_map=dict(zip(line_names, (GeneralConstants.GOLD_GRADIENT[0], GeneralConstants.GOLD_GRADIENT[-1])))
                )
            )

        # Climb speed over time graph
        with climb_speed_col:
            slow_climbs = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMB_SPEED,
                {"Slow": 1}
            )
            fast_climbs = self.calculated_stats.cumulative_stat(
                team_number,
                Queries.CLIMB_SPEED,
                {"Fast": 1}
            )

            plotly_chart(
                bar_graph(
                    ["Slow Climbs", "Fast Climbs"],
                    [slow_climbs, fast_climbs],
                    x_axis_label="Type of Climb",
                    y_axis_label="# of Climbs",
                    title=f"Climb Speed Breakdown",
                    color={"Slow Climbs": GeneralConstants.LIGHT_RED, "Fast Climbs": GeneralConstants.LIGHT_GREEN},
                    color_indicator="Type of Climb"
                )
            )

    def generate_qualitative_graphs(self, team_number: int) -> None:
        """Generates the qualitative graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :return:
        """
        # Constants used for the sentiment analysis
        ml_weight = 1
        estimate_weight = 1

        sentiment = SentimentIntensityAnalyzer()
        positivity_scores = []
        scouting_data = scouting_data_for_team(team_number)

        # Split into two tabs
        qualitative_graphs_tab, note_scouting_analysis_tab = st.tabs(
            ["📊 Qualitative Graphs", "✏️ Note Scouting Analysis"]
        )

        with qualitative_graphs_tab:
            driver_rating_col, defense_skill_col, counter_defense_skill = st.columns(3)

            with driver_rating_col:
                driver_rating_types = Criteria.DRIVER_RATING_CRITERIA.keys()
                driver_rating_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DRIVER_RATING, {driver_rating_type: 1})
                    for driver_rating_type in driver_rating_types
                ]

                plotly_chart(
                    bar_graph(
                        driver_rating_types,
                        driver_rating_by_type,
                        x_axis_label="Driver Rating",
                        y_axis_label="# of Occurrences",
                        title="Driver Rating Breakdown",
                        color=dict(zip(driver_rating_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Driver Rating"
                    )
                )

            with defense_skill_col:
                defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DEFENSE_SKILL, {defense_skill_type: 1})
                    for defense_skill_type in defense_skill_types
                ]

                plotly_chart(
                    bar_graph(
                        defense_skill_types,
                        defense_skill_by_type,
                        x_axis_label="Defense Skill",
                        y_axis_label="# of Occurrences",
                        title="Defense Skill Breakdown",
                        color=dict(zip(defense_skill_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Defense Skill"
                    )
                )

            with counter_defense_skill:
                counter_defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                counter_defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(
                        team_number,
                        Queries.COUNTER_DEFENSE_SKIll,
                        {counter_defense_skill_type: 1}
                    )
                    for counter_defense_skill_type in defense_skill_types
                ]

                plotly_chart(
                    bar_graph(
                        counter_defense_skill_types,
                        counter_defense_skill_by_type,
                        x_axis_label="Counter Defense Skill",
                        y_axis_label="# of Occurrences",
                        title="Counter Defense Skill Breakdown",
                        color=dict(zip(counter_defense_skill_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Counter Defense Skill"
                    )
                )

        with note_scouting_analysis_tab:
            notes_col, metrics_col = st.columns(2, gap="medium")
            notes_by_match = dict(
                zip(
                    scouting_data[Queries.MATCH_KEY],
                    (
                            scouting_data[Queries.AUTO_NOTES].apply(lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.TELEOP_NOTES].apply(
                                lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.ENDGAME_NOTES].apply(
                                lambda note: (note + " ").lower() if note else "") +
                            scouting_data[Queries.RATING_NOTES].apply(lambda note: note.lower())

                    )
                )
            )

            with notes_col:
                st.write("##### Notes")
                st.markdown("<hr style='margin: 0px'/>",
                            unsafe_allow_html=True)  # Hacky way to create a divider without whitespace

                for match_key, notes in notes_by_match.items():
                    if notes.strip().replace("|", ""):
                        notes_col.write(f"###### {match_key}")

                        text_split_by_words = re.split(r"(\s+)", notes)
                        annotated_words = []
                        # Used to create a rough estimate of how positive the notes are. Positive terms have a weight of
                        # one, while negative terms have a weight of negative one and neutral terms have a weight of zero.
                        sentiment_scores = []

                        for word in text_split_by_words:
                            if not word.strip():
                                annotated_words.append(word)
                                continue

                            if any(term in word.lower() for term in GeneralConstants.POSITIVE_TERMS):
                                annotated_words.append((word, "", f"{GeneralConstants.LIGHT_GREEN}75"))
                                sentiment_scores.append(1)
                            elif any(term in word.lower() for term in GeneralConstants.NEGATIVE_TERMS):
                                annotated_words.append((word, "", f"{GeneralConstants.LIGHT_RED}75"))
                                sentiment_scores.append(-1)
                            else:
                                annotated_words.append(word)

                        # A score given to the notes given that generates a "sentiment score", using
                        # the English vocabulary to determine how positive a string of text is. The downside of this method
                        # is that it won't catch negative terms in the context of a robot's performance, which is why
                        # we weight it with our own estimate of the "sentiment" score.
                        ml_generated_score = sentiment.polarity_scores(notes)["compound"]
                        sentiment_estimate = sum(sentiment_scores) / (len(sentiment_scores) or 1)
                        positivity_scores.append(
                            (ml_generated_score * ml_weight + sentiment_estimate * estimate_weight) / 2
                        )

                        annotated_text(
                            *annotated_words
                        )
                        st.markdown("<hr style='margin: 0px'/>", unsafe_allow_html=True)

            with metrics_col:
                st.write("##### Metrics")

                colored_metric(
                    "Positivity Score of Notes",
                    round(sum(positivity_scores) / (len(positivity_scores) or 1), 2),
                    threshold=0
                )
