# Best Practices

This guide covers best practices for using JsonPort effectively in your applications, including design patterns, performance optimization, and common pitfalls to avoid.

## Data Structure Design

### 1. Use Dataclasses for Complex Objects

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# Good: Well-structured dataclass
@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime
    tags: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, str]] = None

# Avoid: Using plain dictionaries
user_dict = {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    # ... more fields
}
```

### 2. Define Clear Type Hints

```python
from typing import Union, Literal, NewType
from dataclasses import dataclass

# Good: Specific type hints
@dataclass
class Configuration:
    host: str
    port: int
    timeout: float
    mode: Literal["development", "production", "testing"]
    retries: Union[int, None] = None

# Use NewType for domain-specific types
UserId = NewType('UserId', int)
Email = NewType('Email', str)

@dataclass
class User:
    id: UserId
    email: Email
    name: str
```

### 3. Use Enums for Constants

```python
from enum import Enum
from dataclasses import dataclass

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

@dataclass
class User:
    name: str
    status: UserStatus
    role: UserRole
```

## Serialization Patterns

### 1. Consistent Naming Conventions

```python
from dataclasses import dataclass
from datetime import datetime

# Good: Consistent field naming
@dataclass
class Product:
    product_id: int
    product_name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

# Avoid: Inconsistent naming
@dataclass
class Product:
    id: int
    name: str
    created: datetime
    last_updated: datetime
    active: bool
```

### 2. Handle Optional Fields

```python
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Article:
    title: str
    content: str
    author: str
    tags: List[str] = field(default_factory=list)
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    view_count: int = 0
```

### 3. Use Default Values Appropriately

```python
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Settings:
    # Use field() for mutable defaults
    allowed_domains: List[str] = field(default_factory=list)
    cache_settings: Dict[str, str] = field(default_factory=dict)
    
    # Use simple defaults for immutable types
    max_retries: int = 3
    timeout: float = 30.0
    debug_mode: bool = False
```

## Error Handling

### 1. Validate Input Data

```python
from jsonport import load, DeserializationError
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

