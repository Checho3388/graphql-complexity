# Installation

## Requirements

- Python 3.8+
- `graphql-core` (installed automatically as a dependency)

## Basic Installation

Install `graphql-complexity` from PyPI using pip:

```bash
pip install graphql-complexity
```

## With Strawberry GraphQL Support

If you use [Strawberry GraphQL](https://strawberry.rocks/), install the optional extras:

```bash
pip install graphql-complexity[strawberry-graphql]
```

Or with Poetry:

```bash
poetry install --extras strawberry-graphql
```

## Verifying the Installation

After installation, confirm everything is working by running the following in a Python shell:

```python
import graphql_complexity
print(graphql_complexity.__version__)
```

## Next Steps

Head over to the [Quick Start](quickstart.md) guide to compute your first query complexity.
