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
    
    st.text("")
    st.write("## Accuracy by Scouter")

    # display scouting accuracy table
    member_name = scouting_accuracy_manager.generate_input_section()
    generated_scouting_accuracy: DataFrame = scouting_accuracy_manager.generate_scouting_accuracy_table(member_name)
    returned_scouting_dataframe = st.dataframe(generated_scouting_accuracy, hide_index = True, use_container_width=True)
    
    st.text("")
    st.write("## Accuracy by Match")
     #display match accuracy table
    generated_match_accuracy: DataFrame = scouting_accuracy_manager.generate_match_accuracy_table()
    returned_match_dataframe = st.dataframe(generated_match_accuracy, hide_index=True, use_container_width=True)