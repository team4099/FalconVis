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
    TEAM_GOLD_GRADIENT = [
        "#EFAE09",
        "#F1B828",
        "#F5CC65",
        "#F7D784",
        "#F9E1A3",
        "#FBEBC2",
        "#FDF5E0"
    ]

    # Colors
    DARK_RED = "#450a0a"
    DARK_BLUE = "#172554"
    DARK_GREEN = "#052e16"

    # Game piece colors
    CONE_COLOR = PRIMARY_COLOR
    CUBE_COLOR = "#4F46E5"


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023new"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"


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

    TELEOP_GRID = "TeleopGrid"
    ENDGAME_FINAL_CHARGE = "EndgameFinalCharge"
    
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
    

class Criteria:
    """Criteria used in `CalculatedStats`."""

    # Autonomous criteria
    AUTO_GRID_POINTAGE = {
        Queries.LOW: 3,
        Queries.MID: 4,
        Queries.HIGH: 6
    }
    MOBILITY_CRITERIA = {
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


