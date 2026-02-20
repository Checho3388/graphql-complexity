# Quick Start

This guide walks you through computing the complexity of a GraphQL query in just a few lines
of code.

## Your First Complexity Check

Create a file named `complexity.py`:

```python
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import build_schema

schema = build_schema("""
    type User {
        id: ID!
        name: String!
    }
    type Query {
        user: User
    }
""")

query = """
    query SomeQuery {
        user {
            id
            name
        }
    }
"""

complexity = get_complexity(
    query=query,
    schema=schema,
    estimator=SimpleEstimator(complexity=1)
)

if complexity > 10:
    raise Exception(f"Query is too complex: {complexity}")

print(f"Query complexity: {complexity}")
```

Run it:

```bash
python complexity.py
# Query complexity: 3
```

## How It Works

The `get_complexity` function accepts three arguments:

| Argument | Type | Description |
|---|---|---|
| `query` | `str` | The GraphQL query string to analyse |
| `schema` | `GraphQLSchema` | The schema the query runs against |
| `estimator` | `ComplexityEstimator` | The strategy used to score each field |

The library **walks every node** in the parsed query AST and calls the estimator on each field.
The scores are summed into a single integer — the total complexity of the operation.

## Enforcing a Complexity Limit

A common pattern is to compute complexity **before executing the query** and reject it if it
exceeds your threshold:

```python
MAX_COMPLEXITY = 50

complexity = get_complexity(query=query, schema=schema, estimator=SimpleEstimator())

if complexity > MAX_COMPLEXITY:
    raise Exception(f"Query complexity {complexity} exceeds the limit of {MAX_COMPLEXITY}")
```

## Next Steps

- Learn about the built-in [Estimators](estimators.md)
- Write your own [Custom Estimator](custom_estimators.md)
- Integrate with [Strawberry GraphQL](strawberry.md)
