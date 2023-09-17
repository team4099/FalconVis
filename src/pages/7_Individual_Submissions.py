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
    misc_tab, auto_data_tab, teleop_data_tab, qualitative_tab = st.tabs(
        ["📊 Miscellaneous Data", "🤖 Autonomous Data", "🎮 Teleop + Endgame Data", "📝 Qualitative Data"]
    )

    # Display miscellaneous data like the scout name and alliance.
    with misc_tab:
        individual_submissions_manager.display_miscellaneous_data(submission)

    # Display autonomous data like the number of cycles and the like.
    with auto_data_tab:
        individual_submissions_manager.display_autonomous_data(submission)

    # Display teleop data
    with teleop_data_tab:
        individual_submissions_manager.display_teleop_data(submission)