# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.2] - 2025-07-15

### Added
- Support to python 3.7 (EOL)
- Bug fixes

## [1.0.1] - 2025-07-15

### Added
- Pre-commit hooks for code quality
- GitHub Actions for CI/CD
- Comprehensive test suite with pytest
- Performance benchmarks with pytest-benchmark
- Code coverage reporting
- Type checking with mypy
- Code formatting with black
- Linting with flake8

## [1.0.0] - 2025-07-14

### Added
- Initial release of JsonPort
- High-performance serialization/deserialization of Python objects
- Support for dataclasses with type hints
- Automatic datetime handling (datetime, date, time)
- Enum serialization support
- Collection type preservation (list, tuple, set, dict)
- File I/O operations with gzip compression support
- Comprehensive error handling with JsonPortError
- Caching optimizations for type hints and optional types
- Custom JSON encoder (JsonPortEncoder)
- Optional type support (Optional[T], Union[T, None])

### Features
- `dump()`: Serialize objects to JSON-serializable format
- `load()`: Deserialize JSON data to Python objects
- `dump_file()`: Save objects to JSON files with compression support
- `load_file()`: Load objects from JSON files with automatic decompression
- `is_serializable()`: Check if objects can be serialized
- Type-safe operations with full type hints support

### Performance
- Caching of type hints (max 1024 entries)
- Caching of optional type resolution (max 512 entries)
- Optimized serialization/deserialization algorithms
- Efficient handling of nested structures

[Unreleased]: https://github.com/Luan1Schons/JsonPort/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/Luan1Schons/JsonPort/releases/tag/v1.0.1
[1.0.0]: https://github.com/Luan1Schons/JsonPort/releases/tag/v1.0.0 