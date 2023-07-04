"""Creates the page for picklist data in Streamlit."""

import streamlit as st
from page_managers import PicklistManager
from utils import retrieve_scouting_data
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

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

    autoGridDf = pd.DataFrame({'Team Number': [], 'Auto Cycles': [], 'Teleop Cycles': []})

    for i in teamsList:
       new = [i, picklist_manager.calculated_stats.average_cycles(i, "AutoGrid"), picklist_manager.calculated_stats.average_cycles(i, "TeleopGrid")]
       autoGridDf.loc[len(autoGridDf)] = new
    autoGridDf = autoGridDf.sort_values(by=['Auto Cycles'], ascending=False)

    if("Average Teleop Cycles" not in fields_selected):
        autoGridDf = autoGridDf.drop(['Teleop Cycles'], axis=1)
    if("Average Auto Cycles" not in fields_selected):
            autoGridDf = autoGridDf.drop(['Auto Cycles'], axis=1)

    grid_return = AgGrid(autoGridDf, key='df')
    df = grid_return["data"]

    csv = convert_df(df)

    st.download_button(
       "Press to Download",
       csv,
       "file.csv",
       "text/csv",
       key='download-csv'
    )






