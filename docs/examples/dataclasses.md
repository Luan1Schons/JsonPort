# Dataclasses

Learn how to work with Python dataclasses using JsonPort.

## Basic Dataclass Serialization

```python
from dataclasses import dataclass
from jsonport import dump, load

@dataclass
class User:
    name: str
    age: int
    email: str

# Create a user
user = User("John Doe", 30, "john@example.com")

# Serialize to dictionary
data = dump(user)
print(data)
# Output: {"name": "John Doe", "age": 30, "email": "john@example.com"}

# Deserialize back to object
restored_user = load(data, User)
print(restored_user.name)  # "John Doe"
```

## Dataclass with Default Values

```python
@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str = ""
    in_stock: bool = True
    tags: list[str] = None

# Create with minimal data
product1 = Product(1, "Laptop", 999.99)
print(product1.description)  # ""
print(product1.in_stock)     # True

# Create with full data
product2 = Product(
    id=2,
    name="Mouse",
    price=29.99,
    description="Wireless mouse",
    in_stock=False,
    tags=["electronics", "wireless"]
)

# Serialize both
data1 = dump(product1)
data2 = dump(product2)
```

## Nested Dataclasses

```python
@dataclass
class Address:
    street: str
    city: str
    country: str
    postal_code: str

@dataclass
class Customer:
    id: int
    name: str
    email: str
    address: Address
    phone: str = None

# Create nested structure
customer = Customer(
    id=1,
    name="Jane Smith",
    email="jane@example.com",
    address=Address(
        street="123 Main St",
        city="New York",
        country="USA",
        postal_code="10001"
    ),
    phone="+1-555-0123"
)

# Serialize nested structure
data = dump(customer)
print(data)
# Output: {
#   "id": 1,
#   "name": "Jane Smith",
#   "email": "jane@example.com",
#   "address": {
#     "street": "123 Main St",
#     "city": "New York",
#     "country": "USA",
#     "postal_code": "10001"
#   },
#   "phone": "+1-555-0123"
# }

# Deserialize nested structure
restored_customer = load(data, Customer)
print(restored_customer.address.city)  # "New York"
```

## Dataclass with Collections

```python
@dataclass
class Order:
    id: int
    customer_id: int
    items: list[str]
    quantities: dict[str, int]
    tags: set[str]
    total: float

order = Order(
    id=1001,
    customer_id=1,
    items=["laptop", "mouse", "keyboard"],
    quantities={"laptop": 1, "mouse": 2, "keyboard": 1},
    tags={"electronics", "office", "urgent"},
    total=1299.97
)

# Serialize with collections
data = dump(order)
print(data["items"])      # ["laptop", "mouse", "keyboard"]
print(data["quantities"]) # {"laptop": 1, "mouse": 2, "keyboard": 1}
print(data["tags"])       # ["electronics", "office", "urgent"]

# Deserialize with proper type restoration
restored_order = load(data, Order)
print(type(restored_order.items))      # <class 'list'>
print(type(restored_order.quantities)) # <class 'dict'>
print(type(restored_order.tags))       # <class 'set'>
```

## Dataclass with Inheritance

```python
@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    is_vaccinated: bool

@dataclass
class Cat(Animal):
    color: str
    is_indoor: bool

# Create instances
dog = Dog("Buddy", 3, "Golden Retriever", True)
cat = Cat("Whiskers", 2, "Orange", True)

# Serialize different types
dog_data = dump(dog)
cat_data = dump(cat)

# Deserialize with proper type
restored_dog = load(dog_data, Dog)
restored_cat = load(cat_data, Cat)

print(restored_dog.breed)  # "Golden Retriever"
print(restored_cat.color)  # "Orange"
```

## Dataclass with Custom Methods

```python
@dataclass
class Rectangle:
    width: float
    height: float
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

rect = Rectangle(5.0, 3.0)

# Serialize (methods are not serialized)
data = dump(rect)
print(data)  # {"width": 5.0, "height": 3.0}

# Deserialize and use methods
restored_rect = load(data, Rectangle)
print(restored_rect.area())      # 15.0
print(restored_rect.perimeter()) # 16.0
```

## Dataclass with Validation

```python
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
        if len(self.name.strip()) == 0:
            raise ValueError("Name cannot be empty")

# Valid user
try:
    user = ValidatedUser("John", 30, "john@example.com")
    data = dump(user)
    print("User created successfully")
except ValueError as e:
    print(f"Validation error: {e}")

# Invalid user
try:
    user = ValidatedUser("", -5, "invalid-email")
except ValueError as e:
    print(f"Validation error: {e}")
```

## Dataclass with Optional Fields

```python
from typing import Optional

@dataclass
class Profile:
    user_id: int
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None

# Minimal profile
profile1 = Profile(1, "john_doe")

# Full profile
profile2 = Profile(
    user_id=2,
    username="jane_smith",
    bio="Software developer and coffee enthusiast",
    avatar_url="https://example.com/avatar.jpg",
    website="https://janesmith.dev"
)

# Serialize both
data1 = dump(profile1)
data2 = dump(profile2)

print(data1)  # {"user_id": 1, "username": "john_doe", "bio": null, "avatar_url": null, "website": null}
print(data2)  # {"user_id": 2, "username": "jane_smith", "bio": "...", "avatar_url": "...", "website": "..."}
```

## Dataclass with Complex Types

```python
from typing import List, Dict, Tuple, Union
from datetime import datetime, date

@dataclass
class Event:
    id: int
    title: str
    date: date
    start_time: datetime
    attendees: List[str]
    metadata: Dict[str, Union[str, int, float]]
    coordinates: Tuple[float, float]

event = Event(
    id=1,
    title="Team Meeting",
    date=date(2024, 1, 15),
    start_time=datetime(2024, 1, 15, 14, 30),
    attendees=["alice", "bob", "charlie"],
    metadata={"room": "Conference A", "duration": 60, "priority": 1.0},
    coordinates=(40.7128, -74.0060)
)

# Serialize complex types
data = dump(event)
print(data["date"])        # "2024-01-15"
print(data["start_time"])  # "2024-01-15T14:30:00"
print(data["coordinates"]) # [40.7128, -74.0060]

# Deserialize with type preservation
restored_event = load(data, Event)
print(type(restored_event.date))        # <class 'datetime.date'>
print(type(restored_event.start_time))  # <class 'datetime.datetime'>
print(type(restored_event.coordinates)) # <class 'tuple'>
```

## Best Practices

1. **Use type hints**: Always define proper type hints for optimal performance
2. **Handle optional fields**: Use `Optional[T]` for fields that might be None
3. **Add validation**: Use `__post_init__` for custom validation
4. **Use meaningful defaults**: Provide sensible default values
5. **Keep it simple**: Avoid complex nested structures when possible

## Next Steps

- [Enums](enums.md) - Working with enumerations
- [Collections](collections.md) - List, dict, set, and tuple handling
- [DateTime](datetime.md) - Date and time serialization
- [Complex Structures](complex-structures.md) - Advanced nested objects 