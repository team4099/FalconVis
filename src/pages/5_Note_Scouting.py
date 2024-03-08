"""Creates the page for note scouting data in Streamlit."""

import streamlit as st
from page_managers import NoteScoutingManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Note Scouting",
    page_icon="📓",
)
note_scouting_manager = NoteScoutingManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Note Scouting")

    # Generate the input section of the `Note Scouting` page.
    team_number = note_scouting_manager.generate_input_section()
