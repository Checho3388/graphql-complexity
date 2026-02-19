"""Explain module for GraphQL complexity calculations.

This module provides functionality to explain how complexity calculations are performed,
including which estimator was used and a detailed breakdown of the calculation.
"""
from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any

from graphql import TypeInfo, TypeInfoVisitor, parse, visit

from . import nodes
from .visitor import ComplexityVisitor
from ..estimators.simple import SimpleEstimator
from ..estimators.directive import DirectivesEstimator

if TYPE_CHECKING:
    from graphql import GraphQLSchema
    from ..config import Config
    from ..estimators import ComplexityEstimator


@dataclasses.dataclass
class FieldExplanation:
    """Explanation for a single field's complexity."""
    field_path: str
    field_name: str
    node_type: str
    field_complexity: int
    children_complexity: int
    total_complexity: int
    multiplier: int | None = None  # For list fields
    details: dict[str, Any] = dataclasses.field(default_factory=dict)

    def __str__(self) -> str:
        result = f"{self.field_path} ({self.node_type})"
        if self.multiplier:
            result += f" [multiplier: {self.multiplier}]"
        result += f"\n  Field complexity: {self.field_complexity}"
        if self.children_complexity:
            result += f"\n  Children complexity: {self.children_complexity}"
            if self.multiplier:
                result += f" × {self.multiplier} = {self.children_complexity * self.multiplier}"
        result += f"\n  Total: {self.total_complexity}"
        return result


