from graphql import build_schema

from graphql_complexity import (
    DirectivesEstimator,
    SimpleEstimator,
    get_complexity
)


def _evaluate_complexity_with_simple_estimator(
    query: str, schema: str, field_complexity=1, multiplier=1
):
    estimator = SimpleEstimator(field_complexity, multiplier)

    return get_complexity(query, build_schema(schema), estimator)


def test_root_fields_complexity_is_added():
    schema = """
    type Obj {
        name: String
        email: String
    }
    type Query {
        user: Obj
    }
    """
    query = """
        query {
            user {
                name
                email
            }
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, schema, 2, 1)

    assert complexity == 6


def _evaluate_complexity_with_directives_estimator(
    query: str,
    schema: str,
):
    estimator = DirectivesEstimator(schema)

    return get_complexity(query, build_schema(schema), estimator)


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
