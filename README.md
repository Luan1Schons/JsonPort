# JsonPort 🚀

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16755989.svg)](https://doi.org/10.5281/zenodo.16755989)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-jsonport-red.svg)](https://pypi.org/project/jsonport/)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://pypi.org/project/jsonport/)
[![Downloads](https://static.pepy.tech/badge/jsonport)](https://pepy.tech/project/jsonport)
[![CI](https://github.com/Luan1Schons/JsonPort/workflows/Tests/badge.svg)](https://github.com/Luan1Schons/JsonPort/actions)
[![Coverage](https://codecov.io/gh/Luan1Schons/JsonPort/branch/main/graph/badge.svg)](https://codecov.io/gh/Luan1Schons/JsonPort)

> **A high-performance Python library for seamless serialization and deserialization of complex Python objects to/from JSON format.** 

JsonPort provides intelligent type handling, caching optimizations, and comprehensive support for dataclasses, enums, datetime objects, collections, and extended standard library types with blazing fast performance! ⚡

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **High Performance** | Introspected type caching and optimized conversion algorithms |
| 🎯 **Type Safety** | PEP 561 compliant (`py.typed`) with full static analysis support (`mypy --strict`) |
| 📦 **Dataclasses & Modern Typing** | Full support for `dataclass`, `NamedTuple`, `TypedDict`, `Literal`, and intelligent `Union` matching |
| 🧩 **Extended Types** | Native serialization/deserialization for `UUID`, `Decimal`, `Path`, `bytes`, IP addresses/networks, `timedelta`, and regex `Pattern` |
| 📝 **Direct String & Stream I/O** | `dumps()` and `loads()` for strings; `dump_stream()` and `load_stream()` for files/network/StringIO |
| 🏷️ **Field Metadata** | Fine-grained dataclass control: `alias`, `exclude`, and per-field custom `serializer` / `deserializer` |
| 🔌 **Custom Registry** | Extensible `@serializer` and `@deserializer` decorators, functional APIs, and isolated `Registry` instances |
| 🛡️ **Strict Mode & Error Paths** | Enforce exact schema match with `strict=True`, pinpoint errors with attribute paths (e.g. `user.address.zip`) |
| 📁 **File & Compression** | Direct file I/O with automatic `.gz` gzip compression/decompression |
| 🔧 **Zero Dependencies** | Pure Python implementation with zero third-party dependencies |

## 🚀 Quick Start

### Installation

```bash
pip install jsonport
```

### 1. 1.x Backwards Compatible Usage (Dict / Primitive Conversion)

JsonPort 2.0 maintains 100% backward compatibility with all 1.x functions:

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from jsonport import dump, load, dump_file, load_file

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

user = User(
    name="John Doe",
    age=30,
    role=UserRole.ADMIN,
    created_at=datetime.now(),
    tags=["developer", "python"],
)

# Serialize to dictionary/primitives
data = dump(user)
print(data["role"])  # "admin"

# Deserialize back to dataclass
restored_user = load(data, User)
assert restored_user.name == "John Doe"

# Save & load directly from JSON or gzipped files
dump_file(user, "user.json.gz")
loaded_user = load_file("user.json.gz", User)
```

### 2. JsonPort 2.0: Direct String & Stream Operations

```python
import io
from jsonport import dumps, loads, dump_stream, load_stream

# Direct JSON string serialization and deserialization
json_str = dumps(user, indent=2)
user_from_str = loads(json_str, User)

# Stream operations with StringIO, files, or network streams
stream = io.StringIO()
dump_stream(user, stream)
stream.seek(0)
user_from_stream = load_stream(stream, User)
```

### 3. JsonPort 2.0: Extended Types & Field Metadata

```python
import uuid
import decimal
import pathlib
import ipaddress
from dataclasses import dataclass, field
from jsonport import dumps, loads

@dataclass
class ServerNode:
    id: uuid.UUID
    rate: decimal.Decimal
    config_path: pathlib.Path
    ip: ipaddress.IPv4Address
    # Field aliases and exclusions
    secret_token: str = field(metadata={"exclude": True})
    display_name: str = field(metadata={"alias": "server_name"})

node = ServerNode(
    id=uuid.uuid4(),
    rate=decimal.Decimal("99.99"),
    config_path=pathlib.Path("/etc/server.conf"),
    ip=ipaddress.IPv4Address("192.168.1.1"),
    secret_token="super-secret",
    display_name="Node-Alpha",
)

json_data = dumps(node)
# {"id": "...", "rate": "99.99", "config_path": "/etc/server.conf", "ip": "192.168.1.1", "server_name": "Node-Alpha"}
restored_node = loads(json_data, ServerNode)
```

### 4. JsonPort 2.0: Custom Registry

```python
from jsonport import serializer, deserializer, dumps, loads

class Money:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

@serializer(Money)
def serialize_money(m: Money) -> str:
    return f"{m.currency} {m.amount:.2f}"

@deserializer(Money)
def deserialize_money(s: str) -> Money:
    curr, amt = s.split()
    return Money(float(amt), curr)

json_str = dumps(Money(49.95, "USD"))
# '"USD 49.95"'
money = loads(json_str, Money)
```

### 5. JsonPort 2.0: Strict Mode & Detailed Error Paths

```python
from jsonport import loads, DeserializationError

raw_json = '{"name": "Alice", "unexpected_field": 123}'

try:
    loads(raw_json, User, strict=True)
except DeserializationError as err:
    print(err)
    # Output: Extra keys not permitted in strict mode for User: ['unexpected_field']
    print(err.target_type)  # <class 'User'>
```

## 🐍 Python Version Support

JsonPort 2.0 supports modern Python versions:

| Version | Status |
|---------|--------|
| **Python 3.9** | ✅ Full Support |
| **Python 3.10** | ✅ Full Support |
| **Python 3.11** | ✅ Full Support |
| **Python 3.12** | ✅ Full Support |
| **Python 3.13** | ✅ Full Support |

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