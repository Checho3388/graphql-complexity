from graphql_complexity.estimators.base import ComplexityEstimator


class SimpleEstimator(ComplexityEstimator):
    """Simple complexity estimator that returns a constant complexity and multiplier for all fields.
    Constants can be set in the constructor.

    Example:
        Given the following query:
        ```qgl
            query {
                user {
                    name
                    email
                }
            }
        ```
        As the complexity and multiplier are constant, the complexity of the fields will be:
            - user: 1 * 1 = 1
            - name: 1 * 1 = 1
            - email: 1 * 1 = 1
        And the total complexity will be 3.
    """

    def __init__(self, complexity: int = 1, multiplier: int = 1):
        if complexity < 0:
            raise ValueError(
                "'complexity' must be a positive integer (greater or equal than 0)"
            )
        if multiplier < 0:
            raise ValueError(
                "'multiplier' must be a positive integer (greater or equal than 0)"
            )
        self.__complexity_constant = complexity
        self.__multiplier_constant = multiplier
        super().__init__()

    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        return self.__complexity_constant

    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        return self.__multiplier_constant
