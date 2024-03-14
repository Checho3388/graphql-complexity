import pytest
from graphql import build_schema

from graphql_complexity import SimpleEstimator, get_complexity
from tests.ut_utils import schema


def _evaluate_complexity_with_simple_estimator(query: str, field_complexity=1):
    estimator = SimpleEstimator(field_complexity)
    return get_complexity(query, build_schema(schema), estimator)


def test_root_fields_do_not_multiply():
    query = """
        query Something {
            version
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 3)

    assert complexity == 3


def test_root_fields_complexity_is_added():
    query = """
        query Something {
            version
            anotherVersion: version
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 5)

    assert complexity == 10


def test_complexity_should_not_count_fields_with_include_directive_false_given_by_variable():
    query = """query Foo ($shouldSkip: Boolean = false) {
        version @include(if: $shouldSkip)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 0


def test_complexity_should_not_count_fields_with_include_directive_false_given_by_boolean_value():
    query = """query {
        version @include(if: false)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 0


def test_complexity_should_not_count_objects_with_include_directive_false_given_by_boolean_value():
    query = """query {
        droid @include(if: false) {
            id
            friends {
                name
            }
        }
        version
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_complexity_should_not_count_inner_directive_of_object_with_include_directive_false_given_by_boolean_value():
    query = """query {
        droid @include(if: false) {
            name @include(if: true)
            friends @include(if: false) {
                name @include(if: true)
            }
        }
        version
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_complexity_should_count_fields_with_include_directive_true_given_by_boolean_value():
    query = """query {
        version @include(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_complexity_should_not_count_fields_with_skip_directive_true_given_by_boolean_value():
    query = """query {
        version(count: 10) @skip(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 0


def test_complexity_should_count_fields_with_skip_directive_false_given_by_boolean_value():
    query = """query {
        version(count: 10) @skip(if: false)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_complexity_should_count_fields_with_skip_directive_followed_by_include():
    query = """query {
        version(count: 10) @skip(if: false) @include(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_complexity_with_other_directives_not_affecting_evaluation():
    query = """query {
        version(count: 10) @deprecated(reason: "Test")
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 1


def test_simple_estimator_should_not_allow_negative_cost():
    """It should now allow negative cost"""
    with pytest.raises(ValueError, match=r"^'complexity' must be a positive integer \(greater or equal than 0\)$"):
        SimpleEstimator(-1)


def test_9():
    # should ignore unknown fragments
    query = """query {
        ...UnknownFragment
        version(count: 100)
      }"""  # Simple Estimator(10): 10
    complexity = _evaluate_complexity_with_simple_estimator(query, 10)
    assert complexity == 10
