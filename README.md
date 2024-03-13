<img src="https://github.com/Checho3388/graphql-complexity/raw/main/.github/logo.png" width="150">

# GraphQL Complexity

Welcome to GraphQL-Complexity! This Python library provides functionality to compute the complexity of a GraphQL operation, contributing to better understanding and optimization of your GraphQL APIs. This library is designed to be stable, robust, and highly useful for developers working with GraphQL.

![Build](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-build.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/graphql-complexity?label=pypi%20package)](https://pypi.org/project/graphql-complexity/)
[![codecov](https://codecov.io/gh/Checho3388/graphql-complexity/graph/badge.svg?token=4LH7AVN119)](https://codecov.io/gh/Checho3388/graphql-complexity)

## Features
- Compute complexity of GraphQL queries
- Multiple built-in estimators for complexity computation
- Customizable estimators for specific use cases
- Support for Strawberry GraphQL library


## Installation (Quick Start)

You can install the library via pip:

```shell
pip install graphql-complexity
```

For Strawberry GraphQL integration, use the following command:

```shell
pip install graphql-complexity[strawberry-graphql]
```

## Getting Started
Create a file named `complexity.py` with the following content:
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
    estimator=SimpleEstimator(complexity=10)
)
if complexity > 10:
    raise Exception("Query is too complex")
```

The library exposes the method `get_complexity` with the algorithm to compute the complexity of a GraphQL operation. 
The algorithm visits each node of the query and computes the complexity of each field using an **estimator**.


## Estimators

GraphQL-Complexity provides various built-in estimators for computing query complexity:

### SimpleEstimator
Estimate fields complexity based on constants for complexity and multiplier. This assigns a constant 
complexity value to each field and multiplies it by another constant, which is propagated along the depth of the query.

```python
from graphql_complexity import SimpleEstimator


estimator = SimpleEstimator(complexity=2)
```

### DirectivesEstimator

Define fields complexity using schema directives. This assigns a complexity value to each field and multiplies it 
by the depth of the query. It also supports the @complexity directive to assign a custom complexity value to a field.

```python
from graphql_complexity import DirectivesEstimator


schema = """
directive @complexity(
  value: Int!
) on FIELD_DEFINITION

type Query {
  oneField: String @complexity(value: 5)
  otherField: String @complexity(value: 1)
  withoutDirective: String
}
"""

estimator = DirectivesEstimator(schema)
```

### Custom estimator
Custom estimators can be defined to compute the complexity of a field using the `ComplexityEstimator` interface.

```python
from graphql_complexity import ComplexityEstimator


class CustomEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        if node.name.value == "specificField":
            return 100
        return 1
```


## Supported libraries
This library is compatible with the following GraphQL libraries:

### Strawberry GraphQL

The library is compatible with [strawberry-graphql](https://pypi.org/project/strawberry-graphql/). 
Use the following command to install the library with Strawberry support:

```shell
poetry install --extras strawberry-graphql
```

To use the library with Strawberry GraphQL, use the `build_complexity_extension` method to build the complexity 
extension and add it to the schema. This method receives an estimator and returns a complexity extension that can be added to the schema.

```python
import strawberry
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


@strawberry.type
class Query:
    @strawberry.field()
    def hello_world(self) -> str:
        return "Hello world!"

extension = build_complexity_extension(estimator=SimpleEstimator())
schema = strawberry.Schema(query=Query, extensions=[extension])

schema.execute_sync("query { helloWorld }")
```

The `build_complexity_extension` method accepts an estimator as optional argument giving the possibility to use one
of the built-in estimators or a custom estimator.

## Credits

Estimators idea was heavily inspired by [graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity).
