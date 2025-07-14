#!/usr/bin/env python3
"""
Basic usage example for JsonPort library.
Demonstrates simple serialization and deserialization.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from jsonport import dump, load, dump_file, load_file

# Define an enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

# Define a simple dataclass
@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None
    role: UserRole = UserRole.USER
    created_at: Optional[datetime] = None
    tags: List[str] = None

def main():
    """Demonstrate basic JsonPort functionality."""
    print("🚀 JsonPort Basic Usage Example")
    print("=" * 40)
    
    # Create a user instance
    user = User(
        name="John Doe",
        age=30,
        email="john@example.com",
        role=UserRole.ADMIN,
        created_at=datetime.now(),
        tags=["developer", "python", "backend"]
    )
    
    print(f"Original user: {user.name}, {user.age} years old, {user.role.value}")
    print(f"Email: {user.email}")
    print(f"Created: {user.created_at}")
    print(f"Tags: {user.tags}")
    
    # Serialize to dictionary
    print("\n📤 Serializing user...")
    data = dump(user)
    print(f"Serialized data: {data}")
    
    # Deserialize back to object
    print("\n📥 Deserializing user...")
    restored_user = load(data, User)
    print(f"Restored user: {restored_user.name}, {restored_user.age} years old, {restored_user.role.value}")
    print(f"Email: {restored_user.email}")
    print(f"Created: {restored_user.created_at}")
    print(f"Tags: {restored_user.tags}")
    
    # File operations
    print("\n💾 Testing file operations...")
    dump_file(user, "user.json")
    loaded_user = load_file("user.json", User)
    print(f"Loaded from file: {loaded_user.name}")
    
    # Compression
    print("\n🗜️ Testing compression...")
    dump_file(user, "user.json.gz")
    compressed_user = load_file("user.json.gz", User)
    print(f"Loaded from compressed file: {compressed_user.name}")
    
    print("\n✅ All operations completed successfully!")

if __name__ == "__main__":
    main() 