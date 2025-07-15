# Collections

JsonPort provides comprehensive support for Python collections including lists, tuples, sets, and dictionaries with full type preservation and nested structure handling.

## Lists

### Basic Lists

```python
from dataclasses import dataclass
from typing import List
from jsonport import dump, load

@dataclass
class User:
    name: str
    tags: List[str]

# Create user with list
user = User("John Doe", ["developer", "python", "json"])

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "tags": ["developer", "python", "json"]
# }

# Deserialize
restored_user = load(data, User)
print(restored_user.tags)  # ["developer", "python", "json"]
```

### Lists of Complex Objects

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Comment:
    text: str
    author: str
    created_at: datetime

@dataclass
class Post:
    title: str
    content: str
    comments: List[Comment]

# Create post with comments
post = Post(
    title="JsonPort Tutorial",
    content="Learn how to use JsonPort...",
    comments=[
        Comment("Great tutorial!", "Alice", datetime.now()),
        Comment("Very helpful", "Bob", datetime.now())
    ]
)

# Serialize
data = dump(post)
print(data)
# Output:
# {
#   "title": "JsonPort Tutorial",
#   "content": "Learn how to use JsonPort...",
#   "comments": [
#     {
#       "text": "Great tutorial!",
#       "author": "Alice",
#       "created_at": "2025-01-14T10:30:00"
#     },
#     {
#       "text": "Very helpful",
#       "author": "Bob",
#       "created_at": "2025-01-14T10:31:00"
#     }
#   ]
# }

# Deserialize
restored_post = load(data, Post)
print(len(restored_post.comments))  # 2
print(restored_post.comments[0].author)  # "Alice"
```

### Nested Lists

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Matrix:
    data: List[List[int]]

# Create matrix
matrix = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Serialize
data = dump(matrix)
print(data)
# Output:
# {
#   "data": [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
#   ]
# }

# Deserialize
restored_matrix = load(data, Matrix)
print(restored_matrix.data[1][1])  # 5
```

## Tuples

### Basic Tuples

```python
from dataclasses import dataclass
from typing import Tuple
from jsonport import dump, load

@dataclass
class Point:
    coordinates: Tuple[int, int]
    color: str

# Create point
point = Point((10, 20), "red")

# Serialize
data = dump(point)
print(data)
# Output:
# {
#   "coordinates": [10, 20],
#   "color": "red"
# }

# Deserialize
restored_point = load(data, Point)
print(restored_point.coordinates)  # (10, 20)
```

### Tuples with Different Types

```python
from dataclasses import dataclass
from typing import Tuple
from datetime import datetime

@dataclass
class UserInfo:
    details: Tuple[str, int, datetime]
    metadata: Tuple[str, bool]

# Create user info
user_info = UserInfo(
    ("John Doe", 30, datetime.now()),
    ("active", True)
)

# Serialize
data = dump(user_info)
print(data)
# Output:
# {
#   "details": ["John Doe", 30, "2025-01-14T10:30:00"],
#   "metadata": ["active", true]
# }

# Deserialize
restored_info = load(data, UserInfo)
print(restored_info.details[0])  # "John Doe"
print(restored_info.details[1])  # 30
```

## Sets

### Basic Sets

```python
from dataclasses import dataclass
from typing import Set
from jsonport import dump, load

@dataclass
class User:
    name: str
    permissions: Set[str]

# Create user with permissions
user = User("Admin", {"read", "write", "delete", "admin"})

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "name": "Admin",
#   "permissions": ["admin", "delete", "read", "write"]
# }

# Deserialize
restored_user = load(data, User)
print(restored_user.permissions)  # {"admin", "delete", "read", "write"}
print("read" in restored_user.permissions)  # True
```

### Sets of Complex Objects

```python
from dataclasses import dataclass
from typing import Set
from enum import Enum

class Tag(Enum):
    PYTHON = "python"
    JSON = "json"
    API = "api"

@dataclass
class Article:
    title: str
    tags: Set[Tag]

# Create article
article = Article("JsonPort Guide", {Tag.PYTHON, Tag.JSON, Tag.API})

# Serialize
data = dump(article)
print(data)
# Output:
# {
#   "title": "JsonPort Guide",
#   "tags": ["api", "json", "python"]
# }

# Deserialize
restored_article = load(data, Article)
print(restored_article.tags)  # {Tag.API, Tag.JSON, Tag.PYTHON}
```

