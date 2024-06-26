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
    SECONDS_TO_CACHE = 60 * 1.5
    PRIMARY_COLOR = "#EFAE09"
    AVERAGE_FOUL_RATE = 1.06

    # Color sequences
    RED_ALLIANCE_GRADIENT = ["#731111", "#b04949", "#ed8282", "#f5b3b3"]
    BLUE_ALLIANCE_GRADIENT = ["#0b2e61", "#355687", "#7da0d1", "#a8c1e3"]
    GOLD_GRADIENT = ["#ffbd4d", "#ff9000", "#dd5f00"]
    LEVEL_GRADIENT = ["#f44a53", "#ff8800", "#f4c717"]
    RED_TO_GREEN_GRADIENT = ["#ffb6b3", "#ffd5d4", "#e7f1e8", "#bde7bd", "#77dd76"]
    SHORT_RED_TO_GREEN_GRADIENT = ["#ffb6b3", "#ffd5d4", "#bde7bd", "#77dd76"]

    # Colors
    DARK_RED = "#450a0a"
    DARK_BLUE = "#172554"
    DARK_GREEN = "#052e16"
    LIGHT_RED = "#ff7276"
    LIGHT_GREEN = "#00873e"

    # Game piece colors
    CONE_COLOR = PRIMARY_COLOR
    CUBE_COLOR = "#4F46E5"

    # General game constants
    TELEOP_TOTAL_TIME = (2 * 60 + 15)
    TELEOP_MINUS_ENDGAME = TELEOP_TOTAL_TIME - 20

    # Sentiment analysis terms
    POSITIVE_TERMS = {"consistent", "speed", "good", "cycle", "fast", "score", "well", "amazing", "spectactular"}
    NEGATIVE_TERMS = {"can't", "disable", "foul", "bad", "drop", "stuck", "poor", "missed", "slow", "only", "tip", "broke", "struggle", "bug", "prone"}


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2024cur"
    EVENT_NAME = "Curie Division"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
    NOTE_SCOUTING_URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_qualitative_data.json"
    PIT_SCOUTING_URL = (
        f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_pit_scouting_data.csv"
    )
    PICKLIST_URL = "https://www.notion.so/team4099/d19066533a8844d3aa2cd9e68e70f214?v=56e109b2298d46ebb00057f05d38bba8"


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

    AUTO_SPEAKER = "AutoSpeaker"
    AUTO_AMP = "AutoAmp"
    AUTO_USED_CENTERLINE = "AutoCenterline"
    LEFT_STARTING_ZONE = "AutoLeave"

    TELEOP_SPEAKER = "TeleopSpeaker"
    TELEOP_AMP = "TeleopAmp"
    TELEOP_TRAP = "TeleopTrap"
    TELEOP_PASSING = "TeleopPassing"

    PARKED_UNDER_STAGE = "Parked"
    CLIMBED_CHAIN = "ClimbStatus"
    HARMONIZED_ON_CHAIN = "Harmonized"
    CLIMB_SPEED = "ClimbSpeed"

    DRIVER_RATING = "DriverRating"
    DEFENSE_TIME = "DefenseTime"
    DEFENSE_SKILL = "DefenseSkill"
    COUNTER_DEFENSE_SKIll = "CounterDefenseSkill"
    DISABLE = "Disabled"

    # Notes
    AUTO_NOTES = "AutoNotes"
    TELEOP_NOTES = "TeleopNotes"
    ENDGAME_NOTES = "EndgameNotes"
    RATING_NOTES = "RatingNotes"

    # Alliance constants
    RED_ALLIANCE = "red"
    BLUE_ALLIANCE = "blue"

    # Modes
    AUTO = "Auto"
    TELEOP = "Teleop"
    ENDGAME = "Endgame"

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
        "true": 1,
        False: 0,
        True: 1
    }

    # Endgame Criteria
    CLIMBING_POINTAGE = {
        "Park": 2,
        "Dock": 6,
        "Engage": 10
    }

    # Ratings criteria
    DRIVER_RATING_CRITERIA = {
        "Very Fluid": 5,
        "Fluid": 4,
        "Average": 3,
        "Poor": 2,
        "Very Poor": 1
    }
    DEFENSE_TIME_CRITERIA = {
        "Very Often": 5,
        "Often": 4,
        "Sometimes": 3,
        "Rarely": 2,
        "Never": 1
    }
    BASIC_RATING_CRITERIA = {
        "Very Good": 5,
        "Good": 4,
        "Okay": 3,
        "Poor": 2,
        "Very Poor": 1
    }
