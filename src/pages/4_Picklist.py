"""Creates the page for picklist data in Streamlit."""

import streamlit as st
from page_managers import PicklistManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Picklist",
    page_icon="🫂",
)
picklist_manager = PicklistManager()

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






