import streamlit as st

from utils import GeneralConstants, GraphType

from src.page_managers.match_accuracy_manager import MatchAccuracyManager
from pandas import DataFrame

# Configuration for Streamlit
st.set_page_config(
    layout="wide",
    page_title="Match",
    page_icon="",
)

match_accuracy_manager = MatchAccuracyManager()

if __name__ == '__main__':
    st.write("# Match Accuracy")

    st.text("")

    acc_table : DataFrame = match_accuracy_manager.generate_match_accuracy_table()
    return_table = st.dataframe(acc_table, hide_index=True, use_container_width=True)