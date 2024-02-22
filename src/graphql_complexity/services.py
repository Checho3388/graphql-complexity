from graphql import parse, visit

from . import ComplexityEstimator, ComplexityVisitor


def get_complexity(query: str, estimator: ComplexityEstimator) -> int:
    ast = parse(query)
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)
    return visitor.evaluate()
