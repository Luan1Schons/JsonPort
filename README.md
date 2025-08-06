# JsonPort 🚀

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16755990.svg)](https://doi.org/10.5281/zenodo.16755990)
[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-jsonport-red.svg)](https://pypi.org/project/jsonport/)
[![Version](https://img.shields.io/pypi/v/jsonport.svg)](https://pypi.org/project/jsonport/)
[![Downloads](https://static.pepy.tech/badge/jsonport)](https://pepy.tech/project/jsonport)
[![CI](https://github.com/Luan1Schons/JsonPort/workflows/Tests/badge.svg)](https://github.com/Luan1Schons/JsonPort/actions)
[![Coverage](https://codecov.io/gh/Luan1Schons/JsonPort/branch/main/graph/badge.svg)](https://codecov.io/gh/Luan1Schons/JsonPort)

> **A high-performance Python library for seamless serialization and deserialization of complex Python objects to/from JSON format.** 

JsonPort provides intelligent type handling, caching optimizations, and comprehensive support for dataclasses, enums, datetime objects, and collections with blazing fast performance! ⚡

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **High Performance** | Optimized with intelligent caching for type hints and optional type resolution |
| 🎯 **Type Safety** | Full type hints support with automatic type conversion and validation |
| 📦 **Dataclass Support** | Native serialization/deserialization of dataclasses with zero configuration |
| 🗓️ **DateTime Handling** | Automatic ISO format conversion for datetime, date, and time objects |
| 🔄 **Collection Support** | Lists, tuples, sets, and dictionaries with perfect type preservation |
| 📁 **File Operations** | Direct file I/O with automatic gzip compression support |
| 🎨 **Enum Support** | Automatic enum value serialization with type safety |
| 🛡️ **Error Handling** | Comprehensive error messages and validation with detailed feedback |
| 🔧 **Zero Dependencies** | Pure Python implementation with no external dependencies |

## 🚀 Quick Start

### Installation

```bash
pip install jsonport
```

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

## 🐍 Python Version Support

JsonPort supports the following Python versions:

| Version | Status | Features |
|---------|--------|----------|
| **Python 3.7** | ✅ Full Support | All features (EOL - End of Life) |
| **Python 3.8** | ✅ Full Support | All features |
| **Python 3.9** | ✅ Full Support | All features |
| **Python 3.10** | ✅ Full Support | All features |
| **Python 3.11** | ✅ Full Support | All features |
| **Python 3.12** | ✅ Full Support | All features |
| **Python 3.13** | ✅ Full Support | All features |

> **Note**: Python 3.7 reached End of Life (EOL) in June 2023. While JsonPort still supports Python 3.7 for compatibility with existing projects, we recommend upgrading to Python 3.8+ for new projects.

## 📚 Advanced Examples

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

## 📊 Performance Features

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

## 🧪 Testing

JsonPort uses **pytest** for all automated tests. To run the test suite:

### Install Test Dependencies
```bash
pip install -e ".[test]"
```

### Run Tests
```bash
# All tests
pytest -v

# With coverage
pytest --cov

# Only fast unit tests
pytest -m 'not slow and not integration' -v

# Only performance tests
pytest -m slow -v

# Only integration tests
pytest -m integration -v
```

### Benchmarking
```bash
# Run performance benchmarks
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

## 📖 API Reference

### Core Functions

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `dump(obj)` | Serialize object to JSON-serializable format | `obj`: Object to serialize | JSON-serializable data |
| `load(data, target_class)` | Deserialize JSON data to Python object | `data`: Data to deserialize<br>`target_class`: Target class | Instance of target class |
| `dump_file(obj, path, overwrite=True)` | Serialize object and save to file | `obj`: Object to serialize<br>`path`: File path<br>`overwrite`: Overwrite existing file | None |
| `load_file(path, target_class)` | Load JSON file and deserialize | `path`: File path<br>`target_class`: Target class | Instance of target class |

### Supported Types

| Category | Types |
|----------|-------|
| **Primitives** | `str`, `int`, `float`, `bool` |
| **Datetime** | `datetime.datetime`, `datetime.date`, `datetime.time` |
| **Collections** | `list`, `tuple`, `set`, `dict` |
| **Custom Types** | `dataclass`, `Enum` |
| **Optional Types** | `Optional[T]`, `Union[T, None]` |

## 🎯 Best Practices

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

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/Luan1Schons/JsonPort.git
cd JsonPort

# Install in development mode
pip install -e ".[dev,test]"

# Run tests
pytest -v

# Format code
black jsonport/ tests/

# Check code quality
flake8 jsonport/ tests/ --max-line-length=88 --extend-ignore=E203,W503,E501,F401,F811,F841,E731
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions, please:

1. 📖 Check the [documentation](https://github.com/luan1schons/jsonport)
2. 🔍 Search [existing issues](https://github.com/luan1schons/jsonport/issues)
3. 🐛 Create a [new issue](https://github.com/luan1schons/jsonport/issues/new)

---

**JsonPort** - Making JSON serialization simple, fast, and type-safe! 🚀 