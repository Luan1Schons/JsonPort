# JsonPort

[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-jsonport-red.svg)](https://pypi.org/project/jsonport/)

A high-performance Python library for seamless serialization and deserialization of complex Python objects to/from JSON format. JsonPort provides intelligent type handling, caching optimizations, and support for dataclasses, enums, datetime objects, and collections.

## Features

- 🚀 **High Performance**: Optimized with caching for type hints and optional type resolution
- 🎯 **Type Safety**: Full type hints support with automatic type conversion
- 📦 **Dataclass Support**: Native serialization/deserialization of dataclasses
- 🗓️ **DateTime Handling**: Automatic ISO format conversion for datetime objects
- 🔄 **Collection Support**: Lists, tuples, sets, and dictionaries with type preservation
- 📁 **File Operations**: Direct file I/O with gzip compression support
- 🎨 **Enum Support**: Automatic enum value serialization
- 🛡️ **Error Handling**: Comprehensive error messages and validation

## Installation

```bash
pip install jsonport
```

## Python Version Support

JsonPort supports the following Python versions:

- **Python 3.8** - Full support with all features
- **Python 3.9** - Full support with all features
- **Python 3.10** - Full support with all features
- **Python 3.11** - Full support with all features
- **Python 3.12** - Full support with all features
- **Python 3.13** - Full support with all features

All features including dataclasses, type hints, datetime handling, and file operations work consistently across all supported Python versions.

## Quick Start

### Basic Usage

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from jsonport import dump, load, dump_file, load_file

# Define your data structures
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

@dataclass
class User:
    name: str
    age: int
    role: UserRole
    created_at: datetime
    tags: list[str]

# Create an instance
user = User(
    name="John Doe",
    age=30,
    role=UserRole.ADMIN,
    created_at=datetime.now(),
    tags=["developer", "python"]
)

# Serialize to dictionary
data = dump(user)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "age": 30,
#   "role": "admin",
#   "created_at": "2025-07-14T10:30:00",
#   "tags": ["developer", "python"]
# }

# Deserialize back to object
restored_user = load(data, User)
print(restored_user.name)  # "John Doe"
```

### File Operations

```python
# Save to JSON file
dump_file(user, "user.json")

# Load from JSON file
loaded_user = load_file("user.json", User)

# Save with compression
dump_file(user, "user.json.gz")

# Load compressed file
compressed_user = load_file("user.json.gz", User)
```

## Advanced Examples

### Complex Nested Structures

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import date

@dataclass
class Address:
    street: str
    city: str
    country: str
    postal_code: str

@dataclass
class Contact:
    email: str
    phone: Optional[str] = None

@dataclass
class Company:
    name: str
    founded: date
    employees: int
    address: Address
    contacts: List[Contact]
    departments: Dict[str, List[str]]

# Create complex object
company = Company(
    name="TechCorp",
    founded=date(2020, 1, 1),
    employees=150,
    address=Address(
        street="123 Tech Street",
        city="San Francisco",
        country="USA",
        postal_code="94105"
    ),
    contacts=[
        Contact("info@techcorp.com"),
        Contact("support@techcorp.com", "+1-555-0123")
    ],
    departments={
        "Engineering": ["Backend", "Frontend", "DevOps"],
        "Sales": ["Enterprise", "SMB"],
        "Marketing": ["Digital", "Content"]
    }
)

# Serialize complex structure
data = dump(company)

# Deserialize with full type preservation
restored_company = load(data, Company)
```

### Collections with Type Information

```python
from dataclasses import dataclass
from typing import Set, Tuple

@dataclass
class Product:
    id: int
    name: str
    price: float
    categories: Set[str]
    dimensions: Tuple[float, float, float]

product = Product(
    id=1,
    name="Laptop",
    price=999.99,
    categories={"electronics", "computers", "portable"},
    dimensions=(35.5, 24.0, 2.1)
)

# Serialize with collection type preservation
data = dump(product)
# Sets are converted to lists, tuples preserved
print(data["categories"])  # ["electronics", "computers", "portable"]
print(data["dimensions"])  # [35.5, 24.0, 2.1]

# Deserialize with proper type restoration
restored_product = load(data, Product)
print(type(restored_product.categories))  # <class 'set'>
print(type(restored_product.dimensions))  # <class 'tuple'>
```

### Custom JSON Encoder

```python
import json
from jsonport import JsonPortEncoder

# Use the custom encoder with standard json module
data = dump(company)
json_string = json.dumps(data, cls=JsonPortEncoder, indent=2)
print(json_string)
```

### Error Handling

```python
from jsonport import JsonPortError

try:
    # Try to serialize non-serializable object
    non_serializable = lambda x: x
    dump(non_serializable)
except JsonPortError as e:
    print(f"Serialization error: {e}")

try:
    # Try to load file that doesn't exist
    load_file("nonexistent.json", User)
except FileNotFoundError:
    print("File not found")
except JsonPortError as e:
    print(f"Deserialization error: {e}")
```

## Performance Features

### Caching Optimizations

JsonPort automatically caches:
- **Type hints** for dataclasses (max 1024 entries)
- **Optional type resolution** (max 512 entries)

This provides significant performance improvements when working with the same dataclass types repeatedly.

### Benchmarks

```python
import time
from dataclasses import dataclass
from jsonport import dump, load

@dataclass
class BenchmarkData:
    id: int
    name: str
    values: list[float]
    metadata: dict[str, str]

# Create test data
test_data = BenchmarkData(
    id=1,
    name="test",
    values=[1.1, 2.2, 3.3] * 1000,
    metadata={"key1": "value1", "key2": "value2"}
)

# Benchmark serialization
start_time = time.time()
for _ in range(1000):
    data = dump(test_data)
serialization_time = time.time() - start_time

# Benchmark deserialization
start_time = time.time()
for _ in range(1000):
    restored = load(data, BenchmarkData)
deserialization_time = time.time() - start_time

print(f"Serialization: {serialization_time:.4f}s")
print(f"Deserialization: {deserialization_time:.4f}s")
```

## API Reference

### Core Functions

#### `dump(obj: Any) -> Any`
Serialize a Python object to JSON-serializable format.

**Parameters:**
- `obj`: Object to serialize (dataclass, list, tuple, set, dict, or primitive)

**Returns:**
- JSON-serializable dictionary, list, or primitive value

#### `load(data: Any, target_class: Type[T]) -> T`
Deserialize JSON data to Python object.

**Parameters:**
- `data`: Dictionary/list to deserialize
- `target_class`: Target class for deserialization

**Returns:**
- Instance of the target class

#### `dump_file(obj: Any, path: str, overwrite: bool = True) -> None`
Serialize object and save to JSON file.

**Parameters:**
- `obj`: Object to serialize
- `path`: Path to the JSON file
- `overwrite`: If False, raises error when file exists

#### `load_file(path: str, target_class: Type[T]) -> T`
Load JSON file and deserialize to object.

**Parameters:**
- `path`: Path to the JSON file
- `target_class`: Target class for deserialization

**Returns:**
- Instance of the target class

### Supported Types

- **Primitives**: `str`, `int`, `float`, `bool`
- **Datetime**: `datetime.datetime`, `datetime.date`, `datetime.time`
- **Collections**: `list`, `tuple`, `set`, `dict`
- **Custom Types**: `dataclass`, `Enum`
- **Optional Types**: `Optional[T]`, `Union[T, None]`

## Best Practices

### 1. Use Type Hints
Always define proper type hints for optimal performance and type safety:

```python
@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = None
```

### 2. Handle Optional Fields
Use `Optional` types for fields that might be None:

```python
@dataclass
class Product:
    id: int
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
```

### 3. Use Appropriate Collections
Choose the right collection type for your data:

```python
@dataclass
class Configuration:
    settings: Dict[str, Any]
    allowed_users: Set[str]
    coordinates: Tuple[float, float]
    items: List[str]
```

### 4. Error Handling
Always handle potential errors in production code:

```python
try:
    data = load_file("config.json", Config)
except (FileNotFoundError, JsonPortError) as e:
    logger.error(f"Failed to load config: {e}")
    data = Config()  # Use default config
```

---

## Running the Tests

JsonPort uses **pytest** for all automated tests. To run the test suite:

1. **Install test dependencies** (only once):

```bash
pip install -e ".[test]"
```

2. **Run all tests:**

```bash
pytest -v
```

3. **Check code coverage:**

```bash
pytest --cov
```

4. **Run only fast unit tests (skip slow/integration):**

```bash
pytest -m 'not slow and not integration' -v
```

5. **Run only performance tests:**

```bash
pytest -m slow -v
```

6. **Run only integration tests:**

```bash
pytest -m integration -v
```

All tests are located in the `tests/` directory and cover all library features. If you see any errors, make sure you are using Python 3.7+ and all dependencies are installed.

---

## Benchmarking

JsonPort includes performance tests using **pytest-benchmark**. To run benchmarks and measure serialization/deserialization speed:

```bash
pytest --benchmark-only -v
```

Example output:

```
--------------------------------------------------------------------------------------------- benchmark: 2 tests -----------------------------------------------------------------------------
Name (time in us)                       Min                 Max                Mean             StdDev              Median                IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_deserialization_benchmark     110.3460 (1.0)      263.2940 (1.0)      120.8443 (1.0)      12.3452 (1.0)      118.4470 (1.0)       6.0770 (1.0)       386;464        8.2751 (1.0)        6829           1
test_serialization_benchmark       251.4210 (2.28)     522.7470 (1.99)     270.2584 (2.24)     16.9108 (1.37)     266.3670 (2.25)     12.2920 (2.02)      218;161        3.7002 (0.45)       2499           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

- **OPS (Kops/s)**: Operations per second (higher is better)
- **Mean**: Average time per operation
- **Rounds/Iterations**: Number of repetitions for statistical accuracy

You can compare results between runs or different machines. For more options, see:

```bash
pytest --help | grep benchmark
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0
- Initial release
- High-performance serialization/deserialization
- Dataclass support with type hints
- File I/O with gzip compression
- Comprehensive error handling
- Caching optimizations for type hints

## Support

If you encounter any issues or have questions, please:

1. Check the [documentation](https://github.com/luan1schons/jsonport)
2. Search [existing issues](https://github.com/luan1schons/jsonport/issues)
3. Create a [new issue](https://github.com/luan1schons/jsonport/issues/new)

---

**JsonPort** - Making JSON serialization simple, fast, and type-safe! 🚀 