## Dictionaries

### Basic Dictionaries

```python
from dataclasses import dataclass
from typing import Dict
from jsonport import dump, load

@dataclass
class Configuration:
    settings: Dict[str, str]
    metadata: Dict[str, int]

# Create configuration
config = Configuration(
    settings={"host": "localhost", "port": "8080"},
    metadata={"version": 1, "max_connections": 100}
)

# Serialize
data = dump(config)
print(data)
# Output:
# {
#   "settings": {
#     "host": "localhost",
#     "port": "8080"
#   },
#   "metadata": {
#     "version": 1,
#     "max_connections": 100
#   }
# }

# Deserialize
restored_config = load(data, Configuration)
print(restored_config.settings["host"])  # "localhost"
print(restored_config.metadata["max_connections"])  # 100
```

### Dictionaries with Complex Values

```python
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class UserProfile:
    name: str
    preferences: Dict[str, List[str]]
    timestamps: Dict[str, datetime]

# Create user profile
profile = UserProfile(
    name="John Doe",
    preferences={
        "languages": ["Python", "JavaScript"],
        "frameworks": ["Django", "React"]
    },
    timestamps={
        "created": datetime.now(),
        "last_login": datetime.now()
    }
)

# Serialize
data = dump(profile)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "preferences": {
#     "languages": ["Python", "JavaScript"],
#     "frameworks": ["Django", "React"]
#   },
#   "timestamps": {
#     "created": "2025-01-14T10:30:00",
#     "last_login": "2025-01-14T10:30:00"
#   }
# }

# Deserialize
restored_profile = load(data, UserProfile)
print(restored_profile.preferences["languages"])  # ["Python", "JavaScript"]
```

### Dictionaries with Enum Keys

```python
from dataclasses import dataclass
from typing import Dict
from enum import Enum

class ConfigKey(Enum):
    HOST = "host"
    PORT = "port"
    DEBUG = "debug"

@dataclass
class AppConfig:
    config: Dict[ConfigKey, str]

# Create config
app_config = AppConfig({
    ConfigKey.HOST: "localhost",
    ConfigKey.PORT: "8080",
    ConfigKey.DEBUG: "true"
})

# Serialize
data = dump(app_config)
print(data)
# Output:
# {
#   "config": {
#     "host": "localhost",
#     "port": "8080",
#     "debug": "true"
#   }
# }

# Deserialize
restored_config = load(data, AppConfig)
print(restored_config.config[ConfigKey.HOST])  # "localhost"
```

## Complex Nested Collections

### Mixed Collection Types

```python
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from datetime import datetime

@dataclass
class ComplexData:
    users: List[Dict[str, str]]
    tags: Set[str]
    coordinates: Tuple[float, float]
    metadata: Dict[str, List[int]]

# Create complex data
complex_data = ComplexData(
    users=[
        {"name": "Alice", "role": "admin"},
        {"name": "Bob", "role": "user"}
    ],
    tags={"python", "json", "serialization"},
    coordinates=(10.5, 20.3),
    metadata={
        "scores": [95, 87, 92],
        "counts": [1, 2, 3, 4, 5]
    }
)

# Serialize
data = dump(complex_data)
print(data)
# Output:
# {
#   "users": [
#     {"name": "Alice", "role": "admin"},
#     {"name": "Bob", "role": "user"}
#   ],
#   "tags": ["json", "python", "serialization"],
#   "coordinates": [10.5, 20.3],
#   "metadata": {
#     "scores": [95, 87, 92],
#     "counts": [1, 2, 3, 4, 5]
#   }
# }

# Deserialize
restored_data = load(data, ComplexData)
print(len(restored_data.users))  # 2
print("python" in restored_data.tags)  # True
print(restored_data.coordinates[0])  # 10.5
```

### Deeply Nested Structures

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Node:
    value: str
    children: List['Node']
    metadata: Optional[Dict[str, str]] = None

@dataclass
class Tree:
    root: Node
    node_count: int

# Create tree structure
tree = Tree(
    root=Node(
        value="root",
        children=[
            Node(
                value="child1",
                children=[
                    Node("grandchild1", []),
                    Node("grandchild2", [])
                ],
                metadata={"type": "branch"}
            ),
            Node(
                value="child2",
                children=[],
                metadata={"type": "leaf"}
            )
        ],
        metadata={"type": "root"}
    ),
    node_count=5
)

