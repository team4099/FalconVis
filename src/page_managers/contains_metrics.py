"""Creates the `ContainsMetrics` graph, used for if a page manager class will generate metrics on its page."""

from abc import abstractmethod


class ContainsMetrics:
    """Used to define an abstract method needed for page managers that are generating metrics on their page."""

    @abstractmethod
    def generate_metrics(self) -> NotImplemented:
        """Used to generate metrics on a single page."""
        return NotImplemented
