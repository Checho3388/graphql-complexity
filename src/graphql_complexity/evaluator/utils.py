from typing import Any

from graphql import (
    DirectiveNode,
    FieldNode,
    VariableNode,
    get_named_type,
    is_introspection_type,
)


def get_node_argument_value(node: FieldNode | DirectiveNode, arg_name: str, variables: dict[str, Any]) -> Any:
    """Returns the value of the argument given by parameter."""
    arg = next((arg for arg in node.arguments if arg.name.value == arg_name), None)
    if not arg:
        raise ValueError(f"Value for {arg_name!r} not found in {node.name.value!r} arguments")

    if isinstance(arg.value, VariableNode):
        return variables.get(arg.value.name.value)

    return arg.value.value


def is_meta_type(type_, node) -> bool:
    """Check if the field is a meta field."""
    unwrapped_type = get_named_type(type_)
    return any(
        (
            unwrapped_type is not None and is_introspection_type(unwrapped_type),
            unwrapped_type is not None and node.name.value == "__typename",
        )
    )
