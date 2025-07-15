# Error Handling

JsonPort provides comprehensive error handling with detailed error messages to help you debug serialization and deserialization issues.

## Error Types

### JsonPortError

The base exception class for all JsonPort errors:

```python
from jsonport import JsonPortError

try:
    # Your serialization/deserialization code
    pass
except JsonPortError as e:
    print(f"JsonPort error: {e}")
```

### SerializationError

Raised when serialization fails:

```python
from jsonport import SerializationError

try:
    data = dump(complex_object)
except SerializationError as e:
    print(f"Serialization failed: {e}")
    print(f"Object type: {e.object_type}")
    print(f"Field: {e.field}")
```

### DeserializationError

Raised when deserialization fails:

```python
from jsonport import DeserializationError

try:
    obj = load(data, TargetClass)
except DeserializationError as e:
    print(f"Deserialization failed: {e}")
    print(f"Expected type: {e.expected_type}")
    print(f"Received value: {e.value}")
```

## Common Error Scenarios

### Type Mismatch

```python
from jsonport import load, DeserializationError

@dataclass
class User:
    name: str
    age: int

# This will raise DeserializationError
try:
    user = load({"name": "John", "age": "thirty"}, User)
except DeserializationError as e:
    print(f"Type error: {e}")
    # Output: Type error: Cannot deserialize 'thirty' to int
```

### Missing Required Fields

```python
from jsonport import load, DeserializationError

@dataclass
class User:
    name: str
    age: int

# This will raise DeserializationError
try:
    user = load({"name": "John"}, User)
except DeserializationError as e:
    print(f"Missing field: {e}")
    # Output: Missing field: Required field 'age' not found
```

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
    print(f"Invalid enum: {e}")
    # Output: Invalid enum: 'moderator' is not a valid UserRole
```

### Circular References

```python
from jsonport import dump, SerializationError

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Create circular reference
node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1

# This will raise SerializationError
try:
    data = dump(node1)
except SerializationError as e:
    print(f"Circular reference: {e}")
    # Output: Circular reference: Cannot serialize object with circular references
```

## Error Handling Best Practices

### 1. Use Specific Exception Types

```python
from jsonport import JsonPortError, SerializationError, DeserializationError

def safe_serialize(obj):
    try:
        return dump(obj)
    except SerializationError as e:
        logger.error(f"Serialization failed: {e}")
        return None
    except JsonPortError as e:
        logger.error(f"Unexpected JsonPort error: {e}")
        return None
```

### 2. Validate Data Before Deserialization

```python
from jsonport import load, DeserializationError

def safe_load_user(data):
    # Validate required fields
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    if "name" not in data:
        raise ValueError("User must have a name")
    
    if "age" not in data:
        raise ValueError("User must have an age")
    
    try:
        return load(data, User)
    except DeserializationError as e:
        logger.error(f"Failed to load user: {e}")
        raise
```

### 3. Handle Partial Failures

```python
from jsonport import load, DeserializationError
from typing import List

def load_users_safely(users_data: List[dict]) -> List[User]:
    valid_users = []
    errors = []
    
    for i, user_data in enumerate(users_data):
        try:
            user = load(user_data, User)
            valid_users.append(user)
        except DeserializationError as e:
            errors.append(f"User {i}: {e}")
    
    if errors:
        logger.warning(f"Failed to load {len(errors)} users: {errors}")
    
    return valid_users
```

### 4. Custom Error Messages

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
```

## Debugging Tips

### 1. Enable Debug Logging

```python
import logging

# Enable debug logging for JsonPort
logging.getLogger('jsonport').setLevel(logging.DEBUG)
```

### 2. Inspect Object Structure

```python
from jsonport import dump

def debug_object(obj):
    try:
        data = dump(obj)
        print("Serialization successful")
        print(f"Result: {data}")
    except Exception as e:
        print(f"Serialization failed: {e}")
        print(f"Object type: {type(obj)}")
        print(f"Object attributes: {dir(obj)}")
```

### 3. Validate Type Hints

```python
from typing import get_type_hints

def validate_dataclass(cls):
    hints = get_type_hints(cls)
    print(f"Type hints for {cls.__name__}:")
    for field, hint in hints.items():
        print(f"  {field}: {hint}")
```

## Error Recovery

### 1. Fallback Values

```python
from jsonport import load, DeserializationError

def load_with_fallback(data, target_class, fallback_value=None):
    try:
        return load(data, target_class)
    except DeserializationError:
        return fallback_value
```

### 2. Partial Deserialization

```python
from jsonport import load, DeserializationError
from dataclasses import fields

def load_partial(data, target_class):
    """Load object with only valid fields"""
    result = {}
    
    for field in fields(target_class):
        if field.name in data:
            try:
                result[field.name] = load(data[field.name], field.type)
            except DeserializationError:
                # Skip invalid field
                continue
    
    return target_class(**result)
```

This comprehensive error handling approach ensures your applications can gracefully handle serialization and deserialization issues while providing useful debugging information. 