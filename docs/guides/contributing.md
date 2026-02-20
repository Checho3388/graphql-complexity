# Contributing

Contributions are welcome! Here's how to get started.

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/Checho3388/graphql-complexity.git
cd graphql-complexity
```

2. Install dependencies with Poetry:

```bash
poetry install --extras strawberry-graphql
```

3. Run the test suite:

```bash
poetry run pytest
```

## Code Style

- The project uses **flake8** for linting and **mypy** for type checking.
- Run linting with:

```bash
poetry run flake8 src/
poetry run mypy src/
```

## Submitting Changes

1. Fork the repository and create a feature branch.
2. Write tests for your changes.
3. Ensure all tests and linters pass.
4. Open a pull request against the `main` branch.

## Reporting Issues

Please use the [GitHub Issues](https://github.com/Checho3388/graphql-complexity/issues)
tracker for bug reports and feature requests.
