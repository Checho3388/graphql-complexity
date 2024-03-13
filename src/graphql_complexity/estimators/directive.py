from typing import Any

from graphql import Visitor, parse, visit, DirectiveNode, DirectiveDefinitionNode, BooleanValueNode, IntValueNode

from graphql_complexity.estimators.base import ComplexityEstimator

DIRECTIVE_ESTIMATOR_FIELD_COMPLEXITY_NAME = "value"
DEFAULT_COMPLEXITY_DIRECTIVE_NAME = "complexity"
DEFAULT_COMPLEXITY_VALUE = 1


class SchemaDirectivesVisitor(Visitor):
    """Visitor that visits the schema and collects the complexity definition for every
    fields"""
    def __init__(self, schema_directive_name: str, collector: dict[str, int]):
        self._collector = collector
        self.schema_directive_name = schema_directive_name
        super().__init__()

    def enter_field_definition(self, node, *args, **kwargs):
        complexity_directive = get_complexity_directive(node)
        if complexity_directive:
            complexity = parse_complexity_directive(complexity_directive)
            self._collector[node.name.value] = complexity


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
    schema_directives: dict[str, Any]

    def __init__(
        self,
        schema: str,
        default_complexity: int = DEFAULT_COMPLEXITY_VALUE,
    ):
        self.__default_complexity = int(default_complexity)
        self.__complexity_map = self.collect_from_schema(
            schema=schema, schema_directive_name=DEFAULT_COMPLEXITY_DIRECTIVE_NAME
        )
        super().__init__()

    @staticmethod
    def collect_from_schema(schema: str, schema_directive_name: str) -> dict[str, int]:
        collector: dict[str, Any] = {}
        ast = parse(schema)
        visitor = SchemaDirectivesVisitor(collector=collector, schema_directive_name=schema_directive_name)
        visit(ast, visitor)
        return collector

    def get_field_complexity(self, node, type_info, path) -> int:
        return self.__complexity_map.get(node.name.value, self.__default_complexity)

    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        # ToDo: Implement this method
        return 1


def get_complexity_directive(node) -> DirectiveNode | None:
    return next(
        (d for d in node.directives if d.name.value == DEFAULT_COMPLEXITY_DIRECTIVE_NAME),
        None
    )


def parse_complexity_directive(directive: DirectiveNode) -> int | None:
    return next(
        (
            int(arg.value.value)
            for arg in directive.arguments
            if arg.name.value == DIRECTIVE_ESTIMATOR_FIELD_COMPLEXITY_NAME and isinstance(arg.value, IntValueNode)
        ),
        None
    )
