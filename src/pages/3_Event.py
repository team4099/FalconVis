"""Creates the page for event-specific graphs in Streamlit."""

import streamlit as st

from page_managers import EventManager
from utils import GraphType


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
    
    # Show breakdown of event (average points contributed of top 8, 16 and 24 teams)
    st.write("### Event Breakdown")
    event_manager.generate_event_breakdown()

    # Create tabs for fuel-scored/point-contribution event-wide graphs.
    fuel_scored_tab, point_contribution_tab = st.tabs(
        ["⛽ Fuel Scored Graphs", "🧮 Point Contribution Graphs"]
    )

    # Generate auto/teleop event-wide box plots regarding fuel scored.
    with fuel_scored_tab:
        event_manager.generate_event_graphs(
            type_of_graph=GraphType.FUEL_CONTRIBUTIONS
        )

    # Generate auto/teleop event-wide box plots regarding the points contributed.
    with point_contribution_tab:
        event_manager.generate_event_graphs(
            type_of_graph=GraphType.POINT_CONTRIBUTIONS
        )
    
