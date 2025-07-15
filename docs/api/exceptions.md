# Exceptions

JsonPort provides comprehensive exception handling with detailed error messages to help you debug serialization and deserialization issues.

## Exception Hierarchy

```python
JsonPortError (Base Exception)
├── SerializationError
└── DeserializationError
```

## Base Exception

### JsonPortError

The base exception class for all JsonPort errors:

```python
from jsonport import JsonPortError

class JsonPortError(Exception):
    """Base exception for all JsonPort errors."""
    pass
```

**Usage:**
```python
from jsonport import JsonPortError

try:
    # Your serialization/deserialization code
    pass
except JsonPortError as e:
    print(f"JsonPort error: {e}")
```

## Serialization Errors

### SerializationError

Raised when serialization fails:

```python
from jsonport import SerializationError

class SerializationError(JsonPortError):
    """Raised when serialization fails."""
    
    def __init__(self, message: str, object_type: str = None, field: str = None):
        self.message = message
        self.object_type = object_type
        self.field = field
        super().__init__(message)
```

**Usage:**
```python
from jsonport import dump, SerializationError

try:
    data = dump(complex_object)
except SerializationError as e:
    print(f"Serialization failed: {e}")
    print(f"Object type: {e.object_type}")
    print(f"Field: {e.field}")
```

**Common Causes:**
- Circular references
- Unsupported object types
- Invalid enum values
- Missing required fields

**Example:**
```python
from dataclasses import dataclass
from jsonport import dump, SerializationError

# Circular reference example
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1  # Circular reference!

try:
    data = dump(node1)
except SerializationError as e:
    print(f"Error: {e}")
    # Output: Error: Cannot serialize object with circular references
```

## Deserialization Errors

### DeserializationError

Raised when deserialization fails:

```python
from jsonport import DeserializationError

class DeserializationError(JsonPortError):
    """Raised when deserialization fails."""
    
    def __init__(self, message: str, expected_type: str = None, value: any = None, field: str = None):
        self.message = message
        self.expected_type = expected_type
        self.value = value
        self.field = field
        super().__init__(message)
```

**Usage:**
```python
from jsonport import load, DeserializationError

try:
    obj = load(data, TargetClass)
except DeserializationError as e:
    print(f"Deserialization failed: {e}")
    print(f"Expected type: {e.expected_type}")
    print(f"Received value: {e.value}")
    print(f"Field: {e.field}")
```

**Common Causes:**
- Type mismatches
- Missing required fields
- Invalid enum values
- Malformed data structures

## Common Error Scenarios

### Type Mismatch

```python
from dataclasses import dataclass
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
    print(f"Expected type: {e.expected_type}")
    print(f"Received value: {e.value}")
    # Output:
    # Type error: Cannot deserialize 'thirty' to int
    # Expected type: int
    # Received value: thirty
```

### Missing Required Fields

```python
from dataclasses import dataclass
from jsonport import load, DeserializationError

@dataclass
class User:
    name: str
    age: int
    email: str

# This will raise DeserializationError
try:
    user = load({"name": "John", "age": 30}, User)
except DeserializationError as e:
    print(f"Missing field: {e}")
    # Output: Missing field: Required field 'email' not found
```

### Invalid Enum Values

```python
from enum import Enum
from dataclasses import dataclass
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
    print(f"Expected type: {e.expected_type}")
    print(f"Received value: {e.value}")
    # Output:
    # Invalid enum: Cannot deserialize 'moderator' to UserRole
    # Expected type: UserRole
    # Received value: moderator
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

## Error Handling Patterns

### 1. Basic Error Handling

```python
from jsonport import dump, load, JsonPortError, SerializationError, DeserializationError

def safe_serialize(obj):
    """Safely serialize an object with error handling."""
    try:
        return dump(obj)
    except SerializationError as e:
        print(f"Serialization failed: {e}")
        return None
    except JsonPortError as e:
        print(f"Unexpected JsonPort error: {e}")
        return None

def safe_deserialize(data, target_class):
    """Safely deserialize data with error handling."""
    try:
        return load(data, target_class)
    except DeserializationError as e:
        print(f"Deserialization failed: {e}")
        return None
    except JsonPortError as e:
        print(f"Unexpected JsonPort error: {e}")
        return None
```

### 2. Validation Before Deserialization

```python
from jsonport import load, DeserializationError

