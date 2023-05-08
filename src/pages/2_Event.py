"""Creates the page for event-specific graphs in Streamlit."""

import streamlit as st

# Configuration for Streamlit
st.set_page_config(
    page_title="Event",
    page_icon="🏅",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Event")
