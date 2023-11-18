"""Defines graphing functions that are later used in FalconVis that wrap around Plotly."""
import numpy as np
import plotly.express as px
import streamlit as st
from pandas import DataFrame
from plotly.graph_objects import Box, Figure

from .constants import GeneralConstants

__all__ = [
    "box_plot",
    "bar_graph",
    "line_graph",
    "plotly_chart",
    "multi_line_graph",
    "stacked_bar_graph"
]


def _create_df(
    x_axis: list,
    y_axis: list,
    x_axis_label: str,
    y_axis_label: str
) -> DataFrame:
    """Helper function that creates a DF where every element in x_axis and every element in y_axis is mapped to each other in a DataFrame.

    :param x_axis: Sequence representing elements in the desired X axis.
    :param y_axis: Sequence representing elements in the desired Y axis.
    :param x_axis_label: Optional label for desired X axis (header for X axis).
    :param y_axis_label: Optional label for desired Y axis (header for Y axis).
    :return: A DataFrame where the headers are `x_axis_label` and `y_axis_label` and each element in `x_axis` is mapped to one in `y_axis`.
    """

    return DataFrame.from_dict(
        [
            {
                x_axis_label: x,
                y_axis_label: y
            } for x, y in zip(x_axis, y_axis)
        ]
    )


def _create_flattened_df(
    x_axis: list,
    y_axis: list[list],
    x_axis_label: str,
    y_axis_label: str
) -> DataFrame:
    """Helper function that creates a flattened DF where every element in x_axis and every element in y_axis (where y_axis is flattened) are mapped to each other in a DataFrame.

    Used primarily for box plots to flatten the structure.

    :param x_axis: Sequence representing elements in the desired X axis.
    :param y_axis: Sequence representing elements in the desired Y axis (nested list).
    :param x_axis_label: Optional label for desired X axis (header for X axis).
    :param y_axis_label: Optional label for desired Y axis (header for Y axis).
    :return: A DataFrame where the headers are `x_axis_label` and `y_axis_label` and each element in `x_axis` is mapped to one in `y_axis`.
    """
    return DataFrame.from_dict(
        [
            {
                x_axis_label: x,
                y_axis_label: value
            } for x, y in zip(x_axis, y_axis) for value in y
        ]
    )


def _create_longform_df(
    x_axis: list,
    y_axis: list,
    x_axis_label: str,
    y_axis_label: list,
    y_axis_title: str
) -> DataFrame:
    """Helper function that creates a long-form DF, used for multi-line chart

    :param x_axis: Sequence representing elements in the desired X axis.
    :param y_axis: Sequence representing elements in the desired Y axis.
    :param x_axis_label: Optional label for desired X axis (header for X axis).
    :param y_axis_label: Optional labels for desired Y axis (header for Y axis).
    :param y_axis_title: The title for the Y-axis.
    :return: A long-form DataFrame where the headers are the id variable (the x-axis label), the repeated variables (the y-axis labels) and their values.
    """

    resultant_df = DataFrame.from_dict(
        [
            {
                x_axis_label: x
            } | {
                individual_label: individual_value
                for individual_label, individual_value in zip(y_axis_label, y)
            }
            for x, y in zip(x_axis, np.transpose(y_axis))
        ]
    )

    resultant_df = resultant_df.melt(
        id_vars=x_axis_label,
        value_vars=y_axis_label,
        var_name="Legend",
        value_name=y_axis_title
    )
    return resultant_df


def _create_multicolumn_df(
    x_axis: list,
    y_axis: list[list],
    x_axis_label: str,
    y_axis_label: list
) -> DataFrame:
    """Helper function that creates a multi column DF, used for hover data

    :param x_axis: Sequence representing elements in the desired X axis.
    :param y_axis: Sequence representing elements in the desired Y axis.
    :param x_axis_label: Optional label for desired X axis (header for X axis).
    :param y_axis_label: Optional labels for desired Y axis (header for Y axis).
    :return: A multiple column DataFrame where the headers are the x-axis label and the y axis labels.
    """
    
    rows = []
    for x, y in zip(x_axis, y_axis):
        row = [x]
        row.extend(y)
        rows.append(row)

    headers = [x_axis_label]
    headers.extend(y_axis_label)

    return DataFrame.from_dict(
        [{header: value for header, value in zip(headers, row)} for row in rows]
    )

  
