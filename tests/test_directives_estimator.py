from graphql import build_schema

from graphql_complexity import DirectivesEstimator, get_complexity


def _evaluate_complexity_with_directives_estimator(
    query: str,
    schema: str,
    **kwargs,
):
    graphql_schema = build_schema(schema)
    estimator = DirectivesEstimator(schema, **kwargs)

    return get_complexity(query, graphql_schema, estimator)


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


def test_():
    schema = """directive @complexity(
      # The complexity value for the field
      value: Int!

      # Optional multipliers
      multipliers: [String!]
    ) on FIELD_DEFINITION

    type Query {
      someField (limit: Int): String @complexity(value: 5, multipliers: ["limit"])
    }
    """

    query = """
        query Something {
            someField (limit: 10)
        }
    """

    complexity = _evaluate_complexity_with_directives_estimator(query, schema)

    assert complexity == 5


# Add more unit tests regarding the directive estimator
def test_directive_estimator_accepts_to_set_missing_complexity():
    schema = """directive @complexity(
      # The complexity value for the field
      value: Int!
    ) on FIELD_DEFINITION

    type Query {
      oneField: String @complexity(value: 3)
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

    complexity = _evaluate_complexity_with_directives_estimator(
        query, schema, default_complexity=10
    )

    assert complexity == 14


def test_directive_estimator_should_accept_field_with_directive_is_part_of_an_object_with_directive():
    schema = """directive @complexity(
      # The complexity value for the field
      value: Int!
    ) on FIELD_DEFINITION

    type Query {
      oneField: Obj @complexity(value: 3)
    }

    type Obj {
      otherField: String @complexity(value: 120)
    }
    """

    query = """
        query Something {
            oneField {
                otherField
            }
        }
    """

    complexity = _evaluate_complexity_with_directives_estimator(query, schema)

    assert complexity == 123
