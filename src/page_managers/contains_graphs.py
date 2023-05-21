"""Creates the `ContainsGraphs` graph, used for if a page manager class will generate graphs on its page."""

from abc import abstractmethod


class ContainsGraphs:
    """Used to define an abstract method needed for page managers that are generating graphs on their page."""

    @abstractmethod
    def generate_graphs(self, *args, **kwargs) -> NotImplemented:
        """Used to generate graphs on a single page."""
        return NotImplemented
