# Types

JsonPort supports a comprehensive set of Python types for serialization and deserialization with full type safety and automatic conversion.

## Basic Types

### Primitive Types

JsonPort supports all Python primitive types:

```python
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class BasicTypes:
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    none_field: None

# Create object with basic types
obj = BasicTypes(
    string_field="Hello World",
    int_field=42,
    float_field=3.14,
    bool_field=True,
    none_field=None
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "string_field": "Hello World",
#   "int_field": 42,
#   "float_field": 3.14,
#   "bool_field": true,
#   "none_field": null
# }

# Deserialize
restored = load(data, BasicTypes)
print(restored.string_field)  # "Hello World"
print(restored.int_field)  # 42
print(restored.float_field)  # 3.14
print(restored.bool_field)  # True
print(restored.none_field)  # None
```

## Collection Types

### Lists

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ListTypes:
    string_list: List[str]
    int_list: List[int]
    mixed_list: List[any]
    nested_list: List[List[int]]

# Create object with lists
obj = ListTypes(
    string_list=["apple", "banana", "cherry"],
    int_list=[1, 2, 3, 4, 5],
    mixed_list=["text", 42, True, None],
    nested_list=[[1, 2], [3, 4], [5, 6]]
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "string_list": ["apple", "banana", "cherry"],
#   "int_list": [1, 2, 3, 4, 5],
#   "mixed_list": ["text", 42, true, null],
#   "nested_list": [[1, 2], [3, 4], [5, 6]]
# }

# Deserialize
restored = load(data, ListTypes)
print(restored.string_list)  # ["apple", "banana", "cherry"]
print(restored.nested_list[0])  # [1, 2]
```

### Tuples

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class TupleTypes:
    simple_tuple: Tuple[int, str]
    mixed_tuple: Tuple[str, int, bool, float]
    nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]]

# Create object with tuples
obj = TupleTypes(
    simple_tuple=(42, "answer"),
    mixed_tuple=("text", 123, True, 3.14),
    nested_tuple=((1, 2), ("a", "b"))
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "simple_tuple": [42, "answer"],
#   "mixed_tuple": ["text", 123, true, 3.14],
#   "nested_tuple": [[1, 2], ["a", "b"]]
# }

# Deserialize
restored = load(data, TupleTypes)
print(restored.simple_tuple)  # (42, "answer")
print(restored.nested_tuple[0])  # (1, 2)
```

### Sets

```python
from dataclasses import dataclass
from typing import Set

@dataclass
class SetTypes:
    string_set: Set[str]
    int_set: Set[int]
    mixed_set: Set[any]

# Create object with sets
obj = SetTypes(
    string_set={"apple", "banana", "cherry"},
    int_set={1, 2, 3, 4, 5},
    mixed_set={"text", 42, True}
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "string_set": ["apple", "banana", "cherry"],
#   "int_set": [1, 2, 3, 4, 5],
#   "mixed_set": ["text", 42, true]
# }

# Deserialize
restored = load(data, SetTypes)
print(restored.string_set)  # {"apple", "banana", "cherry"}
print(42 in restored.mixed_set)  # True
```

### Dictionaries

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DictTypes:
    string_dict: Dict[str, str]
    mixed_dict: Dict[str, Any]
    nested_dict: Dict[str, Dict[str, int]]

# Create object with dictionaries
obj = DictTypes(
    string_dict={"name": "John", "city": "New York"},
    mixed_dict={"count": 42, "active": True, "score": 95.5},
    nested_dict={
        "group1": {"a": 1, "b": 2},
        "group2": {"x": 10, "y": 20}
    }
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "string_dict": {
#     "name": "John",
#     "city": "New York"
#   },
#   "mixed_dict": {
#     "count": 42,
#     "active": true,
#     "score": 95.5
#   },
#   "nested_dict": {
#     "group1": {"a": 1, "b": 2},
#     "group2": {"x": 10, "y": 20}
#   }
# }

# Deserialize
restored = load(data, DictTypes)
print(restored.string_dict["name"])  # "John"
print(restored.nested_dict["group1"]["a"])  # 1
```

## Datetime Types

### DateTime Objects

```python
from dataclasses import dataclass
from datetime import datetime, date, time

@dataclass
class DateTimeTypes:
    datetime_field: datetime
    date_field: date
    time_field: time
    optional_datetime: datetime = None

# Create object with datetime types
obj = DateTimeTypes(
    datetime_field=datetime(2025, 1, 14, 10, 30, 0),
    date_field=date(2025, 1, 14),
    time_field=time(10, 30, 0)
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "datetime_field": "2025-01-14T10:30:00",
#   "date_field": "2025-01-14",
#   "time_field": "10:30:00",
#   "optional_datetime": null
# }

# Deserialize
restored = load(data, DateTimeTypes)
print(restored.datetime_field)  # 2025-01-14 10:30:00
print(restored.date_field)  # 2025-01-14
print(restored.time_field)  # 10:30:00
```

### Timezone-Aware DateTime

```python
from dataclasses import dataclass
from datetime import datetime
import pytz

@dataclass
class TimezoneTypes:
    utc_datetime: datetime
    local_datetime: datetime

# Create timezone-aware datetimes
utc_tz = pytz.UTC
local_tz = pytz.timezone('America/New_York')

obj = TimezoneTypes(
    utc_datetime=datetime(2025, 1, 14, 15, 0, 0, tzinfo=utc_tz),
    local_datetime=local_tz.localize(datetime(2025, 1, 14, 10, 0, 0))
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "utc_datetime": "2025-01-14T15:00:00+00:00",
#   "local_datetime": "2025-01-14T10:00:00-05:00"
# }

# Deserialize
restored = load(data, TimezoneTypes)
print(restored.utc_datetime.tzinfo)  # UTC
print(restored.local_datetime.tzinfo)  # America/New_York
```

## Enum Types

### Basic Enums

```python
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class EnumTypes:
    status: Status
    priority: Priority
    optional_status: Status = None

# Create object with enums
obj = EnumTypes(
    status=Status.ACTIVE,
    priority=Priority.HIGH
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "status": "active",
#   "priority": 3,
#   "optional_status": null
# }

# Deserialize
restored = load(data, EnumTypes)
print(restored.status)  # Status.ACTIVE
print(restored.priority)  # Priority.HIGH
```

### IntEnum

```python
from dataclasses import dataclass
from enum import IntEnum

class StatusCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

@dataclass
class StatusCodeTypes:
    code: StatusCode
    message: str

# Create object with IntEnum
obj = StatusCodeTypes(
    code=StatusCode.OK,
    message="Success"
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "code": 200,
#   "message": "Success"
# }

# Deserialize
restored = load(data, StatusCodeTypes)
print(restored.code)  # StatusCode.OK
print(restored.code.value)  # 200
```

## Optional Types

### Optional Fields

```python
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class OptionalTypes:
    required_field: str
    optional_string: Optional[str] = None
    optional_int: Optional[int] = None
    optional_list: Optional[List[str]] = None
    optional_dict: Optional[Dict[str, any]] = None

# Create object with optional fields
obj1 = OptionalTypes("required")
obj2 = OptionalTypes(
    "required",
    optional_string="optional",
    optional_int=42,
    optional_list=["item1", "item2"],
    optional_dict={"key": "value"}
)

# Serialize
data1 = dump(obj1)
data2 = dump(obj2)
print(data1)
# Output:
# {
#   "required_field": "required",
#   "optional_string": null,
#   "optional_int": null,
#   "optional_list": null,
#   "optional_dict": null
# }

print(data2)
# Output:
# {
#   "required_field": "required",
#   "optional_string": "optional",
#   "optional_int": 42,
#   "optional_list": ["item1", "item2"],
#   "optional_dict": {"key": "value"}
# }

# Deserialize
restored1 = load(data1, OptionalTypes)
restored2 = load(data2, OptionalTypes)
print(restored1.optional_string)  # None
print(restored2.optional_string)  # "optional"
```

## Union Types

### Union with Multiple Types

```python
from dataclasses import dataclass
from typing import Union, List

# Define union types
StringOrInt = Union[str, int]
StringOrNone = Union[str, None]
FlexibleType = Union[str, int, float, bool, None]

@dataclass
class UnionTypes:
    string_or_int: StringOrInt
    string_or_none: StringOrNone
    flexible_field: FlexibleType
    union_list: List[StringOrInt]

# Create object with union types
obj = UnionTypes(
    string_or_int=42,
    string_or_none="text",
    flexible_field=True,
    union_list=["text", 123, "another", 456]
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "string_or_int": 42,
#   "string_or_none": "text",
#   "flexible_field": true,
#   "union_list": ["text", 123, "another", 456]
# }

# Deserialize
restored = load(data, UnionTypes)
print(type(restored.string_or_int))  # <class 'int'>
print(restored.flexible_field)  # True
print(restored.union_list[1])  # 123
```

## NewType Aliases

### Type-Safe Aliases

```python
from dataclasses import dataclass
from typing import NewType, List

# Define NewType aliases
UserId = NewType('UserId', int)
Email = NewType('Email', str)
Username = NewType('Username', str)

@dataclass
class NewTypeTypes:
    user_id: UserId
    email: Email
    username: Username
    user_ids: List[UserId]

# Create object with NewType aliases
obj = NewTypeTypes(
    user_id=UserId(1),
    email=Email("john@example.com"),
    username=Username("john_doe"),
    user_ids=[UserId(1), UserId(2), UserId(3)]
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "user_id": 1,
#   "email": "john@example.com",
#   "username": "john_doe",
#   "user_ids": [1, 2, 3]
# }

# Deserialize
restored = load(data, NewTypeTypes)
print(restored.user_id)  # 1 (type: int, but semantically UserId)
print(restored.email)  # "john@example.com"
```

## Literal Types

### String Literals

```python
from dataclasses import dataclass
from typing import Literal

# Define literal types
Status = Literal["active", "inactive", "pending"]
Environment = Literal["development", "staging", "production"]
LogLevel = Literal["debug", "info", "warning", "error"]

@dataclass
class LiteralTypes:
    status: Status
    environment: Environment
    log_level: LogLevel

# Create object with literal types
obj = LiteralTypes(
    status="active",
    environment="development",
    log_level="debug"
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "status": "active",
#   "environment": "development",
#   "log_level": "debug"
# }

# Deserialize
restored = load(data, LiteralTypes)
print(restored.status)  # "active"
print(restored.environment)  # "development"
```

## Generic Types

### Generic Containers

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Dict

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

@dataclass
class DataCollection(Generic[T]):
    items: List[T]
    total: int

# Create generic objects
string_container = Container("Hello", {"type": "string"})
int_container = Container(42, {"type": "integer"})
kv_pair = KeyValuePair("name", "John")
collection = DataCollection([1, 2, 3, 4, 5], 5)

# Serialize
string_data = dump(string_container)
int_data = dump(int_container)
kv_data = dump(kv_pair)
collection_data = dump(collection)

print(string_data)
# Output:
# {
#   "data": "Hello",
#   "metadata": {"type": "string"}
# }

print(kv_data)
# Output:
# {
#   "key": "name",
#   "value": "John"
# }

# Deserialize
restored_string = load(string_data, Container[str])
restored_kv = load(kv_data, KeyValuePair)
restored_collection = load(collection_data, DataCollection[int])

print(restored_string.data)  # "Hello"
print(restored_kv.key)  # "name"
print(restored_collection.total)  # 5
```

## Complex Nested Types

### Mixed Type Structures

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Complex union type
ValueType = Union[str, int, float, bool, None]

@dataclass
class ComplexTypes:
    # Basic types
    name: str
    count: int
    is_valid: bool
    
    # Collections
    tags: List[str]
    metadata: Dict[str, ValueType]
    
    # Optional fields
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    
    # Enum
    status: Status = Status.ACTIVE
    
    # Nested structures
    nested_data: Optional[Dict[str, List[Dict[str, any]]]] = None

# Create complex object
obj = ComplexTypes(
    name="Complex Object",
    count=42,
    is_valid=True,
    tags=["python", "json", "complex"],
    metadata={
        "version": "1.0",
        "score": 95.5,
        "enabled": True,
        "description": None
    },
    description="A complex type example",
    created_at=datetime.now(),
    nested_data={
        "group1": [
            {"id": 1, "value": "A"},
            {"id": 2, "value": "B"}
        ],
        "group2": [
            {"id": 3, "value": "C"}
        ]
    }
)

# Serialize
data = dump(obj)
print(data)
# Output:
# {
#   "name": "Complex Object",
#   "count": 42,
#   "is_valid": true,
#   "tags": ["python", "json", "complex"],
#   "metadata": {
#     "version": "1.0",
#     "score": 95.5,
#     "enabled": true,
#     "description": null
#   },
#   "description": "A complex type example",
#   "created_at": "2025-01-14T10:30:00",
#   "status": "active",
#   "nested_data": {
#     "group1": [
#       {"id": 1, "value": "A"},
#       {"id": 2, "value": "B"}
#     ],
#     "group2": [
#       {"id": 3, "value": "C"}
#     ]
#   }
# }

# Deserialize
restored = load(data, ComplexTypes)
print(restored.name)  # "Complex Object"
print(restored.status)  # Status.ACTIVE
print(restored.nested_data["group1"][0]["value"])  # "A"
```

## Type Validation

### Type Checking

```python
from dataclasses import dataclass
from typing import List, Dict
from jsonport import load, DeserializationError

@dataclass
class ValidationTest:
    name: str
    age: int
    scores: List[float]
    metadata: Dict[str, str]

# Valid data
valid_data = {
    "name": "John",
    "age": 30,
    "scores": [95.5, 87.2, 92.1],
    "metadata": {"department": "engineering"}
}

# Invalid data (wrong types)
invalid_data = {
    "name": "John",
    "age": "thirty",  # Should be int
    "scores": [95.5, 87.2, 92.1],
    "metadata": {"department": "engineering"}
}

# Load valid data
try:
    valid_obj = load(valid_data, ValidationTest)
    print("Valid data loaded successfully")
except DeserializationError as e:
    print(f"Error loading valid data: {e}")

# Load invalid data
try:
    invalid_obj = load(invalid_data, ValidationTest)
except DeserializationError as e:
    print(f"Error loading invalid data: {e}")
    # Output: Error loading invalid data: Cannot deserialize 'thirty' to int
```

This comprehensive guide covers all the types supported by JsonPort, including basic types, collections, datetime objects, enums, optional types, union types, and complex nested structures. 