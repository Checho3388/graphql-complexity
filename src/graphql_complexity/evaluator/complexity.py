from graphql import parse, visit

from ..estimators import ComplexityEstimator
from .visitor import ComplexityVisitor


def get_complexity(query: str, estimator: ComplexityEstimator) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    ast = parse(query)
    return get_ast_complexity(ast, estimator=estimator)


def get_ast_complexity(ast, estimator: ComplexityEstimator) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)

    return visitor.evaluate()
