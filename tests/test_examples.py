from graphql import parse, visit

from graphql_complexity.estimators import DirectivesEstimator, SimpleEstimator
from graphql_complexity.visitor import ComplexityVisitor


def _evaluate_complexity_with_simple_estimator(
    query: str, field_complexity=1, multiplier=1
):
    ast = parse(query)
    estimator = SimpleEstimator(field_complexity, multiplier)
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)

    return visitor.evaluate()


def test_root_fields_complexity_is_added():
    query = """
        query {
            user {
                name
                email
            }
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 2, 1)

    assert complexity == 6


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
      value: Int!
    ) on FIELD_DEFINITION

    type Query {
      oneField: String @complexity(value: 5)
      otherField: String @complexity(value: 1)
      withoutDirective: String
    }
    """

    query = """
        query Something {
            oneField
            otherField
            withoutDirective
        }
    """

    complexity = _evaluate_complexity_with_directives_estimator(query, schema)

    assert complexity == 7
