"""Defines the constants for FalconVis."""

from enum import Enum

__all__ = [
    "Criteria",
    "EventSpecificConstants",
    "GeneralConstants",
    "GraphType",
    "NoteScoutingQueries",
    "Queries"
]


class GeneralConstants:
    """Year-agnostic constants that will remain the same between all events & years."""

    PICKLIST_FIELDS = [
        "Average Teleop Cycles",
        "Average Auto Cycles"
    ]
    SECONDS_TO_CACHE = 60 * 4
    PRIMARY_COLOR = "#EFAE09"
    AVERAGE_FOUL_RATE = 1.06

    # Color sequences
    RED_ALLIANCE_GRADIENT = ["#731111", "#b04949", "#ed8282", "#f5b3b3"]
    BLUE_ALLIANCE_GRADIENT = ["#0b2e61", "#355687", "#7da0d1", "#a8c1e3"]
    GOLD_GRADIENT = ["#ffbd4d", "#ff9000", "#dd5f00"]
    LEVEL_GRADIENT = ["#f44a53", "#ff8800", "#f4c717"]
    # Colors
    DARK_RED = "#450a0a"
    DARK_BLUE = "#172554"
    DARK_GREEN = "#052e16"

    # Game piece colors
    CONE_COLOR = PRIMARY_COLOR
    CUBE_COLOR = "#4F46E5"

    # Game-specific constants
    CHARGE_STATION_LENGTH = 8  # In feet


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023new"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
    NOTE_SCOUTING_URL = (
        f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_qualitative_data.json"
    )
    PIT_SCOUTING_URL = (
        f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_pit_scouting_data.csv"
    )


class GraphType(Enum):
    """Enum class representing the different graph types (cycle contribution graphs / point contribution graphs)."""
    
    CYCLE_CONTRIBUTIONS = 0
    POINT_CONTRIBUTIONS = 1
    

class Queries:
    """Constants specific to fields in the scouting data."""

    # Constants relating to fields
    MATCH_KEY = "MatchKey"
    MATCH_NUMBER = "MatchNumber"
    TEAM_NUMBER = "TeamNumber"

    AUTO_GRID = "AutoGrid"
    AUTO_MISSED = "AutoMissed"
    LEFT_COMMUNITY = "Mobile"
    AUTO_ENGAGE_ATTEMPTED = "AutoAttemptedCharge"
    AUTO_CHARGING_STATE = "AutoChargingState"
    AUTO_CONES = "AutoCones"
    AUTO_CUBES = "AutoCubes"

    TELEOP_GRID = "TeleopGrid"
    ENDGAME_FINAL_CHARGE = "EndgameFinalCharge"

    DRIVER_RATING = "DriverRating"
    DEFENSE_RATING = "DefenseRating"
    DISABLE = "Disable"

    # Constants for different heights
    LOW = "L"
    MID = "M"
    HIGH = "H"

    # Constants for different game pieces
    CONE = "cone"
    CUBE = "cube"

    # Alliance constants
    RED_ALLIANCE = "red"
    BLUE_ALLIANCE = "blue"

    # Grid placements
    LEFT = "left"
    COOP = "coop"
    RIGHT = "right"

    # Custom graph keywords
    ONE_TEAM_KEYWORD = "Used for custom graphs with one team."
    THREE_TEAMS_KEYWORD = "Used for custom graphs with three teams."
    FULL_EVENT_KEYWORD = "Used for custom graphs with a full event."


class NoteScoutingQueries:
    """Constants specific to fields in the note scouting data."""

    AUTO_GRID = "AutoPieces"
    AUTO_ENGAGED = "AutoEngaged"
    AUTO_INTAKE_ACCURACY = "AutoIntakeAccuracy"
    AUTO_DRIVING_SKILLS = "AutoDrivingSkills"

    TELEOP_GRID = "TeleopPieces"


class Criteria:
    """Criteria used in `CalculatedStats`."""

    # Autonomous criteria
    AUTO_GRID_POINTAGE = {
        Queries.LOW: 3,
        Queries.MID: 4,
        Queries.HIGH: 6
    }
    BOOLEAN_CRITERIA = {
        0: 0,
        "false": 0,
        1: 1,
        "true": 1
    }
    AUTO_CHARGE_POINTAGE = {
        "Dock": 8,
        "Engage": 12
    }
    AUTO_ATTEMPT_CRITERIA = {
        "Engage": 1
    }
    SUCCESSFUL_ENGAGE_CRITERIA = {
        "Engage": 1
    }
    SUCCESSFUL_DOCK_CRITERIA = {
        "Dock": 1
    }

    # Teleop Criteria
    TELEOP_GRID_POINTAGE = {
        Queries.LOW: 2,
        Queries.MID: 3,
        Queries.HIGH: 5
    }

    # Endgame Criteria
    ENDGAME_POINTAGE = {
        "Park": 2,
        "Dock": 6,
        "Engage": 10
    }
