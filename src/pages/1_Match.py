"""Creates the page for match-specific graphs in Streamlit."""

import streamlit as st

from page_managers import MatchManager
from utils import GraphType


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

    with blue_alliance_tab:
        st.write("### :blue[Blue] Alliance Graphs")

