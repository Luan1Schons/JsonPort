# Performance

JsonPort is designed for high performance with intelligent caching and optimizations. This guide covers performance characteristics, optimization techniques, and benchmarking.

## Performance Characteristics

### Caching System

JsonPort uses intelligent caching to improve performance:

- **Type hints cache**: Stores resolved type hints (max 1024 entries)
- **Optional type cache**: Caches resolved Optional types (max 512 entries)
- **Enum cache**: Caches enum value mappings
- **Dataclass field cache**: Caches dataclass field information

### Memory Usage

```python
from jsonport import dump, load
import sys

# Memory usage example
@dataclass
class User:
    name: str
    age: int
    email: str

user = User("John", 30, "john@example.com")

# Serialize
data = dump(user)
print(f"Serialized size: {sys.getsizeof(data)} bytes")

# Deserialize
restored_user = load(data, User)
print(f"Object size: {sys.getsizeof(restored_user)} bytes")
```

## Performance Optimization

### 1. Reuse Objects

```python
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int
    timeout: float

# Good: Reuse the same class
config = Config("localhost", 8080, 30.0)
data = dump(config)
restored_config = load(data, Config)

# Avoid: Creating new classes frequently
# This bypasses caching benefits
```

### 2. Use Type Hints Consistently

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

# Good: Consistent type hints
@dataclass
class User:
    name: str
    age: int
    tags: List[str]
    metadata: Optional[Dict[str, str]] = None

# Avoid: Inconsistent or missing type hints
# This reduces caching effectiveness
```

### 3. Optimize Large Collections

```python
from jsonport import dump, load
from typing import List

@dataclass
class Item:
    id: int
    name: str
    value: float

# For large collections, consider chunking
def process_large_list(items: List[Item], chunk_size: int = 1000):
    results = []
    
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        chunk_data = dump(chunk)
        # Process chunk_data
        results.extend(load(chunk_data, List[Item]))
    
    return results
```

### 4. Use Efficient Data Structures

```python
from jsonport import dump, load
from typing import Dict, Set

# Good: Use appropriate collections
@dataclass
class UserProfile:
    name: str
    permissions: Set[str]  # Fast lookups
    settings: Dict[str, str]  # Key-value pairs

# Avoid: Using lists for set operations
# user.permissions: List[str]  # Slower lookups
```

## Benchmarking

### Basic Benchmark

```python
import time
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class BenchmarkData:
    id: int
    name: str
    values: list[float]
    metadata: dict[str, str]

def benchmark_serialization(data, iterations=1000):
    start_time = time.time()
    
    for _ in range(iterations):
        result = dump(data)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average serialization time: {avg_time * 1000:.2f} ms")

def benchmark_deserialization(data_dict, target_class, iterations=1000):
    start_time = time.time()
    
    for _ in range(iterations):
        result = load(data_dict, target_class)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average deserialization time: {avg_time * 1000:.2f} ms")

# Run benchmark
test_data = BenchmarkData(
    id=1,
    name="Test Object",
    values=[1.1, 2.2, 3.3, 4.4, 5.5],
    metadata={"key1": "value1", "key2": "value2"}
)

benchmark_serialization(test_data)
data_dict = dump(test_data)
benchmark_deserialization(data_dict, BenchmarkData)
```

### Comparison with Standard JSON

```python
import json
import time
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class ComplexObject:
    name: str
    age: int
    scores: list[float]
    metadata: dict[str, str]

def compare_performance():
    obj = ComplexObject(
        name="Test User",
        age=25,
        scores=[95.5, 87.2, 92.1, 88.9],
        metadata={"department": "engineering", "level": "senior"}
    )
    
    iterations = 10000
    
    # JsonPort
    start_time = time.time()
    for _ in range(iterations):
        data = dump(obj)
        restored = load(data, ComplexObject)
    jsonport_time = time.time() - start_time
    
    # Standard JSON (manual conversion)
    def to_dict(obj):
        return {
            "name": obj.name,
            "age": obj.age,
            "scores": obj.scores,
            "metadata": obj.metadata
        }
    
    def from_dict(data):
        return ComplexObject(
            name=data["name"],
            age=data["age"],
            scores=data["scores"],
            metadata=data["metadata"]
        )
    
    start_time = time.time()
    for _ in range(iterations):
        data = json.dumps(to_dict(obj))
        restored = from_dict(json.loads(data))
    std_json_time = time.time() - start_time
    
    print(f"JsonPort time: {jsonport_time:.3f}s")
    print(f"Standard JSON time: {std_json_time:.3f}s")
    print(f"JsonPort is {std_json_time/jsonport_time:.1f}x faster")

compare_performance()
```

### Memory Benchmark

```python
import sys
import psutil
import os
from jsonport import dump, load
from dataclasses import dataclass

@dataclass
class MemoryTest:
    data: list[str]
    metadata: dict[str, int]

def memory_benchmark():
    # Create large test data
    large_data = MemoryTest(
        data=["item_" + str(i) for i in range(10000)],
        metadata={f"key_{i}": i for i in range(1000)}
    )
    
    # Measure memory before
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    
    # Serialize
    serialized = dump(large_data)
    
    # Measure memory after serialization
    memory_after_serialize = process.memory_info().rss
    
    # Deserialize
    deserialized = load(serialized, MemoryTest)
    
    # Measure memory after deserialization
    memory_after_deserialize = process.memory_info().rss
    
    print(f"Memory before: {memory_before / 1024 / 1024:.1f} MB")
    print(f"Memory after serialization: {memory_after_serialize / 1024 / 1024:.1f} MB")
    print(f"Memory after deserialization: {memory_after_deserialize / 1024 / 1024:.1f} MB")
    print(f"Serialization overhead: {(memory_after_serialize - memory_before) / 1024 / 1024:.1f} MB")
    print(f"Total overhead: {(memory_after_deserialize - memory_before) / 1024 / 1024:.1f} MB")

memory_benchmark()
```

## Performance Tips

### 1. Profile Your Code

```python
import cProfile
import pstats
from jsonport import dump, load

def profile_serialization():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your serialization code here
    for i in range(1000):
        data = dump(complex_object)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### 2. Monitor Cache Hit Rates

```python
from jsonport.core import _type_hints_cache, _optional_cache

def print_cache_stats():
    print(f"Type hints cache size: {len(_type_hints_cache)}")
    print(f"Optional cache size: {len(_optional_cache)}")
    
    # Clear caches if needed
    _type_hints_cache.clear()
    _optional_cache.clear()
```

### 3. Use Appropriate Data Types

```python
from typing import Union, Literal
from dataclasses import dataclass

# Good: Use specific types
@dataclass
class Config:
    mode: Literal["development", "production", "testing"]
    timeout: Union[int, float]
    enabled: bool

# Avoid: Using Any or object
# mode: Any
# timeout: object
```

### 4. Batch Operations

```python
from jsonport import dump, load
from typing import List

def batch_serialize(objects: List[object]) -> List[dict]:
    """Serialize multiple objects efficiently"""
    return [dump(obj) for obj in objects]

def batch_deserialize(data_list: List[dict], target_class) -> List[object]:
    """Deserialize multiple objects efficiently"""
    return [load(data, target_class) for data in data_list]
```

## Performance Monitoring

### 1. Timing Decorator

```python
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def serialize_large_dataset(data):
    return dump(data)
```

### 2. Memory Monitoring

```python
import tracemalloc

def monitor_memory():
    tracemalloc.start()
    
    # Your code here
    result = dump(large_object)
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    
    tracemalloc.stop()
```

This comprehensive performance guide helps you optimize JsonPort usage and monitor performance characteristics in your applications. 