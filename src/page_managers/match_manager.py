"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import numpy as np
import streamlit as st

from .page_manager import PageManager
from utils import (
    alliance_breakdown,
    bar_graph,
    box_plot,
    CalculatedStats,
    colored_metric,
    Criteria,
    GeneralConstants,
    get_team_statbotics,
    GraphType,
    multi_line_graph,
    plotly_chart,
    populate_missing_data,
    Queries,
    retrieve_match_schedule,
    retrieve_team_list,
    retrieve_scouting_data,
    scouting_data_for_team,
    stacked_bar_graph,
    win_percentages,
)


class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(retrieve_scouting_data())

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Match` page.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        match_schedule = retrieve_match_schedule()

        filter_teams_col, match_selector_col = st.columns(2)

        filter_by_team_number = str(
            filter_teams_col.selectbox(
                "Filter Matches by Team Number", ["—"] + retrieve_team_list()
            )
        )

        if filter_by_team_number != "—":
            match_schedule = match_schedule[
                match_schedule["red_alliance"]
                    .apply(lambda alliance: ",".join(map(str, alliance)))
                    .str.contains(filter_by_team_number)
                | match_schedule["blue_alliance"]
                    .apply(lambda alliance: ",".join(map(str, alliance)))
                    .str.contains(filter_by_team_number)
                ]

        match_chosen = match_selector_col.selectbox(
            "Choose Match", match_schedule["match_key"]
        )
        match_info = match_schedule[match_schedule["match_key"] == match_chosen]

        return [*match_info["red_alliance"], *match_info["blue_alliance"]]

    def generate_hypothetical_input_section(self) -> list[list, list]:
        """Creates the input section for the `Hypothetical Match` page.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        team_list = retrieve_team_list()

        red_alliance_form, blue_alliance_form = st.columns(2, gap="medium")

        with red_alliance_form:
            red_1_col, red_2_col, red_3_col = st.columns(3)
            red_1 = red_1_col.selectbox(":red[Red 1]", team_list, index=0)
            red_2 = red_2_col.selectbox(":red[Red 2]", team_list, index=1)
            red_3 = red_3_col.selectbox(":red[Red 3]", team_list, index=2)

        with blue_alliance_form:
            blue_1_col, blue_2_col, blue_3_col = st.columns(3)
            blue_1 = blue_1_col.selectbox(":blue[Blue 1]", team_list, index=3)
            blue_2 = blue_2_col.selectbox(":blue[Blue 2]", team_list, index=4)
            blue_3 = blue_3_col.selectbox(":blue[Blue 3]", team_list, index=5)

        return [
            [red_1, red_2, red_3],
            [blue_1, blue_2, blue_3]
        ]

    def generate_match_prediction_dashboard(
            self, red_alliance: list[int], blue_alliance: list[int]
    ) -> None:
        """Generates metrics for match predictions (Red vs. Blue tab).

        :param red_alliance: A list of three integers for the Red Alliance.
        :param blue_alliance: A list of three integers for the Blue Alliance.
        """
        (chance_of_winning_col,) = st.columns(1)
        predicted_red_score_col, red_alliance_breakdown_col = st.columns(2)
        predicted_blue_score_col, blue_alliance_breakdown_col = st.columns(2)

        odds_red, odds_blue, red_mean, blue_mean = self.calculated_stats.chance_of_winning(
            red_alliance, blue_alliance
        )

        with chance_of_winning_col:
            win_percentages(red_odds=odds_red, blue_odds=odds_blue)

        with predicted_red_score_col:
            colored_metric(
                "Predicted Composite (Red)",
                round(red_mean, 1),
                background_color=GeneralConstants.DARK_RED,
                opacity=0.5,
            )

        with predicted_blue_score_col:
            colored_metric(
                "Predicted Composite (Blue)",
                round(blue_mean, 1),
                background_color=GeneralConstants.DARK_BLUE,
                opacity=0.5,
            )

        with red_alliance_breakdown_col:
            avg_composites_red = [
                round(get_team_statbotics(team).get("total_epa") or 0, 1)
                for team in red_alliance
            ]
            best_to_defend_red = self._best_to_defend(red_alliance)
            alliance_breakdown(
                red_alliance,
                avg_composites_red,
                best_to_defend_red,
                Queries.RED_ALLIANCE,
            )

        with blue_alliance_breakdown_col:
            avg_composites_blue = [
                round(get_team_statbotics(team).get("total_epa") or 0, 1)
                for team in blue_alliance
            ]
            best_to_defend_blue = self._best_to_defend(blue_alliance)
            alliance_breakdown(
                blue_alliance,
                avg_composites_blue,
                best_to_defend_blue,
                Queries.BLUE_ALLIANCE,
            )

    def _best_to_defend(self, alliance: list[int]) -> int:
        """Returns the team on the alliance that is hardest to defend against (highest throughput / counter-defense ratio)."""
        rankings = sorted(
            [
                (
                    team,
                    self.calculated_stats.average_throughput_speed(team),
                    max(self.calculated_stats.average_counter_defense_skill(team), 0.01)
                )
                for team in alliance
            ],
            key=lambda info: info[1] / info[2],
        )
        return rankings[-1][0]

    @staticmethod
    def _alliance_sorted_bar(
        red_alliance: list[int],
        blue_alliance: list[int],
        values: list[float],
        x_axis_label: str,
        y_axis_label: str,
        title: str,
        red_color: str,
        blue_color: str,
    ):
        """Returns a bar graph sorted highest→lowest and colored by alliance.

        :param red_alliance: Teams on the red alliance.
        :param blue_alliance: Teams on the blue alliance.
        :param values: One value per team (red first, then blue, 6 total).
        :param red_color: Hex color for red alliance bars.
        :param blue_color: Hex color for blue alliance bars.
        :return: A Plotly Figure.
        """
        combined = red_alliance + blue_alliance
        # Use string keys so Plotly treats the column as categorical (not a continuous gradient)
        color_map = {
            **{str(team): red_color  for team in red_alliance},
            **{str(team): blue_color for team in blue_alliance},
        }
        pairs = sorted(zip(combined, values), key=lambda p: p[1], reverse=True)
        sorted_team_strs = [str(p[0]) for p in pairs]
        sorted_values    = [p[1]      for p in pairs]
        return bar_graph(
            sorted_team_strs, sorted_values,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            title=title,
            color={t: color_map[t] for t in sorted_team_strs},
            color_indicator=x_axis_label,
        )

    def generate_match_prediction_graphs(
            self, red_alliance: list[int], blue_alliance: list[int], type_of_graph: str
    ) -> None:
        """Generate graphs for match prediction (Red vs. Blue tab).

        :param red_alliance: A list of three integers for the Red Alliance.
        :param blue_alliance: A list of three integers for the Blue Alliance.
        :param type_of_graph: Unused; kept for API compatibility.
        """
        combined_teams = red_alliance + blue_alliance

        driver_col, throughput_col = st.columns(2)
        intake_col, defense_col = st.columns(2)

        _RED  = GeneralConstants.RED_ALLIANCE_GRADIENT[1]   # #b04949
        _BLUE = GeneralConstants.BLUE_ALLIANCE_GRADIENT[2]  # #7da0d1

        with driver_col:
            plotly_chart(self._alliance_sorted_bar(
                red_alliance, blue_alliance,
                [self.calculated_stats.average_driver_rating(t) for t in combined_teams],
                x_axis_label="Team", y_axis_label="Avg. Driver Rating (1–5)",
                title="Driver Rating Comparison",
                red_color=_RED, blue_color=_BLUE,
            ))

        with throughput_col:
            plotly_chart(self._alliance_sorted_bar(
                red_alliance, blue_alliance,
                [self.calculated_stats.average_throughput_speed(t) for t in combined_teams],
                x_axis_label="Team", y_axis_label="Avg. Throughput (1–5)",
                title="Throughput Speed Comparison",
                red_color=_RED, blue_color=_BLUE,
            ))

        with intake_col:
            plotly_chart(self._alliance_sorted_bar(
                red_alliance, blue_alliance,
                [self.calculated_stats.average_intake_speed_rating(t) for t in combined_teams],
                x_axis_label="Team", y_axis_label="Avg. Intake Speed (1–5)",
                title="Intake Speed Comparison",
                red_color=_RED, blue_color=_BLUE,
            ))

        with defense_col:
            plotly_chart(self._alliance_sorted_bar(
                red_alliance, blue_alliance,
                [self.calculated_stats.average_defense_rating(t) for t in combined_teams],
                x_axis_label="Team", y_axis_label="Avg. Defense (1–5)",
                title="Defense Rating Comparison",
                red_color=_RED, blue_color=_BLUE,
            ))

    def generate_alliance_dashboard(self, team_numbers: list[int], color_gradient: list[str]) -> None:
        """Generates an alliance dashboard in the `Match` page, ranking teams by composite score.

        :param team_numbers: The teams to generate the alliance dashboard for.
        :param color_gradient: The color gradient depending on alliance.
        """
        rankings = sorted(
            {
                team: float(get_team_statbotics(team).get("total_epa") or 0)
                for team in team_numbers
            }.items(),
            key=lambda pair: pair[1],
            reverse=True
        )

        col1, col2, col3 = st.columns(3)
        labels = ["Highest Composite", "Second Composite", "Lowest Composite"]

        for col, label, (team, _), color in zip(
            [col1, col2, col3], labels, rankings, color_gradient
        ):
            with col:
                colored_metric(
                    label,
                    team,
                    background_color=color,
                    opacity=0.4,
                    border_opacity=0.9
                )

    def generate_autonomous_graphs(
            self,
            team_numbers: list[int],
            type_of_graph: str,
            color_gradient: list[str]
    ) -> None:
        """Generates the autonomous graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: Unused; kept for API compatibility.
        :param color_gradient: The color gradient depending on alliance.
        """
        auto_climb_col, auto_scoring_side_col = st.columns(2)

        with auto_climb_col:
            auto_climb_rates = [
                round(self.calculated_stats.auto_climb_rate(team) * 100, 1)
                for team in team_numbers
            ]
            plotly_chart(bar_graph(
                team_numbers, auto_climb_rates,
                x_axis_label="Team", y_axis_label="Auto Climb Rate (%)",
                title="Auto Climb Rate by Team",
                color=color_gradient
            ))

        with auto_scoring_side_col:
            # Aggregate all scoring sides across teams in the alliance
            all_sides: dict[str, int] = {}
            for team in team_numbers:
                team_data = scouting_data_for_team(team)
                for sides in team_data[Queries.AUTO_SCORING_SIDE]:
                    if isinstance(sides, list):
                        for s in sides:
                            all_sides[s] = all_sides.get(s, 0) + 1

            if all_sides:
                sorted_sides = dict(sorted(all_sides.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(bar_graph(
                    list(sorted_sides.keys()),
                    list(sorted_sides.values()),
                    x_axis_label="Side", y_axis_label="# of Occurrences",
                    title="Auto Scoring Sides (Alliance)",
                    color=color_gradient[0]
                ))
            else:
                st.info("No auto scoring side data.")

    def generate_teleop_graphs(
            self,
            team_numbers: list[int],
            type_of_graph: str,
            color_gradient: list[str]
    ) -> None:
        """Generates the teleop graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param type_of_graph: Unused; kept for API compatibility.
        :param color_gradient: The color gradient depending on alliance.
        """
        teams_data = [scouting_data_for_team(team) for team in team_numbers]

        st.write("## 🧗 Endgame")
        climb_breakdown_col, climb_speed_col = st.columns(2)

        st.divider()
        st.write("## 🎯 Teleop")
        teleop_side_col, shoot_move_col = st.columns(2)

        climb_levels = ["L1", "L2", "L3"]
        level_colors = {
            f"Level {Criteria.CLIMBING_CRITERIA[lvl]} Climbs": color
            for lvl, color in zip(climb_levels, GeneralConstants.LEVEL_GRADIENT)
        }

        with climb_breakdown_col:
            climbs_by_level = [
                [(td[Queries.TELEOP_CLIMB] == level).sum() for td in teams_data]
                for level in climb_levels
            ]
            climb_level_labels = [f"Level {Criteria.CLIMBING_CRITERIA[lvl]} Climbs" for lvl in climb_levels]
            plotly_chart(stacked_bar_graph(
                team_numbers,
                climbs_by_level,
                x_axis_label="Teams",
                y_axis_label=climb_level_labels,
                y_axis_title="# of Climbs by Level",
                title="Climbs by Team",
                color_map=level_colors
            ))

        with climb_speed_col:
            speed_buckets = ["<5 seconds", "5-10 seconds", "10-20 seconds", ">20 seconds"]
            counts_by_speed = [
                [(td[Queries.CLIMB_SPEED] == speed).sum() for td in teams_data]
                for speed in speed_buckets
            ]
            speed_colors = dict(zip(
                speed_buckets,
                GeneralConstants.RED_TO_GREEN_GRADIENT[:len(speed_buckets)][::-1]
            ))
            plotly_chart(stacked_bar_graph(
                team_numbers,
                counts_by_speed,
                x_axis_label="Teams",
                y_axis_label=speed_buckets,
                y_axis_title="# of Matches by Speed",
                title="Climb Speeds by Team",
                color_map=speed_colors
            ))

        with teleop_side_col:
            all_sides: dict[str, int] = {}
            for team in team_numbers:
                team_data = scouting_data_for_team(team)
                for sides in team_data[Queries.TELEOP_SCORING_SIDE]:
                    if isinstance(sides, list):
                        for s in sides:
                            all_sides[s] = all_sides.get(s, 0) + 1

            if all_sides:
                sorted_sides = dict(sorted(all_sides.items(), key=lambda x: x[1], reverse=True))
                plotly_chart(bar_graph(
                    list(sorted_sides.keys()),
                    list(sorted_sides.values()),
                    x_axis_label="Side", y_axis_label="# of Occurrences",
                    title="Teleop Scoring Sides (Alliance)",
                    color=color_gradient[0]
                ))
            else:
                st.info("No teleop scoring side data.")

        with shoot_move_col:
            sotm_rates = [
                round(self.calculated_stats.shoot_on_the_move_rate(team) * 100, 1)
                for team in team_numbers
            ]
            plotly_chart(bar_graph(
                team_numbers, sotm_rates,
                x_axis_label="Team", y_axis_label="Shoot-on-the-Move Rate (%)",
                title="Shoot on the Move Rate",
                color=color_gradient[1]
            ))

    def generate_qualitative_graphs(
            self,
            team_numbers: list[int],
            color_gradient: list[str]
    ):
        """Generates the qualitative graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :param color_gradient: The color gradient depending on alliance.
        """
        driver_rating_col, throughput_col, disables_col = st.columns(3)

        with driver_rating_col:
            driver_ratings = [
                self.calculated_stats.average_driver_rating(team) for team in team_numbers
            ]
            plotly_chart(bar_graph(
                team_numbers, driver_ratings,
                x_axis_label="Teams", y_axis_label="Driver Rating (1–5)",
                title="Average Driver Rating by Team",
                color=color_gradient[0]
            ))

        with throughput_col:
            throughput_ratings = [
                self.calculated_stats.average_throughput_speed(team) for team in team_numbers
            ]
            plotly_chart(bar_graph(
                team_numbers, throughput_ratings,
                x_axis_label="Teams", y_axis_label="Throughput Speed (1–5)",
                title="Average Throughput Speed by Team",
                color=color_gradient[1]
            ))

        with disables_col:
            disable_rates = [
                round(self.calculated_stats.disabled_rate(team) * 100, 1)
                for team in team_numbers
            ]
            plotly_chart(bar_graph(
                team_numbers, disable_rates,
                x_axis_label="Teams", y_axis_label="Disabled Rate (%)",
                title="Disabled Rate by Team",
                color=color_gradient[2] if len(color_gradient) > 2 else GeneralConstants.LIGHT_RED
            ))
