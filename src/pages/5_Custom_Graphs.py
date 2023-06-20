"""Creates the page for creating custom graphs in FalconVis."""

import streamlit as st
from page_managers import CustomGraphsManager

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Custom Graphs",
    page_icon="📊",
)
custom_graphs_manager = CustomGraphsManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Custom Graphs")

    # Generate the input section of the `Custom Graphs` page.
    custom_graphs_manager.generate_input_section()
