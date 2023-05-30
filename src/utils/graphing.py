"""Defines graphing functions that are later used in FalconVis that wrap around Plotly."""
import numpy as np
import plotly.express as px
from pandas import DataFrame
from plotly.graph_objects import Figure

from .constants import GeneralConstants

__all__ = [
    "box_plot",
    "bar_graph",
    "line_graph",
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
    """Helper function that creates a long-form DF, used for stacked graphs (stacked bar chart/multi-line chart/etc.)

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

    return resultant_df.melt(
        id_vars=x_axis_label,
        value_vars=y_axis_label,
        var_name="Legend",
        value_name=y_axis_title
    )


# Primitive graphs
def bar_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: str = "y",
    title: str = "",
    horizontal: bool = False,
    color: str | None = None
) -> Figure:
    data_df = _create_df(x, y, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    return px.bar(
        data_df,
        x=(y_axis_label if horizontal else x_axis_label),
        y=(x_axis_label if horizontal else y_axis_label),
        title=title,
        orientation=("h" if horizontal else "v"),
        color_discrete_sequence=[
            GeneralConstants.PRIMARY_COLOR if color is None else color
        ]
    ).update_xaxes(
        fixedrange=True,
        type="category"
    ).update_yaxes(
        fixedrange=True
    )


def box_plot(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: str = "y",
    title: str = "",
    horizontal: bool = False,
    show_underlying_data: bool = False,
    color: str | None = None
):
    data_df = _create_flattened_df(x, y, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    return px.box(
        data_df,
        x=(y_axis_label if horizontal else x_axis_label),
        y=(x_axis_label if horizontal else y_axis_label),
        title=title,
        orientation=("h" if horizontal else "v"),
        points=("all" if show_underlying_data else "outliers")
    ).update_traces(
        marker_color=(GeneralConstants.PRIMARY_COLOR if color is None else color)
    ).update_xaxes(
        fixedrange=True,
        type="category"
    ).update_yaxes(
        fixedrange=True
    )


def line_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: str = "y",
    title: str = "",
    color: str | None = None
) -> Figure:
    data_df = _create_df(x, y, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    return px.line(
        data_df,
        x=x_axis_label,
        y=y_axis_label,
        title=title
    ).update_traces(
        line_color=GeneralConstants.PRIMARY_COLOR if color is None else color
    ).update_xaxes(
        fixedrange=True,
        type="category"
    ).update_yaxes(
        fixedrange=True
    )


# Add-on graphs
def multi_line_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: list = ["y"],
    y_axis_title: str = "y",
    title: str = ""
) -> Figure:
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
        title=title
    ).update_xaxes(
        fixedrange=True,
        type="category"
    ).update_yaxes(
        fixedrange=True
    )


def stacked_bar_graph(
    x: list,
    y: list,
    x_axis_label: str = "x",
    y_axis_label: list = ["y"],
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
    return px.bar(
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
        },
    ).update_xaxes(
        fixedrange=True,
        type="category"
    ).update_yaxes(
        fixedrange=True
    )
