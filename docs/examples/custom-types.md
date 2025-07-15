# Custom Types

JsonPort provides support for custom types through type hints and can be extended to handle specialized data structures and domain-specific types.

## NewType Aliases

### Domain-Specific Types

```python
from dataclasses import dataclass
from typing import NewType, List
from jsonport import dump, load

# Define domain-specific types
UserId = NewType('UserId', int)
Email = NewType('Email', str)
Username = NewType('Username', str)
Password = NewType('Password', str)

@dataclass
class User:
    id: UserId
    username: Username
    email: Email
    password: Password

# Create user with custom types
user = User(
    id=UserId(1),
    username=Username("john_doe"),
    email=Email("john@example.com"),
    password=Password("secret123")
)

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "password": "secret123"
# }

# Deserialize
restored_user = load(data, User)
print(type(restored_user.id))  # <class 'int'> (NewType is transparent)
print(restored_user.username)  # "john_doe"
```

### Type-Safe Identifiers

```python
from dataclasses import dataclass
from typing import NewType, Dict, List

# Type-safe identifiers
OrderId = NewType('OrderId', str)
ProductId = NewType('ProductId', str)
CustomerId = NewType('CustomerId', str)

@dataclass
class OrderItem:
    product_id: ProductId
    quantity: int
    price: float

@dataclass
class Order:
    order_id: OrderId
    customer_id: CustomerId
    items: List[OrderItem]
    total: float

# Create order with type-safe IDs
order = Order(
    order_id=OrderId("ORD-2025-001"),
    customer_id=CustomerId("CUST-123"),
    items=[
        OrderItem(ProductId("PROD-001"), 2, 29.99),
        OrderItem(ProductId("PROD-002"), 1, 49.99)
    ],
    total=109.97
)

# Serialize
data = dump(order)
print(data)
# Output:
# {
#   "order_id": "ORD-2025-001",
#   "customer_id": "CUST-123",
#   "items": [
#     {
#       "product_id": "PROD-001",
#       "quantity": 2,
#       "price": 29.99
#     },
#     {
#       "product_id": "PROD-002",
#       "quantity": 1,
#       "price": 49.99
#     }
#   ],
#   "total": 109.97
# }

# Deserialize
restored_order = load(data, Order)
print(restored_order.order_id)  # "ORD-2025-001"
print(len(restored_order.items))  # 2
```

## Literal Types

### Status Enums

```python
from dataclasses import dataclass
from typing import Literal, List

# Define literal types for status
OrderStatus = Literal["pending", "processing", "shipped", "delivered", "cancelled"]
PaymentStatus = Literal["pending", "paid", "failed", "refunded"]

@dataclass
class Order:
    id: str
    status: OrderStatus
    payment_status: PaymentStatus
    items: List[str]

# Create orders with literal types
order1 = Order("ORD-001", "pending", "pending", ["item1", "item2"])
order2 = Order("ORD-002", "shipped", "paid", ["item3"])

# Serialize
data1 = dump(order1)
data2 = dump(order2)
print(data1)
# Output:
# {
#   "id": "ORD-001",
#   "status": "pending",
#   "payment_status": "pending",
#   "items": ["item1", "item2"]
# }

print(data2)
# Output:
# {
#   "id": "ORD-002",
#   "status": "shipped",
#   "payment_status": "paid",
#   "items": ["item3"]
# }

# Deserialize
restored_order1 = load(data1, Order)
restored_order2 = load(data2, Order)
print(restored_order1.status)  # "pending"
print(restored_order2.status)  # "shipped"
```

### Configuration Literals

```python
from dataclasses import dataclass
from typing import Literal, Dict

# Environment and mode literals
Environment = Literal["development", "staging", "production"]
LogLevel = Literal["debug", "info", "warning", "error"]
DatabaseType = Literal["sqlite", "postgresql", "mysql"]

@dataclass
class AppConfig:
    environment: Environment
    log_level: LogLevel
    database_type: DatabaseType
    settings: Dict[str, str]

# Create configuration
config = AppConfig(
    environment="development",
    log_level="debug",
    database_type="sqlite",
    settings={"host": "localhost", "port": "8080"}
)

# Serialize
data = dump(config)
print(data)
# Output:
# {
#   "environment": "development",
#   "log_level": "debug",
#   "database_type": "sqlite",
#   "settings": {
#     "host": "localhost",
#     "port": "8080"
#   }
# }

# Deserialize
restored_config = load(data, AppConfig)
print(restored_config.environment)  # "development"
print(restored_config.log_level)  # "debug"
```

## Union Types

