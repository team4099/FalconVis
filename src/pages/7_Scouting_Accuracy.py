"""Page for displaying a scouting team's accuracy based on TBA data"""

import streamlit as st
from page_managers import ScoutingAccuracyManager
from pandas import DataFrame

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

    # Name input Section
    member_name = scouting_accuracy_manager.generate_input_section()

    # Generate the Scouting Accuracy Table

    generated_scouting_accuracy: DataFrame = scouting_accuracy_manager.generate_accuracy_table(member_name)

    # teams, scouted, tba, accuracy ?


    returned_dataframe = st.dataframe(generated_scouting_accuracy)
