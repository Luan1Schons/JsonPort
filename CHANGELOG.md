# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-09-30

### Summary
JsonPort 2.0 is a major evolutionary release introducing a completely modular architecture, extended standard library type support, stream/string operations, custom registry hooks, field metadata controls, and rich error diagnostics.

### Breaking Changes
- **None**: 100% backward compatible with JsonPort 1.x APIs (`dump`, `load`, `dump_file`, `load_file`, `is_serializable`).

### Added
- **String & Stream APIs**:
  - `dumps()`: Direct serialization of complex objects to JSON strings.
  - `loads()`: Direct deserialization from JSON strings to typed objects.
  - `dump_stream()` & `load_stream()`: Streaming serialization/deserialization with `io.StringIO`, file handles, and network streams.
- **Extended Standard Library Types**:
  - `uuid.UUID`: Serialized to string and restored to `UUID` instances.
  - `decimal.Decimal`: Exact decimal precision preserved across serialization.
  - `pathlib.Path` & `pathlib.PurePath`: Filesystem path support.
  - `bytes` & `bytearray`: Standard Base64 encoded string format.
  - `ipaddress.IPv4Address`, `IPv6Address`, `IPv4Network`, `IPv6Network`: Full IP networking support.
  - `datetime.timedelta`: Total seconds representation.
  - `re.Pattern`: Regular expression pattern string serialization and compilation.
- **Modern Python Typing Support**:
  - `typing.Literal`: Validated literal value deserialization.
  - `typing.Union`: Intelligent candidate scoring and dataclass matching.
  - `typing.NamedTuple`: Both dict and sequence deserialization with field defaults.
  - `typing.TypedDict`: Dict-based typed dictionary support with hint validation.
- **Dataclass Field Metadata**:
  - `alias`: Customize external JSON field names while keeping Pythonic attribute names.
  - `exclude`: Exclude sensitive or internal fields from serialization.
  - `serializer`: Per-field custom serializer function.
  - `deserializer`: Per-field custom deserializer function.
- **Extensible Registry**:
  - `@serializer` and `@deserializer` decorators for global type registration.
  - `register_serializer()` and `register_deserializer()` functional APIs supporting classes and predicate functions.
  - `Registry`: Isolated custom registry contexts for multi-tenant or modular applications.
- **Strict Mode & Rich Diagnostics**:
  - `strict=True` option in `load()`, `loads()`, and `load_stream()` to reject unexpected fields.
  - Detailed error paths (e.g. `user.address.zip_code`), object/target types, and offending values on `SerializationError` and `DeserializationError`.
  - `ConfigurationError` for registry issues.
- **PEP 561 Compliance**:
  - Added `py.typed` marker for complete static type checker interoperability.

### Changed
- Minimum Python requirement updated to `>= 3.9` (supporting Python 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14).
- Modernized type hints and modular internal architecture (`inspection`, `serializers`, `deserializers`, `registry`, `file_io`).

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