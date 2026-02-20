# Estimators

An **estimator** is the strategy that decides how much complexity to assign to each field in a
GraphQL query. `graphql-complexity` ships with three built-in estimators that cover the most
common use cases.

---

## SimpleEstimator

`SimpleEstimator` assigns a **constant complexity value** to every field. Nested fields are
multiplied together as the algorithm descends the query tree, so deeper queries naturally cost
more.

### Usage

```python
from graphql_complexity import SimpleEstimator

estimator = SimpleEstimator(complexity=1)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `complexity` | `int` | `1` | Complexity score assigned to each field |

### Example

```python
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import build_schema

schema = build_schema("""
    type Post {
        title: String
        body: String
    }
    type Query {
        post: Post
    }
""")

query = """{ post { title body } }"""

# Each field costs 1 point — post + title + body = 3
complexity = get_complexity(query=query, schema=schema, estimator=SimpleEstimator(complexity=1))
print(complexity)  # 3
```

---

## DirectivesEstimator

`DirectivesEstimator` lets you annotate individual fields in your **schema** with a
`@complexity` directive, giving you fine-grained control over which fields are expensive.

Fields without the directive receive a default cost of `1`.

### Schema Directive

You must include the directive definition in your schema:

```graphql
directive @complexity(
  value: Int!
) on FIELD_DEFINITION
```

### Usage

```python
from graphql_complexity import DirectivesEstimator

schema = """
directive @complexity(
  value: Int!
) on FIELD_DEFINITION

type Query {
  cheapField: String @complexity(value: 1)
  expensiveField: String @complexity(value: 10)
  defaultField: String
}
"""

estimator = DirectivesEstimator(schema)
```

### Full Example

```python
from graphql_complexity import get_complexity, DirectivesEstimator
from graphql import build_schema

raw_schema = """
directive @complexity(value: Int!) on FIELD_DEFINITION

type User {
    id: ID!
    name: String!
    posts: [Post] @complexity(value: 5)
}

type Post {
    title: String
    body: String @complexity(value: 3)
}

type Query {
    user: User @complexity(value: 2)
}
"""

schema = build_schema(raw_schema)

query = """
    query {
        user {
            id
            name
            posts {
                title
                body
            }
        }
    }
"""

estimator = DirectivesEstimator(raw_schema)
complexity = get_complexity(query=query, schema=schema, estimator=estimator)
print(complexity)
```

---

## ArgumentsEstimator

`ArgumentsEstimator` scales the complexity of a field by the value of one of its **numeric
arguments** (e.g. `limit`, `first`) or by the **length of a list argument** (e.g. `ids`).
This makes queries that fetch more items cost proportionally more.

Fields with no matching argument fall back to `default_complexity`.

### Usage

```python
from graphql_complexity import ArgumentsEstimator

estimator = ArgumentsEstimator(
    multipliers=["limit", "first", "ids"],
    default_complexity=1,
)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `multipliers` | `list[str]` | — | Argument names to inspect for a multiplier value |
| `default_complexity` | `int` | `1` | Base complexity score per field, multiplied by the argument value |

### How the multiplier is resolved

1. The estimator walks the field's arguments in **query order** and stops at the first name that
   appears in `multipliers`.
2. If the matching argument value is an **integer**, that integer is used as the multiplier.
3. If the matching argument value is a **list**, the **length** of the list is used.
4. If the value is any other type (e.g. a string), or no argument matches, the multiplier is `1`
   and the field costs `default_complexity`.

### Example

```python
from graphql_complexity import get_complexity, ArgumentsEstimator
from graphql import build_schema

schema = build_schema("""
    type Query {
        books(limit: Int, ids: [String]): String
        version: String
    }
""")

estimator = ArgumentsEstimator(multipliers=["limit", "ids"], default_complexity=1)

# limit: 10  →  1 * 10 = 10
complexity = get_complexity(
    query="{ books(limit: 10) }",
    schema=schema,
    estimator=estimator,
)
print(complexity)  # 10

# ids: ["a", "b", "c"]  →  1 * 3 = 3
complexity = get_complexity(
    query='{ books(ids: ["a", "b", "c"]) }',
    schema=schema,
    estimator=estimator,
)
print(complexity)  # 3

# No matching argument  →  default_complexity = 1
complexity = get_complexity(
    query="{ version }",
    schema=schema,
    estimator=estimator,
)
print(complexity)  # 1
```

---

## Choosing an Estimator

| Use Case | Recommended Estimator |
|---|---|
| Simple uniform pricing per field | `SimpleEstimator` |
| Different costs per field, controlled in schema | `DirectivesEstimator` |
| Pricing based on pagination / list size arguments | `ArgumentsEstimator` |
| Programmatic or dynamic pricing logic | [Custom Estimator](custom_estimators.md) |

---

## Credits

The estimator concept was inspired by
[graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity).
