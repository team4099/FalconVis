"""Creates a component to display win percentages."""

from streamlit.components.v1 import html

__all__ = ["win_percentages"]


def win_percentages(red_odds: float, blue_odds: float) -> None:
    """Creates a component used for match predictions to display the odds for a certain alliance at winning the match.

    In other words, creates a component that acts as a horizontal stacked bar chart.

    :param red_odds: The probability (0-1) of the red alliance winning (eg. 0.2).
    :param blue_odds: The probability (0-1) of the blue alliance winning (eg. 0.8).
    :return:
    """
    with open("./mount/src/utils/components/win_percentages_component.html") as html_file:
        html_template = html_file.read()
        formatted_html = html_template.replace(
            "{red}", f"{red_odds * 100:.1f}"
        ).replace(
            "{blue}", f"{blue_odds * 100:.1f}"
        )

        if red_odds < blue_odds:
            # Fix Z indices so one div is always over another.
            html(
                formatted_html.replace(
                    "{z-red}", f"z-10"
                ).replace(
                    "{z-blue}", f"z-0"
                ),
                height=40
            )
        else:
            html(
                formatted_html.replace(
                    "{z-red}", f"z-0"
                ).replace(
                    "{z-blue}", f"z-10"
                ),
                height=40
            )
