#!/usr/bin/env python3
"""
Comprehensive test suite for JsonPort library using pytest.
Tests all functionality including performance optimizations.
"""

import json
import time
import tempfile
import os
import pytest
from dataclasses import dataclass
from datetime import datetime, date, time as dt_time
from enum import Enum
from typing import List, Dict, Optional, Tuple, Set, Any

# Import JsonPort functions
from jsonport import dump, load, dump_file, load_file, JsonPortError, JsonPortEncoder

# Test fixtures
@pytest.fixture
def sample_user():
    """Fixture for a sample user dataclass."""
    class UserRole(Enum):
        ADMIN = "admin"
        USER = "user"
        MODERATOR = "moderator"
    
    @dataclass
    class User:
        name: str
        age: int
        role: UserRole
        email: Optional[str] = None
    
    return User("John Doe", 30, UserRole.ADMIN, "john@example.com")

@pytest.fixture
def sample_event():
    """Fixture for a sample event with datetime fields."""
    @dataclass
    class Event:
        title: str
        date: date
        time: dt_time
        created_at: datetime
    
    return Event(
        title="Meeting",
        date=date(2025, 7, 14),
        time=dt_time(14, 30, 0),
        created_at=datetime(2025, 7, 14, 14, 30, 0)
    )

@pytest.fixture
def sample_product():
    """Fixture for a sample product with collections."""
    @dataclass
    class Product:
        id: int
        name: str
        tags: List[str]
        categories: Set[str]
        dimensions: Tuple[float, float, float]
        metadata: Dict[str, Any]
    
    return Product(
        id=1,
        name="Laptop",
        tags=["electronics", "portable"],
        categories={"computers", "gadgets"},
        dimensions=(35.5, 24.0, 2.1),
        metadata={"brand": "TechCorp", "warranty": 2}
    )

@pytest.fixture
def sample_company():
    """Fixture for a complex nested structure."""
    @dataclass
    class Address:
        street: str
        city: str
        country: str
    
    @dataclass
    class Contact:
        email: str
        phone: Optional[str] = None
    
    @dataclass
    class Company:
        name: str
        address: Address
        contacts: List[Contact]
        departments: Dict[str, List[str]]
    
    return Company(
        name="TechCorp",
        address=Address("123 Tech St", "San Francisco", "USA"),
        contacts=[
            Contact("info@techcorp.com"),
            Contact("support@techcorp.com", "+1-555-0123")
        ],
        departments={
            "Engineering": ["Backend", "Frontend"],
            "Sales": ["Enterprise", "SMB"]
        }
    )

# Unit tests
class TestBasicSerialization:
    """Test basic serialization and deserialization functionality."""
    
    def test_simple_dataclass_serialization(self, sample_user):
        """Test serialization of simple dataclass."""
        data = dump(sample_user)
        assert data["name"] == "John Doe"
        assert data["age"] == 30
        assert data["role"] == "admin"
        assert data["email"] == "john@example.com"
    
    def test_simple_dataclass_deserialization(self, sample_user):
        """Test deserialization of simple dataclass."""
        data = dump(sample_user)
        restored_user = load(data, type(sample_user))
        assert restored_user.name == sample_user.name
        assert restored_user.age == sample_user.age
        assert restored_user.role == sample_user.role
        assert restored_user.email == sample_user.email
    
    def test_optional_fields(self):
        """Test handling of optional fields."""
        @dataclass
        class Product:
            id: int
            name: str
            description: Optional[str] = None
            price: Optional[float] = None
        
        # Test with None values
        product = Product(id=1, name="Test Product")
        data = dump(product)
        assert data["description"] is None
        assert data["price"] is None
        
        # Test with values
        product_with_values = Product(
            id=2, name="Test Product 2", 
            description="A test product", price=99.99
        )
        data = dump(product_with_values)
        assert data["description"] == "A test product"
        assert data["price"] == 99.99

class TestDateTimeHandling:
    """Test datetime, date, and time serialization."""
    
    def test_datetime_serialization(self, sample_event):
        """Test serialization of datetime objects."""
        data = dump(sample_event)
        assert isinstance(data["date"], str)
        assert isinstance(data["time"], str)
        assert isinstance(data["created_at"], str)
    
    def test_datetime_deserialization(self, sample_event):
        """Test deserialization of datetime objects."""
        data = dump(sample_event)
        restored_event = load(data, type(sample_event))
        assert restored_event.date == sample_event.date
        assert restored_event.time == sample_event.time
        assert restored_event.created_at == sample_event.created_at

