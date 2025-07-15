# Enums

JsonPort provides seamless serialization and deserialization of Python enums with automatic value conversion and type safety.

## Basic Enum Usage

### Simple Enum

```python
from enum import Enum
from dataclasses import dataclass
from jsonport import dump, load

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

@dataclass
class User:
    name: str
    role: UserRole

# Create user with enum
user = User("John Doe", UserRole.ADMIN)

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "role": "admin"
# }

# Deserialize
restored_user = load(data, User)
print(restored_user.role)  # UserRole.ADMIN
print(restored_user.role.value)  # "admin"
```

### Enum with Integer Values

```python
from enum import IntEnum
from dataclasses import dataclass

class StatusCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

@dataclass
class APIResponse:
    status: StatusCode
    message: str

# Create response
response = APIResponse(StatusCode.OK, "Success")

# Serialize
data = dump(response)
print(data)
# Output:
# {
#   "status": 200,
#   "message": "Success"
# }

# Deserialize
restored_response = load(data, APIResponse)
print(restored_response.status)  # StatusCode.OK
print(restored_response.status.value)  # 200
```

## Advanced Enum Patterns

### Enum with Custom Values

```python
from enum import Enum
from dataclasses import dataclass

class Color(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    BLACK = "#000000"
    WHITE = "#FFFFFF"

@dataclass
class Theme:
    primary_color: Color
    secondary_color: Color
    background_color: Color

# Create theme
theme = Theme(Color.BLUE, Color.WHITE, Color.BLACK)

# Serialize
data = dump(theme)
print(data)
# Output:
# {
#   "primary_color": "#0000FF",
#   "secondary_color": "#FFFFFF",
#   "background_color": "#000000"
# }

# Deserialize
restored_theme = load(data, Theme)
print(restored_theme.primary_color)  # Color.BLUE
```

### Enum with Methods

```python
from enum import Enum
from dataclasses import dataclass

class FileType(Enum):
    TEXT = "txt"
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    
    def get_mime_type(self):
        mime_types = {
            FileType.TEXT: "text/plain",
            FileType.JSON: "application/json",
            FileType.CSV: "text/csv",
            FileType.XML: "application/xml"
        }
        return mime_types[self]
    
    def is_text_based(self):
        return self in [FileType.TEXT, FileType.JSON, FileType.CSV, FileType.XML]

@dataclass
class FileInfo:
    name: str
    file_type: FileType
    size: int

# Create file info
file_info = FileInfo("data.json", FileType.JSON, 1024)

# Serialize
data = dump(file_info)
print(data)
# Output:
# {
#   "name": "data.json",
#   "file_type": "json",
#   "size": 1024
# }

# Deserialize
restored_file = load(data, FileInfo)
print(restored_file.file_type.get_mime_type())  # "application/json"
print(restored_file.file_type.is_text_based())  # True
```

## Enum Collections

### Lists of Enums

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

@dataclass
class User:
    name: str
    permissions: List[Permission]

# Create user with multiple permissions
user = User("Admin User", [Permission.READ, Permission.WRITE, Permission.ADMIN])

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "name": "Admin User",
#   "permissions": ["read", "write", "admin"]
# }

# Deserialize
restored_user = load(data, User)
print(restored_user.permissions)  # [Permission.READ, Permission.WRITE, Permission.ADMIN]
```

### Sets of Enums

```python
from enum import Enum
from dataclasses import dataclass
from typing import Set

class Tag(Enum):
    PYTHON = "python"
    JSON = "json"
    API = "api"
    DATABASE = "database"
    TESTING = "testing"

@dataclass
class Article:
    title: str
    tags: Set[Tag]

# Create article with tags
article = Article("JsonPort Tutorial", {Tag.PYTHON, Tag.JSON, Tag.API})

# Serialize
data = dump(article)
print(data)
# Output:
# {
#   "title": "JsonPort Tutorial",
#   "tags": ["python", "json", "api"]
# }

