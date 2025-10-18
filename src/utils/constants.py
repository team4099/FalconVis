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
    GREEN_TO_PURPLE_GRADIENT = ["#68D391", "#B794F4"]
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
    EVENT_CODE = "2025mdbob"
    EVENT_NAME = "Battle o' Baltimore"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
    NOTE_SCOUTING_URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_qualitative_data.json"
    PIT_SCOUTING_URL = (
        f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_pit_scouting_data.csv"
    )
    PICKLIST_URL = "https://www.notion.so/team4099/d19066533a8844d3aa2cd9e68e70f214?v=56e109b2298d46ebb00057f05d38bba8"
    # if no connection
    LOCAL_JSON_PATH = "./src/utils/backup_match_data.json"


class GraphType(Enum):
    """Enum class representing the different graph types (cycle contribution graphs / point contribution graphs)."""

    CYCLE_CONTRIBUTIONS = 0
    POINT_CONTRIBUTIONS = 1


class Queries:
    """Constants specific to fields in the scouting data."""

    # Constants relating to fields
    SCOUT_ID = "ScoutId"
    MATCH_KEY = "MatchKey"
    MATCH_NUMBER = "MatchNumber"
    TEAM_NUMBER = "TeamNumber"

    STARTING_POSITION = "StartingPosition"
    LEFT_STARTING_ZONE = "AutoLeave"
    SCORING_SIDE = "ScoringSide"
    AUTO_CORAL_L1 = "AutoCoralL1"
    AUTO_CORAL_L2 = "AutoCoralL2"
    AUTO_CORAL_L3 = "AutoCoralL3"
    AUTO_CORAL_L4 = "AutoCoralL4"
    AUTO_CORAL_MISSES = "AutoCoralMisses"
    AUTO_BARGE = "AutoBarge"
    AUTO_PROCESSOR = "AutoProcessor"

    TELEOP_CORAL_L1 = "TeleopCoralL1"
    TELEOP_CORAL_L2 = "TeleopCoralL2"
    TELEOP_CORAL_L3 = "TeleopCoralL3"
    TELEOP_CORAL_L4 = "TeleopCoralL4"
    TELEOP_CORAL_MISSES = "TeleopCoralMisses"
    TELEOP_BARGE = "TeleopAlgaeBarge"
    TELEOP_PROCESSOR = "TeleopAlgaeProcessor"
    TELEOP_ALGAE_REMOVAL = "TeleopAlgaeRemoval"

    PARKED_UNDER_BARGE = "Parked"
    CLIMBED_CAGE = "ClimbStatus"
    CLIMB_SPEED = "ClimbSpeed"

    DRIVER_RATING = "DriverRating"
    ROBOT_STYLE_TYPE = "RobotStyleType"
    INTAKE_SPEED = "IntakeSpeed"
    DEFENSE_RATING = "DefenseRating"
    INTAKE_DEFENSE_RATING = "IntakeDefenseRating"
    DISABLE = "Disabled"
    STABILITY = "StabilityRating"

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
    AUTO_CORAL = "AutoCoral"
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
        "No Climb": 2,
        "Shallow Climb": 6,
        "Deep Climb": 12
    }

    CLIMBING_CRITERIA = {
        "No Climb": 0,
        "Shallow Climb": 1,
        "Deep Climb": 1
    }

    # Ratings criteria
    DRIVER_RATING_CRITERIA = {
        "Very Fluid": 5,
        "Fluid": 4,
        "Average": 3,
        "Poor": 2,
        "Very Poor": 1
    }
    INTAKE_SPEED_CRITERIA = {
        "Very Fast": 5,
        "Fast": 4,
        "Average": 3,
        "Slow": 2,
        "Very Slow": 1
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
