"""Creates the page for event-specific graphs in Streamlit."""

import streamlit as st
from page_managers import EventManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Event",
    page_icon="🏅",
)
event_manager = EventManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Event")
    
    # Show breakdown of event (average cycles of top 8, 16 and 24 teams)
    st.write("### Event Breakdown")
    event_manager.generate_event_breakdown()
    