def safe_load_user(data):
    # Validate data structure
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    required_fields = ["name", "age", "email"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate age
    if not isinstance(data["age"], int) or data["age"] < 0:
        raise ValueError("Age must be a positive integer")
    
    try:
        return load(data, User)
    except DeserializationError as e:
        raise ValueError(f"Invalid user data: {e}")
```

### 2. Handle Partial Failures

```python
from jsonport import load, DeserializationError
from typing import List, Tuple

def load_users_with_errors(users_data: List[dict]) -> Tuple[List[User], List[str]]:
    """Load users and collect errors for failed ones"""
    users = []
    errors = []
    
    for i, user_data in enumerate(users_data):
        try:
            user = load(user_data, User)
            users.append(user)
        except DeserializationError as e:
            errors.append(f"User {i}: {e}")
    
    return users, errors
```

### 3. Provide Meaningful Error Messages

```python
from jsonport import load, DeserializationError

def load_with_context(data, target_class, context=""):
    try:
        return load(data, target_class)
    except DeserializationError as e:
        raise DeserializationError(
            f"{context}: {e.message}",
            expected_type=e.expected_type,
            value=e.value,
            field=e.field
        )

# Usage
try:
    user = load_with_context(user_data, User, "Loading user from API")
except DeserializationError as e:
    print(f"Failed to load user: {e}")
```

## Performance Optimization

### 1. Reuse Classes and Objects

```python
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int
    timeout: float

# Good: Reuse the same class
config_class = Config
configs = []

for config_data in configs_data:
    config = load(config_data, config_class)
    configs.append(config)

# Avoid: Creating new classes
for config_data in configs_data:
    @dataclass
    class Config:  # This bypasses caching
        host: str
        port: int
        timeout: float
    config = load(config_data, Config)
```

### 2. Batch Operations

```python
from jsonport import dump, load
from typing import List

def batch_serialize(objects: List[object]) -> List[dict]:
    """Serialize multiple objects efficiently"""
    return [dump(obj) for obj in objects]

def batch_deserialize(data_list: List[dict], target_class) -> List[object]:
    """Deserialize multiple objects efficiently"""
    return [load(data, target_class) for data in data_list]

# Usage
users = [User("John", 30), User("Jane", 25)]
user_data = batch_serialize(users)
restored_users = batch_deserialize(user_data, User)
```

### 3. Use Efficient Data Structures

```python
from typing import Set, Dict, List
from dataclasses import dataclass

@dataclass
class UserProfile:
    # Use Set for unique collections
    permissions: Set[str]
    
    # Use Dict for key-value lookups
    settings: Dict[str, str]
    
    # Use List for ordered collections
    recent_activities: List[str]
```

## File Operations

### 1. Handle File Paths Safely

```python
import os
from pathlib import Path
from jsonport import dump_to_file, load_from_file

def safe_save_config(config, filepath):
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Use temporary file for atomic writes
    temp_path = f"{filepath}.tmp"
    try:
        dump_to_file(config, temp_path)
        os.replace(temp_path, filepath)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise

def safe_load_config(filepath, config_class):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    
    try:
        return load_from_file(filepath, config_class)
    except Exception as e:
        raise ValueError(f"Failed to load config from {filepath}: {e}")
```

### 2. Use Compression for Large Files

```python
from jsonport import dump_to_file, load_from_file

# For large datasets, use compression
def save_large_dataset(data, filepath):
    dump_to_file(data, filepath, compress=True)

def load_large_dataset(filepath, target_class):
    return load_from_file(filepath, target_class, decompress=True)
```

## API Design

### 1. Version Your Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UserV1:
    name: str
    age: int

@dataclass
class UserV2:
    name: str
    age: int
    email: Optional[str] = None
    version: str = field(default="v2", init=False)

def migrate_user_v1_to_v2(user_v1_data):
    user_v1 = load(user_v1_data, UserV1)
    return UserV2(
        name=user_v1.name,
        age=user_v1.age,
        email=None
    )
```

### 2. Use Schema Validation

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class APIResponse:
    success: bool
    data: Dict[str, Any]
    message: str
    timestamp: datetime

def validate_api_response(response_data):
    try:
        response = load(response_data, APIResponse)
        return response
    except DeserializationError as e:
        raise ValueError(f"Invalid API response format: {e}")
```

## Testing Best Practices

### 1. Test Serialization Round-trip

```python
import pytest
from jsonport import dump, load

def test_serialization_roundtrip():
    original_user = User("John", 30, "john@example.com")
    
    # Serialize
    user_data = dump(original_user)
    
    # Deserialize
    restored_user = load(user_data, User)
    
    # Verify equality
    assert restored_user == original_user
    assert restored_user.name == original_user.name
    assert restored_user.age == original_user.age
    assert restored_user.email == original_user.email
```

### 2. Test Error Cases

```python
import pytest
from jsonport import load, DeserializationError

def test_invalid_data():
    invalid_data = {
        "name": "John",
        "age": "not_a_number",  # Invalid type
        "email": "john@example.com"
    }
    
    with pytest.raises(DeserializationError) as exc_info:
        load(invalid_data, User)
    
    assert "Cannot deserialize" in str(exc_info.value)
```

### 3. Test Edge Cases

```python
def test_empty_collections():
    user = User(
        name="John",
        age=30,
        email="john@example.com",
        tags=[],  # Empty list
        metadata={}  # Empty dict
    )
    
    user_data = dump(user)
    restored_user = load(user_data, User)
    
    assert restored_user.tags == []
    assert restored_user.metadata == {}
```

## Common Pitfalls

### 1. Avoid Circular References

```python
# Bad: Circular references
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1  # Circular reference!

# This will raise SerializationError
# data = dump(node1)

# Good: Break circular references
class Node:
    def __init__(self, value):
        self.value = value
        self.next_id = None  # Store ID instead of reference
```

### 2. Don't Overuse Optional Types

```python
# Bad: Too many optional fields
@dataclass
class User:
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Good: Use separate classes for different contexts
@dataclass
class UserBasic:
    name: str
    email: str

@dataclass
class UserExtended(UserBasic):
    age: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
```

### 3. Avoid Deep Nesting

```python
# Bad: Deep nesting
@dataclass
class DeeplyNested:
    level1: Dict[str, Dict[str, Dict[str, Dict[str, str]]]]

# Good: Flatten structure
@dataclass
class FlatStructure:
    settings: Dict[str, str]
    metadata: Dict[str, str]
```

Following these best practices will help you create robust, maintainable, and performant applications with JsonPort. 