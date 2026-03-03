"""Creates the page for team-specific graphs in Streamlit."""

import streamlit as st

from page_managers import TeamManager
from utils import GraphType

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Teams",
    page_icon="🤖",
)
team_manager = TeamManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Teams")

    # Generate the input section of the `Teams` page.
    team_number = team_manager.generate_input_section()

    metric_tab, auto_graphs_tab, teleop_graphs_tab, qualitative_graphs_tab = st.tabs(
        ["📊 Metrics", "🤖 Autonomous Graphs", "🎮 Teleop + Endgame Graphs", "📝 Qualitative Graphs"]
    )

    with metric_tab:
        st.write("### Metrics")

        # Generate metrics (cards with information surrounding teams)
        team_manager.generate_metrics(team_number)

    with auto_graphs_tab:
        st.write("#### 🤖 Autonomous Graphs")

        # Create fuel-scored and point-contribution graph tabs.
        auto_fuel_tab, auto_point_tab = st.tabs(
            ["⛽ Fuel vs Match Index", "🧮 Points vs Match Index"]
        )
        
        with auto_fuel_tab:
            team_manager.generate_autonomous_graphs(
                team_number,
                type_of_graph=GraphType.FUEL_CONTRIBUTIONS
            )
        
        with auto_point_tab:
            team_manager.generate_autonomous_graphs(
                team_number,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS
            )

    with teleop_graphs_tab:
        st.write("#### 🎮 Teleop + Endgame Graphs")

        # Create climb-points graph tabs.
        teleop_climb_tab, teleop_climb_alt_tab = st.tabs(
            ["🧗 Climb Pts vs Match Index", "🧗 Climb Pts vs Match Index"]
        )

        with teleop_climb_tab:
            team_manager.generate_teleop_graphs(
                team_number,
                type_of_graph=GraphType.FUEL_CONTRIBUTIONS
            )

        with teleop_climb_alt_tab:
            team_manager.generate_teleop_graphs(
                team_number,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS
            )

    with qualitative_graphs_tab:
        st.write("#### 📝 Qualitative Graphs")
        team_manager.generate_qualitative_graphs(
            team_number,
        )
