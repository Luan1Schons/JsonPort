# Basic Usage

Learn the fundamental functions and patterns for using JsonPort effectively.

## Core Functions

JsonPort provides four main functions for serialization and deserialization:

### `dump()` - Serialize Objects

Convert Python objects to JSON-serializable data:

```python
from jsonport import dump
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

user = User("John", 30)
data = dump(user)
print(data)
# Output: {"name": "John", "age": 30}
```

### `load()` - Deserialize Objects

Convert JSON data back to Python objects:

```python
from jsonport import load

data = {"name": "John", "age": 30}
user = load(data, User)
print(user.name)  # "John"
print(user.age)   # 30
```

### `dump_file()` - Save to File

Serialize and save objects directly to files:

```python
from jsonport import dump_file

user = User("John", 30)
dump_file(user, "user.json")
# Creates user.json with the serialized data
```

### `load_file()` - Load from File

Load and deserialize objects from files:

```python
from jsonport import load_file

user = load_file("user.json", User)
print(user.name)  # "John"
```

## Supported Types

### Primitive Types
```python
# All basic Python types work automatically
data = dump({
    "string": "hello",
    "integer": 42,
    "float": 3.14,
    "boolean": True,
    "none": None
})
```

### Dataclasses
```python
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
    in_stock: bool

product = Product(1, "Laptop", 999.99, True)
data = dump(product)
# Output: {"id": 1, "name": "Laptop", "price": 999.99, "in_stock": true}
```

### Enums
```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Task:
    title: str
    status: Status

task = Task("Complete docs", Status.PENDING)
data = dump(task)
# Output: {"title": "Complete docs", "status": "pending"}
```

### DateTime Objects
```python
from datetime import datetime, date, time

@dataclass
class Event:
    name: str
    date: date
    time: time
    created_at: datetime

event = Event(
    "Meeting",
    date(2024, 1, 15),
    time(14, 30),
    datetime.now()
)

data = dump(event)
# Output: {
#   "name": "Meeting",
#   "date": "2024-01-15",
#   "time": "14:30:00",
#   "created_at": "2024-01-15T14:30:00"
# }
```

### Collections
```python
@dataclass
class ShoppingCart:
    items: list[str]
    quantities: dict[str, int]
    tags: set[str]

cart = ShoppingCart(
    items=["apple", "banana"],
    quantities={"apple": 3, "banana": 2},
    tags={"fruits", "organic"}
)

data = dump(cart)
# Output: {
#   "items": ["apple", "banana"],
#   "quantities": {"apple": 3, "banana": 2},
#   "tags": ["fruits", "organic"]
# }
```

## Type Safety

JsonPort provides automatic type validation:

```python
# This will work
data = {"name": "John", "age": 30}
user = load(data, User)

# This will raise JsonPortError
try:
    data = {"name": "John", "age": "thirty"}  # age should be int
    user = load(data, User)
except JsonPortError as e:
    print(f"Type error: {e}")
```

## Error Handling

Always handle potential errors in production code:

```python
from jsonport import JsonPortError

try:
    data = dump(complex_object)
except JsonPortError as e:
    print(f"Serialization failed: {e}")

try:
    user = load_file("user.json", User)
except FileNotFoundError:
    print("File not found")
except JsonPortError as e:
    print(f"Deserialization failed: {e}")
```

## Performance Tips

1. **Reuse types**: JsonPort caches type information for better performance
2. **Use type hints**: Always define proper type hints for optimal performance
3. **Batch operations**: Process multiple objects together when possible

```python
# Good - types are cached
users = [User("John", 30), User("Jane", 25)]
for user in users:
    data = dump(user)  # Fast after first call

# Better - batch processing
data_list = [dump(user) for user in users]
```

## Next Steps

- [Advanced Usage](advanced-usage.md) - Explore advanced features
- [Examples](examples/) - Practical examples
- [API Reference](api/) - Complete API documentation 