### Flexible Data Types

```python
from dataclasses import dataclass
from typing import Union, List, Optional
from datetime import datetime

# Union types for flexible data
ValueType = Union[str, int, float, bool, None]
Timestamp = Union[datetime, str, None]

@dataclass
class DataPoint:
    name: str
    value: ValueType
    timestamp: Timestamp
    metadata: Optional[Dict[str, ValueType]] = None

# Create data points with different types
data_points = [
    DataPoint("temperature", 25.5, datetime.now()),
    DataPoint("status", "active", "2025-01-14T10:30:00"),
    DataPoint("enabled", True, None),
    DataPoint("count", 42, datetime.now(), {"unit": "items"})
]

# Serialize
data = dump(data_points)
print(data)
# Output:
# [
#   {
#     "name": "temperature",
#     "value": 25.5,
#     "timestamp": "2025-01-14T10:30:00",
#     "metadata": null
#   },
#   {
#     "name": "status",
#     "value": "active",
#     "timestamp": "2025-01-14T10:30:00",
#     "metadata": null
#   },
#   {
#     "name": "enabled",
#     "value": true,
#     "timestamp": null,
#     "metadata": null
#   },
#   {
#     "name": "count",
#     "value": 42,
#     "timestamp": "2025-01-14T10:30:00",
#     "metadata": {"unit": "items"}
#   }
# ]

# Deserialize
restored_points = load(data, List[DataPoint])
print(len(restored_points))  # 4
print(restored_points[0].value)  # 25.5
print(restored_points[1].value)  # "active"
```

### Optional Fields with Unions

```python
from dataclasses import dataclass
from typing import Union, Optional, List

# Union types for optional fields
StringOrInt = Union[str, int]
StringOrNone = Optional[str]

@dataclass
class FlexibleObject:
    id: StringOrInt
    name: str
    description: StringOrNone
    tags: List[StringOrInt]

# Create flexible objects
obj1 = FlexibleObject(1, "Object 1", "Description", ["tag1", 2, "tag3"])
obj2 = FlexibleObject("OBJ-002", "Object 2", None, [1, "important", 3])

# Serialize
data1 = dump(obj1)
data2 = dump(obj2)
print(data1)
# Output:
# {
#   "id": 1,
#   "name": "Object 1",
#   "description": "Description",
#   "tags": ["tag1", 2, "tag3"]
# }

print(data2)
# Output:
# {
#   "id": "OBJ-002",
#   "name": "Object 2",
#   "description": null,
#   "tags": [1, "important", 3]
# }

# Deserialize
restored_obj1 = load(data1, FlexibleObject)
restored_obj2 = load(data2, FlexibleObject)
print(type(restored_obj1.id))  # <class 'int'>
print(type(restored_obj2.id))  # <class 'str'>
```

## Generic Types

### Generic Containers

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Dict, Optional

# Define type variables
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

@dataclass
class Container(Generic[T]):
    data: T
    metadata: Dict[str, str]

@dataclass
class KeyValuePair(Generic[K, V]):
    key: K
    value: V
    description: Optional[str] = None

@dataclass
class DataCollection(Generic[T]):
    items: List[T]
    total_count: int
    page: int

# Create generic containers
string_container = Container("Hello World", {"type": "string", "length": "11"})
int_container = Container(42, {"type": "integer", "range": "positive"})

# Create key-value pairs
kv1 = KeyValuePair("name", "John", "User's full name")
kv2 = KeyValuePair(1, True, "Boolean flag")

# Create data collection
collection = DataCollection([1, 2, 3, 4, 5], 5, 1)

# Serialize
string_data = dump(string_container)
int_data = dump(int_container)
kv_data = dump([kv1, kv2])
collection_data = dump(collection)

print(string_data)
# Output:
# {
#   "data": "Hello World",
#   "metadata": {
#     "type": "string",
#     "length": "11"
#   }
# }

print(kv_data)
# Output:
# [
#   {
#     "key": "name",
#     "value": "John",
#     "description": "User's full name"
#   },
#   {
#     "key": 1,
#     "value": true,
#     "description": "Boolean flag"
#   }
# ]

# Deserialize
restored_string = load(string_data, Container[str])
restored_kvs = load(kv_data, List[KeyValuePair])
restored_collection = load(collection_data, DataCollection[int])

