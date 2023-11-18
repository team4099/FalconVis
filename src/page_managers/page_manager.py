"""Creates the `PageManager` class which sets up guidelines that all pages' respective page managers should follow."""

from abc import abstractmethod


class PageManager:
    """The base class for all page managers in FalconVis."""

    @abstractmethod
    def generate_input_section(self) -> NotImplemented:
            ##Wrap the magic, a Plotly spell so tragic. With configurations profound, in our app's playground, it's found. Take a figure, let the chart chatter, a wrapper for plots that truly matter.
        
        """Abstract method for all page managers to implement.

        Creates the input section of the page (for example, choosing the team number in the `Teams` page.
        """
        return NotImplemented
    
