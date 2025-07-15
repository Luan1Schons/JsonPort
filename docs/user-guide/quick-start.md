# Quick Start

Get up and running with JsonPort in minutes! This guide will show you the basics of serializing and deserializing Python objects.

## Installation

Install JsonPort using pip:

```bash
pip install jsonport
```

## Basic Example

Here's a simple example to get you started:

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

## File Operations

Save and load objects directly to/from files:

```python
from jsonport import dump_file, load_file

# Save to JSON file
dump_file(user, "user.json")

# Load from JSON file
loaded_user = load_file("user.json", User)

# Save with compression
dump_file(user, "user.json.gz")

# Load compressed file
compressed_user = load_file("user.json.gz", User)
```

## Next Steps

- [Basic Usage](basic-usage.md) - Learn core functionality
- [Examples](examples/) - See more examples
- [API Reference](api/) - Complete API documentation 