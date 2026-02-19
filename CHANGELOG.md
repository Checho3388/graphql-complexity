# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `ArgumentsEstimator`: a new built-in estimator that multiplies field complexity by a numeric argument value (e.g. `limit: 10`) or by the length of a list argument (e.g. `ids: ["a","b","c"]`). Useful for APIs with pagination or batch arguments.

## [0.4.2] - 2026-02-10

This release focuses on broadening environment support, improving project documentation, and strengthening our testing suite.

### 🌟 Highlights
* **Python 3.13 Support:** We've officially added support for the latest Python release. Stay on the cutting edge without breaking your complexity logic.

### 📝 Documentation & DX
* **New Guidelines:** Added `CHANGELOG.md` and `CONTRIBUTING.md` to make it easier for the community to get involved.
* **Better Examples:** Expanded the `README.md` with more detailed use cases to help you implement complex cost analysis faster.

### 🛠️ Internal Improvements
* **Unit Testing:** Significant improvements to the test suite to ensure better stability and reliability by @Checho3388 in #11

## [0.3.2] - 2024-03-14

### Added
- DirectivesEstimator for schema-based complexity calculation
- SimpleEstimator for basic complexity calculation
- Support for Strawberry GraphQL integration
- Comprehensive test coverage
- CI/CD with GitHub Actions

### Fixed
- Various bug fixes and stability improvements

## [0.3.1] - 2024-02

### Added
- Core complexity calculation functionality
- Custom estimator support

### Fixed
- Bug fixes from initial release

## [0.3.0] - 2024-01

Initial public release.

### Added
- Basic GraphQL query complexity analysis
- Visit-based complexity calculation algorithm
- Extensible estimator interface
- PyPI package publication
- MIT license

[0.3.2]: https://github.com/Checho3388/graphql-complexity/releases/tag/v0.3.2
[0.3.1]: https://github.com/Checho3388/graphql-complexity/releases/tag/v0.3.1
[0.3.0]: https://github.com/Checho3388/graphql-complexity/releases/tag/v0.3.0
