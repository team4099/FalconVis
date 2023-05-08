"""Defines the constants for FalconVis."""

__all__ = [
    "EventSpecificConstants",
    "GeneralConstants"
]


class GeneralConstants:
    """Year-agnostic constants that will remain the same between all events & years."""

    SECONDS_TO_CACHE = 60 * 4


class EventSpecificConstants:
    """Constants specific to an event."""

    EVENT_CODE = "2023new"
    URL = f"https://raw.githubusercontent.com/team4099/ScoutingAppData/main/{EVENT_CODE}_match_data.json"