# Deserialize
restored_article = load(data, Article)
print(restored_article.tags)  # {Tag.PYTHON, Tag.JSON, Tag.API}
```

### Dictionaries with Enum Keys

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict

class ConfigKey(Enum):
    HOST = "host"
    PORT = "port"
    TIMEOUT = "timeout"
    DEBUG = "debug"

@dataclass
class Configuration:
    settings: Dict[ConfigKey, str]

# Create configuration
config = Configuration({
    ConfigKey.HOST: "localhost",
    ConfigKey.PORT: "8080",
    ConfigKey.TIMEOUT: "30",
    ConfigKey.DEBUG: "true"
})

# Serialize
data = dump(config)
print(data)
# Output:
# {
#   "settings": {
#     "host": "localhost",
#     "port": "8080",
#     "timeout": "30",
#     "debug": "true"
#   }
# }

# Deserialize
restored_config = load(data, Configuration)
print(restored_config.settings[ConfigKey.HOST])  # "localhost"
```

## Complex Enum Structures

### Nested Enums

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

@dataclass
class UserProfile:
    name: str
    status: UserStatus
    role: UserRole
    previous_role: Optional[UserRole] = None

# Create user profile
profile = UserProfile(
    name="Jane Doe",
    status=UserStatus.ACTIVE,
    role=UserRole.ADMIN,
    previous_role=UserRole.USER
)

# Serialize
data = dump(profile)
print(data)
# Output:
# {
#   "name": "Jane Doe",
#   "status": "active",
#   "role": "admin",
#   "previous_role": "user"
# }

# Deserialize
restored_profile = load(data, UserProfile)
print(restored_profile.status)  # UserStatus.ACTIVE
print(restored_profile.role)  # UserRole.ADMIN
```

### Enum with Optional Fields

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    title: str
    priority: Priority
    assigned_priority: Optional[Priority] = None

# Create tasks
task1 = Task("Fix bug", Priority.HIGH)
task2 = Task("Update docs", Priority.MEDIUM, Priority.LOW)

# Serialize
data1 = dump(task1)
data2 = dump(task2)
print(data1)
# Output:
# {
#   "title": "Fix bug",
#   "priority": "high",
#   "assigned_priority": null
# }

print(data2)
# Output:
# {
#   "title": "Update docs",
#   "priority": "medium",
#   "assigned_priority": "low"
# }

# Deserialize
restored_task1 = load(data1, Task)
restored_task2 = load(data2, Task)
```

## Error Handling with Enums

### Invalid Enum Values

```python
from enum import Enum
from jsonport import load, DeserializationError

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

@dataclass
class User:
    name: str
    role: UserRole

# This will raise DeserializationError
try:
    user = load({"name": "John", "role": "moderator"}, User)
except DeserializationError as e:
    print(f"Error: {e}")
    # Output: Error: Cannot deserialize 'moderator' to UserRole
```

### Handling Unknown Enum Values

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

@dataclass
class User:
    name: str
    role: UserRole
    fallback_role: Optional[UserRole] = None

def safe_load_user(data):
    try:
        return load(data, User)
    except DeserializationError as e:
        if "role" in str(e):
            # Try with fallback role
            data["role"] = "user"  # Default to user role
            return load(data, User)
        raise

# Test with invalid role
user_data = {"name": "John", "role": "unknown"}
user = safe_load_user(user_data)
print(user.role)  # UserRole.USER (fallback)
```

## Performance Considerations

### Enum Caching

JsonPort caches enum value mappings for better performance:

```python
from enum import Enum
from jsonport import dump, load
import time

class LargeEnum(Enum):
    # Many enum values...
    pass

# First serialization (slower due to cache population)
start_time = time.time()
data = dump(large_enum_object)
first_time = time.time() - start_time

# Subsequent serializations (faster due to caching)
start_time = time.time()
data = dump(large_enum_object)
second_time = time.time() - start_time

print(f"First serialization: {first_time:.4f}s")
print(f"Second serialization: {second_time:.4f}s")
```

### Enum Comparison

```python
from enum import Enum
from jsonport import dump, load

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

@dataclass
class Task:
    name: str
    status: Status

# Create and serialize
task = Task("Test task", Status.PENDING)
data = dump(task)

# Deserialize and compare
restored_task = load(data, Task)

# Enum comparison works correctly
print(restored_task.status == Status.PENDING)  # True
print(restored_task.status is Status.PENDING)  # True
print(restored_task.status.value == "pending")  # True
```

This comprehensive guide shows how to effectively use enums with JsonPort, including advanced patterns, error handling, and performance considerations. 