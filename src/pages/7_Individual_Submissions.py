"""Creates the page to view individual submissions by team in Streamlit."""

import streamlit as st

from page_managers import IndividualSubmissionsManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Individual Submissions",
    page_icon="🤖",
)
individual_submissions_manager = IndividualSubmissionsManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Individual Submissions")

    # Generate the input section of the `Individual Submissions` page.
    submission = individual_submissions_manager.generate_input_section()
    misc_tab, auto_graphs_tab, teleop_graphs_tab, qualitative_tab = st.tabs(
        ["📊 Miscellaneous Data", "🤖 Autonomous Data", "🎮 Teleop + Endgame Data", "📝 Qualitative Data"]
    )

    # Display miscellaneous data like the scout name,
    with misc_tab:
        individual_submissions_manager.display_miscellaneous_data(submission)
