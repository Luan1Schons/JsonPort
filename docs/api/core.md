# Core Functions & APIs

The core functions of JsonPort 2.0 provide high-performance serialization, deserialization, streaming, and custom type registry capabilities.

---

## Direct Object & Primitive Conversion

### `dump`

Serialize a Python object to JSON-compatible data structures (dictionaries, lists, primitives).

```python
def dump(obj: Any, **kwargs: Any) -> Any
```

**Parameters:**
- `obj`: The Python object to serialize (dataclass, enum, datetime, collection, or extended type).
- `**kwargs`: Optional parameters passed to serializer (e.g. `registry`).

**Returns:**
- JSON-serializable structure (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`).

**Example:**
```python
from dataclasses import dataclass
from jsonport import dump

@dataclass
class User:
    name: str
    age: int

user = User("John", 30)
data = dump(user)
# Returns: {"name": "John", "age": 30}
```

---

### `load`

Deserialize a JSON data structure back into a Python object of `target_class`.

```python
def load(data: Any, target_class: Type[T], **kwargs: Any) -> T
```

**Parameters:**
- `data`: The JSON data structure to deserialize (`dict`, `list`, primitive).
- `target_class`: The target type or class (`Type[T]`, `NamedTuple`, `TypedDict`, `Union`, `Literal`, etc.).
- `strict` *(bool, optional)*: When `True`, raises `DeserializationError` if unexpected extra fields are present.
- `**kwargs`: Optional parameters passed to deserializer (e.g. `registry`).

**Returns:**
- An instance of `target_class`.

**Example:**
```python
from jsonport import load

data = {"name": "John", "age": 30}
user = load(data, User)
# Returns: User(name="John", age=30)
```

---

## String Operations (JSON Text)

### `dumps`

Serialize a Python object directly to a JSON string.

```python
def dumps(
    obj: Any,
    *,
    indent: Optional[int] = None,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> str
```

**Parameters:**
- `obj`: Object to serialize.
- `indent` *(int, optional)*: Number of spaces for pretty indentation (default: `None` for compact representation).
- `ensure_ascii` *(bool, optional)*: Escape non-ASCII characters (default: `False`).
- `**kwargs`: Additional arguments passed to serializer.

**Returns:**
- JSON-formatted string (`str`).

**Example:**
```python
from jsonport import dumps

json_str = dumps(user, indent=2)
```

---

### `loads`

Deserialize a JSON string directly to an instance of `target_class`.

```python
def loads(
    s: Union[str, bytes],
    target_class: Type[T],
    **kwargs: Any,
) -> T
```

**Parameters:**
- `s`: JSON string (`str` or `bytes`).
- `target_class`: Target type for deserialization.
- `strict` *(bool, optional)*: Reject unexpected fields if `True`.
- `**kwargs`: Additional deserialization options.

**Returns:**
- Deserialized instance of `target_class`.

**Example:**
```python
from jsonport import loads

user = loads('{"name": "John", "age": 30}', User)
```

---

## Stream Operations

### `dump_stream`

Serialize a Python object and write it directly to a text stream (`io.StringIO`, file handle, socket stream).

```python
def dump_stream(
    obj: Any,
    stream: TextIO,
    *,
    indent: Optional[int] = None,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> None
```

**Example:**
```python
import io
from jsonport import dump_stream

stream = io.StringIO()
dump_stream(user, stream, indent=2)
content = stream.getvalue()
```

---

### `load_stream`

Read and deserialize JSON from a text stream directly to `target_class`.

```python
def load_stream(
    stream: TextIO,
    target_class: Type[T],
    **kwargs: Any,
) -> T
```

**Example:**
```python
stream.seek(0)
restored = load_stream(stream, User)
```

---

## File Operations

### `dump_file`

Serialize an object and write it to a file. Supports automatic gzip compression when the file path ends with `.gz`.

```python
def dump_file(
    obj: Any,
    path: Union[str, os.PathLike[str]],
    overwrite: bool = True,
    *,
    indent: Optional[int] = None,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> None
```

---

### `load_file`

Load and deserialize a JSON or gzipped JSON file into `target_class`. Automatically detects `.gz` extension and decompresses transparently.

```python
def load_file(
    path: Union[str, os.PathLike[str]],
    target_class: Type[T],
    **kwargs: Any,
) -> T
```

---

## Introspection & Utilities

### `is_serializable`

Check whether an object can be serialized by JsonPort without raising an exception.

```python
def is_serializable(obj: Any) -> bool
```

---

## Custom Registry

JsonPort provides a global registry and isolated `Registry` instances for custom type handlers.

### Decorator APIs

```python
from jsonport import serializer, deserializer

@serializer(CustomType)
def serialize_custom(obj: CustomType) -> str:
    return str(obj)

@deserializer(CustomType)
def deserialize_custom(val: str) -> CustomType:
    return CustomType.from_str(val)
```

### Functional Registration APIs

```python
from jsonport import register_serializer, register_deserializer

register_serializer(CustomType, serialize_custom)
register_deserializer(CustomType, deserialize_custom)
```

### Registry Management

- `get_serializer(obj_or_type)`: Look up custom serializer function.
- `get_deserializer(target_type)`: Look up custom deserializer function.
- `clear_registry()`: Clear all registered serializers and deserializers from the global registry.
- `Registry()`: Instantiate an isolated registry for modular or thread-local contexts.
- `get_default_registry()`: Retrieve the default global registry.