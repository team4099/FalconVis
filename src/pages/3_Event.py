"""Creates the page for event-specific graphs in Streamlit."""

import streamlit as st

from page_managers import EventManager
from utils import GraphType

st.set_page_config(
    layout="wide",
    page_title="Event",
    page_icon="🏅",
)
event_manager = EventManager()

if __name__ == '__main__':
    st.write("# Event")

    st.write("### Event Breakdown")
    event_manager.generate_event_breakdown()

    st.divider()
    st.write("### Rating Distributions")
    event_manager.generate_event_graphs(type_of_graph=GraphType.RATING_CONTRIBUTIONS)
