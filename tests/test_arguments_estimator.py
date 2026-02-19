from graphql import build_schema

from graphql_complexity import get_complexity
from graphql_complexity.estimators import ArgumentsEstimator

_schema = """
type Query {
    books(limit: Int, ids: [String], name: String, after: Int): String
    version: String
    user: User
}

type User {
    id: String
    name: String
    posts(limit: Int): String
}
"""


def _evaluate_complexity(query: str, multipliers: list[str], default_complexity: int = 1):
    estimator = ArgumentsEstimator(multipliers=multipliers, default_complexity=default_complexity)
    return get_complexity(query, build_schema(_schema), estimator)


def test_field_without_matching_argument_returns_default_complexity():
    query = """query { version }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 1


def test_int_argument_multiplies_complexity():
    query = """query { books(limit: 10) }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 10


def test_list_argument_uses_length_as_multiplier():
    query = """query { books(ids: ["a", "b", "c"]) }"""
    complexity = _evaluate_complexity(query, multipliers=["ids"])
    assert complexity == 3


def test_custom_default_complexity_scales_with_multiplier():
    query = """query { books(limit: 5) }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"], default_complexity=3)
    assert complexity == 15


def test_non_matching_argument_is_ignored():
    query = """query { books(name: "foo") }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 1


def test_non_int_non_list_argument_falls_back_to_default_multiplier():
    """String-valued argument matching a multiplier name is ignored (non-extractable), so multiplier stays 1."""
    query = """query { books(name: "graphql") }"""
    complexity = _evaluate_complexity(query, multipliers=["name"])
    assert complexity == 1


def test_first_matching_query_argument_is_used():
    """When multiple query arguments match multipliers, the first one in query order wins."""
    query = """query { books(limit: 5, after: 10) }"""
    complexity = _evaluate_complexity(query, multipliers=["limit", "after"])
    assert complexity == 5


def test_multiple_root_fields_complexities_are_summed():
    query = """query { books(limit: 3) version }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 4  # books=3, version=1


def test_nested_field_with_matching_argument():
    query = """query { user { posts(limit: 7) } }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 8  # user=1, posts=7


def test_field_without_arguments_uses_default_complexity():
    query = """query { user { id name } }"""
    complexity = _evaluate_complexity(query, multipliers=["limit"])
    assert complexity == 3  # user=1, id=1, name=1


def test_empty_list_argument_results_in_zero_complexity():
    query = """query { books(ids: []) }"""
    complexity = _evaluate_complexity(query, multipliers=["ids"])
    assert complexity == 0  # len([]) = 0 → default_complexity * 0 = 0