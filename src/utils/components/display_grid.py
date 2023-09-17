"""Creates a component to display a grid full of game pieces scored by a team."""

from pandas import Series
from streamlit.components.v1 import html

from utils.constants import Queries

__all__ = ["display_grid"]


def display_grid(type_of_grid: str, alliance: str, grid_data: Series, component_height: float = 282.5) -> None:
    """Creates a component used for match predictions to display the odds for a certain alliance at winning the match.

    In other words, creates a component that acts as a horizontal stacked bar chart.

    :param type_of_grid: The grid type (autonomous/teleop).
    :param alliance: The alliance the team was on when scoring game pieces onto the grid.
    :param grid_data: The data on where the team scored.
    :param component_height: The height of the component.
    :return:
    """
    with (
        open("./src/utils/components/grid_component.html") as html_file,
        open("./src/utils/components/cone_svg.html") as cone_file,
        open("./src/utils/components/cube_svg.html") as cube_file,
        open("./src/utils/components/circle_svg.html") as circle_file,
    ):
        cone_svg = cone_file.read()
        cube_svg = cube_file.read()
        circle_svg = circle_file.read()
        game_piece_to_svg = {Queries.CUBE: cube_svg, Queries.CONE: cone_svg}

        html_content = html_file.read().split("\n\n")

        # Used to format the grid data into something readable for the program.
        cube_positions = {2, 5, 8}
        formatted_grid_data = {
            "high_game_pieces": [None] * 9,
            "mid_game_pieces": [None] * 9,
            "low_game_pieces": [None] * 9
        }
        height_to_keys = dict(zip(["H", "M", "L"], formatted_grid_data.keys()))
        for game_piece in grid_data:
            if game_piece:
                position = (
                    int(game_piece[0])
                    if alliance.lower() == Queries.BLUE_ALLIANCE
                    else 10 - int(game_piece[0])
                )
                height = game_piece[1]

                if Queries.CUBE in game_piece or (position in cube_positions and height != Queries.LOW):
                    type_of_piece = Queries.CUBE
                else:
                    type_of_piece = Queries.CONE

                formatted_grid_data[height_to_keys[height]][position - 1] = type_of_piece

        # Rewrite dictionary to change each game piece to their respective SVGs and join them together.
        formatted_grid_data = {
            height: "\n".join(game_piece_to_svg.get(game_piece, circle_svg) for game_piece in row_data)
            for height, row_data in formatted_grid_data.items()
        }

        # Generate component using HTML.
        html(
            html_content[0] + html_content[1].format(
                **formatted_grid_data,
                title="Autonomous Grid" if type_of_grid == Queries.AUTO_GRID else "Teleop Grid",
                height=str(component_height)
            ),
            height=component_height
        )
