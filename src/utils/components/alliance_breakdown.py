"""Creates a component to display colored metrics."""

from streamlit.components.v1 import html

__all__ = ["alliance_breakdown"]


def alliance_breakdown(
    team_numbers: list[int],
    average_points_contributed: list[int],
    best_to_defend: int,
    alliance: str
) -> None:
    """Creates a card containing breakdowns of each team on an alliance and their score contributions.

    :param team_numbers: The list of teams to display breakdowns for.
    :param average_points_contributed: A list of average points contributed by team (in order of `team_numbers`)
    :param best_to_defend: A team number representing the team that is "best to defend" in a match.
    :param alliance: The alliance to create the breakdown for to change the background color.
    :return:
    """
    with (
        open("./src/utils/components/alliance_breakdown_component.html") as html_file,
        open("./src/utils/components/defense_svg.html") as defense_svg_file,
        open("./src/utils/components/offense_svg.html") as offense_svg_file
    ):
        defense_svg = defense_svg_file.read()
        offense_svg = offense_svg_file.read()

        html_template = html_file.read().format(
            background_color=(
                "#450a0a" if alliance == "red" else "#172554"  # Dark red/blue constants
            ),
            team_1=team_numbers[0],
            team_1_pts=average_points_contributed[0],
            team_1_svg=(
                defense_svg
                if team_numbers[0] == best_to_defend
                else offense_svg
            ),
            team_2=team_numbers[1],
            team_2_pts=average_points_contributed[1],
            team_2_svg=(
                defense_svg
                if team_numbers[1] == best_to_defend
                else offense_svg
            ),
            team_3=team_numbers[2],
            team_3_pts=average_points_contributed[2],
            team_3_svg=(
                defense_svg
                if team_numbers[2] == best_to_defend
                else offense_svg
            )
        )
        html(html_template, height=130)
