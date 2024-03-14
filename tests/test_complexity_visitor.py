import pytest
from graphql import build_schema

from graphql_complexity import SimpleEstimator, get_complexity
from graphql_complexity.evaluator.visitor import ComplexityVisitor
from tests import ut_utils


def _evaluate_complexity(query: str, estimator=None):
    estimator = estimator or SimpleEstimator(1)
    schema = build_schema(ut_utils.schema)
    return get_complexity(query, schema, estimator)


def test_one_field_simple_complexity_calculation():
    query = """
        query {
            version
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 1


def test_typename_has_zero_complexity():
    query = """query {
        __typename
    }"""

    complexity = _evaluate_complexity(query)

    assert complexity == 0


def test_two_fields_simple_complexity_calculation():
    query = """
        query Something {
            version
            alias: version
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 2


def test_complexity_visitor_with_complex_query():
    query = """
        query Something {
            version
            hero {
                name
            }
            droid {
                id
                name
                friends {
                    name
                }
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 8


def test_complexity_works_with_multiple_operation_definitions():
    query = """
        query FirstOne {
            version
        }
        query OtherOne {
            version
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 2


def test_complexity_handles_fragments():
    query = """
        fragment fields on Character {
            name
        }
        query Something {
            hero {
                ... fields
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 2


def test_complexity_handles_fragments_used_more_than_once():
    query = """
        fragment fields on Character {
            name
        }
        query Something {
            hero {
                ... fields
            }
            another_hero: hero {
                ... fields
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 4


def test_complexity_handles_fragments_definition_after_operation_definition():
    query = """
        query Something {
            hero {
                ... fields
            }
            another_hero: hero {
                ... fields
            }
        }
        fragment fields on Character {
            name
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 4


def test_complexity_visitor_handles_input_arguments():
    query = """
        query Something {
            droid (id: "1") {
                name
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 2


def test_visitor_should_raise_when_no_estimator_is_given():
    with pytest.raises(
        ValueError, match="Estimator must be of type 'ComplexityEstimator'"
    ):
        ComplexityVisitor(estimator=None, type_info=None)


def test_introspection_query_is_allowed():
    query = """{
      __schema {
        directives {
          name
          description
        }
        subscriptionType {
          name
          description
        }
        types {
          name
          description
        }
        queryType {
          name
          description
        }
        mutationType {
          name
          description
        }
        queryType {
          name
          description
        }
      }
    }

    fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 0
