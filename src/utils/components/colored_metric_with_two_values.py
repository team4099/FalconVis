"""Creates a component to display colored metrics."""

from typing import Any, Callable
from streamlit.components.v1 import html

__all__ = ["colored_metric_with_two_values"]


def colored_metric_with_two_values(
    metric_title: str,
    metric_subtitle: str,
    metric_first_value: Any,
    metric_second_value: Any,
    *,
    height: int = 130,
    background_color: str = "#OE1117",
    opacity: float = 1.0,
    first_threshold: float | None = None,
    second_threshold: float | None = None,
    invert_threshold: bool = False,
    value_formatter: Callable = None,
    border_color: str | None = None,
    border_opacity: float | None = None,
    create_ring: bool = False,
    ring_color: str = "#262730"
) -> None:
    """Creates a card similar to st.metric that can be colored/customized.

    :param metric_title: The title for the colored metric.
    :param metric_subtitle: The subtitle for the colored metric.
    :param metric_first_value: The first value for the colored metric.
    :param metric_second_value: The second value for the colored metric.
    :param height: A number representing the height of the metric, in pixels. If not specified, the height is automatically found.
    :param background_color: A hex code representing the background color of the metric.
    :param opacity: The opacity of the metric if a background color exists.
    :param first_threshold: If a threshold exists, change the background color to denote whether the metric "passes" a threshold.
    :param second_threshold: If a threshold exists, change the background color to denote whether the metric "passes" a threshold (same as first_threshold but for a diff value).
    :param invert_threshold: Determines whether or not to invert the threshold (greater than threshold = red)
    :param value_formatter: Optional argument that formats the metric value passed in.
    :param border_color: A hex code representing the color of the border attached to the metric.
    :param border_opacity: The opacity of the border if it exists.
    :param create_ring: A boolean representing whether a ring should be created around the metric.
    :param ring_color: A hex code representing the color of the ring if it exists.
    :return:
    """
    # Set background color based on threshold
    if first_threshold is not None and second_threshold is not None:
        if (
                ((metric_first_value >= first_threshold or metric_second_value >= second_threshold) and not invert_threshold)
                or ((metric_first_value <= first_threshold or metric_first_value <= second_threshold) and invert_threshold)
        ):
            background_color = "#052e16"
            opacity = 0.5

        if (
                ((metric_first_value < first_threshold or metric_second_value < second_threshold) and not invert_threshold)
                or ((metric_first_value > first_threshold or metric_second_value > second_threshold) and invert_threshold)
        ):
            background_color = "#450a0a"
            opacity = 0.5

    # Style card to use background color if border color isn't defined
    if border_color is None:
        border_color = background_color
        border_opacity = (1 if border_opacity is None else border_opacity)

    with open("./mount/src/utils/components/colored_metric_with_two_values_component.html") as html_file:
        html_content = html_file.read().split("\n\n")
        html_template = html_content[0] + html_content[1].format(
            metric_title=metric_title,
            metric_subtitle=metric_subtitle,
            metric_first_value=(str(metric_first_value) if value_formatter is None else value_formatter(metric_first_value)),
            metric_second_value=(str(metric_second_value) if value_formatter is None else value_formatter(metric_second_value)),
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

