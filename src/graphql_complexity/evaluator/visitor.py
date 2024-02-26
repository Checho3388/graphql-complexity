import dataclasses
from typing import Any

from graphql import (
    SKIP,
    BooleanValueNode,
    DirectiveNode,
    FragmentDefinitionNode,
    GraphQLIncludeDirective,
    GraphQLSkipDirective,
    OperationDefinitionNode,
    VariableNode,
    Visitor, is_introspection_type, get_named_type, TypeInfo
)

from graphql_complexity.estimators.base import ComplexityEstimator

UNNAMED_OPERATION = "UnnamedOperation"


@dataclasses.dataclass(frozen=True, slots=True)
class ComplexityEvaluationNode:
    name: str

    def evaluate(
        self, fragments_definition: dict[str, list["ComplexityEvaluationNode"]]
    ) -> int:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True, slots=True)
class LazyFragment(ComplexityEvaluationNode):

    def evaluate(
        self, fragments_definition: dict[str, list["ComplexityEvaluationNode"]]
    ):
        nodes = fragments_definition.get(self.name)
        if not nodes:
            return 0
        return sum(
            node.evaluate(fragments_definition=fragments_definition) for node in nodes
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Field(ComplexityEvaluationNode):
    complexity: int
    multiplier: int

    def evaluate(self, *args, **kwargs) -> int:
        return self.complexity * self.multiplier


class ComplexityVisitor(Visitor):
    """Visitor that calculates the complexity of the operations in the document.
    The complexity is calculated by visiting the document and using the
    ComplexityEstimator to get the complexity of each field.

    The complexity of the fields is calculated by multiplying the complexity of
    the field by the complexity of the parent fields.

    The complexity of the operations is calculated by summing the complexity of
    the fields in the operation.
    """

    def __init__(self, estimator: ComplexityEstimator, type_info: TypeInfo, variables: dict[str, Any] | None = None):
        if not isinstance(estimator, ComplexityEstimator):
            raise ValueError("Estimator must be of type 'ComplexityEstimator'")
        self.estimator: ComplexityEstimator = estimator
        self.variables = variables or {}
        self.type_info = type_info
        self._operations: dict[str, list[ComplexityEvaluationNode]] = {}
        self._fragments: dict[str, list[ComplexityEvaluationNode]] = {}
        self._current_complexity_stack: list[ComplexityEvaluationNode] = []
        self._multipliers_stack = [1]
        self._ignore_until_leave = None
        super().__init__()

    def evaluate(self) -> int:
        """Evaluate the complexity of the operations after visiting the document."""
        complexity = 0
        for operation in self._operations.values():
            complexity += sum(
                n.evaluate(fragments_definition=self._fragments) for n in operation
            )
        return complexity

    def enter_variable_definition(self, node, key, parent, path, ancestors):
        input_variable = self.variables.get(node.variable.name.value)
        if input_variable is None:
            self.variables[node.variable.name.value] = node.default_value.value

    def enter_directive(self, node, key, parent, path, ancestors):
        if not should_include_field(node, self.variables):
            # Pop the last node added (parent) and ignore the next fields until the
            # parent field is left.
            self._ignore_until_leave = self._current_complexity_stack.pop()

    def enter_selection_set(self, node, key, parent, path, ancestors):
        if isinstance(parent, (OperationDefinitionNode, FragmentDefinitionNode)):
            self._multipliers_stack = [1]
        else:
            multiplier = self.estimator.get_field_multiplier(
                node, key, parent, path, ancestors
            )
            self._multipliers_stack.append(multiplier * self._multipliers_stack[-1])

    def leave_selection_set(self, *args, **kwargs):
        self._multipliers_stack.pop()

    def enter_operation_definition(self, *args, **kwargs):
        """Reset the current complexity list on every new operation."""
        self._current_complexity_stack = []

    def leave_operation_definition(self, node, *args, **kwargs):
        """Add the current complexity list to the operations dict."""
        operation_name = node.name.value if node.name else UNNAMED_OPERATION
        self._operations[operation_name] = self._current_complexity_stack

    def enter_field(self, node, key, parent, path, ancestors):
        """Add the complexity of the current field to the current complexity list."""
        type_ = get_named_type(self.type_info.get_type())
        if type_ is not None and is_introspection_type(type_):
            # Skip introspection fields
            return SKIP

        if self._ignore_until_leave is not None:
            # Skip fields until the parent field is left
            return SKIP

        complexity = self.estimator.get_field_complexity(
            node, key, parent, path, ancestors
        )
        self._current_complexity_stack.append(
            Field(
                name=node.name.value,
                complexity=complexity,
                multiplier=self._multipliers_stack[-1],
            )
        )

    def leave_field(self, node, key, parent, path, ancestors):
        if (
            self._ignore_until_leave is not None
            and node.name.value == self._ignore_until_leave.name
        ):
            # If we are leaving the ignored node, reset the flag
            self._ignore_until_leave = None

    def enter_fragment_definition(self, *args, **kwargs):
        """Start a new complexity list for the current fragment."""
        self._current_complexity_stack = []

    def leave_fragment_definition(self, node, *args, **kwargs):
        """Add the current complexity list to the fragments dict."""
        self._fragments[node.name.value] = self._current_complexity_stack

    def enter_fragment_spread(self, node, *args, **kwargs):
        """Add a lazy fragment to the current complexity list."""
        self._current_complexity_stack.append(LazyFragment(name=node.name.value))

    def enter_inline_fragment(self, *args, **kwargs):
        """Start a new complexity list for the current inline fragment."""
        self._current_complexity_stack = []


def should_include_field(node: DirectiveNode, variables: dict[str, Any]) -> bool:
    """Check if a field should be ignored based on the 'skip' and 'include' directives."""
    if node.name.value == GraphQLIncludeDirective.name:
        return get_directive_if_value(node, variables)

    if node.name.value == GraphQLSkipDirective.name:
        return not get_directive_if_value(node, variables)

    return True


def get_directive_if_value(directive: DirectiveNode, variables: dict[str, Any]) -> bool:
    """Returns the value of the `if` argument from the Directive. Used to get the boolean
    value for skip/include directives."""
    if_arg = next(arg for arg in directive.arguments if arg.name.value == "if")
    if isinstance(if_arg.value, VariableNode):
        return bool(variables.get(if_arg.value.name.value))
    elif isinstance(if_arg.value, BooleanValueNode):
        return bool(if_arg.value.value)

    raise ValueError("Value for `if` argument not found")
