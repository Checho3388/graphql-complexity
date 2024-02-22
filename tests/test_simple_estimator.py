import pytest

from graphql_complexity import SimpleEstimator, get_complexity


def _evaluate_complexity_with_simple_estimator(
    query: str, field_complexity=1, multiplier=1
):
    estimator = SimpleEstimator(field_complexity, multiplier)
    return get_complexity(query, estimator)


def test_root_fields_do_not_multiply():
    query = """
        query Something {
            a_field
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 3, 10)

    assert complexity == 3


def test_root_fields_complexity_is_added():
    query = """
        query Something {
            a_field
            another_field
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 5, 1)

    assert complexity == 10


def test_complexity_multiplies_with_objects():
    query = """
        query Something {
            anObj {
                a_field
                another_field
            }
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 21


def test_complexity_multiplies_two_levels():
    query = """
        query Something {
            anObj {
                anotherObj {
                    a_field
                }
            }
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 111


def test_complexity_multiplies_with_depth():
    query = """
        query Something {
            anObj {
                anotherObj {
                    a_field
                }
                another_field
            }
        }
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 121


def test_1():
    query = """query {
        variableScalar(count: 10)
    }"""  # Simple Estimator: 1
    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)
    assert complexity == 1


def test_complexity_should_not_count_fields_with_include_directive_false_given_by_variable():
    query = """query Foo ($shouldSkip: Boolean = false) {
        variableScalar(count: 10) @include(if: $shouldSkip)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 0


def test_complexity_should_not_count_fields_with_include_directive_false_given_by_boolean_value():
    query = """query {
        variableScalar(count: 10) @include(if: false)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 0


def test_complexity_should_not_count_objects_with_include_directive_false_given_by_boolean_value():
    query = """query {
        objectField @include(if: false) {
            ignoreMe
            ignoreMeToo {
                innerIgnoredField
            }
        }
        thisShouldBeIncluded
        thisAlsoShouldBeIncluded
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 2


def test_complexity_should_not_count_inner_directive_of_object_with_include_directive_false_given_by_boolean_value():
    query = """query {
        objectField @include(if: false) {
            ignoreMe @include(if: true)
            ignoreMeToo @include(if: false) {
                innerIgnoredField @include(if: true)
            }
        }
        thisShouldBeIncluded
        thisAlsoShouldBeIncluded
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 2


def test_complexity_should_count_fields_with_include_directive_true_given_by_boolean_value():
    query = """query {
        variableScalar(count: 10) @include(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 1


def test_complexity_should_not_count_fields_with_skip_directive_true_given_by_boolean_value():
    query = """query {
        variableScalar(count: 10) @skip(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 0


def test_complexity_should_count_fields_with_skip_directive_false_given_by_boolean_value():
    query = """query {
        variableScalar(count: 10) @skip(if: false)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 1


def test_complexity_should_count_fields_with_skip_directive_followed_by_include():
    query = """query {
        variableScalar(count: 10) @skip(if: false) @include(if: true)
    }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 1)

    assert complexity == 1


def test_simple_estimator_should_not_allow_negative_cost():
    """It should now allow negative cost"""
    with pytest.raises(ValueError):
        SimpleEstimator(-1, 1)


def test_9():
    # should ignore unknown fragments
    query = """query {
        ...UnknownFragment
        variableScalar(count: 100)
      }"""  # Simple Estimator(10): 10
    complexity = _evaluate_complexity_with_simple_estimator(query, 10, 1)
    assert complexity == 10
