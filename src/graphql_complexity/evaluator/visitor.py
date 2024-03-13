from typing import Any

from graphql import (
    DirectiveNode,
    GraphQLIncludeDirective,
    GraphQLSkipDirective,
    TypeInfo,
    Visitor
)

from graphql_complexity.estimators.base import ComplexityEstimator
from . import nodes
from .utils import get_node_argument_value
from ..config import Config


class ComplexityVisitor(Visitor):
    """Visitor that calculates the complexity of the operations in the document.
    The complexity is calculated by visiting the document and using the
    ComplexityEstimator to get the complexity of each field.

    The complexity of the fields is calculated by multiplying the complexity of
    the field by the complexity of the parent fields.

    The complexity of the operations is calculated by summing the complexity of
    the fields in the operation.
    """

    def __init__(
            self,
            estimator: ComplexityEstimator,
            type_info: TypeInfo,
            config: Config = None,
            variables: dict[str, Any] | None = None,
    ):
        if not isinstance(estimator, ComplexityEstimator):
            raise ValueError("Estimator must be of type 'ComplexityEstimator'")
        self.config = config or Config()
        self.estimator: ComplexityEstimator = estimator
        self.variables = variables or {}
        self.type_info = type_info
        self.fragments: dict[str, nodes.ComplexityNode] = {}
        self.root = nodes.RootNode(name="root")
        self.current_node = self.root
        self._previous_current_node = None
        super().__init__()

    @property
    def complexity_tree(self) -> nodes.ComplexityNode:
        """Return the complexity tree after visiting the document.
        The tree is represented by a RootNode with the complexity of the operations
        represented as Node children. Each node is evaluated returning the complexity."""
        return self.root

    def enter_variable_definition(self, node, key, parent, path, ancestors):
        input_variable = self.variables.get(node.variable.name.value)
        if input_variable is None:
            self.variables[node.variable.name.value] = node.default_value.value

    def enter_directive(self, node, key, parent, path, ancestors):
        if not should_include_field(node, self.variables):
            # Pop the last node added (parent) and ignore the next fields until the
            # parent field is left.
            self.current_node = nodes.SkippedField.wrap(self.current_node)

    def enter_field(self, node, key, parent, path, ancestors):
        """Add the complexity of the current field to the current complexity list."""
        complexity = self.estimator.get_field_complexity(node, self.type_info, path)

        cn = nodes.build_node(node, self.type_info, complexity, self.variables, self.config)
        self.current_node.add_child(cn)
        self.current_node = cn

    def leave_field(self, node, key, parent, path, ancestors):
        self.current_node = self.current_node.parent

    def enter_fragment_definition(self, *args, **kwargs):
        """Start a new complexity list for the current fragment."""
        self._previous_current_node = self.current_node
        self.current_node = nodes.RootNode(name="fragment")

    def leave_fragment_definition(self, node, *args, **kwargs):
        """Add the current complexity list to the fragments dict."""
        self.fragments[node.name.value] = self.current_node
        self.current_node = self._previous_current_node

    def enter_fragment_spread(self, node, *args, **kwargs):
        """Add a lazy fragment to the current complexity list."""
        self.current_node.add_child(
            nodes.FragmentSpreadNode(
                name=node.name.value,
                fragments_definition=self.fragments
            )
        )


def should_include_field(node: DirectiveNode, variables: dict[str, Any]) -> bool:
    """Check if a field should be ignored based on the 'skip' and 'include' directives."""
    if node.name.value == GraphQLIncludeDirective.name:
        value = get_node_argument_value(node=node, arg_name="if", variables=variables)
        return bool(value)

    if node.name.value == GraphQLSkipDirective.name:
        value = get_node_argument_value(node=node, arg_name="if", variables=variables)
        return not bool(value)

    return True
