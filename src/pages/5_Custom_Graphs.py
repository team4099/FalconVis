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

    # Create two tabs for the Custom Graphs page
    config_tab, graph_tab = st.tabs(
        ["🗃️ Configuring the Graph", "📈 Custom Graph"]
    )

    # Generate the input section of the `Custom Graphs` page.
    with config_tab:
        x_data, y_data, type_of_graph, stat_name = custom_graphs_manager.generate_input_section()

    # Generate the custom graph given the input provided.
    with graph_tab:
        custom_graphs_manager.generate_custom_graph(x_data, y_data, type_of_graph, stat_name)
