from typing import Any

from graphql import Visitor, parse, visit

from graphql_complexity.estimators.base import ComplexityEstimator

DIRECTIVE_ESTIMATOR_FIELD_COMPLEXITY_NAME = "value"
DEFAULT_COMPLEXITY_DIRECTIVE_NAME = "complexity"
DEFAULT_COMPLEXITY_VALUE = 1


class DirectivesVisitor(Visitor):
    def __init__(self, directive_name: str, collector: dict[str, int]):
        self._collector = collector
        self.directive_name = directive_name
        super().__init__()

    def enter_field_definition(self, node, key, parent, path, ancestors):
        for directive in node.directives:
            if directive.name.value == self.directive_name:
                complexity = next(
                    arg.value.value
                    for arg in directive.arguments
                    if arg.name.value == DIRECTIVE_ESTIMATOR_FIELD_COMPLEXITY_NAME
                )
                self._collector[node.name.value] = int(complexity)
                break


class DirectivesEstimator(ComplexityEstimator):
    """Complexity estimator that uses directives to get the complexity of the fields.
    The complexity is calculated by visiting the schema and using the complexity
    directive to get the complexity of each field.

    Example:
        Given the following schema:
        ```qgl
            directive @complexity(
              value: Int!
            ) on FIELD_DEFINITION

            type Query {
              oneField: String @complexity(value: 5)
              otherField: String @complexity(value: 1)
            }
        ```
        The complexity of the fields will be:
            - oneField: 5
            - otherField: 1
        And the total complexity will be 6.
    """

    def __init__(
        self,
        schema: str,
        directive_name: str = DEFAULT_COMPLEXITY_DIRECTIVE_NAME,
        missing_complexity: int = DEFAULT_COMPLEXITY_VALUE,
    ):
        self.__directive_name = directive_name
        self.__missing_complexity = int(missing_complexity)
        self.__complexity_map = self.collect_from_schema(
            schema=schema, directive_name=directive_name
        )
        super().__init__()

    @staticmethod
    def collect_from_schema(schema: str, directive_name: str) -> dict[str, int]:
        collector: dict[str, Any] = {}
        ast = parse(schema)
        visitor = DirectivesVisitor(collector=collector, directive_name=directive_name)
        visit(ast, visitor)
        return collector

    def get_field_complexity(self, node, type_info, path) -> int:
        return self.__complexity_map.get(node.name.value, self.__missing_complexity)
