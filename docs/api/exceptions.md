# Exceptions

JsonPort 2.0 provides a rich, informative exception hierarchy designed to pinpoint errors with exact property paths, target types, and offending values.

---

## Exception Hierarchy

```text
JsonPortError (Base Exception)
├── SerializationError
├── DeserializationError
└── ConfigurationError
```

---

## Base Exception

### `JsonPortError`

The root exception class for all errors originating within JsonPort.

```python
from jsonport import JsonPortError

class JsonPortError(Exception):
    message: str
```

---

## Serialization Errors

### `SerializationError`

Raised when an object or field cannot be converted into a JSON-compatible format.

```python
from jsonport import SerializationError

class SerializationError(JsonPortError):
    object_type: Optional[Type[Any]]
    field: Optional[str]
    path: str
```

**Attributes:**
- `message` *(str)*: Descriptive error explanation.
- `object_type` *(type or None)*: The Python class/type that failed serialization.
- `field` *(str or None)*: The attribute/field name where serialization failed.
- `path` *(str)*: Dot-separated navigation path in the object graph (e.g. `order.items[0].sku`).

**String Representation:**
Includes contextual details whenever available:
```text
Type UUID is not serializable by JsonPort (path: 'user.id', field: 'id', type: UUID)
```

**Example:**
```python
from jsonport import dump, SerializationError

try:
    data = dump(unsupported_object)
except SerializationError as err:
    print(f"Failed at path: {err.path}")
    print(f"Object type: {err.object_type}")
    print(f"Field: {err.field}")
```

---

## Deserialization Errors

### `DeserializationError`

Raised when input JSON data cannot be deserialized into the requested target type or dataclass schema.

```python
from jsonport import DeserializationError

class DeserializationError(JsonPortError):
    target_type: Optional[Type[Any]]
    field: Optional[str]
    path: str
    value: Any
```

**Attributes:**
- `message` *(str)*: Descriptive explanation of the deserialization failure.
- `target_type` *(type or None)*: The expected target type (`int`, `UUID`, dataclass, etc.).
- `field` *(str or None)*: The field name that failed validation or conversion.
- `path` *(str)*: Hierarchical path where the failure occurred (e.g. `payload.user.address.postal_code`).
- `value` *(Any)*: The raw value that caused the conversion failure.

**String Representation:**
```text
Cannot convert 'abc' to int: invalid literal for int() with base 10: 'abc' (path: 'user.age', field: 'age', target_type: int)
```

---

## Configuration Errors

### `ConfigurationError`

Raised when custom serializers, deserializers, or registry configuration encounters an invalid state or definition.

```python
from jsonport import ConfigurationError
```

---

## Strict Mode Violations

When `strict=True` is passed to `load()`, `loads()`, or `load_stream()`, extra fields not present in dataclass definitions (or not mapped by `alias`) raise a `DeserializationError`:

```python
from jsonport import loads, DeserializationError

raw = '{"name": "Alice", "unknown_key": 42}'
try:
    user = loads(raw, User, strict=True)
except DeserializationError as err:
    print(err)
    # Output: Extra keys not permitted in strict mode for User: ['unknown_key']
```