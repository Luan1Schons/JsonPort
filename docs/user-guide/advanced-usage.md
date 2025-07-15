# Advanced Usage

Explore advanced features and patterns for complex use cases with JsonPort.

## Nested Structures

JsonPort handles complex nested objects seamlessly:

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Address:
    street: str
    city: str
    country: str
    postal_code: str

@dataclass
class Contact:
    email: str
    phone: Optional[str] = None

@dataclass
class Company:
    name: str
    founded: datetime
    employees: int
    address: Address
    contacts: List[Contact]
    departments: Dict[str, List[str]]

# Create complex nested structure
company = Company(
    name="TechCorp",
    founded=datetime(2020, 1, 1),
    employees=150,
    address=Address(
        street="123 Tech Street",
        city="San Francisco",
        country="USA",
        postal_code="94105"
    ),
    contacts=[
        Contact("info@techcorp.com"),
        Contact("support@techcorp.com", "+1-555-0123")
    ],
    departments={
        "Engineering": ["Backend", "Frontend", "DevOps"],
        "Sales": ["Enterprise", "SMB"],
        "Marketing": ["Digital", "Content"]
    }
)

# Serialize complex structure
data = dump(company)

# Deserialize with full type preservation
restored_company = load(data, Company)
```

## Generic Types

JsonPort supports generic types and complex type hints:

```python
from typing import Generic, TypeVar, Union, Any

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]

@dataclass
class User:
    name: str
    age: int

# Use with generic types
result = Result[User](
    success=True,
    data=User("John", 30),
    error=None
)

data = dump(result)
restored_result = load(data, Result[User])
```

## Union Types

Handle multiple possible types:

```python
from typing import Union

@dataclass
class Config:
    value: Union[str, int, float, bool]
    metadata: Dict[str, Any]

config = Config(
    value=42,  # int
    metadata={"type": "integer", "description": "Sample value"}
)

data = dump(config)
restored_config = load(data, Config)
```

## Optional Fields

Handle optional fields with default values:

```python
@dataclass
class Product:
    id: int
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    tags: List[str] = None

# Create with minimal data
product1 = Product(id=1, name="Laptop")

# Create with full data
product2 = Product(
    id=2,
    name="Mouse",
    description="Wireless mouse",
    price=29.99,
    tags=["electronics", "wireless"]
)

data1 = dump(product1)
data2 = dump(product2)
```

## Custom Type Handling

For types not natively supported, you can extend JsonPort:

```python
from decimal import Decimal
from jsonport import JsonPortEncoder

# Custom encoder for Decimal
class CustomEncoder(JsonPortEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

# Use custom encoder
data = dump(product, encoder=CustomEncoder)
```

## Performance Optimization

### Caching Benefits

JsonPort automatically caches type information:

```python
import time
from dataclasses import dataclass

@dataclass
class PerformanceTest:
    id: int
    name: str
    values: List[float]

# First call - slower (type analysis)
start = time.time()
data1 = dump(PerformanceTest(1, "test", [1.1, 2.2, 3.3]))
first_call = time.time() - start

# Subsequent calls - faster (cached)
start = time.time()
for i in range(1000):
    data = dump(PerformanceTest(i, f"test{i}", [1.1, 2.2, 3.3]))
subsequent_calls = time.time() - start

print(f"First call: {first_call:.4f}s")
print(f"1000 calls: {subsequent_calls:.4f}s")
```

### Batch Processing

Process multiple objects efficiently:

```python
# Efficient batch processing
users = [
    User(f"user{i}", 20 + i) 
    for i in range(1000)
]

# Serialize all at once
data_list = [dump(user) for user in users]

# Deserialize all at once
restored_users = [load(data, User) for data in data_list]
```

## Error Recovery

Implement robust error handling for production:

```python
from jsonport import JsonPortError
import logging

logger = logging.getLogger(__name__)

def safe_load(data, target_class, fallback=None):
    """Safely load data with fallback on error."""
    try:
        return load(data, target_class)
    except JsonPortError as e:
        logger.error(f"Failed to load {target_class.__name__}: {e}")
        return fallback
    except Exception as e:
        logger.error(f"Unexpected error loading {target_class.__name__}: {e}")
        return fallback

# Usage
user = safe_load(invalid_data, User, User("Unknown", 0))
```

## Validation Patterns

Add custom validation to your dataclasses:

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ValidatedUser:
    name: str
    age: int
    email: str
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if "@" not in self.email:
            raise ValueError("Invalid email format")

# This will raise ValueError
try:
    user = ValidatedUser("John", -5, "invalid-email")
except ValueError as e:
    print(f"Validation error: {e}")
```

## Integration Patterns

### With Web Frameworks

```python
from flask import Flask, request, jsonify
from jsonport import dump, load

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = load(data, User)
        # Process user...
        return jsonify(dump(user)), 201
    except JsonPortError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = get_user_from_db(user_id)
    return jsonify(dump(user))
```

### With Databases

```python
import sqlite3
from jsonport import dump, load

def save_user_to_db(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Serialize user data
    user_data = dump(user)
    
    cursor.execute(
        "INSERT INTO users (data) VALUES (?)",
        (json.dumps(user_data),)
    )
    conn.commit()
    conn.close()

def load_user_from_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT data FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_data = json.loads(result[0])
        return load(user_data, User)
    return None
```

## Next Steps

- [File Operations](file-operations.md) - Working with files
- [Error Handling](error-handling.md) - Error handling patterns
- [Examples](examples/) - More practical examples
- [API Reference](api/) - Complete API documentation 