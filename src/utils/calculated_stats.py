"""File that contains the class which calculates statistics for a team/event/for other purposes."""

from pandas import DataFrame, Series

from .base_calculated_stats import BaseCalculatedStats
from .constants import Criteria, Queries
from .functions import scouting_data_for_team, retrieve_pit_scouting_data

__all__ = ["CalculatedStats"]


class CalculatedStats(BaseCalculatedStats):
    """Utility class for calculating statistics in an event."""

    def __init__(self, data: DataFrame):
        super().__init__(data)

    # Point contribution methods
    def average_points_contributed(self, team_number: int) -> float:
        """Returns the average points contributed by a team.

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average points contributed for.
        """
        return self.points_contributed_by_match(team_number).mean()

    def points_contributed_by_match(self, team_number: int, type_of_grid: str = "") -> Series:
        """Returns the points contributed by match for a team.

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the points contributed over the matches they played.
        :param type_of_grid: Optional argument defining which mode to return the total points for (AutoGrid/TeleopGrid)
        :return: A Series containing the points contributed by said team per match.
        """
        team_data = scouting_data_for_team(team_number, self.data)

        auto_grid_points = team_data[Queries.AUTO_GRID].apply(
            lambda grid_data: sum([
                Criteria.AUTO_GRID_POINTAGE[game_piece[1]]
                for game_piece in grid_data.split("|")
                if game_piece and game_piece != "None"
            ])
        )
        auto_mobility_points = team_data[Queries.LEFT_COMMUNITY].apply(
            lambda left_community: Criteria.BOOLEAN_CRITERIA[left_community] * 3
        )
        auto_charge_station_points = team_data[Queries.AUTO_CHARGING_STATE].apply(
            lambda charging_state: Criteria.AUTO_CHARGE_POINTAGE.get(charging_state, 0)
        )

        teleop_grid_points = team_data[Queries.TELEOP_GRID].apply(
            lambda grid_data: sum([
                Criteria.TELEOP_GRID_POINTAGE[game_piece[1]]
                for game_piece in grid_data.split("|")
                if game_piece and game_piece != "None"
            ])
        )

        endgame_points = team_data[Queries.ENDGAME_FINAL_CHARGE].apply(
            lambda charging_state: Criteria.ENDGAME_POINTAGE.get(charging_state, 0)
        )

        if type_of_grid == Queries.AUTO_GRID:
            return auto_grid_points + auto_mobility_points + auto_charge_station_points
        elif type_of_grid == Queries.TELEOP_GRID:
            return teleop_grid_points

        return (
            auto_grid_points
            + auto_mobility_points
            + auto_charge_station_points
            + teleop_grid_points
            + endgame_points
        )

    def classify_autos_by_match(self, team_number: int) -> Series:
        """Classifies each auto mode performed by a team.
        As of now, this method only classifies grid placement (cable cover/charge station/loading zone).

        :return: A series containing grid placements indicating where the team started.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        positions_to_placements = {
            "1": Queries.LEFT, "2": Queries.LEFT, "3": Queries.RIGHT,
            "4": Queries.COOP, "5": Queries.COOP, "6": Queries.COOP,
            "7": Queries.RIGHT, "8": Queries.RIGHT, "9": Queries.RIGHT
        }

        return team_data[Queries.AUTO_GRID].apply(
            lambda grid_data: (
                positions_to_placements[grid_data[0]]
                if grid_data and grid_data != "None"
                else Queries.LEFT
            )
        )

    # Cycle calculation methods
    def average_cycles(self, team_number: int, type_of_grid: str) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param type_of_grid: The mode to calculate said cycles for (AutoGrid/TeleopGrid)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        return self.cycles_by_match(team_number, type_of_grid).mean()

    def average_cycles_for_height(self, team_number: int, type_of_grid: str, height: str) -> float:
        """Calculates the average cycles for a team in either autonomous or teleop (wrapper around `cycles_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team number to calculate the average cycles for.
        :param type_of_grid: The mode to calculate said cycles for (AutoGrid/TeleopGrid)
        :param height: The height to return cycles by match for (H/M/L)
        :return: A float representing the average cycles for said team in the mode specified.
        """
        return self.cycles_by_height_per_match(team_number, type_of_grid, height).mean()

    def cycles_by_match(self, team_number: int, type_of_grid: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by match for.
        :param type_of_grid: The mode to return cycles by match for (AutoGrid/TeleopGrid)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[type_of_grid].apply(
            lambda grid_data: len(grid_data) if type(grid_data) is list else len(grid_data.split("|"))
        )

    def cycles_by_height_per_match(self, team_number: int, type_of_grid: str, height: str) -> Series:
        """Returns the cycles for a certain mode (autonomous/teleop) and height in a match

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by height per match for.
        :param type_of_grid: The mode to return cycles by match for (AutoGrid/TeleopGrid)
        :param height: The height to return cycles by match for (H/M/L)
        :return: A series containing the cycles per match for the mode specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return team_data[type_of_grid].apply(
            lambda grid_data: len([
                game_piece for game_piece in grid_data.split("|")
                if game_piece and game_piece[1] == height
            ])
        )

    def cycles_by_game_piece_per_match(self, team_number: int, type_of_grid: str, game_piece: str) -> Series:
        """Returns the cycles for a certain game piece across matches.

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team number to calculate the cycles by game piece per match for.
        :param type_of_grid: The type of mode to calculate the game piece cycles for (AutoGrid/TeleopGrid)
        :param game_piece: The type of game piece to count cycles for (cone/cube)
        :return: A series containing the cycles per match for the game piece specified.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        game_piece_positions = (
            {"1", "3", "4", "6", "7", "9"}
            if game_piece == Queries.CONE
            else {"2", "5", "8"}
        )

        return team_data[type_of_grid].apply(
            lambda grid_data: len([
                cycle for cycle in grid_data.split("|")
                if cycle and (
                        cycle[0] in game_piece_positions
                        or cycle[2:] == game_piece
                )
            ])
        )

    # Accuracy methods
    def average_auto_accuracy(self, team_number: int) -> float:
        """Returns the average auto accuracy of a team (wrapper around `auto_accuracy_by_match`).

        The following custom graphs are supported with this function:
        - Bar graph

        :param team_number: The team to determine the average auto accuracy for.
        :return: A float representing a percentage of the average auto accuracy of said team.
        """
        return self.auto_accuracy_by_match(team_number).mean()

    def auto_accuracy_by_match(self, team_number: int) -> Series:
        """Returns the auto accuracy of a team by match.

        The following custom graphs are supported with this function:
        - Line graph
        - Box plot
        - Multi line graph

        :param team_number: The team to determine the auto accuracy per match for.
        :return: A series containing the auto accuracy by match for said team.
        """
        auto_missed_by_match = self.stat_per_match(
            team_number,
            Queries.AUTO_MISSED
        )
        auto_cycles_by_match = self.cycles_by_match(
            team_number,
            Queries.AUTO_GRID
        ) + auto_missed_by_match  # Adding auto missed in order to get an accurate % (2 scored + 1 missed = 33%)
        return 1 - (auto_missed_by_match / auto_cycles_by_match)
    
    def average_driver_rating(self, team_number: int) -> float:
        """Returns the average driver rating of a team

        :param team_number: The team to determine the driver rating for.
        :return: A float representing the average driver rating of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DRIVER_RATING].mean()
    
    def average_defense_rating(self, team_number: int) -> float:
        """Returns the average defense rating of a team

        :param team_number: The team to determine the defense rating for.
        :return: A float representing the average defense rating of said team.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DEFENSE_RATING].mean()
    
    def disables_by_team(self, team_number: int) -> float:
        """Returns a series of data representing the teams disables

        :param team_number: The team to find disable data for.
        :return: A series with the teams disable data.
        """
        return scouting_data_for_team(team_number, self.data)[Queries.DISABLE]
    
    def drivetrain_width_by_team(self, team_number: int) -> float:
        """Returns a float representing the teams drivetrain width

        :param team_number: The team to find disable data for.
        :return: A float with the team drivtrain width in inches
        """
        pit_scouting_data = retrieve_pit_scouting_data()
        return pit_scouting_data[
                            pit_scouting_data["Team Number"] == team_number
                        ].iloc[0]["Drivetrain Width"]

    # Miscellaneous methods
    def driving_index(self, team_number: int) -> float:
        """Determines how fast a team is based on multiplying their teleop cycles by their driver rating.

        - Used for custom graphs with three teams.
        - Used for custom graphs with a full event.

        :param team_number: The team number to calculate a driving index for.
        """
        team_data = scouting_data_for_team(team_number, self.data)
        return self.cycles_by_match(team_number, Queries.TELEOP_GRID).mean() * team_data[Queries.DRIVER_RATING].mean()