# Serialize
data = dump(tree)
print(data)
# Output:
# {
#   "root": {
#     "value": "root",
#     "children": [
#       {
#         "value": "child1",
#         "children": [
#           {"value": "grandchild1", "children": [], "metadata": null},
#           {"value": "grandchild2", "children": [], "metadata": null}
#         ],
#         "metadata": {"type": "branch"}
#       },
#       {
#         "value": "child2",
#         "children": [],
#         "metadata": {"type": "leaf"}
#       }
#     ],
#     "metadata": {"type": "root"}
#   },
#   "node_count": 5
# }

# Deserialize
restored_tree = load(data, Tree)
print(restored_tree.root.value)  # "root"
print(len(restored_tree.root.children))  # 2
```

## Collection Operations

### List Operations

```python
from dataclasses import dataclass
from typing import List
from jsonport import dump, load

@dataclass
class ShoppingList:
    items: List[str]
    quantities: List[int]

# Create shopping list
shopping = ShoppingList(
    items=["apples", "bananas", "milk"],
    quantities=[5, 3, 2]
)

# Serialize
data = dump(shopping)

# Deserialize and perform operations
restored_shopping = load(data, ShoppingList)

# List operations work normally
print(len(restored_shopping.items))  # 3
print(restored_shopping.items[0])  # "apples"
restored_shopping.items.append("bread")
restored_shopping.quantities.append(1)

# Re-serialize
updated_data = dump(restored_shopping)
```

### Set Operations

```python
from dataclasses import dataclass
from typing import Set
from jsonport import dump, load

@dataclass
class UserGroups:
    user_id: str
    groups: Set[str]

# Create user groups
user_groups = UserGroups("user123", {"admin", "developers", "testers"})

# Serialize
data = dump(user_groups)

# Deserialize and perform set operations
restored_groups = load(data, UserGroups)

# Set operations work normally
print("admin" in restored_groups.groups)  # True
restored_groups.groups.add("moderators")
restored_groups.groups.remove("testers")

# Re-serialize
updated_data = dump(restored_groups)
```

### Dictionary Operations

```python
from dataclasses import dataclass
from typing import Dict
from jsonport import dump, load

@dataclass
class Cache:
    data: Dict[str, str]
    max_size: int

# Create cache
cache = Cache({"key1": "value1", "key2": "value2"}, 100)

# Serialize
data = dump(cache)

# Deserialize and perform dict operations
restored_cache = load(data, Cache)

# Dictionary operations work normally
print(restored_cache.data["key1"])  # "value1"
restored_cache.data["key3"] = "value3"
del restored_cache.data["key2"]

# Re-serialize
updated_data = dump(restored_cache)
```

## Performance Considerations

### Large Collections

```python
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class LargeDataset:
    items: List[Dict[str, str]]
    metadata: Dict[str, int]

# Create large dataset
large_data = LargeDataset(
    items=[{"id": f"item_{i}", "value": f"value_{i}"} for i in range(10000)],
    metadata={f"key_{i}": i for i in range(1000)}
)

# Measure serialization time
start_time = time.time()
data = dump(large_data)
serialization_time = time.time() - start_time

# Measure deserialization time
start_time = time.time()
restored_data = load(data, LargeDataset)
deserialization_time = time.time() - start_time

print(f"Serialization time: {serialization_time:.3f}s")
print(f"Deserialization time: {deserialization_time:.3f}s")
print(f"Items count: {len(restored_data.items)}")
```

### Memory Usage

```python
import sys
from dataclasses import dataclass
from typing import List

@dataclass
class MemoryTest:
    data: List[str]

# Test memory usage
original_data = MemoryTest(["item"] * 10000)
print(f"Original size: {sys.getsizeof(original_data)} bytes")

serialized = dump(original_data)
print(f"Serialized size: {sys.getsizeof(serialized)} bytes")

restored = load(serialized, MemoryTest)
print(f"Restored size: {sys.getsizeof(restored)} bytes")
```

This comprehensive guide demonstrates how to effectively use Python collections with JsonPort, including complex nested structures, operations, and performance considerations. 