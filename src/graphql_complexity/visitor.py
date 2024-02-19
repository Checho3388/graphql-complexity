import dataclasses

from graphql import Visitor, OperationDefinitionNode, FragmentDefinitionNode

from graphql_complexity.estimators import ComplexityEstimator

UNNAMED_OPERATION = "UnnamedOperation"


@dataclasses.dataclass(frozen=True, slots=True)
class LazyFragment:
    name: str
    fragments: dict[str, list["Field"]]

    def evaluate(self):
        nodes = self.fragments[self.name]
        return sum(node.evaluate() for node in nodes)


@dataclasses.dataclass(frozen=True, slots=True)
class Field:
    complexity: int
    multiplier: int
    name: str

    def evaluate(self):
        return self.complexity * self.multiplier


class ComplexityVisitor(Visitor):
    """Visitor that calculates the complexity of the operations in the document.
    The complexity is calculated by visiting the document and using the
    ComplexityEstimator to get the complexity of each field.

    The complexity of the fields is calculated by multiplying the complexity of
    the field by the complexity of the parent fields.

    The complexity of the operations is calculated by summing the complexity of
    the fields in the operation.

    Examples:
        >>> from graphql import parse, visit
        >>> from src.estimators import SimpleEstimator
        >>> from src.visitor import ComplexityVisitor
        >>> query = "query { user { name  email } }"
        >>> ast = parse(query)
        >>> visitor = ComplexityVisitor(estimator=SimpleEstimator())
        >>> exc = visit(ast, visitor)
        >>> visitor.evaluate()
        3

    """

    def __init__(self, estimator: ComplexityEstimator):
        self.estimator: ComplexityEstimator = estimator
        self.operations: dict[str, list[Field]] = {}
        self.fragments: dict[str, list[Field]] = {}
        self.current_complexity: list[Field | LazyFragment] = []
        self.in_fragment_definition: bool = False
        self.multipliers = [1]
        super().__init__()

    def evaluate(self) -> int:
        """Evaluate the complexity of the operations after visiting the document."""
        complexity = 0
        for operation in self.operations.values():
            complexity += sum(n.evaluate() for n in operation)
        return complexity

    def enter_selection_set(self, node, key, parent, path, ancestors):
        if isinstance(parent, (OperationDefinitionNode, FragmentDefinitionNode)):
            self.multipliers = [1]
        else:
            multiplier = self.estimator.get_field_multiplier(
                node, key, parent, path, ancestors
            )
            self.multipliers.append(multiplier * self.multipliers[-1])

    def leave_selection_set(self, *args, **kwargs):
        self.multipliers.pop()

    def enter_operation_definition(self, *args, **kwargs):
        """Reset the current complexity list on every new operation."""
        self.current_complexity = []

    def leave_operation_definition(self, node, *args, **kwargs):
        """Add the current complexity list to the operations dict."""
        operation_name = node.name.value if node.name else UNNAMED_OPERATION
        self.operations[operation_name] = self.current_complexity

    def enter_field(self, node, key, parent, path, ancestors):
        """Add the complexity of the current field to the current complexity list."""
        complexity = self.estimator.get_field_complexity(
            node, key, parent, path, ancestors
        )
        self.current_complexity.append(
            Field(
                complexity=complexity,
                multiplier=self.multipliers[-1],
                name=node.name.value,
            )
        )

    def enter_fragment_definition(self, *args, **kwargs):
        """Start a new complexity list for the current fragment."""
        self.in_fragment_definition = True
        self.current_complexity = []

    def leave_fragment_definition(self, node, *args, **kwargs):
        """Add the current complexity list to the fragments dict."""
        self.in_fragment_definition = False
        self.fragments[node.name.value] = self.current_complexity

    def enter_fragment_spread(self, node, *args, **kwargs):
        """Add a lazy fragment to the current complexity list."""
        self.current_complexity.append(
            LazyFragment(
                name=node.name.value,
                fragments=self.fragments,
            )
        )
