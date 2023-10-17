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

    metric_tab, auto_graphs_tab, teleop_graphs_tab, qualitative_tab = st.tabs(
        ["📊 Metrics", "🤖 Autonomous Graphs", "🎮 Teleop + Endgame Graphs", "📝 Qualitative Data"]
    )

    with metric_tab:
        st.write("### Metrics")

        # Generate metrics (cards with information surrounding teams)
        team_manager.generate_metrics(team_number)

    with auto_graphs_tab:
        st.write("#### 🤖 Autonomous Graphs")

        # Create cycle contribution and point contribution graph tabs.
        auto_cycle_contrib_tab, auto_point_contrib_tab = st.tabs(
            ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
        )

        with auto_cycle_contrib_tab:
            team_manager.generate_autonomous_graphs(
                team_number,
                type_of_graph=GraphType.CYCLE_CONTRIBUTIONS
            )

        with auto_point_contrib_tab:
            team_manager.generate_autonomous_graphs(
                team_number,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS
            )

    with teleop_graphs_tab:
        st.write("#### 🎮 Teleop + Endgame Graphs")

        # Create cycle contribution and point contribution graph tabs.
        teleop_cycle_contrib_tab, teleop_point_contrib_tab = st.tabs(
            ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
        )

        with teleop_cycle_contrib_tab:
            team_manager.generate_teleop_graphs(
                team_number,
                type_of_graph=GraphType.CYCLE_CONTRIBUTIONS
            )

        with teleop_point_contrib_tab:
            team_manager.generate_teleop_graphs(
                team_number,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS
            )
            
    with qualitative_tab:
        st.write("#### 📝 Qualitative Data")
        team_manager.display_qualitative_data(team_number)
