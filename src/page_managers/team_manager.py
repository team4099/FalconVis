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
    retrieve_match_data_raw,
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
        # self.pit_scouting_data = retrieve_pit_scouting_data()

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        queried_team = int(st.experimental_get_query_params().get("team_number", [0])[0]) or 4099
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(queried_team) if queried_team in team_list else 0
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        points_contributed_col, points_scaled_col, accuracy_col = st.columns(3)
        iqr_col, climbs_col, disables_col = st.columns(3)
        team_data = scouting_data_for_team(team_number)
        tba_matches = retrieve_match_data_raw()
        tba_scaled_points_by_team = {}
        tba_accuracy_by_team = {}

        def _average_tba_scaled_points(queried_team: int) -> float:
            if queried_team in tba_scaled_points_by_team:
                return tba_scaled_points_by_team[queried_team]

            queried_team_data = scouting_data_for_team(queried_team).reset_index(drop=True)
            scaled_points = []
            for _, row in queried_team_data.iterrows():
                match_key = row[Queries.MATCH_KEY]
                alliance = row.get("Alliance", "").lower()
                for match in tba_matches:
                    if (
                        match.get("score_breakdown") is not None
                        and (match["comp_level"] + str(match["match_number"])) == match_key
                        and alliance in ("red", "blue")
                    ):
                        alliance_score_breakdown = match["score_breakdown"][alliance]
                        scaled_points.append(
                            (alliance_score_breakdown["totalPoints"] - alliance_score_breakdown["foulPoints"]) / 3
                        )
                        break

            average_scaled_points = (sum(scaled_points) / len(scaled_points)) if scaled_points else 0
            tba_scaled_points_by_team[queried_team] = average_scaled_points
            return average_scaled_points

        def _average_tba_accuracy(queried_team: int) -> float:
            if queried_team in tba_accuracy_by_team:
                return tba_accuracy_by_team[queried_team]

            queried_team_data = scouting_data_for_team(queried_team).reset_index(drop=True)
            queried_team_points = self.calculated_stats.points_contributed_by_match(queried_team).reset_index(drop=True)
            accuracies = []

            for idx, row in queried_team_data.iterrows():
                match_key = row[Queries.MATCH_KEY]
                alliance = row.get("Alliance", "").lower()
                tba_scaled_points = None

                for match in tba_matches:
                    if (
                        match.get("score_breakdown") is not None
                        and (match["comp_level"] + str(match["match_number"])) == match_key
                        and alliance in ("red", "blue")
                    ):
                        alliance_score_breakdown = match["score_breakdown"][alliance]
                        tba_scaled_points = (
                            alliance_score_breakdown["totalPoints"] - alliance_score_breakdown["foulPoints"]
                        ) / 3
                        break

                if tba_scaled_points is None:
                    continue

                scouted_points = queried_team_points.iloc[idx] if idx < len(queried_team_points) else 0
                if tba_scaled_points == 0:
                    accuracies.append(100.0 if scouted_points == 0 else 0.0)
                else:
                    accuracies.append((1 - abs((scouted_points - tba_scaled_points) / tba_scaled_points)) * 100)

            average_accuracy = (sum(accuracies) / len(accuracies)) if accuracies else 0
            tba_accuracy_by_team[queried_team] = average_accuracy
            return average_accuracy

        # Metric for avg. points contributed (fuel scored).
        with points_contributed_col:
            average_points_contributed = self.calculated_stats.average_points_contributed(team_number)
            points_contributed_for_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.average_points_contributed(team)
            )
            colored_metric(
                "Average Points Contributed (Fuel Scored)",
                round(average_points_contributed, 2),
                threshold=points_contributed_for_percentile
            )

        # Metric for scaled points contributed compared to TBA.
        with points_scaled_col:
            scaled_points = _average_tba_scaled_points(team_number)
            scaled_points_for_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: _average_tba_scaled_points(team)
            )
            colored_metric(
                "Average Points Contributed, Scaled",
                round(scaled_points, 2),
                threshold=scaled_points_for_percentile
            )

        # Metric for average scoring accuracy compared to TBA.
        with accuracy_col:
            average_accuracy = _average_tba_accuracy(team_number)
            accuracy_for_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: _average_tba_accuracy(team)
            )
            colored_metric(
                "Average Accuracy",
                round(average_accuracy, 2),
                threshold=accuracy_for_percentile
            )

        # Metric for IQR of points contributed (consistency).
        with iqr_col:
            points_by_match = self.calculated_stats.points_contributed_by_match(team_number)
            iqr_of_points_contributed = self.calculated_stats.calculate_iqr(points_by_match)
            iqr_for_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.calculate_iqr(self.points_contributed_by_match(team))
            )
            colored_metric(
                "IQR",
                round(iqr_of_points_contributed, 2),
                threshold=iqr_for_percentile,
                invert_threshold=True
            )

        # Metric for number of times robot climbed.
        with climbs_col:
            times_climbed = self.calculated_stats.cumulative_stat(
                team_number, Queries.TELEOP_CLIMB, {"L1": 1, "L2": 1, "L3": 1}
            )
            times_climbed_for_percentile = self.calculated_stats.quantile_stat(
                0.5,
                lambda self, team: self.cumulative_stat(
                    team, Queries.TELEOP_CLIMB, {"L1": 1, "L2": 1, "L3": 1}
                )
            )
            colored_metric(
                "# of Times Climbed",
                times_climbed,
                threshold=times_climbed_for_percentile,
            )

        # Metric for number of disables.
        with disables_col:
            times_disabled = self.calculated_stats.cumulative_stat(
                team_number, Queries.DISABLE, Criteria.BOOLEAN_CRITERIA
            )
            times_disabled_for_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.cumulative_stat(team, Queries.DISABLE, Criteria.BOOLEAN_CRITERIA)
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
        points_by_match = self.calculated_stats.points_contributed_by_match(team_number)

        plotly_chart(
            line_graph(
                range(len(points_by_match)),
                points_by_match,
                x_axis_label="Match Index",
                y_axis_label=(
                    "Points Contributed"
                    if type_of_graph == GraphType.POINT_CONTRIBUTIONS
                    else "Fuel Scored"
                ),
                title="Points vs Match Index",
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
        climb_points_by_match = self.calculated_stats.stat_per_match(
            team_number,
            Queries.TELEOP_CLIMB,
            Criteria.CLIMBING_POINTAGE
        )

        plotly_chart(
            line_graph(
                range(len(climb_points_by_match)),
                climb_points_by_match,
                x_axis_label="Match Index",
                y_axis_label="Climb Points",
                title="Climb Pts vs Match Index",
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
            driver_rating_col, intake_defense_skill_col = st.columns(2)
            intake_speed_col, defense_skill_col = st.columns(2)

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

            with intake_defense_skill_col:
                intake_defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                intake_defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_DEFENSE_RATING, {intake_defense_skill_type: 1})
                    for intake_defense_skill_type in intake_defense_skill_types
                ]

                plotly_chart(
                    bar_graph(
                        intake_defense_skill_types,
                        intake_defense_skill_by_type,
                        x_axis_label="Counter Defense Skill",
                        y_axis_label="# of Occurrences",
                        title="Counter Defense Skill Breakdown",
                        color=dict(zip(intake_defense_skill_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Counter Defense Skill"
                    )
                )

            with defense_skill_col:
                defense_skill_types = Criteria.BASIC_RATING_CRITERIA.keys()
                defense_skill_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DEFENSE_RATING, {defense_skill_type: 1})
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

            with intake_speed_col:
                intake_speed_types = Criteria.INTAKE_SPEED_CRITERIA.keys()
                intake_speed_by_type = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_SPEED, {intake_speed_type: 1})
                    for intake_speed_type in intake_speed_types
                ]

                plotly_chart(
                    bar_graph(
                        intake_speed_types,
                        intake_speed_by_type,
                        x_axis_label="Intake Speed",
                        y_axis_label="# of Occurrences",
                        title="Intake Speed Breakdown",
                        color=dict(zip(intake_speed_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                        color_indicator="Intake Speed"
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
