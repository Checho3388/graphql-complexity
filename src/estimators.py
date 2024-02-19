import abc

from graphql import Visitor, visit, parse


class ComplexityEstimator(abc.ABC):
    @abc.abstractmethod
    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        """Return the complexity of the field."""

    @abc.abstractmethod
    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        """Return the multiplier of the field."""


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
        self.__complexity_constant = complexity
        self.__multiplier_constant = multiplier
        super().__init__()

    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        return self.__complexity_constant

    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        return self.__multiplier_constant


class DirectivesVisitor(Visitor):
    def __init__(self, directive_name: str):
        self.complexity_map = {}
        self.directive_name = directive_name
        super().__init__()

    def enter_field_definition(self, node, key, parent, path, ancestors):
        for directive in node.directives:
            if directive.name.value == self.directive_name:
                complexity = next(
                    arg.value.value
                    for arg in directive.arguments
                    if arg.name.value == "value"
                )
                self.complexity_map[node.name.value] = int(complexity)
                break


DEFAULT_COMPLEXITY_DIRECTIVE_NAME = "complexity"
DEFAULT_COMPLEXITY_VALUE = 1


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
        self.__complexity_map = {}
        self.__schema = schema
        self.__directive_name = directive_name
        self.__missing_complexity = int(missing_complexity)
        self.parse_schema()
        super().__init__()

    def parse_schema(self):
        ast = parse(self.__schema)
        visitor = DirectivesVisitor(directive_name=self.__directive_name)
        visit(ast, visitor)
        self.__complexity_map = visitor.complexity_map

    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        return self.__complexity_map.get(
            node.name.value,
            self.__missing_complexity
        )

    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        return 1
