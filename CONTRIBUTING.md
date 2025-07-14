# Contributing to JsonPort

Thank you for your interest in contributing to JsonPort! This document provides guidelines and information for contributors.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/JsonPort.git
   cd JsonPort
   ```

2. **Install development dependencies:**
   ```bash
   pip install -e ".[dev,test]"
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make your changes
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation if needed

### 3. Run tests and checks
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run benchmarks
make benchmark

# Run all quality checks
make check
```

### 4. Commit your changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and create a Pull Request
```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Code Style
- Use **Black** for code formatting (configured in `pyproject.toml`)
- Follow **PEP 8** guidelines
- Use **type hints** for all function parameters and return values
- Keep functions small and focused

### Documentation
- Use **docstrings** for all public functions and classes
- Follow **Google-style** docstring format
- Include examples in docstrings for complex functions
- Update README.md for user-facing changes

### Testing
- Write **unit tests** for all new functionality
- Aim for **90%+ code coverage**
- Include **integration tests** for complex workflows
- Add **performance benchmarks** for performance-critical code

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Pull Request Guidelines

### Before submitting a PR:
1. **Tests pass:** All tests must pass
2. **Code coverage:** Maintain or improve coverage
3. **Documentation:** Update docs for new features
4. **Type checking:** No mypy errors
5. **Linting:** No flake8 errors
6. **Formatting:** Code formatted with Black

### PR Description should include:
- **Summary:** Brief description of changes
- **Motivation:** Why this change is needed
- **Testing:** How to test the changes
- **Breaking changes:** Any API changes
- **Related issues:** Link to related issues

## Issue Reporting

When reporting issues, please include:

1. **Environment:**
   - Python version
   - Operating system
   - JsonPort version

2. **Reproduction:**
   - Minimal code example
   - Expected vs actual behavior
   - Error messages/tracebacks

3. **Additional context:**
   - Use case
   - Workarounds tried

## Release Process

### For maintainers:

1. **Update version:**
   - Update version in `pyproject.toml`
   - Update `CHANGELOG.md`

2. **Create release:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

3. **GitHub Actions will automatically:**
   - Run tests on multiple Python versions
   - Build and publish to PyPI
   - Create GitHub release

## Getting Help

- **Issues:** Use GitHub Issues for bug reports and feature requests
- **Discussions:** Use GitHub Discussions for questions and general discussion
- **Code of Conduct:** Please be respectful and inclusive

## License

By contributing to JsonPort, you agree that your contributions will be licensed under the MIT License. 