"""Creates the page for creating custom graphs in FalconVis."""

import streamlit as st
from page_managers import RankingSimulatorManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Ranking Simulator",
    page_icon="❓",
)
ranking_simulator_manager = RankingSimulatorManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Ranking Simulation")

    # Add the input section of the page.
    match_chosen = ranking_simulator_manager.generate_input_section()

    # Display the simulated rankings.
    ranking_simulator_manager.generate_simulated_rankings(match_chosen)