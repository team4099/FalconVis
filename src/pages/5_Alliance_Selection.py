"""Creates the page for match-specific graphs in Streamlit, allowing the user to choose the teams.."""

import streamlit as st

from page_managers import AllianceSelectionManager
from utils import GeneralConstants, GraphType

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Alliance Selection",
    page_icon="🤭",
)
alliance_selection_manager = AllianceSelectionManager()

if __name__ == '__main__':
    # Write the title of the page.
    st.write("# Alliance Selection Dashboard")

    # Generate the input section of the `Alliance Selection` page.
    teams_selected = alliance_selection_manager.generate_input_section()

    # Generate alliance dashboard
    alliance_selection_manager.generate_alliance_dashboard(
        teams_selected,
        color_gradient=GeneralConstants.GOLD_GRADIENT
    )

    auto_tab, teleop_tab, rating_tab = st.tabs(
        ["🤖 Autonomous", "🎮 Teleop", "📊 Ratings"]
    )

    with auto_tab:
        auto_cycle_tab, auto_points_tab = st.tabs(
            ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
        )

        with auto_cycle_tab:
            alliance_selection_manager.generate_autonomous_graphs(
                teams_selected,
                type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                color_gradient=GeneralConstants.GOLD_GRADIENT
            )

        with auto_points_tab:
            alliance_selection_manager.generate_autonomous_graphs(
                teams_selected,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                color_gradient=GeneralConstants.GOLD_GRADIENT
            )

    with teleop_tab:
        alliance_selection_manager.generate_drivetrain_dashboard(
            teams_selected,
            color_gradient=GeneralConstants.GOLD_GRADIENT
        )

        teleop_cycle_tab, teleop_points_tab = st.tabs(
            ["📈 Cycle Contribution Graphs", "🧮 Point Contribution Graphs"]
        )

        with teleop_cycle_tab:
            alliance_selection_manager.generate_teleop_graphs(
                teams_selected,
                type_of_graph=GraphType.CYCLE_CONTRIBUTIONS,
                color_gradient=GeneralConstants.GOLD_GRADIENT
            )

        with teleop_points_tab:
            alliance_selection_manager.generate_teleop_graphs(
                teams_selected,
                type_of_graph=GraphType.POINT_CONTRIBUTIONS,
                color_gradient=GeneralConstants.GOLD_GRADIENT
            )

    with rating_tab:
        alliance_selection_manager.generate_rating_graphs(
            teams_selected,
            color_gradient=GeneralConstants.GOLD_GRADIENT
        )
