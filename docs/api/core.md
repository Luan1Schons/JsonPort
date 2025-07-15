# Core Functions

The core functions of JsonPort provide the main serialization and deserialization capabilities.

## dump

Serialize a Python object to a JSON-serializable format.

```python
def dump(obj: Any) -> Any
```

**Parameters:**
- `obj`: The object to serialize

**Returns:**
- JSON-serializable data (dict, list, str, int, float, bool, None)

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

## load

Deserialize JSON data back to a Python object of the specified type.

```python
def load(data: Any, target_class: Type[T]) -> T
```

**Parameters:**
- `data`: The data to deserialize
- `target_class`: The target class type

**Returns:**
- Instance of the target class

**Example:**
```python
from jsonport import load

data = {"name": "John", "age": 30}
user = load(data, User)
# Returns: User(name="John", age=30)
```

## dump_file

Serialize an object and save it to a file.

```python
def dump_file(obj: Any, path: str, overwrite: bool = True) -> None
```

**Parameters:**
- `obj`: The object to serialize
- `path`: File path to save to
- `overwrite`: Whether to overwrite existing files (default: True)

**Example:**
```python
from jsonport import dump_file

user = User("John", 30)
dump_file(user, "user.json")
# Saves user data to user.json
```

## load_file

Load and deserialize data from a file.

```python
def load_file(path: str, target_class: Type[T]) -> T
```

**Parameters:**
- `path`: File path to load from
- `target_class`: The target class type

**Returns:**
- Instance of the target class

**Example:**
```python
from jsonport import load_file

user = load_file("user.json", User)
# Loads and deserializes user from user.json
```

## Supported Types

JsonPort supports serialization and deserialization of:

- **Primitive types**: `str`, `int`, `float`, `bool`, `None`
- **Datetime objects**: `datetime.datetime`, `datetime.date`, `datetime.time`
- **Collections**: `list`, `tuple`, `set`, `dict`
- **Custom types**: `dataclass`, `Enum`
- **Optional types**: `Optional[T]`, `Union[T, None]`

## Performance Notes

- JsonPort uses intelligent caching for type hints and optional type resolution
- Repeated operations with the same types are significantly faster
- File operations with `.gz` extension automatically use gzip compression 