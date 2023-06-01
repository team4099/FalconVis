"""Creates a component to display colored metrics."""

from typing import Any, Callable
from streamlit.components.v1 import html

__all__ = ["colored_metric"]


def colored_metric(
    metric_title: str,
    metric_value: Any,
    *,
    height: int = 130,
    background_color: str = "#OE1117",
    opacity: float = 1.0,
    threshold: float | None = None,
    value_formatter: Callable = None,
    border_color: str | None = None,
    border_opacity: float | None = None,
    create_ring: bool = False,
    ring_color: str = "#262730"
) -> None:
    """Creates a card similar to st.metric that can be colored/customized.

    :param metric_title: The title for the colored metric.
    :param metric_value: The value for the colored metric.
    :param height: A number representing the height of the metric, in pixels. If not specified, the height is automatically found.
    :param background_color: A hex code representing the background color of the metric.
    :param opacity: The opacity of the metric if a background color exists.
    :param threshold: If a threshold exists, change the background color to denote whether the metric "passes" a threshold.
    :param value_formatter: Optional argument that formats the metric value passed in.
    :param border_color: A hex code representing the color of the border attached to the metric.
    :param border_opacity: The opacity of the border if it exists.
    :param create_ring: A boolean representing whether a ring should be created around the metric.
    :param ring_color: A hex code representing the color of the ring if it exists.
    :return:
    """
    # Set background color based on threshold
    if threshold is not None and metric_value >= threshold:
        background_color = "#052e16"
        opacity = 0.5
    elif threshold is not None and metric_value < threshold:
        background_color = "#450a0a"
        opacity = 0.5

    # Style card to use background color if border color isn't defined
    if border_color is None:
        border_color = background_color
        border_opacity = 1

    with open("./src/utils/components/colored_metric_component.html") as html_file:
        html_template = html_file.read().format(
            metric_title=metric_title,
            metric_value=(str(metric_value) if value_formatter is None else value_formatter(metric_value)),
            height=f"[{height}px]",
            background_color=background_color,
            opacity=str(opacity),
            border_color=border_color,
            border_opacity=border_opacity,
            ring=(
                ""
                if not create_ring
                else f"ring ring-[{ring_color}] ring-offset-2"
            )
        )

        html(
            html_template,
            height=height
        )

