"""
Example demonstrating the explain_complexity feature.

This shows how to use the explain command to understand:
- Which estimator was used
- How complexity was calculated
- Field-by-field breakdown
"""

from graphql import build_schema
from graphql_complexity import (
    explain_complexity,
    SimpleEstimator,
    DirectivesEstimator,
)

# Example 1: Simple Estimator
print("=" * 80)
print("Example 1: Using SimpleEstimator")
print("=" * 80)

schema1 = build_schema("""
    type User {
        id: ID!
        name: String!
        email: String!
        posts: [Post!]!
    }

    type Post {
        id: ID!
        title: String!
        content: String!
        author: User!
    }

    type Query {
        user(id: ID!): User
        users: [User!]!
    }
""")

query1 = """
    query GetUser {
        user(id: "1") {
            id
            name
            email
            posts {
                id
                title
                author {
                    name
                }
            }
        }
    }
"""

explanation1 = explain_complexity(
    query=query1,
    schema=schema1,
    estimator=SimpleEstimator(complexity=5)
)

print(explanation1)
print("\n\n")

# Example 2: Directives Estimator
print("=" * 80)
print("Example 2: Using DirectivesEstimator")
print("=" * 80)

schema2_str = """
    directive @complexity(
        value: Int!
    ) on FIELD_DEFINITION

    type User {
        id: ID!
        name: String!
        email: String!
        expensiveField: String! @complexity(value: 50)
        posts: [Post!]! @complexity(value: 10)
    }

    type Post {
        id: ID!
        title: String!
        content: String!
    }

    type Query {
        user(id: ID!): User @complexity(value: 5)
    }
"""

schema2 = build_schema(schema2_str)

query2 = """
    query GetUserWithExpensiveField {
        user(id: "1") {
            id
            name
            expensiveField
            posts {
                id
                title
            }
        }
    }
"""

explanation2 = explain_complexity(
    query=query2,
    schema=schema2,
    estimator=DirectivesEstimator(schema=schema2_str)
)

print(explanation2)
print("\n\n")

# Example 3: Complex nested query
print("=" * 80)
print("Example 3: Complex Nested Query with Fragments")
print("=" * 80)

schema3 = build_schema("""
    type Organization {
        id: ID!
        name: String!
        teams: [Team!]!
    }

    type Team {
        id: ID!
        name: String!
        members: [User!]!
    }

    type User {
        id: ID!
        name: String!
        email: String!
    }

    type Query {
        organization(id: ID!): Organization
    }
""")

query3 = """
    query GetOrgStructure {
        organization(id: "1") {
            id
            name
            teams {
                id
                name
                members {
                    ...UserFields
                }
            }
        }
    }

    fragment UserFields on User {
        id
        name
        email
    }
"""

explanation3 = explain_complexity(
    query=query3,
    schema=schema3,
    estimator=SimpleEstimator(complexity=2)
)

print(explanation3)
print("\n\n")

# Example 4: Accessing explanation data programmatically
print("=" * 80)
print("Example 4: Programmatic Access to Explanation Data")
print("=" * 80)

# Use explanation2 from above
data = explanation3.to_dict()

print(f"Total Complexity: {data['total_complexity']}")
print(f"Estimator: {data['estimator']['name']}")
print(f"\nFields analyzed: {len(data['breakdown'])}")

print("\nTop 5 most complex fields:")
sorted_fields = sorted(
    data['breakdown'],
    key=lambda x: x['total_complexity'],
    reverse=True
)[:5]

for field in sorted_fields:
    print(f"  {field['path']}: {field['total_complexity']} (type: {field['type']})")

print("\n" + "=" * 80)
