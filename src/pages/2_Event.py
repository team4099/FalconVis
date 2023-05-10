"""Creates the page for event-specific graphs in Streamlit."""

import streamlit as st
from page_managers import EventManager

# Configuration for Streamlit
event_manager = EventManager()
st.set_page_config(
    layout="wide",
    page_title="Event",
    page_icon="🏅",
)

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Event")
