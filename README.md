# graphql-complexity
Python library to compute the complexity of a GraphQL operation

![Unit Tests](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-package.yml/badge.svg)


## Usage
The library uses the query complexity algorithm to compute the complexity of a GraphQL operation. The algorithm is 
based on the number of fields requested in the operation and the depth of the query.

```python
from graphql import parse, visit
from graphql_complexity.visitor import ComplexityVisitor
from graphql_complexity.estimators import SimpleEstimator


query = """
    query SomeQuery {
        user {
            id
            name
        }
    }
"""

ast = parse(query)
visitor = ComplexityVisitor(estimator=SimpleEstimator(complexity=1, multiplier=1))
visit(ast, visitor)

complexity = visitor.evaluate()
if complexity > 10:
    raise Exception("Query is too complex")
```

## Estimators
In order to get the complexity of a query, an estimator needs to be defined. The main responsibility of
the estimator is to give each node an integer value representing its complexity and (optionally) a
multiplier that reflects the complexity in relation to the depth of the query.

There are two built-in estimators, plus the capability to create any new estimator by
implementing the `ComplexityEstimator` interface.

### Estimate fields complexity based on constants for complexity and multiplier

This estimator assigns a **constant** complexity value to each field and multiplies
it by another **constant** which is propagated along the depth of the query.

```python
from graphql_complexity.estimators import SimpleEstimator


estimator = SimpleEstimator(complexity=1, multiplier=2)
```

Given the following query:
```qgl
query {
    user {
        name
        email
    }
}
```
As the complexity and multiplier are constant, the complexity of the fields will be:

| Field | Complexity    |
|-------|---------------|
| user  | `1`           |
| name  | `2 * (2 * 1)` |
| email | `2 * (2 * 1)` |

And the total complexity will be `5`.

### Define fields complexity using schema directives

Assigns a complexity value to each field and multiplies it by the depth of the query. 
It also supports the `@complexity` directive to assign a custom complexity value to a field.

This approach requires to provide the schema to the estimator.

```python
from graphql_complexity.estimators import DirectivesEstimator


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
```qgl
query {
    oneField
    otherField
    withoutDirective
}
```

The complexity of the fields will be:

| Field            | Complexity | Comment                                                                                           |
|------------------|------------|---------------------------------------------------------------------------------------------------|
| oneField         | `5`        |                                                                                                   |
| otherField       | `1`        |                                                                                                   |
| withoutDirective | `1`        | The default complexity for fields without directive is `1`, this can be modified by parameters.   |

And the total complexity will be `7`.

### Create a custom estimator
This option allows to define a custom estimator to compute the complexity of a field using the `ComplexityEstimator` interface. For example:

```python
from graphql_complexity.estimators import ComplexityEstimator


class CustomEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, key, parent, path, ancestors) -> int:
        if node.name.value == "specificField":
            return 100
        return 1

    def get_field_multiplier(self, node, key, parent, path, ancestors) -> int:
        return 1
```


## Supported libraries (based on GraphQL-core)
The library is compatible with the following GraphQL libraries:

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
from graphql_complexity.extensions import build_complexity_extension

@strawberry.type
class Query:
    @strawberry.field()
    def hello_world(self) -> str:
        return "Hello world!"

extension = build_complexity_extension()
schema = strawberry.Schema(query=Query, extensions=[extension])

schema.execute_sync("query { helloWorld }")
```
The `build_complexity_extension` method accepts an estimator as optional argument giving the possibility to use one
of the built-in estimators or a custom estimator.

## Credits

Estimators idea was heavily inspired by [graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity).
