from graphql_complexity.estimators.base import ComplexityEstimator


class SimpleEstimator(ComplexityEstimator):
    """Simple complexity estimator that returns a constant complexity for all fields.
    Constant can be set in the constructor."""

    def __init__(self, complexity: int = 1):
        if complexity < 0:
            raise ValueError(
                "'complexity' must be a positive integer (greater or equal than 0)"
            )
        self.__complexity_constant = complexity
        super().__init__()

    def get_field_complexity(self, *_, **__) -> int:
        return self.__complexity_constant
