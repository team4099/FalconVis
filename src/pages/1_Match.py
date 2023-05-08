"""Creates the page for match-specific graphs in Streamlit."""

import streamlit as st
from page_managers import MatchManager

# Configuration for Streamlit
match_manager = MatchManager()
st.set_page_config(
    page_title="Match",
    page_icon="🏁",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Match")

    # Generate the input section of the `Teams` page.
    teams_selected = match_manager.generate_input_section()

