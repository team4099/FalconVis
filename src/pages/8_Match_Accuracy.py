"""Page for displaying match accuracy based on TBA data"""

import streamlit as st
from page_managers import MatchAccuracyManager
from pandas import DataFrame

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Match Accuracy",
    page_icon="🎯",
)

# Initialize the MatchAccuracyManager
match_accuracy_manager = MatchAccuracyManager()

if __name__ == "__main__":
    # Write the name of the page
    st.write("# Match Accuracy")

    generated_match_accuracy: DataFrame = match_accuracy_manager.generate_accuracy_table()


    # Display the dataframe in Streamlit
    returned_dataframe = st.dataframe(generated_match_accuracy, hide_index=True, use_container_width=True)
