# Testing

Learn how to run and write tests for JsonPort.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=jsonport

# Run specific test file
pytest tests/test_jsonport.py -v

# Run specific test function
pytest tests/test_jsonport.py::test_basic_serialization -v
```

### Test Categories

```bash
# Run only unit tests (fast)
pytest -m "not slow and not integration" -v

# Run only performance tests
pytest -m slow -v

# Run only integration tests
pytest -m integration -v

# Run all tests except performance
pytest -m "not slow" -v
```

### Coverage Reports

```bash
# Terminal coverage report
pytest --cov=jsonport --cov-report=term-missing

# HTML coverage report
pytest --cov=jsonport --cov-report=html

# XML coverage report (for CI)
pytest --cov=jsonport --cov-report=xml
```

## Test Structure

### Test Files

Tests are organized in the `tests/` directory:

```
tests/
├── test_jsonport.py      # Main test file
├── conftest.py           # Pytest configuration
└── __init__.py
```

### Test Naming Convention

- **Test files**: `test_*.py`
- **Test functions**: `test_*`
- **Test classes**: `Test*`

## Writing Tests

### Basic Test Example

```python
import pytest
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class TestUser:
    name: str
    age: int

def test_basic_serialization():
    """Test basic object serialization."""
    user = TestUser("John", 30)
    data = dump(user)
    
    assert data["name"] == "John"
    assert data["age"] == 30
    assert isinstance(data, dict)

def test_basic_deserialization():
    """Test basic object deserialization."""
    data = {"name": "John", "age": 30}
    user = load(data, TestUser)
    
    assert user.name == "John"
    assert user.age == 30
    assert isinstance(user, TestUser)
```

### Test with Fixtures

```python
import pytest
from dataclasses import dataclass

@dataclass
class TestProduct:
    id: int
    name: str
    price: float

@pytest.fixture
def sample_product():
    """Provide a sample product for testing."""
    return TestProduct(1, "Laptop", 999.99)

@pytest.fixture
def sample_product_data():
    """Provide sample product data for testing."""
    return {"id": 1, "name": "Laptop", "price": 999.99}

def test_product_serialization(sample_product):
    """Test product serialization using fixture."""
    data = dump(sample_product)
    
    assert data["id"] == 1
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99

def test_product_deserialization(sample_product_data):
    """Test product deserialization using fixture."""
    product = load(sample_product_data, TestProduct)
    
    assert product.id == 1
    assert product.name == "Laptop"
    assert product.price == 999.99
```

### Test with Parameters

```python
import pytest
from datetime import datetime, date

@pytest.mark.parametrize("input_date,expected_str", [
    (date(2024, 1, 1), "2024-01-01"),
    (date(2023, 12, 31), "2023-12-31"),
    (date(2020, 2, 29), "2020-02-29"),  # Leap year
])
def test_date_serialization(input_date, expected_str):
    """Test date serialization with different inputs."""
    data = dump(input_date)
    assert data == expected_str

@pytest.mark.parametrize("input_datetime,expected_str", [
    (datetime(2024, 1, 1, 12, 0, 0), "2024-01-01T12:00:00"),
    (datetime(2024, 1, 1, 0, 0, 0), "2024-01-01T00:00:00"),
    (datetime(2024, 1, 1, 23, 59, 59), "2024-01-01T23:59:59"),
])
def test_datetime_serialization(input_datetime, expected_str):
    """Test datetime serialization with different inputs."""
    data = dump(input_datetime)
    assert data == expected_str
```

### Test Error Cases

```python
import pytest
from jsonport import JsonPortError

def test_invalid_type_serialization():
    """Test serialization of unsupported types."""
    unsupported_object = lambda x: x  # Function objects are not serializable
    
    with pytest.raises(JsonPortError):
        dump(unsupported_object)

def test_invalid_data_deserialization():
    """Test deserialization of invalid data."""
    invalid_data = {"name": "John", "age": "invalid_age"}  # age should be int
    
    with pytest.raises(JsonPortError):
        load(invalid_data, TestUser)

def test_missing_field_deserialization():
    """Test deserialization with missing required fields."""
    incomplete_data = {"name": "John"}  # missing age field
    
    with pytest.raises(JsonPortError):
        load(incomplete_data, TestUser)
```

### Test File Operations

```python
import pytest
import tempfile
import os
from jsonport import dump_file, load_file

