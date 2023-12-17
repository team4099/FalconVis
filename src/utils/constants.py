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

    # Game-specific constants
    CHARGE_STATION_LENGTH = 8  # In feet

    # Qualitative data constants
    POSITIVE_TERMS = {"consistent", "speed", "good", "cycle", "fast", "score", "well"}
    NEGATIVE_TERMS = {"can't", "disable", "foul", "bad", "drop", "stuck", "poor", "missed", "slow", "only", "tip", "broke", "struggle", "bug"}


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2022mockdata"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"


class GraphType(Enum):
    """Enum class representing the different graph types (cycle contribution graphs / point contribution graphs)."""
    
    CYCLE_CONTRIBUTIONS = 0
    POINT_CONTRIBUTIONS = 1
    

class Queries:
    """Constants specific to fields in the scouting data."""

    # Constants relating to fields
    MATCH_KEY = "match_key"
    MATCH_NUMBER = "match_number"
    TEAM_NUMBER = "team_number"
    SCOUT_ID = "scout_id"
    ALLIANCE = "alliance"
    DRIVER_STATION = "driver_station"

    # Year specific data points
    AUTO_UPPER_HUB = "auto_upper_hub"
    AUTO_LOWER_HUB = "auto_lower_hub"
    AUTO_MISSES = "auto_misses"
    TAXIED = "taxied"

    TELEOP_LOWER_HUB = "teleop_lower_hub"
    TELEOP_UPPER_HUB = "teleop_upper_hub"
    TELEOP_MISSES = "teleop_misses"

    FINAL_CLIMB_TYPE = "final_climb_type"
    CLIMB_TIME = "climb_time"
    DEFENSE_RATING = "defense_rating"
    DEFENSE_PERCENT = "defense_pct"
    COUNTER_DEFENSE_RATING = "counter_defense_rating"
    COUNTER_DEFENSE_PERCENT = "counter_defense_pct"

    # Alliance constants
    RED_ALLIANCE = "red"
    BLUE_ALLIANCE = "blue"

    # Mode
    AUTO = "auto"
    TELEOP = "teleop"

    # Heights
    UPPER_HUB = "upper_hub"
    LOWER_HUB = "lower_hub"


class NoteScoutingQueries:
    """Constants specific to fields in the note scouting data."""
    AUTO_GRID = "AutoPieces"
    AUTO_ENGAGED = "AutoEngaged"
    AUTO_INTAKE_ACCURACY = "AutoIntakeAccuracy"
    AUTO_DRIVING_SKILLS = "AutoDrivingSkills"
    AUTO_STARTING_POSITION = "AutoStartingPosition"
    AUTO_SCORING_ACCURACY = "AutoScoringAccuracy"

    TELEOP_GRID = "TeleopPieces"
    TELEOP_PATH = "TeleopPath"
    TELEOP_ALIGNING_SPEED = "TeleopAligningSpeed"
    TELEOP_INTAKING_LOCATION = "TeleopIntakingLocation"
    COMMUNITY_DRIVING_SKILLS = "TeleopCommunitySkill"

    DISABLED = "Disabled"
    TIPPY = "Tippy"
    DRIVER_RATING = "DriverRating"
    CONE_INTAKING_SKILLS = "ConeIntakingSkill"
    CUBE_INTAKING_SKILLS = "CubeIntakingSkill"
    LOADING_ZONE_SPEED = "SubstationSpeed"

    CHOICE_NAMES = {
        AUTO_STARTING_POSITION: ["Cable protector side", "Charging station", "Loading zone side"],
        AUTO_SCORING_ACCURACY: ["Lousy", "Poor", "Okay", "Decent", "Great"],
        DRIVER_RATING: ["Very Poor", "Poor", "Average", "Fluid", "Very Fluid"],
        TELEOP_PATH: [
            "No specific path",
            "Cable protector side to loading zone",
            "Over the charging station to loading zone",
            "No cable protector side to loading zone"
        ],
        TELEOP_ALIGNING_SPEED: ["Very Slow", "Slow", "Fast", "Quick"],
        COMMUNITY_DRIVING_SKILLS: ["Very Poor", "Poor", "Well", "Smoothly"],
        TELEOP_INTAKING_LOCATION: ["Ground", "Single substation", "Double substation"],
        CONE_INTAKING_SKILLS: ["Very Poor", "Poor", "Average", "Good", "Very Good"],
        CUBE_INTAKING_SKILLS: ["Very Poor", "Poor", "Average", "Good", "Very Good"],
        LOADING_ZONE_SPEED: ["Very Poor", "Poor", "Average", "Good", "Very Good"],
    }

    @staticmethod
    def classify_driver_rating_from_decimal(rating: float) -> str:
        """Returns the corresponding name for the driver rating based on the rating passed in (like 4.2 -> Very Fluid).

        :param rating: A float representing the rating that should be converted.
        """
        if rating >= 4.5:
            return "Very Fluid"
        elif 4 <= rating < 4.5:
            return "Fluid"
        elif 3 <= rating < 4:
            return "Average"
        elif 2 <= rating < 3:
            return "Poor"
        elif 1 <= rating < 2:
            return "Very Poor"


class Criteria:
    """Criteria used in `CalculatedStats`."""

    # Autonomous criteria
    BOOLEAN_CRITERIA = {
        0: 0,
        "false": 0,
        1: 1,
        "true": 1
    }

    # Endgame Criteria
    ENDGAME_POINTAGE = {
        "Low": 4,
        "Mid": 6,
        "High": 10,
        "Traversal": 15
    }
