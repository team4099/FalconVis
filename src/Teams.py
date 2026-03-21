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
    st.write("# Teams")

    team_number = team_manager.generate_input_section()

    metric_tab, auto_graphs_tab, teleop_graphs_tab, qualitative_graphs_tab = st.tabs(
        ["📊 Metrics", "🤖 Autonomous Graphs", "🎮 Teleop + Endgame Graphs", "📝 Qualitative Graphs"]
    )

    with metric_tab:
        st.write("### Quantitative Metrics")
        team_manager.generate_quantitative_metrics(team_number)

        st.divider()

        st.write("### Qualitative Metrics")
        team_manager.generate_metrics(team_number)

    with auto_graphs_tab:
        st.write("#### 🤖 Autonomous Graphs")
        team_manager.generate_autonomous_graphs(team_number)

    with teleop_graphs_tab:
        st.write("#### 🎮 Teleop + Endgame Graphs")
        team_manager.generate_teleop_graphs(team_number)

    with qualitative_graphs_tab:
        st.write("#### 📝 Qualitative Graphs")
        team_manager.generate_qualitative_graphs(team_number)
