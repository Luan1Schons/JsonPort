# File Operations

Learn how to work with files using JsonPort's built-in file I/O capabilities.

## Basic File Operations

### Saving Objects to Files

```python
from jsonport import dump_file, load_file
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

user = User("John Doe", 30, "john@example.com")

# Save to JSON file
dump_file(user, "user.json")

# Load from JSON file
loaded_user = load_file("user.json", User)
print(loaded_user.name)  # "John Doe"
```

### Overwriting Files

By default, `dump_file` overwrites existing files:

```python
# This will overwrite user.json if it exists
dump_file(user, "user.json")

# To prevent overwriting, set overwrite=False
try:
    dump_file(user, "user.json", overwrite=False)
except FileExistsError:
    print("File already exists!")
```

## Compression Support

JsonPort automatically handles gzip compression for files with `.gz` extension:

### Saving Compressed Files

```python
# Save with automatic gzip compression
dump_file(user, "user.json.gz")

# The file will be compressed automatically
# File size will be smaller than the original JSON
```

### Loading Compressed Files

```python
# Load compressed file (automatic decompression)
compressed_user = load_file("user.json.gz", User)
print(compressed_user.name)  # "John Doe"
```

### Compression Benefits

```python
import os

# Save uncompressed
dump_file(large_object, "data.json")
uncompressed_size = os.path.getsize("data.json")

# Save compressed
dump_file(large_object, "data.json.gz")
compressed_size = os.path.getsize("data.json.gz")

print(f"Uncompressed: {uncompressed_size} bytes")
print(f"Compressed: {compressed_size} bytes")
print(f"Compression ratio: {compressed_size/uncompressed_size:.2%}")
```

## Batch File Operations

### Saving Multiple Objects

```python
users = [
    User("Alice", 25, "alice@example.com"),
    User("Bob", 30, "bob@example.com"),
    User("Charlie", 35, "charlie@example.com")
]

# Save each user to separate files
for i, user in enumerate(users):
    dump_file(user, f"user_{i}.json")

# Or save all to a single file
import json
all_users_data = [dump(user) for user in users]
with open("all_users.json", "w") as f:
    json.dump(all_users_data, f, indent=2)
```

### Loading Multiple Objects

```python
# Load multiple files
loaded_users = []
for i in range(len(users)):
    user = load_file(f"user_{i}.json", User)
    loaded_users.append(user)

# Or load from single file
with open("all_users.json", "r") as f:
    all_users_data = json.load(f)
    
loaded_users = [load(user_data, User) for user_data in all_users_data]
```

## Error Handling

### File Not Found

```python
from jsonport import JsonPortError

try:
    user = load_file("nonexistent.json", User)
except FileNotFoundError:
    print("File not found")
    # Create default user
    user = User("Unknown", 0, "unknown@example.com")
```

### Invalid JSON

```python
try:
    user = load_file("corrupted.json", User)
except JsonPortError as e:
    print(f"Invalid JSON data: {e}")
    # Handle corrupted file
```

### Permission Errors

```python
try:
    dump_file(user, "/root/restricted.json")
except PermissionError:
    print("Permission denied")
    # Try alternative location
    dump_file(user, "./user.json")
```

## File Path Handling

### Relative and Absolute Paths

```python
import os

# Relative path (relative to current working directory)
dump_file(user, "data/user.json")

# Absolute path
dump_file(user, "/home/user/data/user.json")

# Using os.path for cross-platform compatibility
data_dir = os.path.join("data", "users")
os.makedirs(data_dir, exist_ok=True)
dump_file(user, os.path.join(data_dir, "user.json"))
```

### Creating Directories

```python
import os

# Create directory if it doesn't exist
os.makedirs("data/users", exist_ok=True)
dump_file(user, "data/users/user.json")
```

## Performance Considerations

### Large Files

For very large objects, consider streaming or chunking:

```python
# For large datasets, save in chunks
chunk_size = 1000
for i in range(0, len(large_dataset), chunk_size):
    chunk = large_dataset[i:i + chunk_size]
    dump_file(chunk, f"data_chunk_{i//chunk_size}.json")
```

### Compression Trade-offs

```python
import time

# Test compression vs speed
start = time.time()
dump_file(large_object, "data.json")
uncompressed_time = time.time() - start

start = time.time()
dump_file(large_object, "data.json.gz")
compressed_time = time.time() - start

print(f"Uncompressed save time: {uncompressed_time:.4f}s")
print(f"Compressed save time: {compressed_time:.4f}s")
```

## Integration Examples

### Configuration Files

```python
@dataclass
class AppConfig:
    debug: bool
    port: int
    database_url: str
    api_keys: dict[str, str]

# Load configuration
config = load_file("config.json", AppConfig)

# Save updated configuration
config.debug = True
dump_file(config, "config.json")
```

### Data Backup

```python
import shutil
from datetime import datetime

# Create backup with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f"backup_{timestamp}.json.gz"

# Save compressed backup
dump_file(data, backup_file)

# Verify backup
try:
    backup_data = load_file(backup_file, DataType)
    print("Backup verified successfully")
except Exception as e:
    print(f"Backup verification failed: {e}")
```

### Logging Data

```python
import logging
from jsonport import JsonPortError

logger = logging.getLogger(__name__)

def save_log_data(log_entry):
    try:
        dump_file(log_entry, "logs/application.json.gz")
    except JsonPortError as e:
        logger.error(f"Failed to save log: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving log: {e}")
```

## Best Practices

1. **Use compression for large files**: `.gz` extension for automatic compression
2. **Handle errors gracefully**: Always catch `FileNotFoundError` and `JsonPortError`
3. **Use meaningful file names**: Include timestamps or version numbers
4. **Create directories**: Use `os.makedirs()` with `exist_ok=True`
5. **Verify file operations**: Check if files were created successfully
6. **Use absolute paths**: For critical operations, use absolute paths

## Next Steps

- [Advanced Usage](advanced-usage.md) - Explore advanced features
- [Examples](examples/) - More practical examples
- [API Reference](api/) - Complete API documentation 