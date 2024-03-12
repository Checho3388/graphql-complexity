from graphql import GraphQLSchema, TypeInfo, TypeInfoVisitor, parse, visit

from .visitor import ComplexityVisitor
from ..config import Config
from ..estimators import ComplexityEstimator


def get_complexity(query: str, schema: GraphQLSchema, estimator: ComplexityEstimator, config: Config = None) -> int:
    """Calculate the complexity of a query using the provided estimator."""
    ast = parse(query)
    type_info = TypeInfo(schema)

    visitor = ComplexityVisitor(estimator=estimator, type_info=type_info, config=config)
    visit(ast, TypeInfoVisitor(type_info, visitor))

    return visitor.evaluate()
