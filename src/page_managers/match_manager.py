"""Creates the `MatchManager` class used to set up the Match page and its graphs."""

import streamlit as st

from .page_manager import PageManager
from utils import CalculatedStats, Queries, retrieve_team_list, retrieve_scouting_data, scouting_data_for_team, multi_line_graph, bar_graph, stacked_bar_graph
from streamlit_toggle import toggle

class MatchManager(PageManager):
    """The page manager for the `Match` page."""

    def __init__(self):
        self.calculated_stats = CalculatedStats(
            retrieve_scouting_data()
        )

    def generate_input_section(self) -> list[list, list]:
        """Creates the input section for the `Match` page.

        Creates six dropdowns to choose teams for each alliance separately.

        :return: Returns a 2D list with the lists being the three teams for the Red and Blue alliances.
        """
        team_list = retrieve_team_list()

        # Create the separate columns for submitting teams.
        red_alliance_form, blue_alliance_form = st.columns(2, gap="medium")

        # Create the different dropdowns to choose the three teams for Red Alliance.
        with red_alliance_form:
            red_1_col, red_2_col, red_3_col = st.columns(3)
            red_1 = red_1_col.selectbox(
                ":red[Red 1]",
                team_list
            )
            red_2 = red_2_col.selectbox(
                ":red[Red 2]",
                team_list
            )
            red_3 = red_3_col.selectbox(
                ":red[Red 3]",
                team_list
            )

        # Create the different dropdowns to choose the three teams for Blue Alliance.
        with blue_alliance_form:
            blue_1_col, blue_2_col, blue_3_col = st.columns(3)
            blue_1 = blue_1_col.selectbox(
                ":blue[Blue 1]",
                team_list
            )
            blue_2 = blue_2_col.selectbox(
                ":blue[Blue 2]",
                team_list
            )
            blue_3 = blue_3_col.selectbox(
                ":blue[Blue 3]",
                team_list
            )

        return [
            [red_1, red_2, red_3],
            [blue_1, blue_2, blue_3]
        ]
    
    def generate_graphs(self, team_numbers: list, display_points: bool = False) -> None:
        """Generates the graphs for the `Match` page.

        :param team_numbers: The teams to generate the graphs for.
        :return:
        """
        
        teams_data = [scouting_data_for_team(team) for team in team_numbers]

        
        auto_graphs_tab, teleop_graphs_tab, endgame_graphs_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop", "🧗 Endgame"]
        )

        # Autonomous graphs
        with auto_graphs_tab:
            st.write("#### Autonomous")

            # Graph for auto cycles over time
            auto_cycles_over_time_per_team = [self.calculated_stats.points_contributed_by_match(team, Queries.AUTO_GRID) if display_points else self.calculated_stats.cycles_by_match(team, Queries.AUTO_GRID) for team in team_numbers]

            st.plotly_chart(
                multi_line_graph(
                    x=teams_data[0][Queries.MATCH_KEY],
                    y=auto_cycles_over_time_per_team,
                    x_axis_label="Match Key",
                    y_axis_label=team_numbers,
                    y_axis_title= "Auto Point Total" if display_points else "# of Auto Cycles"
                ),
                use_container_width=True
            )

            auto_cycles_cone_vs_cube_col, auto_cycles_by_level_col = st.columns(2)

            with auto_cycles_cone_vs_cube_col:
                auto_cycles_cone_vs_cube = [[self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.AUTO_CONES).mean() for team in team_numbers], [self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.AUTO_CUBES).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=auto_cycles_cone_vs_cube,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "Cones","Cubes"
                        ],
                        y_axis_title="Auto Cones vs Cubes",
                    ),use_container_width=True
                )

            with auto_cycles_by_level_col:
                auto_cycles_by_level = [[self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.HIGH).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.MID).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.AUTO_GRID, Queries.LOW).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=auto_cycles_by_level,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "High","Mid", "Low"
                        ],
                        y_axis_title="Auto Game Pieces by Level",
                    ),use_container_width=True
                )

            # Graph for auto charge station psuccess_rate
            auto_engage_success_rate_per_team = [[self.calculated_stats.auto_engage_success_rate(team), self.calculated_stats.auto_total_attempted_charge(team), self.calculated_stats.auto_total_successful_charge(team)] for team in team_numbers]

            st.plotly_chart(
                    bar_graph(
                        x=team_numbers,
                        y=auto_engage_success_rate_per_team,
                        x_axis_label="Teams",
                        y_axis_label="Auto Engage Success Rate",
                        hover_data=["Attempts", "Successful Engages"]
                    ),use_container_width=True
                )
            

        # Teleop + endgame graphs
        with teleop_graphs_tab:
            st.write("#### Teleop")

            # Graph for teleop cycles over time
            teleop_cycles_over_time_per_team =  [self.calculated_stats.points_contributed_by_match(team, Queries.TELEOP_GRID) if display_points else self.calculated_stats.cycles_by_match(team, Queries.TELEOP_GRID) for team in team_numbers]

            st.plotly_chart(multi_line_graph(
                    x=teams_data[0][Queries.MATCH_KEY],
                    y=teleop_cycles_over_time_per_team,
                    x_axis_label="Match Key",
                    y_axis_label=team_numbers,
                    y_axis_title="Teleop Point Total" if display_points else "# of Teleop Cycles"
                    ),
                    use_container_width=True
            )
                

            teleop_cycles_cone_vs_cube_col, teleop_cycles_by_level_col = st.columns(2)

            with teleop_cycles_cone_vs_cube_col:
                teleop_cycles_cone_vs_cube = [[self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.TELEOP_CONES).mean() for team in team_numbers], [self.calculated_stats.cycles_by_game_piece_per_match(team, Queries.TELEOP_CUBES).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=teleop_cycles_cone_vs_cube,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "Cones","Cubes"
                        ],
                        y_axis_title="Teleop Cones vs Cubes",
                    ), use_container_width=True
                )
            
            with teleop_cycles_by_level_col:
                teleop_cycles_by_level = [[self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.HIGH).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.MID).mean() for team in team_numbers], [self.calculated_stats.cycles_by_height_per_match(team, Queries.TELEOP_GRID, Queries.LOW).mean() for team in team_numbers]]
                st.plotly_chart(
                    stacked_bar_graph(
                        x=team_numbers,
                        y=teleop_cycles_by_level,
                        x_axis_label="Teams",
                        y_axis_label=[
                            "High","Mid", "Low"
                        ],
                        y_axis_title="Teleop Game Pieces by Level",
                    ), use_container_width=True
                )
            

        with endgame_graphs_tab:
            st.write("#### Endgame")
