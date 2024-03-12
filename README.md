# graphql-complexity
Python library to compute the complexity of a GraphQL operation

![Build](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-buildlu.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/graphql-complexity?label=pypi%20package)](https://pypi.org/project/graphql-complexity/)
[![codecov](https://codecov.io/gh/Checho3388/graphql-complexity/graph/badge.svg?token=4LH7AVN119)](https://codecov.io/gh/Checho3388/graphql-complexity)

## Installation (Quick Start)
The library can be installed using pip:
```shell
pip install graphql-complexity
```
To use `strawberry-graphql` integration, you need to install the library with the `strawberry-graphql` extra.
```shell
pip install graphql-complexity[strawberry-graphql]
```

## Getting Started
Create a file named `complexity.py` with the following content:
```python
from graphql_complexity import (get_complexity, SimpleEstimator)
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
In order to get the complexity of a query, an estimator needs to be defined. 

>The main responsibility of an estimator is to give each node an integer value representing its complexity and
> (optionally) a multiplier that reflects the complexity in relation to the depth of the query.

There are two built-in estimators (`SimpleEstimator` and `DirectiveEstimator`), plus the capability to create any new
estimator by implementing the `ComplexityEstimator` interface.

### SimpleEstimator
Estimate fields complexity based on constants for complexity and multiplier. 

This estimator assigns a **constant** complexity value to each field and multiplies
it by another **constant** which is propagated along the depth of the query.

```python
from graphql_complexity import SimpleEstimator


estimator = SimpleEstimator(complexity=2)
```

Given the following GraphQL query:
```graphql
query {
    user {
        name
        email
    }
}
```
As the complexity and multiplier are constant, the complexity of the fields is:

| Field | Complexity    |
|-------|---------------|
| user  | `1`           |
| name  | `2 * (2 * 1)` |
| email | `2 * (2 * 1)` |

And the total complexity is `6`.

### DirectivesEstimator

Define fields complexity using schema directives.

Assigns a complexity value to each field and multiplies it by the depth of the query. 
It also supports the `@complexity` directive to assign a custom complexity value to a field.

This approach requires to provide the schema to the estimator.

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

Given the schema from above and the following query:
```graphql
query {
    oneField
    otherField
    withoutDirective
}
```

The complexity of the fields results in the following table:

| Field            | Complexity | Comment                                                                                         |
|------------------|------------|-------------------------------------------------------------------------------------------------|
| oneField         | `5`        | Complexity given by `@complexity(value: 5)`                                                     |
| otherField       | `1`        | Complexity given by `@complexity(value: 1)`                                                     |
| withoutDirective | `1`        | The default complexity for fields without directive is `1`, this can be modified by parameters. |

And the total complexity is `7`.

### Custom estimator
This option allows to define a custom estimator to compute the complexity of a field using the `ComplexityEstimator` interface. For example:

```python
from graphql_complexity import ComplexityEstimator


class CustomEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        if node.name.value == "specificField":
            return 100
        return 1
```


## Supported libraries (based on GraphQL-core)
This library is compatible with the following GraphQL libraries:

### Strawberry

The library is compatible with [strawberry-graphql](https://pypi.org/project/strawberry-graphql/). 
To use the library with strawberry-graphql, you need to install the library with the `strawberry-graphql` extra.
```shell
poetry install --extras strawberry-graphql
```

To use the library with [strawberry-graphql](https://pypi.org/project/strawberry-graphql/), you need to use the `build_complexity_extension` method to build
the complexity extension and add it to the schema. This method receives an estimator and returns a complexity 
extension that can be added to the schema.

```python
import strawberry
from graphql_complexity.estimators import SimpleEstimator
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
