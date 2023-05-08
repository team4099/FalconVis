"""Creates the page for picklist data in Streamlit."""

import streamlit as st

# Configuration for Streamlit
st.set_page_config(
    page_title="Picklist",
    page_icon="🫂",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Picklist")
