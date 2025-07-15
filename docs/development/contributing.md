# Contributing

We welcome contributions to JsonPort! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- pip

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/JsonPort.git
   cd JsonPort
   ```

2. **Install in development mode**
   ```bash
   pip install -e ".[dev,test,docs]"
   ```

3. **Verify installation**
   ```bash
   python -c "import jsonport; print(jsonport.__version__)"
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 2. Make Your Changes

- Write your code
- Add tests for new functionality
- Update documentation if needed

### 3. Run Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=jsonport

# Run specific test file
pytest tests/test_specific.py -v
```

### 4. Check Code Quality

```bash
# Format code
black jsonport/ tests/

# Check code style
flake8 jsonport/ tests/ --max-line-length=88 --extend-ignore=E203,W503,E501,F401,F811,F841,E731

# Type checking
mypy jsonport/
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add amazing feature"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
# Create PR on GitHub
```

## Code Style

### Python Code

We follow these style guidelines:

- **Black**: Code formatting (line length: 88)
- **Flake8**: Code linting
- **MyPy**: Type checking
- **Type hints**: Required for all functions

### Documentation

- **Docstrings**: Use Google style docstrings
- **README**: Keep updated with new features
- **Examples**: Add examples for new functionality

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(core): add support for custom encoders
fix(serialization): handle None values in collections
docs(api): update function documentation
test(core): add tests for edge cases
```

## Testing

### Running Tests

```bash
# All tests
pytest -v

# With coverage
pytest --cov=jsonport --cov-report=html

# Only unit tests
pytest -m "not slow and not integration" -v

# Only performance tests
pytest -m slow -v

# Only integration tests
pytest -m integration -v
```

### Writing Tests

1. **Test file naming**: `test_*.py`
2. **Test function naming**: `test_*`
3. **Test class naming**: `Test*`

Example test:

```python
import pytest
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class TestUser:
    name: str
    age: int

def test_basic_serialization():
    user = TestUser("John", 30)
    data = dump(user)
    assert data["name"] == "John"
    assert data["age"] == 30

def test_basic_deserialization():
    data = {"name": "John", "age": 30}
    user = load(data, TestUser)
    assert user.name == "John"
    assert user.age == 30
```

### Test Categories

- **Unit tests**: Test individual functions
- **Integration tests**: Test complete workflows
- **Performance tests**: Benchmark critical operations

## Documentation

### Building Documentation

```bash
# Build docs
mkdocs build

# Serve docs locally
mkdocs serve
```

### Documentation Structure

- **User Guide**: How to use JsonPort
- **Examples**: Practical examples
- **API Reference**: Complete API documentation
- **Development**: Contributing and development guides

## Performance

### Benchmarks

Run performance benchmarks:

```bash
pytest --benchmark-only -v
```

### Performance Guidelines

- **Caching**: Leverage JsonPort's built-in caching
- **Type hints**: Always use type hints for optimal performance
- **Batch operations**: Process multiple objects together

## Release Process

### Version Management

1. **Update version** in `pyproject.toml`
2. **Update changelog** in `CHANGELOG.md`
3. **Create release** on GitHub
4. **Publish to PyPI**

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Version is bumped
- [ ] Release notes are written

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Python version**
2. **JsonPort version**
3. **Operating system**
4. **Minimal reproduction code**
5. **Expected vs actual behavior**

### Feature Requests

When requesting features, include:

1. **Use case description**
2. **Expected API**
3. **Benefits**
4. **Implementation suggestions** (if any)

## Code Review

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Tests** must be included
4. **Documentation** must be updated

### Review Guidelines

- **Functionality**: Does it work as expected?
- **Performance**: Is it efficient?
- **Maintainability**: Is the code clean and readable?
- **Testing**: Are there adequate tests?
- **Documentation**: Is it well documented?

## Getting Help

### Questions and Discussion

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion

### Resources

- **Documentation**: https://luan1schons.github.io/JsonPort/
- **Source Code**: https://github.com/Luan1Schons/JsonPort
- **PyPI**: https://pypi.org/project/jsonport/

## Recognition

Contributors will be recognized in:

- **README.md**: Major contributors
- **CHANGELOG.md**: All contributors
- **GitHub**: Commit history and PRs

Thank you for contributing to JsonPort! 🚀 