@dataclasses.dataclass
class ExplanationResult:
    """Complete explanation of a complexity calculation."""
    total_complexity: int
    estimator_name: str
    estimator_details: dict[str, Any]
    tree_representation: str
    field_breakdown: list[FieldExplanation]
    query: str

    def __str__(self) -> str:
        """Return a human-readable explanation."""
        lines = [
            "=" * 80,
            "GraphQL Complexity Explanation",
            "=" * 80,
            "",
            f"Total Complexity: {self.total_complexity}",
            "",
            "Estimator Used:",
            f"  Name: {self.estimator_name}",
        ]

        if self.estimator_details:
            lines.append("  Details:")
            for key, value in self.estimator_details.items():
                lines.append(f"    {key}: {value}")

        lines.extend([
            "",
            "Complexity Tree:",
            "-" * 80,
            self.tree_representation,
            "",
            "Field-by-Field Breakdown:",
            "-" * 80,
        ])

        for field_exp in self.field_breakdown:
            lines.append(str(field_exp))
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary representation."""
        return {
            "total_complexity": self.total_complexity,
            "estimator": {
                "name": self.estimator_name,
                "details": self.estimator_details,
            },
            "tree": self.tree_representation,
            "breakdown": [
                {
                    "path": field.field_path,
                    "name": field.field_name,
                    "type": field.node_type,
                    "field_complexity": field.field_complexity,
                    "children_complexity": field.children_complexity,
                    "total_complexity": field.total_complexity,
                    "multiplier": field.multiplier,
                    "details": field.details,
                }
                for field in self.field_breakdown
            ],
            "query": self.query,
        }


def _extract_estimator_details(estimator: ComplexityEstimator) -> dict[str, Any]:
    """Extract details about the estimator being used."""
    details = {}

    if isinstance(estimator, SimpleEstimator):
        # Access the private complexity constant through name mangling
        details["complexity_constant"] = estimator._SimpleEstimator__complexity_constant
    elif isinstance(estimator, DirectivesEstimator):
        details["directive_name"] = estimator._DirectivesEstimator__directive_name
        details["missing_complexity"] = estimator._DirectivesEstimator__missing_complexity
        details["complexity_map"] = estimator._DirectivesEstimator__complexity_map
    else:
        details["type"] = type(estimator).__name__

    return details


def _extract_field_breakdown(
    node: nodes.ComplexityNode,
    path: str = "",
    breakdown: list[FieldExplanation] | None = None
) -> list[FieldExplanation]:
    """Extract field-by-field breakdown from the complexity tree."""
    if breakdown is None:
        breakdown = []

    # Skip root node in the path
    if isinstance(node, nodes.RootNode) and not path:
        current_path = ""
    else:
        current_path = f"{path}.{node.name}" if path else node.name

    # Calculate complexities
    if isinstance(node, (nodes.Field, nodes.ListField)):
        children_complexity = sum(child.evaluate() for child in node.children)

        if isinstance(node, nodes.ListField):
            multiplier = node.count
            total_complexity = node.complexity + multiplier * children_complexity
            field_explanation = FieldExplanation(
                field_path=current_path,
                field_name=node.name,
                node_type="ListField",
                field_complexity=node.complexity,
                children_complexity=children_complexity,
                total_complexity=total_complexity,
                multiplier=multiplier,
            )
        else:
            total_complexity = node.complexity + children_complexity
            field_explanation = FieldExplanation(
                field_path=current_path,
                field_name=node.name,
                node_type="Field",
                field_complexity=node.complexity,
                children_complexity=children_complexity,
                total_complexity=total_complexity,
            )

        breakdown.append(field_explanation)
    elif isinstance(node, nodes.FragmentSpreadNode):
        field_explanation = FieldExplanation(
            field_path=current_path,
            field_name=node.name,
            node_type="FragmentSpread",
            field_complexity=0,
            children_complexity=node.evaluate(),
            total_complexity=node.evaluate(),
            details={"fragment_name": node.name},
        )
        breakdown.append(field_explanation)
    elif isinstance(node, nodes.SkippedField):
        field_explanation = FieldExplanation(
            field_path=current_path,
            field_name=node.name,
            node_type="SkippedField",
            field_complexity=0,
            children_complexity=0,
            total_complexity=0,
            details={"reason": "Field was skipped due to @skip or @include directive"},
        )
        breakdown.append(field_explanation)
    elif isinstance(node, nodes.MetaField):
        field_explanation = FieldExplanation(
            field_path=current_path,
            field_name=node.name,
            node_type="MetaField",
            field_complexity=0,
            children_complexity=0,
            total_complexity=0,
            details={"reason": "Meta fields like __typename have zero complexity"},
        )
        breakdown.append(field_explanation)

    # Recursively process children
    for child in node.children:
        _extract_field_breakdown(child, current_path, breakdown)

    return breakdown


def explain_complexity(
    query: str,
    schema: GraphQLSchema,
    estimator: ComplexityEstimator,
    config: Config = None
) -> ExplanationResult:
    """
    Explain how the complexity of a GraphQL query is calculated.

    This function provides detailed information about:
    - Which estimator was used and its configuration
    - The complexity tree structure
    - Field-by-field breakdown showing how each field contributes to total complexity
    - The final total complexity

    Args:
        query: The GraphQL query string to analyze
        schema: The GraphQL schema
        estimator: The complexity estimator to use
        config: Optional configuration for complexity calculation

    Returns:
        ExplanationResult containing detailed explanation of the complexity calculation

    Example:
        >>> from graphql import build_schema
        >>> from graphql_complexity import SimpleEstimator
        >>> from graphql_complexity.evaluator.explain import explain_complexity
        >>>
        >>> schema = build_schema('''
        ...     type Query {
        ...         user: User
        ...     }
        ...     type User {
        ...         id: ID!
        ...         name: String!
        ...     }
        ... ''')
        >>>
        >>> query = '''
        ...     query {
        ...         user {
        ...             id
        ...             name
        ...         }
        ...     }
        ... '''
        >>>
        >>> explanation = explain_complexity(
        ...     query=query,
        ...     schema=schema,
        ...     estimator=SimpleEstimator(complexity=10)
        ... )
        >>>
        >>> print(explanation)
        >>> # or access specific parts:
        >>> print(f"Total: {explanation.total_complexity}")
        >>> print(f"Estimator: {explanation.estimator_name}")
    """
    # Build the complexity tree
    ast = parse(query)
    type_info = TypeInfo(schema)
    visitor = ComplexityVisitor(estimator=estimator, type_info=type_info, config=config)
    visit(ast, TypeInfoVisitor(type_info, visitor))
    tree = visitor.complexity_tree

    # Extract estimator information
    estimator_name = type(estimator).__name__
    estimator_details = _extract_estimator_details(estimator)

    # Get tree representation
    tree_representation = tree.describe()

    # Get field breakdown
    field_breakdown = _extract_field_breakdown(tree)

    # Calculate total complexity
    total_complexity = tree.evaluate()

    return ExplanationResult(
        total_complexity=total_complexity,
        estimator_name=estimator_name,
        estimator_details=estimator_details,
        tree_representation=tree_representation,
        field_breakdown=field_breakdown,
        query=query,
    )