print(restored_string.data)  # "Hello World"
print(restored_kvs[0].key)  # "name"
print(restored_collection.total_count)  # 5
```

## Custom Classes with Type Hints

### Domain Objects

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self.value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"Email('{self.value}')"

class PhoneNumber:
    def __init__(self, value: str):
        # Simple validation
        if not value.replace("-", "").replace(" ", "").isdigit():
            raise ValueError("Invalid phone number format")
        self.value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"PhoneNumber('{self.value}')"

@dataclass
class Contact:
    name: str
    email: Email
    phone: PhoneNumber
    created_at: datetime

# Create contact with custom types
contact = Contact(
    name="John Doe",
    email=Email("john@example.com"),
    phone=PhoneNumber("+1-555-0123"),
    created_at=datetime.now()
)

# Serialize
data = dump(contact)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "email": "john@example.com",
#   "phone": "+1-555-0123",
#   "created_at": "2025-01-14T10:30:00"
# }

# Deserialize
restored_contact = load(data, Contact)
print(restored_contact.email)  # "john@example.com"
print(restored_contact.phone)  # "+1-555-0123"
```

### Custom Collections

```python
from dataclasses import dataclass
from typing import List, Dict, Any

class TaggedList:
    def __init__(self, items: List[Any], tag: str):
        self.items = items
        self.tag = tag
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __iter__(self):
        return iter(self.items)

class MetadataDict:
    def __init__(self, data: Dict[str, Any], metadata: Dict[str, str]):
        self.data = data
        self.metadata = metadata
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def keys(self):
        return self.data.keys()

@dataclass
class CustomData:
    items: TaggedList
    settings: MetadataDict
    version: str

# Create custom data
custom_data = CustomData(
    items=TaggedList([1, 2, 3, 4, 5], "numbers"),
    settings=MetadataDict(
        {"host": "localhost", "port": 8080},
        {"type": "configuration", "source": "file"}
    ),
    version="1.0"
)

# Serialize
data = dump(custom_data)
print(data)
# Output:
# {
#   "items": [1, 2, 3, 4, 5],
#   "settings": {
#     "host": "localhost",
#     "port": 8080
#   },
#   "version": "1.0"
# }

# Deserialize
restored_data = load(data, CustomData)
print(len(restored_data.items))  # 5
print(restored_data.settings["host"])  # "localhost"
```

## Type Aliases

### Complex Type Aliases

```python
from dataclasses import dataclass
from typing import TypeAlias, List, Dict, Optional
from datetime import datetime

# Define complex type aliases
UserId = TypeAlias = int
Email = TypeAlias = str
Timestamp = TypeAlias = datetime

# Nested type aliases
UserData = TypeAlias = Dict[str, str]
UserList = TypeAlias = List[UserData]
ApiResponse = TypeAlias = Dict[str, any]

@dataclass
class User:
    id: UserId
    email: Email
    data: UserData
    created_at: Timestamp

@dataclass
class UserCollection:
    users: UserList
    total: int
    response: ApiResponse

# Create user collection
user_collection = UserCollection(
    users=[
        {"name": "John", "role": "admin"},
        {"name": "Jane", "role": "user"}
    ],
    total=2,
    response={"status": "success", "message": "Users retrieved"}
)

# Serialize
data = dump(user_collection)
print(data)
# Output:
# {
#   "users": [
#     {"name": "John", "role": "admin"},
#     {"name": "Jane", "role": "user"}
#   ],
#   "total": 2,
#   "response": {
#     "status": "success",
#     "message": "Users retrieved"
#   }
# }

# Deserialize
restored_collection = load(data, UserCollection)
print(len(restored_collection.users))  # 2
print(restored_collection.response["status"])  # "success"
```

## Performance Considerations

### Type Resolution Performance

```python
from dataclasses import dataclass
from typing import Union, List, Optional
import time

# Complex union types
ComplexType = Union[str, int, float, bool, List[str], Dict[str, any], None]

@dataclass
class PerformanceTest:
    simple_field: str
    union_field: ComplexType
    optional_field: Optional[ComplexType]

# Create test data
test_data = PerformanceTest(
    simple_field="test",
    union_field={"key": "value", "number": 42},
    optional_field=["item1", "item2", "item3"]
)

# Measure serialization performance
start_time = time.time()
for _ in range(1000):
    data = dump(test_data)
serialization_time = time.time() - start_time

# Measure deserialization performance
start_time = time.time()
for _ in range(1000):
    restored = load(data, PerformanceTest)
deserialization_time = time.time() - start_time

print(f"Serialization time: {serialization_time:.3f}s")
print(f"Deserialization time: {deserialization_time:.3f}s")
```

This comprehensive guide demonstrates how to work with custom types in JsonPort, including NewType aliases, literal types, union types, generic types, and custom classes with type hints. 