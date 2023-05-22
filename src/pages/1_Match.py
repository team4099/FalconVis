"""Creates the page for match-specific graphs in Streamlit."""

import streamlit as st

from page_managers import MatchManager
from streamlit_toggle import toggle



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

    display_points = toggle(label="Display Point Total")

    # Tabs to switch between the Comparison Graphs/Red Alliance/Blue Alliance
    comparison_tab, red_alliance_tab, blue_alliance_tab = st.tabs(
        [":red[Red] vs. :blue[Blue]", ":red[Red Alliance]", ":blue[Blue Alliance]"]
    )

    with comparison_tab:
        st.write("### :red[Red] vs. :blue[Blue] Graphs")

    with red_alliance_tab:
        st.write("### :red[Red] Alliance Graphs")
        match_manager.generate_graphs(teams_selected[0], display_points)


    with blue_alliance_tab:
        st.write("### :blue[Blue] Alliance Graphs")
        match_manager.generate_graphs(teams_selected[1], display_points)
