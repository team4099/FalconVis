"""Creates the `PageManager` class which sets up guidelines that all pages' respective page managers should follow."""

from abc import abstractmethod


class PageManager:
    """The base class for all page managers in FalconVis."""

    @abstractmethod
    def generate_input_section(self) -> NotImplemented:
        """Abstract method for all page managers to implement.

        Creates the input section of the page (for example, choosing the team number in the `Teams` page.
        """
        return NotImplemented
    