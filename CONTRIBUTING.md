# Contributing to graphql-complexity

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

Found a bug? Please [open an issue](https://github.com/Checho3388/graphql-complexity/issues/new) with:

- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment details

### Suggesting Features

Have an idea? [Open an issue](https://github.com/Checho3388/graphql-complexity/issues/new) describing:

- The problem you’re trying to solve
- Your proposed solution
- Any alternatives you’ve considered

### Pull Requests

1. Fork the repository
1. Create a branch: `git checkout -b feature/your-feature`
1. Make your changes
1. Run tests: `pytest tests/ -v`
1. Commit: `git commit -m "Add your feature"`
1. Push: `git push origin feature/your-feature`
1. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/graphql-complexity.git
cd graphql-complexity

# Install dependencies
poetry install

# Run tests
pytest tests/ -v

# Run linting
flake8 src/
mypy src/
```

### Code Style

- Follow PEP 8
- Add type hints
- Write tests for new features
- Update documentation

### Testing

All code must include tests:

```bash
pytest tests/ -v --cov=src/graphql_complexity
```

### Questions?

Feel free to open an issue or start a discussion!

## Code of Conduct

Be respectful and constructive. We’re all here to build great software together.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.