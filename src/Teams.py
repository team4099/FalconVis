"""Creates the page for team-specific graphs in Streamlit."""

import streamlit as st

from page_managers import TeamManager

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

    metric_tab, graphs_tab = st.tabs(["📊 Metrics", "📈 Graphs"])

    with metric_tab:
        st.write("## Metrics")

        quartile = st.select_slider(
            "Quartile for Comparisons (The deltas for each metric represent the deviation from said quartile).",
            options=[1, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 99]
        ) / 100
        team_manager.generate_metrics(team_number, quartile)

    with graphs_tab:
        st.write("## Graphs")

        team_manager.generate_graphs(team_number)
