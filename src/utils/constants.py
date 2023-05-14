"""Defines the constants for FalconVis."""

__all__ = [
    "EventSpecificConstants",
    "GeneralConstants",
    "Queries"
]


class GeneralConstants:
    """Year-agnostic constants that will remain the same between all events & years."""

    PICKLIST_FIELDS = [
        "Average Teleop Cycles",
        "Average Auto Cycles"
    ]
    SECONDS_TO_CACHE = 60 * 4


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023new"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"


class Queries:
    """Constants specific to fields in the scouting data."""

    # Constants relating to fields
    AUTO_GRID = "AutoGrid"
    LEFT_COMMUNITY = "Mobile"
    AUTO_CHARGING_STATE = "AutoChargingState"

    TELEOP_GRID = "TeleopGrid"
    ENDGAME_FINAL_CHARGE = "EndgameFinalCharge"

    # Criterion
    AUTO_CHARGE_POINTAGE = {
        "Dock": 8,
        "Engage": 12
    }
    AUTO_GRID_POINTAGE = {
        "L": 3,
        "M": 4,
        "H": 6
    }
    MOBILITY_CRITERIA = {
        0: 0,
        "false": 0,
        1: 1,
        "true": 1
    }
    TELEOP_GRID_POINTAGE = {
        "L": 2,
        "M": 3,
        "H": 5
    }
    ENDGAME_POINTAGE = {
        "Dock": 6,
        "Engage": 10
    }