def test_file_operations():
    """Test saving and loading objects to/from files."""
    user = TestUser("John", 30)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Save to file
        dump_file(user, temp_file)
        
        # Verify file exists and has content
        assert os.path.exists(temp_file)
        assert os.path.getsize(temp_file) > 0
        
        # Load from file
        loaded_user = load_file(temp_file, TestUser)
        
        # Verify data integrity
        assert loaded_user.name == user.name
        assert loaded_user.age == user.age
        assert isinstance(loaded_user, TestUser)
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_compressed_file_operations():
    """Test saving and loading compressed files."""
    user = TestUser("John", 30)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json.gz', delete=False) as f:
        temp_file = f.name
    
    try:
        # Save compressed file
        dump_file(user, temp_file)
        
        # Verify file exists and is compressed
        assert os.path.exists(temp_file)
        
        # Load compressed file
        loaded_user = load_file(temp_file, TestUser)
        
        # Verify data integrity
        assert loaded_user.name == user.name
        assert loaded_user.age == user.age
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
```

## Performance Testing

### Benchmark Tests

```python
import pytest
import time
from dataclasses import dataclass

@dataclass
class BenchmarkData:
    id: int
    name: str
    values: list[float]
    metadata: dict[str, str]

@pytest.mark.slow
def test_serialization_benchmark(benchmark):
    """Benchmark serialization performance."""
    test_data = BenchmarkData(
        id=1,
        name="test",
        values=[1.1, 2.2, 3.3] * 1000,
        metadata={"key1": "value1", "key2": "value2"}
    )
    
    result = benchmark(dump, test_data)
    assert isinstance(result, dict)

@pytest.mark.slow
def test_deserialization_benchmark(benchmark):
    """Benchmark deserialization performance."""
    test_data = BenchmarkData(
        id=1,
        name="test",
        values=[1.1, 2.2, 3.3] * 1000,
        metadata={"key1": "value1", "key2": "value2"}
    )
    
    data = dump(test_data)
    result = benchmark(load, data, BenchmarkData)
    assert isinstance(result, BenchmarkData)
```

### Memory Tests

```python
import pytest
import psutil
import os

@pytest.mark.slow
def test_memory_usage():
    """Test memory usage during large operations."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Create large dataset
    large_objects = [
        TestUser(f"user{i}", i) 
        for i in range(10000)
    ]
    
    # Serialize all objects
    data_list = [dump(obj) for obj in large_objects]
    
    # Check memory usage
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable (less than 100MB)
    assert memory_increase < 100 * 1024 * 1024  # 100MB
```

## Integration Testing

### End-to-End Workflows

```python
@pytest.mark.integration
def test_complete_workflow():
    """Test complete serialization/deserialization workflow."""
    # Create complex nested structure
    @dataclass
    class Address:
        street: str
        city: str
    
    @dataclass
    class Company:
        name: str
        address: Address
        employees: list[str]
    
    company = Company(
        name="TechCorp",
        address=Address("123 Tech St", "San Francisco"),
        employees=["Alice", "Bob", "Charlie"]
    )
    
    # Complete workflow
    data = dump(company)
    restored_company = load(data, Company)
    
    # Verify complete restoration
    assert restored_company.name == company.name
    assert restored_company.address.street == company.address.street
    assert restored_company.address.city == company.address.city
    assert restored_company.employees == company.employees
```

## Test Configuration

### Pytest Configuration

The project uses `pyproject.toml` for pytest configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=jsonport",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### Coverage Configuration

```toml
[tool.coverage.run]
source = ["jsonport"]
omit = [
    "*/tests/*",
    "*/test_*",
    "setup.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:

- **Push to main**: Full test suite
- **Pull requests**: Full test suite
- **Multiple Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### Local Development

Before committing:

```bash
# Run all checks
pytest -v --cov=jsonport
black jsonport/ tests/
flake8 jsonport/ tests/
mypy jsonport/
```

## Best Practices

1. **Test coverage**: Aim for >80% coverage
2. **Test isolation**: Each test should be independent
3. **Meaningful assertions**: Test specific behavior, not implementation
4. **Error testing**: Test both success and failure cases
5. **Performance testing**: Include benchmarks for critical operations
6. **Documentation**: Write clear test docstrings

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute to JsonPort
- [Benchmarking](benchmarking.md) - Performance testing guide
- [API Reference](api/) - Complete API documentation 