# Custom Estimators

If the built-in estimators don't fit your requirements, you can implement your own by
subclassing `ComplexityEstimator` and overriding `get_field_complexity`.

---

## The Interface

```python
from graphql_complexity import ComplexityEstimator


class MyEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        ...
```

### Method Parameters

| Parameter | Description |
|---|---|
| `node` | The AST `FieldNode` currently being visited |
| `type_info` | A `TypeInfo` object with schema type information for the current node |
| `path` | A list of field names representing the current path from the root |

The method must return an `int` — the complexity score for that single field.

---

## Example: Field-Name Based Pricing

Charge a fixed high cost for a specific field, and a default of `1` for everything else:

```python
from graphql_complexity import ComplexityEstimator, get_complexity
from graphql import build_schema


class FieldNameEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        if node.name.value == "expensiveField":
            return 100
        return 1


schema = build_schema("""
    type Query {
        cheapField: String
        expensiveField: String
    }
""")

query = "{ cheapField expensiveField }"

estimator = FieldNameEstimator()
complexity = get_complexity(query=query, schema=schema, estimator=estimator)
print(complexity)  # 101
```

---

## Example: Depth-Aware Pricing

Use the `path` argument to charge more for deeply nested fields:

```python
from graphql_complexity import ComplexityEstimator


class DepthEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        depth = len(path)
        return depth * 2  # cost grows with depth
```

---

## Example: Type-Aware Pricing

Inspect `type_info` to assign cost based on the GraphQL type being returned:

```python
from graphql_complexity import ComplexityEstimator
from graphql import GraphQLList


class TypeAwareEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        # List fields are more expensive
        if isinstance(type_info.get_type(), GraphQLList):
            return 10
        return 1
```

---

## Tips

- Keep `get_field_complexity` **pure and fast** — it is called once per field per query.
- Return `0` for fields you want to treat as free (e.g. `__typename`).
- You can combine multiple heuristics inside a single estimator.
