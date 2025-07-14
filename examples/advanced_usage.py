#!/usr/bin/env python3
"""
Advanced usage example for JsonPort library.
Demonstrates complex nested structures and collections.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Set, Tuple, Optional, Any

from jsonport import dump, load, dump_file, load_file

# Define enums
class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    BOOKS = "books"
    CLOTHING = "clothing"
    FOOD = "food"

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Define nested dataclasses
@dataclass
class Address:
    street: str
    city: str
    state: str
    country: str
    postal_code: str

@dataclass
class Contact:
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None

@dataclass
class Product:
    id: int
    name: str
    price: float
    category: ProductCategory
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    dimensions: Optional[Tuple[float, float, float]] = None

@dataclass
class Customer:
    id: int
    name: str
    email: str
    address: Address
    contacts: List[Contact]
    preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class OrderItem:
    product: Product
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Order:
    id: int
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus
    order_date: datetime
    shipping_address: Address
    billing_address: Optional[Address] = None
    notes: Optional[str] = None
    
    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)
    
    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

def main():
    """Demonstrate advanced JsonPort functionality."""
    print("🚀 JsonPort Advanced Usage Example")
    print("=" * 50)
    
    # Create complex nested structure
    print("📦 Creating complex nested structure...")
    
    # Create addresses
    customer_address = Address(
        street="123 Main St",
        city="San Francisco",
        state="CA",
        country="USA",
        postal_code="94105"
    )
    
    shipping_address = Address(
        street="456 Oak Ave",
        city="San Francisco",
        state="CA",
        country="USA",
        postal_code="94102"
    )
    
    # Create contacts
    contacts = [
        Contact("john@example.com", "+1-555-0123"),
        Contact("support@example.com", website="https://example.com")
    ]
    
    # Create customer
    customer = Customer(
        id=1,
        name="John Doe",
        email="john@example.com",
        address=customer_address,
        contacts=contacts,
        preferences={"newsletter": True, "language": "en"}
    )
    
    # Create products
    products = [
        Product(
            id=1,
            name="Laptop",
            price=999.99,
            category=ProductCategory.ELECTRONICS,
            tags={"portable", "computer", "tech"},
            metadata={"brand": "TechCorp", "warranty": 2},
            dimensions=(35.5, 24.0, 2.1)
        ),
        Product(
            id=2,
            name="Python Programming Book",
            price=49.99,
            category=ProductCategory.BOOKS,
            tags={"programming", "python", "education"},
            metadata={"author": "John Smith", "pages": 400}
        )
    ]
    
    # Create order items
    order_items = [
        OrderItem(products[0], 1, 999.99),
        OrderItem(products[1], 2, 49.99)
    ]
    
    # Create order
    order = Order(
        id=1001,
        customer=customer,
        items=order_items,
        status=OrderStatus.CONFIRMED,
        order_date=datetime.now(),
        shipping_address=shipping_address,
        notes="Please deliver during business hours"
    )
    
    print(f"Order ID: {order.id}")
    print(f"Customer: {order.customer.name}")
    print(f"Total Amount: ${order.total_amount:.2f}")
    print(f"Item Count: {order.item_count}")
    print(f"Status: {order.status.value}")
    
    # Serialize complex structure
    print("\n📤 Serializing complex structure...")
    data = dump(order)
    print(f"Serialized data keys: {list(data.keys())}")
    print(f"Customer data: {data['customer']['name']}")
    print(f"Items count: {len(data['items'])}")
    
    # Deserialize complex structure
    print("\n📥 Deserializing complex structure...")
    restored_order = load(data, Order)
    print(f"Restored Order ID: {restored_order.id}")
    print(f"Restored Customer: {restored_order.customer.name}")
    print(f"Restored Total Amount: ${restored_order.total_amount:.2f}")
    print(f"Restored Status: {restored_order.status.value}")
    
    # Verify nested structures
    print(f"Customer Address: {restored_order.customer.address.street}")
    print(f"First Product: {restored_order.items[0].product.name}")
    print(f"Product Tags: {restored_order.items[0].product.tags}")
    
    # File operations with complex data
    print("\n💾 Testing file operations with complex data...")
    dump_file(order, "complex_order.json")
    loaded_order = load_file("complex_order.json", Order)
    print(f"Loaded complex order: {loaded_order.customer.name}")
    
    # Compression with complex data
    print("\n🗜️ Testing compression with complex data...")
    dump_file(order, "complex_order.json.gz")
    compressed_order = load_file("complex_order.json.gz", Order)
    print(f"Loaded compressed complex order: {compressed_order.customer.name}")
    
    print("\n✅ Advanced operations completed successfully!")

if __name__ == "__main__":
    main() 