def validate_user_data(data):
    """Validate user data before deserialization."""
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    required_fields = ["name", "age", "email"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate age
    if not isinstance(data["age"], int) or data["age"] < 0:
        raise ValueError("Age must be a positive integer")
    
    # Validate email format
    if "@" not in data["email"]:
        raise ValueError("Invalid email format")

def safe_load_user(data):
    """Load user with validation."""
    try:
        validate_user_data(data)
        return load(data, User)
    except (ValueError, DeserializationError) as e:
        print(f"Failed to load user: {e}")
        raise
```

### 3. Partial Failure Handling

```python
from jsonport import load, DeserializationError
from typing import List, Tuple

def load_users_with_errors(users_data: List[dict]) -> Tuple[List[User], List[str]]:
    """Load users and collect errors for failed ones."""
    users = []
    errors = []
    
    for i, user_data in enumerate(users_data):
        try:
            user = load(user_data, User)
            users.append(user)
        except DeserializationError as e:
            errors.append(f"User {i}: {e}")
    
    return users, errors

# Usage
users_data = [
    {"name": "John", "age": 30, "email": "john@example.com"},
    {"name": "Jane", "age": "twenty-five", "email": "jane@example.com"},  # Invalid age
    {"name": "Bob", "age": 35, "email": "bob@example.com"}
]

users, errors = load_users_with_errors(users_data)
print(f"Successfully loaded {len(users)} users")
print(f"Failed to load {len(errors)} users:")
for error in errors:
    print(f"  - {error}")
```

### 4. Custom Error Messages

```python
from jsonport import load, DeserializationError

def load_with_context(data, target_class, context=""):
    """Load object with contextual error messages."""
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
    # Output: Failed to load user: Loading user from API: Cannot deserialize 'thirty' to int
```

### 5. Fallback Values

```python
from jsonport import load, DeserializationError

def load_with_fallback(data, target_class, fallback_value=None):
    """Load object with fallback value on failure."""
    try:
        return load(data, target_class)
    except DeserializationError:
        return fallback_value

# Usage
user = load_with_fallback(invalid_data, User, User("Default", 0, "default@example.com"))
```

### 6. Retry with Different Types

```python
from jsonport import load, DeserializationError
from typing import Union

def load_flexible(data, target_class, alternative_class=None):
    """Try to load with target class, fallback to alternative if specified."""
    try:
        return load(data, target_class)
    except DeserializationError as e:
        if alternative_class:
            try:
                return load(data, alternative_class)
            except DeserializationError:
                raise e
        raise

# Usage
try:
    # Try to load as User, fallback to BasicUser if needed
    user = load_flexible(data, User, BasicUser)
except DeserializationError as e:
    print(f"Failed to load user: {e}")
```

## Debugging Tips

### 1. Enable Debug Logging

```python
import logging

# Enable debug logging for JsonPort
logging.getLogger('jsonport').setLevel(logging.DEBUG)

# This will show detailed information about serialization/deserialization
```

### 2. Inspect Object Structure

```python
from jsonport import dump

def debug_object(obj):
    """Debug object serialization."""
    try:
        data = dump(obj)
        print("Serialization successful")
        print(f"Result: {data}")
    except Exception as e:
        print(f"Serialization failed: {e}")
        print(f"Object type: {type(obj)}")
        print(f"Object attributes: {dir(obj)}")
        if hasattr(obj, '__dict__'):
            print(f"Object dict: {obj.__dict__}")
```

### 3. Validate Type Hints

```python
from typing import get_type_hints

def validate_dataclass(cls):
    """Validate dataclass type hints."""
    hints = get_type_hints(cls)
    print(f"Type hints for {cls.__name__}:")
    for field, hint in hints.items():
        print(f"  {field}: {hint}")
```

### 4. Check Data Structure

```python
def inspect_data_structure(data, indent=0):
    """Recursively inspect data structure."""
    prefix = "  " * indent
    
    if isinstance(data, dict):
        print(f"{prefix}Dict with {len(data)} keys:")
        for key, value in data.items():
            print(f"{prefix}  {key}: {type(value).__name__}")
            inspect_data_structure(value, indent + 2)
    elif isinstance(data, list):
        print(f"{prefix}List with {len(data)} items:")
        for i, item in enumerate(data):
            print(f"{prefix}  [{i}]: {type(item).__name__}")
            inspect_data_structure(item, indent + 2)
    else:
        print(f"{prefix}Value: {type(data).__name__} = {data}")

# Usage
inspect_data_structure(user_data)
```

## Error Recovery Strategies

### 1. Partial Deserialization

```python
from jsonport import load, DeserializationError
from dataclasses import fields

def load_partial(data, target_class):
    """Load object with only valid fields."""
    result = {}
    
    for field in fields(target_class):
        if field.name in data:
            try:
                result[field.name] = load(data[field.name], field.type)
            except DeserializationError:
                # Skip invalid field
                continue
    
    return target_class(**result)

# Usage
try:
    user = load_partial(invalid_data, User)
    print(f"Loaded user with {len(user.__dict__)} fields")
except Exception as e:
    print(f"Failed to load even partially: {e}")
```

### 2. Data Cleaning

```python
def clean_data_for_loading(data, target_class):
    """Clean data to make it compatible with target class."""
    cleaned_data = {}
    
    for field in fields(target_class):
        field_name = field.name
        if field_name in data:
            value = data[field_name]
            
            # Handle type conversions
            if field.type == int and isinstance(value, str):
                try:
                    cleaned_data[field_name] = int(value)
                except ValueError:
                    continue  # Skip invalid conversion
            
            elif field.type == float and isinstance(value, str):
                try:
                    cleaned_data[field_name] = float(value)
                except ValueError:
                    continue
            
            else:
                cleaned_data[field_name] = value
    
    return cleaned_data

# Usage
cleaned_data = clean_data_for_loading(raw_data, User)
user = load(cleaned_data, User)
```

This comprehensive guide covers all the exception types in JsonPort, common error scenarios, error handling patterns, debugging tips, and recovery strategies. 