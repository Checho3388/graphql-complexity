from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from graphql import DocumentNode, TypeInfo, TypeInfoVisitor, parse, visit

from .visitor import ComplexityVisitor

if TYPE_CHECKING:
    from graphql import GraphQLSchema
    from . import nodes
    from ..config import Config
    from ..estimators import ComplexityEstimator


@lru_cache(maxsize=256)
def _parse_cached(query: str) -> DocumentNode:
    return parse(query)


def get_complexity(query: str | DocumentNode, schema: GraphQLSchema, estimator: ComplexityEstimator, config: Config = None) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    tree = build_complexity_tree(query, schema, estimator, config)

    return tree.evaluate()


def build_complexity_tree(
        query: str | DocumentNode,
        schema: GraphQLSchema,
        estimator: ComplexityEstimator,
        config: Config | None = None,
) -> nodes.ComplexityNode:
    """Calculate the complexity of a query using the provided estimator."""
    ast = query if isinstance(query, DocumentNode) else _parse_cached(query)
    type_info = TypeInfo(schema)

    visitor = ComplexityVisitor(estimator=estimator, type_info=type_info, config=config)
    visit(ast, TypeInfoVisitor(type_info, visitor))

    return visitor.complexity_tree
