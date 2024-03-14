import dataclasses
import logging
from typing import Any

from graphql import (
    GraphQLList,
    TypeInfo,
    get_named_type,
    is_introspection_type, FieldNode
)

from graphql_complexity.config import Config
from graphql_complexity.evaluator.utils import get_node_argument_value, is_meta_type

logger = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True, kw_only=True)
class ComplexityNode:
    name: str
    parent: 'ComplexityNode' = None
    children: list['ComplexityNode'] = dataclasses.field(default_factory=list)

    def evaluate(self) -> int:
        raise NotImplementedError

    def describe(self, depth=0) -> str:
        """Return a friendly representation of the node and its children complexity."""
        return (
            f"{chr(9) * depth}{self.name} ({self.__class__.__name__}) = {self.evaluate()}" +
            f"{chr(10) if self.children else ''}" +
            '\n'.join(c.describe(depth=depth+1) for c in self.children)
        )

    def add_child(self, node: 'ComplexityNode') -> None:
        """Add a child to the current node."""
        self.children.append(node)
        node.parent = self


@dataclasses.dataclass(slots=True, kw_only=True)
class RootNode(ComplexityNode):
    def evaluate(self) -> int:
        return sum(child.evaluate() for child in self.children)


@dataclasses.dataclass(slots=True, kw_only=True)
class FragmentSpreadNode(ComplexityNode):
    fragments_definition: dict

    def evaluate(self):
        fragment = self.fragments_definition.get(self.name)
        if not fragment:
            return 0
        return fragment.evaluate()


@dataclasses.dataclass(slots=True, kw_only=True)
class Field(ComplexityNode):
    complexity: int

    def evaluate(self) -> int:
        return self.complexity + sum(child.evaluate() for child in self.children)


@dataclasses.dataclass(slots=True, kw_only=True)
class ListField(Field):
    count: int = 1

    def evaluate(self) -> int:
        return self.complexity + self.count * sum(child.evaluate() for child in self.children)


@dataclasses.dataclass(slots=True, kw_only=True)
class SkippedField(ComplexityNode):
    wraps: ComplexityNode

    @classmethod
    def wrap(cls, node: ComplexityNode):
        wrapper = cls(
            name=node.name,
            parent=node.parent,
            children=node.children,
            wraps=node,
        )
        node.parent.children.remove(node)
        node.parent.add_child(wrapper)
        return wrapper

    def evaluate(self) -> int:
        return 0


@dataclasses.dataclass(slots=True, kw_only=True)
class MetaField(ComplexityNode):

    def evaluate(self) -> int:
        return 0


def build_node(
    node: FieldNode,
    type_info: TypeInfo,
    complexity: int,
    variables: dict[str, Any],
    config: Config,
) -> ComplexityNode:
    """Build a complexity node from a field node."""
    type_ = type_info.get_type()
    if is_meta_type(type_, node):
        return MetaField(name=node.name.value)
    if isinstance(type_, GraphQLList):
        return build_list_node(node, complexity, variables, config)
    return Field(
        name=node.name.value,
        complexity=complexity,
    )


def build_list_node(node: FieldNode, complexity: int, variables: dict[str, Any], config: Config) -> ListField:
    """Build a list complexity node from a field node."""
    if config.count_arg_name:
        try:
            count = int(
                get_node_argument_value(node=node, arg_name=config.count_arg_name, variables=variables)
            )
        except ValueError:
            logger.debug("Missing or invalid value for argument '%s' in node '%s'", config.count_arg_name, node)
            count = config.count_missing_arg_value
    else:
        count = 1
    return ListField(
        name=node.name.value,
        complexity=complexity,
        count=count,
    )
