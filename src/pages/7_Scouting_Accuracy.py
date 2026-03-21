"""Page for displaying scouting coverage statistics."""

import streamlit as st
from page_managers import ScoutingAccuracyManager
from pandas import DataFrame

st.set_page_config(
    layout="wide",
    page_title="Scouting Coverage",
    page_icon="🫂",
)
scouting_accuracy_manager = ScoutingAccuracyManager()

if __name__ == '__main__':
    st.write("# Scouting Coverage")
    st.caption(
        "Since the current dataset is qualitative-only, this page shows scouting "
        "coverage (matches & teams per scouter) rather than numerical TBA accuracy."
    )

    st.text("")
    st.write("## Coverage by Scouter")

    member_name = scouting_accuracy_manager.generate_input_section()
    generated_scouting_accuracy: DataFrame = scouting_accuracy_manager.generate_scouting_accuracy_table(member_name)
    st.dataframe(generated_scouting_accuracy, hide_index=True, use_container_width=True)

    st.text("")
    st.write("## Coverage by Match")
    generated_match_accuracy: DataFrame = scouting_accuracy_manager.generate_match_accuracy_table()
    st.dataframe(generated_match_accuracy, hide_index=True, use_container_width=True)