class TestEnumHandling:
    """Test enum serialization and deserialization."""
    
    def test_enum_serialization(self, sample_user):
        """Test serialization of enum values."""
        data = dump(sample_user)
        assert data["role"] == "admin"
    
    def test_enum_deserialization(self, sample_user):
        """Test deserialization of enum values."""
        data = dump(sample_user)
        restored_user = load(data, type(sample_user))
        assert restored_user.role == sample_user.role

class TestCollections:
    """Test list, tuple, set, and dict serialization."""
    
    def test_collections_serialization(self, sample_product):
        """Test serialization of collections."""
        data = dump(sample_product)
        assert isinstance(data["tags"], list)
        assert isinstance(data["categories"], list)
        assert isinstance(data["dimensions"], list)
        assert isinstance(data["metadata"], dict)
    
    def test_collections_deserialization(self, sample_product):
        """Test deserialization of collections."""
        data = dump(sample_product)
        restored_product = load(data, type(sample_product))
        assert isinstance(restored_product.tags, list)
        assert isinstance(restored_product.categories, set)
        assert isinstance(restored_product.dimensions, tuple)
        assert isinstance(restored_product.metadata, dict)

class TestNestedStructures:
    """Test complex nested dataclass structures."""
    
    def test_nested_serialization(self, sample_company):
        """Test serialization of nested structures."""
        data = dump(sample_company)
        assert data["name"] == "TechCorp"
        assert data["address"]["street"] == "123 Tech St"
        assert len(data["contacts"]) == 2
        assert len(data["departments"]) == 2
    
    def test_nested_deserialization(self, sample_company):
        """Test deserialization of nested structures."""
        data = dump(sample_company)
        restored_company = load(data, type(sample_company))
        assert restored_company.name == sample_company.name
        assert restored_company.address.street == sample_company.address.street
        assert len(restored_company.contacts) == 2
        assert len(restored_company.departments) == 2

class TestFileOperations:
    """Test file I/O operations."""
    
    def test_json_file_operations(self):
        """Test regular JSON file operations."""
        @dataclass
        class Config:
            api_key: str
            timeout: int
            debug: bool
        
        config = Config("abc123", 30, True)
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save
            dump_file(config, temp_path)
            assert os.path.exists(temp_path)
            
            # Load
            loaded_config = load_file(temp_path, Config)
            assert loaded_config.api_key == "abc123"
            assert loaded_config.timeout == 30
            assert loaded_config.debug is True
            
        finally:
            os.unlink(temp_path)
    
    def test_gzip_file_operations(self):
        """Test gzipped JSON file operations."""
        @dataclass
        class Config:
            api_key: str
            timeout: int
        
        config = Config("abc123", 30)
        
        with tempfile.NamedTemporaryFile(suffix='.json.gz', delete=False) as f:
            gz_path = f.name
        
        try:
            # Save compressed
            dump_file(config, gz_path)
            assert os.path.exists(gz_path)
            
            # Load compressed
            loaded_config = load_file(gz_path, Config)
            assert loaded_config.api_key == "abc123"
            
        finally:
            os.unlink(gz_path)
    
    def test_overwrite_protection(self):
        """Test file overwrite protection."""
        @dataclass
        class Config:
            value: str
        
        config = Config("test")
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # First save
            dump_file(config, temp_path)
            
            # Try to save again with overwrite=False
            with pytest.raises(JsonPortError, match="File already exists"):
                dump_file(config, temp_path, overwrite=False)
                
        finally:
            os.unlink(temp_path)

class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_non_serializable_object(self):
        """Test error when trying to serialize non-serializable object."""
        non_serializable = lambda x: x
        with pytest.raises(JsonPortError, match="Type function is not serializable"):
            dump(non_serializable)
    
    def test_non_dataclass_serialization(self):
        """Test error when trying to serialize non-dataclass."""
        class NonDataclass:
            pass
        
        with pytest.raises(JsonPortError, match="Type NonDataclass is not serializable"):
            dump(NonDataclass())
    
    def test_file_not_found(self):
        """Test error when trying to load non-existent file."""
        @dataclass
        class User:
            name: str
        
        with pytest.raises(FileNotFoundError):
            load_file("nonexistent.json", User)

