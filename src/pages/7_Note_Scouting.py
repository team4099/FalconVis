"""Creates the page for viewing note scouting data in FalconVis."""

import streamlit as st
from page_managers import NoteScoutingManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Note Scouting",
    page_icon="📝",
)
note_scouting_manager = NoteScoutingManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Note Scouting")

    team_number = note_scouting_manager.generate_team_input_section()
    auto_tab, teleop_tab = st.tabs(["🤖 Autonomous", "🎮 Teleop"])

    # Generate the metrics and bar plots for the Autonomous section in the Team page.
    with auto_tab:
        note_scouting_manager.generate_team_autonomous_graphs(team_number)

    # Generate the metrics and bar plots for the Teleop section in the Team page.
    with teleop_tab:
        note_scouting_manager.generate_team_teleop_graphs(team_number)
