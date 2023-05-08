"""Creates the page for team-specific graphs in Streamlit."""

import streamlit as st
from page_managers import TeamManager

# Configuration for Streamlit
team_manager = TeamManager()
st.set_page_config(
    page_title="Teams",
    page_icon="🤖",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Teams")

    # Generate the input section of the `Teams` page.
    team_number = team_manager.generate_input_section()

