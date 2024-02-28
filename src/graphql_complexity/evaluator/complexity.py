from graphql import GraphQLSchema, TypeInfo, TypeInfoVisitor, parse, visit

from ..estimators import ComplexityEstimator
from .visitor import ComplexityVisitor


def get_complexity(query: str, schema: GraphQLSchema, estimator: ComplexityEstimator) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    ast = parse(query)
    return get_ast_complexity(ast, schema=schema, estimator=estimator)


def get_ast_complexity(ast, schema: GraphQLSchema, estimator: ComplexityEstimator) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    type_info = TypeInfo(schema)

    visitor = ComplexityVisitor(estimator=estimator, type_info=type_info)
    visit(ast, TypeInfoVisitor(type_info, visitor))

    return visitor.evaluate()
