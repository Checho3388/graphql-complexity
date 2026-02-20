# Framework Integrations

`graphql-complexity` is framework-agnostic — it works with any GraphQL server by wrapping
`get_complexity` around your execution pipeline. This page shows how to wire it up with the
most common Python frameworks.

---

## Strawberry GraphQL

Strawberry has first-class support via a schema extension. Install the extra first:

```bash
pip install graphql-complexity[strawberry-graphql]
```

Use `build_complexity_extension` to create the extension and attach it to your schema:

```python
import strawberry
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


@strawberry.type
class Query:
    @strawberry.field
    def hello_world(self) -> str:
        return "Hello world!"


extension = build_complexity_extension(
    estimator=SimpleEstimator(complexity=1),
    max_complexity=100,
)
schema = strawberry.Schema(query=Query, extensions=[extension])

schema.execute_sync("query { helloWorld }")
```

When a query exceeds `max_complexity` the extension adds an error to the response and
**prevents execution** — no resolver is ever called.

### `build_complexity_extension` reference

```python
build_complexity_extension(
    estimator: ComplexityEstimator = SimpleEstimator(),
    max_complexity: int | None = None,
) -> type[SchemaExtension]
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `estimator` | `ComplexityEstimator` | `SimpleEstimator()` | Estimator used to score fields |
| `max_complexity` | `int \| None` | `None` | Reject queries above this score. `None` disables the limit |

---

## Django

With Graphene-Django, the cleanest integration point is a custom middleware class that intercepts
each request and checks complexity before any resolver runs.

```python
# myapp/complexity.py
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import GraphQLError


class ComplexityMiddleware:
    def __init__(self, max_complexity=1000):
        self.max_complexity = max_complexity
        self.estimator = SimpleEstimator(complexity=1)

    def resolve(self, next, root, info, **args):
        if not hasattr(info.context, '_complexity_checked'):
            complexity = get_complexity(
                query=info.operation.loc.source.body,
                schema=info.schema,
                estimator=self.estimator,
            )

            if complexity > self.max_complexity:
                raise GraphQLError(
                    f"Query too complex: {complexity}. "
                    f"Maximum allowed: {self.max_complexity}"
                )

            info.context._complexity_checked = True
            info.context._query_complexity = complexity

        return next(root, info, **args)
```

Register it in `settings.py`:

```python
# settings.py
GRAPHENE = {
    "MIDDLEWARE": [
        "myapp.complexity.ComplexityMiddleware",
    ],
}
```

The `_complexity_checked` flag on `info.context` ensures the check only runs once per request
even though `resolve` is called for every field.

---

## FastAPI

With Strawberry's FastAPI router, you can reuse the same `build_complexity_extension` approach
as in the Strawberry section above:

```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return User(id=id, name="John Doe", email="john@example.com")

    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(id="1", name="John Doe", email="john@example.com"),
            User(id="2", name="Jane Smith", email="jane@example.com"),
        ]


extension = build_complexity_extension(
    estimator=SimpleEstimator(complexity=1),
    max_complexity=1000,
)

schema = strawberry.Schema(query=Query, extensions=[extension])

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

---

## Flask

With Flask-GraphQL, subclass `GraphQLView` and validate complexity in `dispatch_request`
before delegating to the standard execution:

```python
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from graphql import build_schema, GraphQLError
from graphql_complexity import get_complexity, SimpleEstimator


app = Flask(__name__)

schema = build_schema("""
    type User {
        id: ID!
        name: String!
        email: String!
    }

    type Query {
        user(id: ID!): User
        users: [User!]!
    }
""")

MAX_COMPLEXITY = 1000
estimator = SimpleEstimator(complexity=1)


class ComplexityGraphQLView(GraphQLView):
    def dispatch_request(self):
        data = request.get_json()
        query = data.get("query", "")

        try:
            complexity = get_complexity(
                query=query,
                schema=schema,
                estimator=estimator,
            )
        except Exception as e:
            return jsonify({"errors": [{"message": f"Complexity analysis failed: {e}"}]}), 400

        if complexity > MAX_COMPLEXITY:
            return jsonify({
                "errors": [{
                    "message": (
                        f"Query exceeds complexity limit. "
                        f"Query complexity: {complexity}, max allowed: {MAX_COMPLEXITY}"
                    )
                }]
            }), 400

        # Store for logging/monitoring
        request.query_complexity = complexity

        return super().dispatch_request()


app.add_url_rule(
    "/graphql",
    view_func=ComplexityGraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
    ),
)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Choosing the right pattern

All patterns reject the query before any resolver runs, so your business logic is never
reached for over-budget queries.