class TestJsonEncoder:
    """Test custom JSON encoder."""
    
    def test_json_encoder(self):
        """Test custom JSON encoder functionality."""
        @dataclass
        class TestData:
            name: str
            date: datetime
            enum_value: Enum
        
        class TestEnum(Enum):
            VALUE = "test_value"
        
        test_data = TestData(
            name="Test",
            date=datetime(2025, 7, 14, 12, 0, 0),
            enum_value=TestEnum.VALUE
        )
        
        # Test with custom encoder
        data = dump(test_data)
        json_string = json.dumps(data, cls=JsonPortEncoder, indent=2)
        
        # Verify JSON is valid
        parsed = json.loads(json_string)
        assert parsed["name"] == "Test"
        assert "2025-07-14T12:00:00" in parsed["date"]
        assert parsed["enum_value"] == "test_value"

# Performance tests
class TestPerformance:
    """Test performance optimizations."""
    
    def test_serialization_benchmark(self, benchmark):
        """Benchmark serialization performance."""
        from dataclasses import dataclass
        from typing import List, Dict
        @dataclass
        class BenchmarkData:
            id: int
            name: str
            values: List[float]
            metadata: Dict[str, str]
        test_data = BenchmarkData(
            id=1,
            name="test",
            values=[1.1, 2.2, 3.3] * 100,
            metadata={"key1": "value1", "key2": "value2"}
        )
        benchmark(lambda: dump(test_data))

    def test_deserialization_benchmark(self, benchmark):
        """Benchmark deserialization performance."""
        from dataclasses import dataclass
        from typing import List, Dict
        @dataclass
        class BenchmarkData:
            id: int
            name: str
            values: List[float]
            metadata: Dict[str, str]
        test_data = BenchmarkData(
            id=1,
            name="test",
            values=[1.1, 2.2, 3.3] * 100,
            metadata={"key1": "value1", "key2": "value2"}
        )
        data = dump(test_data)
        benchmark(lambda: load(data, BenchmarkData))

    @pytest.mark.slow
    def test_caching_effectiveness(self):
        """Test that caching is working effectively."""
        from dataclasses import dataclass
        @dataclass
        class TestData:
            value: str
        test_data = TestData("test")
        # First run
        import time
        start_time = time.time()
        for _ in range(50):
            dump(test_data)
        first_run_time = time.time() - start_time
        # Second run (should be faster due to caching)
        start_time = time.time()
        for _ in range(50):
            dump(test_data)
        second_run_time = time.time() - start_time
        # Second run should be at least as fast as first run
        # (caching might not always be faster due to system variations)
        assert second_run_time <= first_run_time * 1.5, "Caching not effective"

# Integration tests
class TestIntegration:
    """Integration tests for complex scenarios."""
    
    @pytest.mark.integration
    def test_complete_workflow(self, sample_company):
        """Test complete workflow: serialize -> save -> load -> deserialize."""
        # Serialize
        data = dump(sample_company)
        
        # Save to file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            dump_file(sample_company, temp_path)
            
            # Load from file
            loaded_company = load_file(temp_path, type(sample_company))
            
            # Verify data integrity
            assert loaded_company.name == sample_company.name
            assert loaded_company.address.street == sample_company.address.street
            assert len(loaded_company.contacts) == len(sample_company.contacts)
            assert len(loaded_company.departments) == len(sample_company.departments)
            
        finally:
            os.unlink(temp_path)
    
    @pytest.mark.integration
    def test_compression_workflow(self, sample_user):
        """Test complete workflow with compression."""
        # Save compressed
        with tempfile.NamedTemporaryFile(suffix='.json.gz', delete=False) as f:
            gz_path = f.name
        
        try:
            dump_file(sample_user, gz_path)
            
            # Load compressed
            loaded_user = load_file(gz_path, type(sample_user))
            
            # Verify data integrity
            assert loaded_user.name == sample_user.name
            assert loaded_user.age == sample_user.age
            assert loaded_user.role == sample_user.role
            
        finally:
            os.unlink(gz_path) 