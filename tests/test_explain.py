"""Tests for the explain_complexity functionality."""

from graphql import build_schema

from graphql_complexity import (
    explain_complexity,
    SimpleEstimator,
    DirectivesEstimator,
    get_complexity,
)
from graphql_complexity.evaluator.explain import ExplanationResult, FieldExplanation


def test_explain_with_simple_estimator():
    """Test explain_complexity with SimpleEstimator."""
    schema = build_schema("""
        type Query {
            user: User
        }
        type User {
            id: ID!
            name: String!
        }
    """)

    query = """
        query {
            user {
                id
                name
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=10)
    )

    assert isinstance(explanation, ExplanationResult)
    assert explanation.estimator_name == "SimpleEstimator"
    assert explanation.estimator_details["complexity_constant"] == 10
    assert explanation.total_complexity == get_complexity(query, schema, SimpleEstimator(complexity=10))
    assert len(explanation.field_breakdown) > 0


def test_explain_with_directives_estimator():
    """Test explain_complexity with DirectivesEstimator."""
    schema_str = """
        directive @complexity(value: Int!) on FIELD_DEFINITION

        type Query {
            user: User @complexity(value: 5)
        }
        type User {
            id: ID!
            name: String! @complexity(value: 3)
        }
    """

    schema = build_schema(schema_str)

    query = """
        query {
            user {
                id
                name
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=DirectivesEstimator(schema=schema_str)
    )

    assert explanation.estimator_name == "DirectivesEstimator"
    assert "complexity_map" in explanation.estimator_details
    assert explanation.total_complexity == get_complexity(
        query, schema, DirectivesEstimator(schema=schema_str)
    )


def test_explain_field_breakdown():
    """Test that field breakdown is correctly generated."""
    schema = build_schema("""
        type Query {
            user: User
        }
        type User {
            id: ID!
            name: String!
            posts: [Post!]!
        }
        type Post {
            id: ID!
            title: String!
        }
    """)

    query = """
        query {
            user {
                id
                name
                posts {
                    id
                    title
                }
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=1)
    )

    # Check that we have field explanations
    assert len(explanation.field_breakdown) > 0

    # Check that each field explanation is valid
    for field in explanation.field_breakdown:
        assert isinstance(field, FieldExplanation)
        assert field.field_name
        assert field.node_type in [
            "Field", "ListField", "FragmentSpread", "SkippedField", "MetaField"
        ]
        assert field.total_complexity >= 0


def test_explain_with_fragments():
    """Test explain_complexity with fragment spreads."""
    schema = build_schema("""
        type Query {
            user: User
        }
        type User {
            id: ID!
            name: String!
            email: String!
        }
    """)

    query = """
        query {
            user {
                ...UserFields
            }
        }

        fragment UserFields on User {
            id
            name
            email
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=2)
    )

    # Should handle fragments
    assert explanation.total_complexity > 0

    # Check for fragment in breakdown
    fragment_fields = [f for f in explanation.field_breakdown if f.node_type == "FragmentSpread"]
    assert len(fragment_fields) > 0


def test_explain_to_dict():
    """Test conversion to dictionary."""
    schema = build_schema("""
        type Query {
            user: User
        }
        type User {
            id: ID!
            name: String!
        }
    """)

    query = """
        query {
            user {
                id
                name
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=5)
    )

    result_dict = explanation.to_dict()

    assert isinstance(result_dict, dict)
    assert "total_complexity" in result_dict
    assert "estimator" in result_dict
    assert "tree" in result_dict
    assert "breakdown" in result_dict
    assert "query" in result_dict

    # Check estimator structure
    assert "name" in result_dict["estimator"]
    assert "details" in result_dict["estimator"]

    # Check breakdown structure
    assert isinstance(result_dict["breakdown"], list)
    if len(result_dict["breakdown"]) > 0:
        first_field = result_dict["breakdown"][0]
        assert "path" in first_field
        assert "name" in first_field
        assert "type" in first_field
        assert "field_complexity" in first_field
        assert "total_complexity" in first_field


def test_explain_str_representation():
    """Test string representation of explanation."""
    schema = build_schema("""
        type Query {
            user: User
        }
        type User {
            id: ID!
            name: String!
        }
    """)

    query = """
        query {
            user {
                id
                name
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=3)
    )

    str_repr = str(explanation)

    assert isinstance(str_repr, str)
    assert "Total Complexity:" in str_repr
    assert "Estimator Used:" in str_repr
    assert "Complexity Tree:" in str_repr
    assert "Field-by-Field Breakdown:" in str_repr
    assert str(explanation.total_complexity) in str_repr


def test_explain_nested_query():
    """Test explain with deeply nested query."""
    schema = build_schema("""
        type Query {
            organization: Organization
        }
        type Organization {
            id: ID!
            teams: [Team!]!
        }
        type Team {
            id: ID!
            members: [User!]!
        }
        type User {
            id: ID!
            name: String!
        }
    """)

    query = """
        query {
            organization {
                id
                teams {
                    id
                    members {
                        id
                        name
                    }
                }
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=1)
    )

    # Should have multiple levels of fields
    assert explanation.total_complexity > 0
    assert len(explanation.field_breakdown) >= 6  # organization, id, teams, id, members, id, name

    # Check that paths are correctly formatted
    paths = [f.field_path for f in explanation.field_breakdown]
    assert any("organization" in path for path in paths)
    assert any("teams" in path for path in paths)
    assert any("members" in path for path in paths)


def test_explain_list_field_multiplier():
    """Test that list fields show multiplier information.

    Note: List fields must NOT be wrapped with NonNull for proper detection.
    [User!]! won't be detected as a list, but [User] will be.
    """
    schema = build_schema("""
        type Query {
            users(first: Int): [User]
        }
        type User {
            id: ID!
            name: String!
        }
    """)

    query = """
        query {
            users(first: 5) {
                id
                name
            }
        }
    """

    explanation = explain_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=1)
    )

    # Find list fields
    list_fields = [f for f in explanation.field_breakdown if f.node_type == "ListField"]

    # Should have at least the users field as a list
    assert len(list_fields) > 0

    # List fields should have multiplier information
    for list_field in list_fields:
        assert list_field.multiplier is not None
        # In this case, multiplier should be 5 (from first: 5)
        if list_field.field_name == "users":
            assert list_field.multiplier == 5


def test_explain_matches_get_complexity():
    """Ensure explain_complexity returns same total as get_complexity."""
    schema = build_schema("""
        type Query {
            user(id: ID!): User
        }
        type User {
            id: ID!
            name: String!
            posts: [Post!]!
        }
        type Post {
            id: ID!
            title: String!
        }
    """)

    query = """
        query {
            user(id: "1") {
                id
                name
                posts {
                    id
                    title
                }
            }
        }
    """

    estimator = SimpleEstimator(complexity=7)

    explanation = explain_complexity(query=query, schema=schema, estimator=estimator)
    direct_complexity = get_complexity(query=query, schema=schema, estimator=estimator)

    assert explanation.total_complexity == direct_complexity
