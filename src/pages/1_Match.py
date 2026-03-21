"""Creates the page for match-specific graphs in Streamlit."""

import streamlit as st

from page_managers import MatchManager
from utils import GeneralConstants, GraphType

st.set_page_config(
    layout="wide",
    page_title="Match",
    page_icon="🏁",
)
match_manager = MatchManager()

if __name__ == '__main__':
    st.write("# Match")

    teams_selected = match_manager.generate_input_section()

    comparison_tab, red_alliance_tab, blue_alliance_tab = st.tabs(
        [":red[Red] vs. :blue[Blue]", ":red[Red Alliance]", ":blue[Blue Alliance]"]
    )

    with comparison_tab:
        st.write("### :red[Red] vs. :blue[Blue] Graphs")
        match_manager.generate_match_prediction_dashboard(*teams_selected)

        st.divider()
        st.write("### Rating Comparisons")
        match_manager.generate_match_prediction_graphs(
            *teams_selected,
            type_of_graph=GraphType.RATING_CONTRIBUTIONS
        )

    with red_alliance_tab:
        st.write("### :red[Red] Alliance Graphs")
        match_manager.generate_alliance_dashboard(
            teams_selected[0],
            color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
        )

        red_auto_tab, red_teleop_tab, red_qualitative_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop + Endgame", "📝 Qualitative"]
        )

        with red_auto_tab:
            match_manager.generate_autonomous_graphs(
                teams_selected[0],
                type_of_graph=GraphType.RATING_CONTRIBUTIONS,
                color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
            )

        with red_teleop_tab:
            match_manager.generate_teleop_graphs(
                teams_selected[0],
                type_of_graph=GraphType.RATING_CONTRIBUTIONS,
                color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
            )

        with red_qualitative_tab:
            match_manager.generate_qualitative_graphs(
                teams_selected[0],
                color_gradient=GeneralConstants.RED_ALLIANCE_GRADIENT
            )

    with blue_alliance_tab:
        st.write("### :blue[Blue] Alliance Graphs")
        match_manager.generate_alliance_dashboard(
            teams_selected[1],
            color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
        )

        blue_auto_tab, blue_teleop_tab, blue_qualitative_tab = st.tabs(
            ["🤖 Autonomous", "🎮 Teleop + Endgame", "📝 Qualitative"]
        )

        with blue_auto_tab:
            match_manager.generate_autonomous_graphs(
                teams_selected[1],
                type_of_graph=GraphType.RATING_CONTRIBUTIONS,
                color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
            )

        with blue_teleop_tab:
            match_manager.generate_teleop_graphs(
                teams_selected[1],
                type_of_graph=GraphType.RATING_CONTRIBUTIONS,
                color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
            )

        with blue_qualitative_tab:
            match_manager.generate_qualitative_graphs(
                teams_selected[1],
                color_gradient=GeneralConstants.BLUE_ALLIANCE_GRADIENT
            )
