import abc


class ComplexityEstimator(abc.ABC):
    """Interface for the complexity estimator."""
    @abc.abstractmethod
    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        """Return the complexity of the field."""

    @abc.abstractmethod
    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        """Return the multiplier that will be applied to the children of the given node."""
