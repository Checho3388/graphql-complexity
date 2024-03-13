import abc


class ComplexityEstimator(abc.ABC):
    """Interface for the complexity estimator."""
    @abc.abstractmethod
    def get_field_complexity(self, node, type_info, path) -> int:
        """Return the complexity of the field."""
