"""Page for displaying a scouting team's accuracy based on TBA data"""

import streamlit as st
from page_managers import ScoutingAccuracyManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Scouting Accuracy",
    page_icon="🫂",
)
scouting_accuracy_manager = ScoutingAccuracyManager()

if __name__ == '__main__':
    # Write the name of the page.
    st.write("# Scouting Accuracy")

    # Generate the Scouting Accuracy Table
    generated_scouting_accuracy = scouting_accuracy_manager.generate_accuracy_table()

    returned_dataframe = st.dataframe(generated_scouting_accuracy)
