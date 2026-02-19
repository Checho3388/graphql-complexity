from graphql import IntValueNode, ListValueNode
from graphql_complexity.estimators.base import ComplexityEstimator


class ArgumentsEstimator(ComplexityEstimator):
    """
    Estimates complexity by multiplying a base value by
    numeric argument values (e.g. first, limit, ids).

    Usage:
        estimator = ArgumentsEstimator(
            multipliers=["limit", "first", "ids"],
            default_complexity=1,
        )
    """

    def __init__(
        self,
        multipliers: list[str],
        default_complexity: int = 1,
    ):
        self.multipliers = multipliers
        self.default_complexity = default_complexity

    def get_field_complexity(self, node, type_info, path) -> int:
        multiplier = self._get_multiplier(node)
        return self.default_complexity * multiplier

    def _get_multiplier(self, node) -> int:
        for arg in node.arguments or []:
            if arg.name.value in self.multipliers:
                value = self._extract_value(arg.value)
                if value is not None:
                    return value
        return 1

    def _extract_value(self, value_node) -> int | None:
        # limit: 10  →  10
        if isinstance(value_node, IntValueNode):
            return int(value_node.value)
        # ids: ["a", "b", "c"]  →  3 (length of list)
        if isinstance(value_node, ListValueNode):
            return len(value_node.values)
        return None
