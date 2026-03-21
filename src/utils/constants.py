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
        "Average Driver Rating",
        "Average Throughput Speed",
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

    # General game constants
    TELEOP_TOTAL_TIME = (2 * 60 + 15)
    TELEOP_MINUS_ENDGAME = TELEOP_TOTAL_TIME - 20

    # Sentiment analysis terms
    POSITIVE_TERMS = {"consistent", "speed", "good", "cycle", "fast", "score", "well", "amazing", "spectactular"}
    NEGATIVE_TERMS = {"can't", "disable", "foul", "bad", "drop", "stuck", "poor", "missed", "slow", "only", "tip", "broke", "struggle", "bug", "prone", "beached"}


class EventSpecificConstants:
    """Constants specific to an event."""
    EVENT_CODE = "2026vache"
    EVENT_NAME = "Week 3 Chesapeake"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
    NOTE_SCOUTING_URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_qualitative_data.json"
    PIT_SCOUTING_URL = (
        f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_pit_scouting_data.json"
    )
    PICKLIST_URL = "https://www.notion.so/team4099/d19066533a8844d3aa2cd9e68e70f214?v=56e109b2298d46ebb00057f05d38bba8"
    # if no connection
    LOCAL_JSON_PATH = f"./src/data/{EVENT_CODE}_match_data.json"


class GraphType(Enum):
    """Enum class representing the different graph types."""

    RATING_CONTRIBUTIONS = 0
    POINT_CONTRIBUTIONS = 1


class Queries:
    """Constants specific to fields in the scouting data."""

    # Identity / match fields
    SCOUT_ID = "ScoutId"
    MATCH_KEY = "MatchKey"
    MATCH_NUMBER = "MatchNumber"
    TEAM_NUMBER = "TeamNumber"
    ALLIANCE = "Alliance"
    DRIVER_STATION = "DriverStation"

    # Robot placement / movement fields
    STARTING_POSITION = "StartingPosition"
    AUTO_SCORING_SIDE = "AutoScoringSide"
    AUTO_TRENCH_BUMP = "AutoTrenchBump"
    TELEOP_SCORING_SIDE = "TeleopScoringSide"
    TELEOP_TRENCH_BUMP = "TeleopTrenchBump"

    # Auto fields
    AUTO_CLIMB = "AutoClimb"
    AUTO_NOTES = "AutoNotes"

    # Teleop fields
    SHOOT_ON_THE_MOVE = "ShootOnTheMove"
    TELEOP_CLIMB = "TeleopClimb"
    CLIMB_SPEED = "ClimbSpeed"
    TELEOP_NOTES = "TeleopNotes"

    # Robot state
    DISABLE = "Disabled"

    # Qualitative ratings
    STABILITY = "StabilityRating"
    ROBOT_STYLE_TYPE = "RobotStyleType"
    DRIVER_RATING = "DriverRating"
    INTAKE_SPEED = "IntakeSpeed"
    THROUGHPUT_SPEED = "ThroughputSpeed"
    DEFENSE_RATING = "DefenseRating"
    SHOOTER_DEFENSE_RATING = "ShooterDefenseRating"
    INTAKE_DEFENSE_RATING = "IntakeDefenseRating"
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

    # Boolean string criteria (AutoClimb, Disabled, ShootOnTheMove are stored as strings)
    BOOLEAN_CRITERIA = {
        0: 0,
        "false": 0,
        1: 1,
        "true": 1,
        False: 0,
        True: 1
    }

    # Endgame / Climb criteria
    CLIMBING_CRITERIA = {
        None: 0,
        "No climb": 0,
        "L1": 1,
        "L2": 2,
        "L3": 3
    }

    CLIMBING_POINTAGE = {
        "No climb": 0,
        "L1": 10,
        "L2": 20,
        "L3": 30
    }

    CLIMB_SPEED_CRITERIA = {
        "<5 seconds": 5,
        "5-10 seconds": 4,
        "10-20 seconds": 3,
        ">20 seconds": 2,
        "": 0
    }

    STABILITY_CRITERIA = {
        "Stable": 3,
        "Moderately tippy": 2,
        "Very tippy": 1
    }

    # Rating criteria
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

    BASIC_RATING_CRITERIA = {
        "Very Good": 5,
        "Good": 4,
        "Okay": 3,
        "Poor": 2,
        "Very Poor": 1
    }
