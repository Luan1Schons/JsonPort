# JsonPort 🚀

> **A high-performance Python library for seamless serialization and deserialization of complex Python objects to/from JSON format.**

JsonPort provides intelligent type handling, caching optimizations, and comprehensive support for dataclasses, enums, datetime objects, and collections with blazing fast performance! ⚡

## ✨ Key Features

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

### Basic Example

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from jsonport import dump, load

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

## 🐍 Python Version Support

JsonPort supports Python 3.7+ with full feature compatibility across all versions:

| Version | Status | Features |
|---------|--------|----------|
| **Python 3.7** | ✅ Full Support | All features (EOL - End of Life) |
| **Python 3.8** | ✅ Full Support | All features |
| **Python 3.9** | ✅ Full Support | All features |
| **Python 3.10** | ✅ Full Support | All features |
| **Python 3.11** | ✅ Full Support | All features |
| **Python 3.12** | ✅ Full Support | All features |
| **Python 3.13** | ✅ Full Support | All features |

## 📊 Performance

JsonPort is optimized for high performance with intelligent caching:

- **Type hints caching** (max 1024 entries)
- **Optional type resolution** (max 512 entries)
- **Zero external dependencies**
- **Pure Python implementation**

### Benchmark Results

```
--------------------------------------------------------------------------------------------- benchmark: 2 tests -----------------------------------------------------------------------------
Name (time in us)                       Min                 Max                Mean             StdDev              Median                IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_deserialization_benchmark     110.3460 (1.0)      263.2940 (1.0)      120.8443 (1.0)      12.3452 (1.0)      118.4470 (1.0)       6.0770 (1.0)       386;464        8.2751 (1.0)        6829           1
test_serialization_benchmark       251.4210 (2.28)     522.7470 (1.99)     270.2584 (2.24)     16.9108 (1.37)     266.3670 (2.25)     12.2920 (2.02)      218;161        3.7002 (0.45)       2499           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

## 🎯 Why JsonPort?

### vs Standard `json` Module
- **Type Safety**: Automatic type conversion and validation
- **Complex Objects**: Native support for dataclasses, enums, datetime
- **Performance**: Intelligent caching for repeated operations
- **Error Handling**: Detailed error messages and validation

### vs Other Libraries
- **Zero Dependencies**: Pure Python, no external libraries
- **Type Hints**: Full support for modern Python type hints
- **Performance**: Optimized for speed with intelligent caching
- **Simplicity**: Simple API, powerful features

## 📚 Documentation Sections

### User Guide
- [Quick Start](user-guide/quick-start.md) - Get up and running in minutes
- [Installation](user-guide/installation.md) - Installation instructions
- [Basic Usage](user-guide/basic-usage.md) - Core functionality
- [Advanced Usage](user-guide/advanced-usage.md) - Advanced features
- [File Operations](user-guide/file-operations.md) - Working with files
- [Error Handling](user-guide/error-handling.md) - Error handling patterns
- [Performance](user-guide/performance.md) - Performance optimization
- [Best Practices](user-guide/best-practices.md) - Recommended patterns

### Examples
- [Dataclasses](examples/dataclasses.md) - Working with dataclasses
- [Enums](examples/enums.md) - Enum serialization
- [Collections](examples/collections.md) - Lists, sets, tuples, dicts
- [DateTime](examples/datetime.md) - Date and time handling
- [Complex Structures](examples/complex-structures.md) - Nested objects
- [Custom Types](examples/custom-types.md) - Custom type handling

### API Reference
- [Core Functions](api/core.md) - Main API functions
- [Types](api/types.md) - Supported types
- [Exceptions](api/exceptions.md) - Error types

### Development
- [Contributing](development/contributing.md) - How to contribute
- [Testing](development/testing.md) - Running tests
- [Benchmarking](development/benchmarking.md) - Performance testing

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](development/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Luan1Schons/JsonPort/blob/main/LICENSE) file for details.

---

**JsonPort** - Making JSON serialization simple, fast, and type-safe! 🚀 