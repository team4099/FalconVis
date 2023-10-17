"""Defines the constants for FalconVis."""

from enum import Enum

__all__ = [
    "Criteria",
    "EventSpecificConstants",
    "GeneralConstants",
    "GraphType",
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
    LIGHT_RED = "#ff7276"
    LIGHT_GREEN = "#00873e"

    # Game piece colors
    CONE_COLOR = PRIMARY_COLOR
    CUBE_COLOR = "#4F46E5"

    # Game-specific constants
    CHARGE_STATION_LENGTH = 8  # In feet

    # Qualitative data constants
    POSITIVE_TERMS = {"consistent", "speed", "good", "cycle", "fast", "score", "well"}
    NEGATIVE_TERMS = {"can't", "disable", "foul", "bad", "drop", "stuck", "poor", "missed", "slow", "only", "tip", "broke", "struggle", "bug"}


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023bob"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
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
    SCOUT_ID = "ScoutId"
    ALLIANCE = "Alliance"
    DRIVER_STATION = "DriverStation"

    # Starting positions
    STARTING_POSITION = "StartingPosition"
    CABLE_COVER = "Cable Cover"
    CHARGE_STATION = "Charge Station"
    LOADING_ZONE = "Loading Zone"

    AUTO_GRID = "AutoGrid"  # Only used as a parameter to signify the mode
    AUTO_HIGH = "AutoHigh"
    AUTO_MID = "AutoMid"
    AUTO_LOW = "AutoLow"
    AUTO_MISSED = "AutoMissed"
    LEFT_COMMUNITY = "Mobile"
    AUTO_ENGAGE_ATTEMPTED = "AutoEngageAttempted"
    AUTO_ENGAGE_SUCCESSFUL = "AutoEngageSuccessful"
    AUTO_CONES = "AutoCones"
    AUTO_CUBES = "AutoCubes"

    TELEOP_GRID = "TeleopGrid"  # Only used as a parameter to signify the mode
    TELEOP_CONES = "TeleopCones"
    TELEOP_CUBES = "TeleopCubes"
    TELEOP_NOTES = "TeleopNotes"
    TELEOP_MISSED = "TeleopMissed"
    ENDGAME_FINAL_CHARGE = "EndgameFinalCharge"

    DRIVER_RATING = "DriverRating"
    DEFENSE_RATING = "DefenseRating"
    DISABLE = "Disable"
    TIPPY = "Tippy"

    # Constants for different heights
    LOW = "Low"
    MID = "Mid"
    HIGH = "High"

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
    

class Criteria:
    """Criteria used in `CalculatedStats`."""

    # Autonomous criteria
    BOOLEAN_CRITERIA = {
        0: 0,
        "false": 0,
        1: 1,
        "true": 1
    }
    AUTO_CHARGE_POINTAGE = {
        "true": 12,
        1: 12,
        0: 0,
        "false": 0
    }
    ENGAGE_CRITERIA = {
        "true": "Engage",
        "false": "None"
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
