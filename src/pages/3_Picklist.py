"""Creates the page for picklist data in Streamlit."""

import streamlit as st
from page_managers import PicklistManager

# Configuration for Streamlit
picklist_manager = PicklistManager()
st.set_page_config(
    layout="wide",
    page_title="Picklist",
    page_icon="🫂",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Picklist")

    # Generate the input section of the `Picklist` page.
    fields_selected = picklist_manager.generate_input_section()