# Wrapper around `st.plotly_chart` for attaching a configuration making graphs static.
def plotly_chart(fig: Figure, use_container_width: bool = True, **kwargs) -> None:
    """A wrapper around `st.plotly_chart` for plotting Plotly figures.

    Used for attaching configurations and other valuable arguments for our app.

    :param fig: A Plotly figure.
    :param use_container_width: Whether or not to use the full container.
    """
    st.plotly_chart(
        fig,
        use_container_width=use_container_width,
        config={"staticPlot": True},
        **kwargs
    )


# Primitive graphs
def bar_graph(
    x: list,
    y: list,
    x_axis_label: str = "",
    y_axis_label: str = "",
    title: str = "",
    horizontal: bool = False,
    color: str | None = None,
    hover_data: list = None
) -> Figure:
    """
    - Used for custom graphs with one team.
    - Used for custom graphs with three teams.
    - Used for custom graphs with a full event.
    """
    if hover_data:
        data_df = _create_multicolumn_df(x, y, x_axis_label=x_axis_label, y_axis_label=[y_axis_label] + hover_data)
    else:
        data_df = _create_df(x, y, x_axis_label=x_axis_label, y_axis_label=y_axis_label)

    return px.bar(
        data_df,
        x=(y_axis_label if horizontal else x_axis_label),
        y=(x_axis_label if horizontal else y_axis_label),
        title=title,
        orientation=("h" if horizontal else "v"),
        hover_data=hover_data,
        color_discrete_sequence=[
            GeneralConstants.PRIMARY_COLOR if color is None else color
        ]
    ).update_xaxes(
        type="category"
    )


def box_plot(
    x: list,
    y: list,
    x_axis_label: str = "",
    y_axis_label: str = "",
    title: str = "",
    horizontal: bool = False,
    show_underlying_data: bool = False,
    color_sequence: list | None = None
):
    """
    - Used for custom graphs with one team.
    - Used for custom graphs with three teams.
    - Used for custom graphs with a full event.
    """
    # Use graph objects in order to be able to individually color candlesticks.
    fig = Figure()

    for x_data, y_data, color in zip(
        x,
        y,
        (color_sequence if color_sequence else [GeneralConstants.PRIMARY_COLOR] * len(y))
    ):
        fig.add_trace(
            Box(
                y=y_data,
                name=x_data,
                marker_color=color,
                boxpoints=("all" if show_underlying_data else "outliers")
            )
        )

    return fig.update_traces(
        orientation=("h" if horizontal else "v")
    ).update_layout(
        xaxis={"title": x_axis_label},
        yaxis={"title": y_axis_label},
        legend={
            "orientation": "h"
        },
        title_text=title
    ).update_xaxes(
        type="category"
    )


def line_graph(
    ## Hunt the digital realm, where scouting secrets dwell. The team's data treasure, a dataframe's measure, access the latest scouting at the event's leisure.
    
    x: list,
    y: list,
    x_axis_label: str = "",
    y_axis_label: str = "",
    title: str = "",
    color: str | None = None
) -> Figure:
    """
    - Used for custom graphs with one team.
    """
    data_df = _create_df(x, y, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    return px.line(
        data_df,
        x=x_axis_label,
        y=y_axis_label,
        title=title
    ).update_traces(
        line_color=GeneralConstants.PRIMARY_COLOR if color is None else color,
        line={"width": 4}
    )


# Add-on graphs
def multi_line_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: list = ["y"],
    y_axis_title: str = "y",
    title: str = "",
    color_map: dict | None = None
) -> Figure:
    """
    - Used for custom graphs with three teams.
    - Used for custom graphs with a full event.
    """
    data_df = _create_longform_df(
        x,
        y,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        y_axis_title=y_axis_title
    )
    return px.line(
        data_df,
        x=x_axis_label,
        y=y_axis_title,
        color="Legend",
        title=title,
        color_discrete_map=color_map
    ).update_traces(
        line=dict(width=4)
    )


def stacked_bar_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: list = [""],
    y_axis_title: str = "y",
    horizontal: bool = False,
    title: str = "",
    color_map: dict | None = None
) -> Figure:
    data_df = _create_longform_df(
        x,
        y,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        y_axis_title=y_axis_title
    )
    fig = px.bar(
        data_df,
        x=(y_axis_title if horizontal else x_axis_label),
        y=(x_axis_label if horizontal else y_axis_title),
        color="Legend",
        title=title,
        orientation=("h" if horizontal else "v"),
        color_discrete_map=color_map
    ).update_layout(
        legend_traceorder="reversed",
        legend={
            "orientation": "h"
        }
    ).update_xaxes(
        type="category"
    )
    fig.update_xaxes(type='category')
    return fig
