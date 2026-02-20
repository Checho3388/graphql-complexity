[![GraphQL Complexity Logo](https://github.com/Checho3388/graphql-complexity/raw/main/.github/logo.png)](https://github.com/Checho3388/graphql-complexity/raw/main/.github/logo.png)

# GraphQL Complexity

[![Build](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-build.yml/badge.svg)](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-build.yml)
[![PyPI](https://img.shields.io/pypi/v/graphql-complexity?label=pypi%20package)](https://pypi.org/project/graphql-complexity/)
[![codecov](https://codecov.io/gh/Checho3388/graphql-complexity/graph/badge.svg?token=4LH7AVN119)](https://codecov.io/gh/Checho3388/graphql-complexity)
[![Downloads](https://static.pepy.tech/badge/graphql-complexity)](https://pepy.tech/project/graphql-complexity)
[![Python Version](https://img.shields.io/pypi/pyversions/graphql-complexity)](https://pypi.org/project/graphql-complexity/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library to compute the complexity of a GraphQL operation. Protect your API from expensive queries and potential DoS attacks by calculating complexity before execution.

🎮 **Try it live:** [graphql-complexity playground](https://graphql-complexity-playground-production.up.railway.app/)
📖 **Full docs:** [graphql-complexity.readthedocs.io](https://graphql-complexity.readthedocs.io)

---

## Installation

```bash
pip install graphql-complexity

# With Strawberry GraphQL support
pip install graphql-complexity[strawberry-graphql]
```

## Quick Start

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

complexity = get_complexity(
    query="query { user { id name } }",
    schema=schema,
    estimator=SimpleEstimator(complexity=1),
)

if complexity > 10:
    raise Exception(f"Query is too complex: {complexity}")
```

## Estimators

| Estimator | Description |
|---|---|
| `SimpleEstimator` | Assigns a constant cost to every field |
| `DirectivesEstimator` | Reads cost from `@complexity(value: N)` schema directives |
| `ArgumentsEstimator` | Multiplies cost by a numeric/list argument (e.g. `limit`, `ids`) |
| Custom | Subclass `ComplexityEstimator` and implement `get_field_complexity` |

See the [estimators docs](https://graphql-complexity.readthedocs.io/guides/estimators.html) for full reference and examples.

## Integrations

See the [integrations docs](https://graphql-complexity.readthedocs.io/guides/integrations.html) for examples
about how this library integrates with `strawberry`, `FastAPI`, `Flask` and `graphene-django`.


## Credits

Estimators idea was heavily inspired by [graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity).

## License

[MIT](LICENSE)