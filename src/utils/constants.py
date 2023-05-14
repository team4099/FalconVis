"""Defines the constants for FalconVis."""

__all__ = [
    "Criteria",
    "EventSpecificConstants",
    "GeneralConstants",
    "Queries"
]


class Criteria:
    """Criteria used in `CalculatedStats`."""

    # Autonomous criteria
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
        "L": 2,
        "M": 3,
        "H": 5
    }

    # Endgame Criteria
    ENDGAME_POINTAGE = {
        "Park": 2,
        "Dock": 6,
        "Engage": 10
    }


class GeneralConstants:
    """Year-agnostic constants that will remain the same between all events & years."""

    PICKLIST_FIELDS = [
        "Average Teleop Cycles",
        "Average Auto Cycles"
    ]
    SECONDS_TO_CACHE = 60 * 4
    PRIMARY_COLOR = "#EFAE09"


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023new"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"


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

