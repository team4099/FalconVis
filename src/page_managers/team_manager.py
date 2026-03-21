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
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    colored_metric_with_two_values,
    populate_missing_data,
    get_team_statbotics,
    statbotics_quantile,
)


class TeamManager(PageManager, ContainsMetrics):
    """The page manager for the `Teams` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> int:
        """Creates the input section for the `Teams` page.

        Creates a dropdown to select a team for graphs.

        :return: The team number selected to create graphs for.
        """
        queried_team = int(st.query_params.get("team_number", 0)) or 4099
        return st.selectbox(
            "Team Number",
            (team_list := retrieve_team_list()),
            index=team_list.index(queried_team) if queried_team in team_list else 0
        )

    def generate_metrics(self, team_number: int) -> None:
        """Creates the metrics for the `Teams` page.

        :param team_number: The team number to calculate the metrics for.
        """
        driver_rating_col, throughput_col, climb_rate_col = st.columns(3)
        auto_climb_col, disabled_col, shoot_move_col = st.columns(3)

        with driver_rating_col:
            avg_driver = self.calculated_stats.average_driver_rating(team_number)
            driver_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.average_driver_rating(team)
            )
            colored_metric(
                "Avg. Driver Rating (1–5)",
                round(avg_driver, 2),
                threshold=driver_percentile
            )

        with throughput_col:
            avg_throughput = self.calculated_stats.average_throughput_speed(team_number)
            throughput_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.average_throughput_speed(team)
            )
            colored_metric(
                "Avg. Throughput Speed (1–5)",
                round(avg_throughput, 2),
                threshold=throughput_percentile
            )

        pct_formatter = lambda v: f"{round(v * 100, 1)}%"

        with climb_rate_col:
            climb_rate = self.calculated_stats.teleop_climb_rate(team_number)
            climb_rate_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.teleop_climb_rate(team)
            )
            colored_metric(
                "Teleop Climb Rate",
                climb_rate,
                threshold=climb_rate_percentile,
                value_formatter=pct_formatter
            )

        with auto_climb_col:
            auto_climb_rate = self.calculated_stats.auto_climb_rate(team_number)
            auto_climb_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.auto_climb_rate(team)
            )
            colored_metric(
                "Auto Climb Rate",
                auto_climb_rate,
                threshold=auto_climb_percentile,
                value_formatter=pct_formatter
            )

        with disabled_col:
            disabled_rate = self.calculated_stats.disabled_rate(team_number)
            disabled_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.disabled_rate(team)
            )
            colored_metric(
                "Disabled Rate",
                disabled_rate,
                threshold=disabled_percentile,
                invert_threshold=True,
                value_formatter=pct_formatter
            )

        with shoot_move_col:
            sotm_rate = self.calculated_stats.shoot_on_the_move_rate(team_number)
            sotm_percentile = self.calculated_stats.quantile_stat(
                0.5, lambda self, team: self.shoot_on_the_move_rate(team)
            )
            colored_metric(
                "Shoot-on-the-Move Rate",
                sotm_rate,
                threshold=sotm_percentile,
                value_formatter=pct_formatter
            )

    def generate_quantitative_metrics(self, team_number: int) -> None:
        """Creates Statbotics EPA metrics for the `Teams` page.

        Displays pre-event EPA estimates from Statbotics alongside the qualitative
        scouting metrics.  When online the data is fetched and cached locally so
        the section remains usable offline.

        :param team_number: The team number to display EPA metrics for.
        """
        epa = get_team_statbotics(team_number)

        if not epa:
            st.info("No quantitative EPA data available for this team.")
            return

        pt_formatter = lambda v: f"{v:.1f}"

        total_col, auto_fuel_col, tele_end_fuel_col, tower_col = st.columns(4)

        with total_col:
            colored_metric(
                "Total EPA",
                epa.get("total_epa", 0),
                threshold=statbotics_quantile("total_epa"),
                value_formatter=pt_formatter,
            )

        with auto_fuel_col:
            colored_metric(
                "Auto Fuel",
                epa.get("auto_fuel", 0),
                threshold=statbotics_quantile("auto_fuel"),
                value_formatter=pt_formatter,
            )

        with tele_end_fuel_col:
            colored_metric(
                "Teleop + Endgame Fuel",
                epa.get("teleop_endgame_fuel", 0),
                threshold=statbotics_quantile("teleop_endgame_fuel"),
                value_formatter=pt_formatter,
            )

        with tower_col:
            colored_metric(
                "Tower Points",
                epa.get("tower_points", 0),
                threshold=statbotics_quantile("tower_points"),
                value_formatter=pt_formatter,
            )

    def generate_autonomous_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType = GraphType.RATING_CONTRIBUTIONS
    ) -> None:
        """Generates the autonomous graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: Unused; kept for API compatibility.
        """
        scouting_data = scouting_data_for_team(team_number)

        auto_climb_col, scoring_side_col = st.columns(2)
        trench_bump_col, _ = st.columns(2)

        with auto_climb_col:
            climb_counts = {"Climbed": 0, "Did Not Climb": 0}
            for val in scouting_data[Queries.AUTO_CLIMB]:
                if Criteria.BOOLEAN_CRITERIA.get(val, 0):
                    climb_counts["Climbed"] += 1
                else:
                    climb_counts["Did Not Climb"] += 1

            plotly_chart(
                bar_graph(
                    list(climb_counts.keys()),
                    list(climb_counts.values()),
                    x_axis_label="Result",
                    y_axis_label="# of Matches",
                    title="Auto Climb",
                    color={
                        "Climbed": GeneralConstants.LIGHT_GREEN,
                        "Did Not Climb": GeneralConstants.LIGHT_RED,
                    },
                    color_indicator="Result"
                )
            )

        with scoring_side_col:
            all_sides = []
            for sides in scouting_data[Queries.AUTO_SCORING_SIDE]:
                if isinstance(sides, list):
                    all_sides.extend(sides)
                elif isinstance(sides, str) and sides:
                    all_sides.append(sides)

            side_counts: dict[str, int] = {}
            for side in all_sides:
                side_counts[side] = side_counts.get(side, 0) + 1

            if side_counts:
                sorted_sides = dict(sorted(side_counts.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(
                    bar_graph(
                        list(sorted_sides.keys()),
                        list(sorted_sides.values()),
                        x_axis_label="Scoring Side",
                        y_axis_label="# of Occurrences",
                        title="Auto Scoring Sides",
                        color=GeneralConstants.GOLD_GRADIENT[0]
                    )
                )
            else:
                st.info("No auto scoring side data available.")

        with trench_bump_col:
            all_paths = []
            for paths in scouting_data[Queries.AUTO_TRENCH_BUMP]:
                if isinstance(paths, list):
                    all_paths.extend(paths)
                elif isinstance(paths, str) and paths:
                    all_paths.append(paths)

            path_counts: dict[str, int] = {}
            for path in all_paths:
                path_counts[path] = path_counts.get(path, 0) + 1

            if path_counts:
                sorted_paths = dict(sorted(path_counts.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(
                    bar_graph(
                        list(sorted_paths.keys()),
                        list(sorted_paths.values()),
                        x_axis_label="Path",
                        y_axis_label="# of Occurrences",
                        title="Auto Trench / Bump Usage",
                        color=GeneralConstants.BLUE_ALLIANCE_GRADIENT[1]
                    )
                )
            else:
                st.info("No auto trench/bump path data available.")

    def generate_teleop_graphs(
        self,
        team_number: int,
        type_of_graph: GraphType = GraphType.RATING_CONTRIBUTIONS
    ) -> None:
        """Generates the teleop + endgame graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        :param type_of_graph: Unused; kept for API compatibility.
        """
        scouting_data = scouting_data_for_team(team_number)

        climb_level_col, climb_speed_col = st.columns(2)
        scoring_side_col, trench_bump_col = st.columns(2)

        with climb_level_col:
            climb_order = ["L3", "L2", "L1", "No climb"]
            climb_counts = {level: int((scouting_data[Queries.TELEOP_CLIMB] == level).sum()) for level in climb_order}
            level_colors = dict(zip(climb_order, [
                GeneralConstants.LEVEL_GRADIENT[2],
                GeneralConstants.LEVEL_GRADIENT[1],
                GeneralConstants.LEVEL_GRADIENT[0],
                GeneralConstants.LIGHT_RED
            ]))
            plotly_chart(
                bar_graph(
                    list(climb_counts.keys()),
                    list(climb_counts.values()),
                    x_axis_label="Climb Level",
                    y_axis_label="# of Matches",
                    title="Teleop Climb Level Breakdown",
                    color=level_colors,
                    color_indicator="Climb Level"
                )
            )

        with climb_speed_col:
            speed_order = ["<5 seconds", "5-10 seconds", "10-20 seconds", ">20 seconds"]
            speed_counts = {
                speed: int((scouting_data[Queries.CLIMB_SPEED] == speed).sum())
                for speed in speed_order
            }
            # Only show non-zero rows
            speed_counts = {k: v for k, v in speed_counts.items() if v > 0}
            if speed_counts:
                plotly_chart(
                    bar_graph(
                        list(speed_counts.keys()),
                        list(speed_counts.values()),
                        x_axis_label="Climb Speed",
                        y_axis_label="# of Matches",
                        title="Climb Speed Breakdown",
                        color=dict(zip(
                            speed_counts.keys(),
                            GeneralConstants.RED_TO_GREEN_GRADIENT[:len(speed_counts)][::-1]
                        )),
                        color_indicator="Climb Speed"
                    )
                )
            else:
                st.info("No climb speed data recorded.")

        with scoring_side_col:
            all_sides = []
            for sides in scouting_data[Queries.TELEOP_SCORING_SIDE]:
                if isinstance(sides, list):
                    all_sides.extend(sides)
                elif isinstance(sides, str) and sides:
                    all_sides.append(sides)

            side_counts: dict[str, int] = {}
            for side in all_sides:
                side_counts[side] = side_counts.get(side, 0) + 1

            if side_counts:
                sorted_sides = dict(sorted(side_counts.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(
                    bar_graph(
                        list(sorted_sides.keys()),
                        list(sorted_sides.values()),
                        x_axis_label="Scoring Side",
                        y_axis_label="# of Occurrences",
                        title="Teleop Scoring Sides",
                        color=GeneralConstants.GOLD_GRADIENT[1]
                    )
                )
            else:
                st.info("No teleop scoring side data available.")

        with trench_bump_col:
            all_paths = []
            for paths in scouting_data[Queries.TELEOP_TRENCH_BUMP]:
                if isinstance(paths, list):
                    all_paths.extend(paths)
                elif isinstance(paths, str) and paths:
                    all_paths.append(paths)

            path_counts: dict[str, int] = {}
            for path in all_paths:
                path_counts[path] = path_counts.get(path, 0) + 1

            if path_counts:
                sorted_paths = dict(sorted(path_counts.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(
                    bar_graph(
                        list(sorted_paths.keys()),
                        list(sorted_paths.values()),
                        x_axis_label="Path",
                        y_axis_label="# of Occurrences",
                        title="Teleop Trench / Bump Usage",
                        color=GeneralConstants.BLUE_ALLIANCE_GRADIENT[2]
                    )
                )
            else:
                st.info("No teleop trench/bump path data available.")

    def generate_qualitative_graphs(self, team_number: int) -> None:
        """Generates the qualitative graphs for the `Team` page.

        :param team_number: The team to generate the graphs for.
        """
        ml_weight = 1
        estimate_weight = 1

        sentiment = SentimentIntensityAnalyzer()
        positivity_scores = []
        scouting_data = scouting_data_for_team(team_number)

        qualitative_graphs_tab, note_scouting_analysis_tab = st.tabs(
            ["📊 Qualitative Graphs", "✏️ Note Scouting Analysis"]
        )

        with qualitative_graphs_tab:
            row1_left, row1_right = st.columns(2)
            row2_left, row2_right = st.columns(2)
            row3_left, row3_right = st.columns(2)
            row4_col, _ = st.columns(2)

            with row1_left:
                driver_rating_types = list(Criteria.DRIVER_RATING_CRITERIA.keys())
                driver_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DRIVER_RATING, {t: 1})
                    for t in driver_rating_types
                ]
                plotly_chart(bar_graph(
                    driver_rating_types, driver_counts,
                    x_axis_label="Driver Rating", y_axis_label="# of Matches",
                    title="Driver Rating Breakdown",
                    color=dict(zip(driver_rating_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Driver Rating"
                ))

            with row1_right:
                throughput_types = list(Criteria.BASIC_RATING_CRITERIA.keys())
                throughput_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.THROUGHPUT_SPEED, {t: 1})
                    for t in throughput_types
                ]
                plotly_chart(bar_graph(
                    throughput_types, throughput_counts,
                    x_axis_label="Throughput Speed", y_axis_label="# of Matches",
                    title="Throughput Speed Breakdown",
                    color=dict(zip(throughput_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Throughput Speed"
                ))

            with row2_left:
                intake_types = list(Criteria.INTAKE_SPEED_CRITERIA.keys())
                intake_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_SPEED, {t: 1})
                    for t in intake_types
                ]
                plotly_chart(bar_graph(
                    intake_types, intake_counts,
                    x_axis_label="Intake Speed", y_axis_label="# of Matches",
                    title="Intake Speed Breakdown",
                    color=dict(zip(intake_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Intake Speed"
                ))

            with row2_right:
                defense_types = list(Criteria.BASIC_RATING_CRITERIA.keys())
                defense_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.DEFENSE_RATING, {t: 1})
                    for t in defense_types
                ]
                plotly_chart(bar_graph(
                    defense_types, defense_counts,
                    x_axis_label="Defense Rating", y_axis_label="# of Matches",
                    title="Defense Rating Breakdown",
                    color=dict(zip(defense_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Defense Rating"
                ))

            with row3_left:
                intake_defense_types = list(Criteria.BASIC_RATING_CRITERIA.keys())
                intake_defense_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.INTAKE_DEFENSE_RATING, {t: 1})
                    for t in intake_defense_types
                ]
                plotly_chart(bar_graph(
                    intake_defense_types, intake_defense_counts,
                    x_axis_label="Intake Defense Rating", y_axis_label="# of Matches",
                    title="Intake Defense Rating Breakdown",
                    color=dict(zip(intake_defense_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Intake Defense Rating"
                ))

            with row3_right:
                shooter_defense_types = list(Criteria.BASIC_RATING_CRITERIA.keys())
                shooter_defense_counts = [
                    self.calculated_stats.cumulative_stat(team_number, Queries.SHOOTER_DEFENSE_RATING, {t: 1})
                    for t in shooter_defense_types
                ]
                plotly_chart(bar_graph(
                    shooter_defense_types, shooter_defense_counts,
                    x_axis_label="Shooter Defense Rating", y_axis_label="# of Matches",
                    title="Shooter Defense Rating Breakdown",
                    color=dict(zip(shooter_defense_types, GeneralConstants.RED_TO_GREEN_GRADIENT[::-1])),
                    color_indicator="Shooter Defense Rating"
                ))

            with row4_col:
                stability_types = list(Criteria.STABILITY_CRITERIA.keys())
                stability_counts = [
                    int((scouting_data[Queries.STABILITY] == t).sum())
                    for t in stability_types
                ]
                stability_colors = {
                    "Stable": GeneralConstants.LIGHT_GREEN,
                    "Moderately tippy": GeneralConstants.GOLD_GRADIENT[0],
                    "Very tippy": GeneralConstants.LIGHT_RED,
                }
                plotly_chart(bar_graph(
                    stability_types, stability_counts,
                    x_axis_label="Stability", y_axis_label="# of Matches",
                    title="Stability Rating Breakdown",
                    color=stability_colors,
                    color_indicator="Stability"
                ))

            # Robot style type breakdown (list field — flatten across all matches)
            st.divider()
            st.write("##### Robot Style Breakdown")
            all_styles = []
            for styles in scouting_data[Queries.ROBOT_STYLE_TYPE]:
                if isinstance(styles, list):
                    all_styles.extend(styles)
                elif isinstance(styles, str) and styles:
                    all_styles.append(styles)
            style_counts: dict[str, int] = {}
            for style in all_styles:
                style_counts[style] = style_counts.get(style, 0) + 1
            if style_counts:
                sorted_styles = dict(sorted(style_counts.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(bar_graph(
                    list(sorted_styles.keys()),
                    list(sorted_styles.values()),
                    x_axis_label="Robot Style",
                    y_axis_label="# of Occurrences",
                    title="Robot Style Type Distribution",
                    color=GeneralConstants.PRIMARY_COLOR
                ))
            else:
                st.info("No robot style type data available.")

        with note_scouting_analysis_tab:
            notes_col, metrics_col = st.columns(2, gap="medium")
            notes_by_match = dict(
                zip(
                    scouting_data[Queries.MATCH_KEY],
                    (
                        scouting_data[Queries.AUTO_NOTES].apply(lambda n: (n + " ").lower() if n else "")
                        + scouting_data[Queries.TELEOP_NOTES].apply(lambda n: (n + " ").lower() if n else "")
                        + scouting_data[Queries.RATING_NOTES].apply(lambda n: n.lower() if n else "")
                    )
                )
            )

            with notes_col:
                st.write("##### Notes")
                st.markdown("<hr style='margin: 0px'/>", unsafe_allow_html=True)

                for match_key, notes in notes_by_match.items():
                    if notes.strip():
                        notes_col.write(f"###### {match_key}")

                        text_split_by_words = re.split(r"(\s+)", notes)
                        annotated_words = []
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

                        ml_generated_score = sentiment.polarity_scores(notes)["compound"]
                        sentiment_estimate = sum(sentiment_scores) / (len(sentiment_scores) or 1)
                        positivity_scores.append(
                            (ml_generated_score * ml_weight + sentiment_estimate * estimate_weight) / 2
                        )

                        annotated_text(*annotated_words)
                        st.markdown("<hr style='margin: 0px'/>", unsafe_allow_html=True)

            with metrics_col:
                st.write("##### Metrics")
                colored_metric(
                    "Positivity Score of Notes",
                    round(sum(positivity_scores) / (len(positivity_scores) or 1), 2),
                    threshold=0
                )
