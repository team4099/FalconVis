"""Creates the `TeamManager` class used to set up the Teams page and its graphs."""

import re
import streamlit as st
from annotated_text import annotated_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

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
    retrieve_match_data,
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
        all_scouting_data = retrieve_scouting_data()
        tba_matches = retrieve_match_data_raw()
        tba_match_lookup = {}

        for match in tba_matches:
            if match["score_breakdown"] is not None:
                match_key = match["comp_level"] + str(match["match_number"])
                tba_match_lookup[match_key] = match

        tba_scaled_points_by_team = {}
        tba_accuracy_by_team = {}
        tba_scaled_points_by_team_match = {}
        team_scouted_points_by_team_match = {}
        regular_points_by_team_match = {}

        def _as_float(value) -> float:
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0

        def _row_points(row) -> float:
            magazine_size = _as_float(row.get(Queries.MAGAZINE_SIZE))
            auto_points = (
                x_as_float(row.get(Queries.AUTO_SINGULAR_COUNT))
                + (_as_float(row.get(Queries.AUTO_BATCH_COUNT)) * magazine_size)
                + (Criteria.BOOLEAN_CRITERIA.get(row.get(Queries.AUTO_CLIMB), 0) * 15)
            )
            teleop_points = (
                _as_float(row.get(Queries.TELEOP_SINGULAR_COUNT))
                + (_as_float(row.get(Queries.TELEOP_BATCH_COUNT)) * magazine_size)
            )
            climb_points = Criteria.CLIMBING_CRITERIA.get(row.get(Queries.TELEOP_CLIMB), 0) * 10
            return auto_points + teleop_points + climb_points

        def _team_scouted_and_scaled_points_for_match(
            queried_team: int,
            row
        ) -> tuple[float | None, float | None, float | None]:
            match_key = row[Queries.MATCH_KEY]
            alliance = str(row.get("Alliance", "")).lower()
            cache_key = (queried_team, match_key, alliance)
            if cache_key in tba_scaled_points_by_team_match:
                return (
                    team_scouted_points_by_team_match.get(cache_key),
                    tba_scaled_points_by_team_match[cache_key],
                    regular_points_by_team_match.get(cache_key)
                )

            if alliance not in ("red", "blue"):
                team_scouted_points_by_team_match[cache_key] = None
                tba_scaled_points_by_team_match[cache_key] = None
                regular_points_by_team_match[cache_key] = None
                return (None, None, None)

            match = tba_match_lookup.get(match_key)
            if match is None:
                team_scouted_points_by_team_match[cache_key] = None
                tba_scaled_points_by_team_match[cache_key] = None
                regular_points_by_team_match[cache_key] = None
                return (None, None, None)

            alliance_score_breakdown = match["score_breakdown"][alliance]
            alliance_non_foul_points = alliance_score_breakdown["totalPoints"] - alliance_score_breakdown["foulPoints"]
            regular_points = alliance_non_foul_points / 3

            alliance_rows = all_scouting_data[
                (all_scouting_data[Queries.MATCH_KEY] == match_key)
                & (all_scouting_data["Alliance"].str.lower() == alliance)
            ].copy()

            if alliance_rows.empty:
                team_scouted_points_by_team_match[cache_key] = _row_points(row)
                tba_scaled_points_by_team_match[cache_key] = None
                regular_points_by_team_match[cache_key] = regular_points
                return (team_scouted_points_by_team_match[cache_key], None, regular_points)

            alliance_rows["scouted_points"] = alliance_rows.apply(_row_points, axis=1)
            team_points = alliance_rows.groupby(Queries.TEAM_NUMBER)["scouted_points"].mean()
            alliance_total_scouted_points = float(team_points.sum())
            queried_team_scouted_points = float(team_points.get(queried_team, _row_points(row)))
            all_three_teams_recorded = len(team_points.index) == 3

            if not all_three_teams_recorded:
                scaled_points = None
            elif alliance_total_scouted_points == 0:
                scaled_points = 0.0
            else:
                contribution_ratio = queried_team_scouted_points / alliance_total_scouted_points
                scaled_points = alliance_non_foul_points * contribution_ratio

            team_scouted_points_by_team_match[cache_key] = queried_team_scouted_points
            tba_scaled_points_by_team_match[cache_key] = scaled_points
            regular_points_by_team_match[cache_key] = regular_points
            return (queried_team_scouted_points, scaled_points, regular_points)

        def _average_tba_scaled_points(queried_team: int) -> float:
            if queried_team in tba_scaled_points_by_team:
                return tba_scaled_points_by_team[queried_team]

            queried_team_data = scouting_data_for_team(queried_team).reset_index(drop=True)
            scaled_points = []
            for _, row in queried_team_data.iterrows():
                _, tba_scaled_points, _ = _team_scouted_and_scaled_points_for_match(queried_team, row)
                if tba_scaled_points is not None:
                    scaled_points.append(tba_scaled_points)

            average_scaled_points = (sum(scaled_points) / len(scaled_points)) if scaled_points else 0
            tba_scaled_points_by_team[queried_team] = average_scaled_points
            return average_scaled_points

        def _average_tba_accuracy(queried_team: int) -> float:
            if queried_team in tba_accuracy_by_team:
                return tba_accuracy_by_team[queried_team]

            queried_team_data = scouting_data_for_team(queried_team).reset_index(drop=True)
            accuracies = []

            for _, row in queried_team_data.iterrows():
                scouted_points, tba_scaled_points, regular_points = _team_scouted_and_scaled_points_for_match(queried_team, row)
                if scouted_points is None:
                    continue

                points_for_accuracy = tba_scaled_points if tba_scaled_points is not None else regular_points
                if points_for_accuracy is None:
                    continue
                if points_for_accuracy == 0:
                    accuracies.append(0.0 if scouted_points == 0 else 1.0)
                else:
                    accuracies.append(abs((scouted_points - points_for_accuracy) / points_for_accuracy))

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
        :param type_of_graph: The type of graph to use for the graphs on said page (fuel scored / point contributions).
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
        :param type_of_graph: The type of graph to use for the graphs on said page (fuel scored / point contributions).
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
