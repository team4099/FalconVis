"""Creates the page for picklist data in Streamlit."""

import streamlit as st
from page_managers import PicklistManager
from utils import retrieve_scouting_data
import pandas as pd

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Picklist",
    page_icon="🫂",
)
picklist_manager = PicklistManager()

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Picklist")

    # Generate the input section of the `Picklist` page.
    fields_selected = picklist_manager.generate_input_section()

    # exportButton = st.button("Export to csv")

    teamsList = []
    for index, row in retrieve_scouting_data().iterrows():
        if row.TeamNumber not in teamsList:
            teamsList.append(row.TeamNumber)

    gridDf = pd.DataFrame({'Team Number': [], 'Auto Cycles': [], 'Teleop Cycles': []})

    for i in teamsList:
       new = [i, picklist_manager.calculated_stats.average_cycles(i, "AutoGrid"), picklist_manager.calculated_stats.average_cycles(i, "TeleopGrid")]
       gridDf.loc[len(gridDf)] = new
    gridDf = gridDf.sort_values(by=['Auto Cycles'], ascending=False)

    if("Average Teleop Cycles" not in fields_selected):
        gridDf = gridDf.drop(['Teleop Cycles'], axis=1)
    if("Average Auto Cycles" not in fields_selected):
            gridDf = gridDf.drop(['Auto Cycles'], axis=1)

    grid_return = st.data_editor(gridDf)

    csv = convert_df(grid_return)

    st.download_button(
       "Press to Download",
       csv,
       "file.csv",
       "text/csv",
       key='download-csv'
    )






