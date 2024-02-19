from graphql import parse, visit

from graphql_complexity.estimators import DirectivesEstimator
from graphql_complexity.visitor import ComplexityVisitor


def _evaluate_complexity_with_directives_estimator(
    query: str,
    schema: str,
):
    ast = parse(query)
    estimator = DirectivesEstimator(schema)
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)

    return visitor.evaluate()


def test_simple_query_with_directive_estimator():
    schema = """directive @complexity(
      # The complexity value for the field
      value: Int!

      # Optional multipliers
      multipliers: [String!]
    ) on FIELD_DEFINITION

    type Query {
      # Fixed complexity of 5
      someField: String @complexity(value: 5)
    }
    """

    query = """
        query Something {
            someField
        }
    """

    complexity = _evaluate_complexity_with_directives_estimator(query, schema)

    assert complexity == 5
