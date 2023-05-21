"""Defines graphing functions that are later used in FalconVis that wrap around Plotly."""

import plotly.express as px
from pandas import DataFrame
from plotly.graph_objects import Figure

from .constants import GeneralConstants

__all__ = [
    "line_graph"
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
    )
