"""Creates the page for picklist data in Streamlit."""

import streamlit as st
from page_managers import PicklistManager
from page_managers import NoteScoutingManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Picklist + Notes",
    page_icon="🫂",
)
picklist_manager = PicklistManager()
note_scouting_manager = NoteScoutingManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Picklist")

    # Generate the input section of the `Picklist` page.
    fields_selected = picklist_manager.generate_input_section()

    # Generate the picklist using the fields selected.
    generated_picklist = picklist_manager.generate_picklist(fields_selected)

    returned_dataframe = st.dataframe(generated_picklist)

    st.download_button(
       "Press to Download",
       generated_picklist.to_csv(index=False),
       "Picklist.csv",
       "text/csv",
       key='download-csv'
    )

    st.write("# Note Scouting")

    team_number = note_scouting_manager.generate_team_input_section()
    auto_tab, teleop_tab = st.tabs(["🤖 Autonomous", "🎮 Teleop"])

    # Generate the metrics and bar plots for the Autonomous section in the Team page.
    with auto_tab:
        note_scouting_manager.generate_team_autonomous_graphs(team_number)

    # Generate the metrics and bar plots for the Teleop section in the Team page.
    with teleop_tab:
        note_scouting_manager.generate_team_teleop_graphs(team_number)






