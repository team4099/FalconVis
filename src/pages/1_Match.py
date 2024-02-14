"""Creates the page for match-specific graphs in Streamlit."""

import streamlit as st

from page_managers import MatchManager
from utils import GeneralConstants, GraphType

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Match",
    page_icon="🏁",
)
match_manager = MatchManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Match")

    # Generate the input section of the `Match` page.
    teams_selected = match_manager.generate_input_section()

    # Tabs to switch between the Comparison Graphs/Red Alliance/Blue Alliance
    comparison_tab, red_alliance_tab, blue_alliance_tab = st.tabs(
        [":red[Red] vs. :blue[Blue]", ":red[Red Alliance]", ":blue[Blue Alliance]"]
    )

    with comparison_tab:
        st.write("### :red[Red] vs. :blue[Blue] Graphs")

        # Generate the match prediction dashboard that give a rough overview of the two alliances.
        match_manager.generate_match_prediction_dashboard(*teams_selected)

        # Create cycle contribution and point contribution tabs for the different types of graphs
        cycle_contribution_breakdown_tab, point_contribution_breakdown_tab = st.tabs(
            ["📈 Cycle Contribution Breakdown", "🧮 Point Contribution Breakdown"]
        )

        # Plot cycle contribution graphs
        with cycle_contribution_breakdown_tab:
            match_manager.generate_match_prediction_graphs(
                *teams_selected,
                type_of_graph=GraphType.CYCLE_CONTRIBUTIONS
            )

        # Plot point contribution graphs
        with point_contribution_breakdown_tab:
            match_manager.generate_match_prediction_graphs(
                *teams_selected,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS
            )

    with red_alliance_tab:
        st.write("### :red[Red] Alliance Graphs")

        # Generate alliance dashboard
        match_manager.generate_alliance_dashboard(
            teams_selected[0],
            color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
        )

        red_auto_tab, red_teleop_tab, red_qualitative_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop", "📝 Qualitative"]
        )

        with red_auto_tab:
            red_auto_cycle_tab, red_auto_points_tab = st.tabs(
                ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
            )

            with red_auto_cycle_tab:
                match_manager.generate_autonomous_graphs(
                    teams_selected[0],
                    type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
                )

            with red_auto_points_tab:
                match_manager.generate_autonomous_graphs(
                    teams_selected[0],
                    type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
                )

        with red_teleop_tab:
            red_teleop_cycle_tab, red_teleop_points_tab = st.tabs(
                ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
            )

            with red_teleop_cycle_tab:
                match_manager.generate_teleop_graphs(
                    teams_selected[0],
                    type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
                )

            with red_teleop_points_tab:
                match_manager.generate_teleop_graphs(
                    teams_selected[0],
                    type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
                )
        
        with red_qualitative_tab:
            match_manager.generate_qualitative_graphs(
                teams_selected[0],
                color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
            )

    with blue_alliance_tab:
        st.write("### :blue[Blue] Alliance Graphs")

        # Generate alliance dashboard
        match_manager.generate_alliance_dashboard(
            teams_selected[1],
            color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
        )

        blue_auto_tab, blue_teleop_tab, blue_qualitative_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop", "📝 Qualitative"]
        )

        with blue_auto_tab:
            blue_auto_cycle_tab, blue_auto_points_tab = st.tabs(
                ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
            )

            with blue_auto_cycle_tab:
                match_manager.generate_autonomous_graphs(
                    teams_selected[1],
                    type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
                )

            with blue_auto_points_tab:
                match_manager.generate_autonomous_graphs(
                    teams_selected[1],
                    type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
                )

        with blue_teleop_tab:
            blue_teleop_cycle_tab, blue_teleop_points_tab = st.tabs(
                ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
            )

            with blue_teleop_cycle_tab:
                match_manager.generate_teleop_graphs(
                    teams_selected[1],
                    type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
                )

            with blue_teleop_points_tab:
                match_manager.generate_teleop_graphs(
                    teams_selected[1],
                    type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                    color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
                )

        with blue_qualitative_tab:
            match_manager.generate_qualitative_graphs(
                teams_selected[1],
                color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
            )
