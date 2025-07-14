import json
import datetime
import os
import gzip
from typing import Any, Type, TypeVar, get_type_hints, get_origin, get_args, Union, Optional, List, Tuple, Set, Dict, Generic
from dataclasses import is_dataclass, asdict
from enum import Enum
from functools import lru_cache

T = TypeVar('T')

class JsonPortError(Exception):
    """Custom error for the jsonport library."""
    pass

# Cache for type hints to avoid repeated lookups
@lru_cache(maxsize=1024)
def _get_cached_type_hints(cls: Type) -> Dict[str, Type]:
    """Cache type hints for better performance."""
    return get_type_hints(cls)

# Cache for optional type resolution
@lru_cache(maxsize=512)
def _get_cached_optional_type(target_type: Type) -> Type:
    """Cache optional type resolution for better performance."""
    if get_origin(target_type) is Union:
        args = get_args(target_type)
        if len(args) == 2 and type(None) in args:
            return next(arg for arg in args if arg is not type(None))
    return target_type

def is_serializable(obj: Any) -> bool:
    """
    Check if an object is serializable by jsonport.
    
    Args:
        obj: Object to check for serializability
        
    Returns:
        bool: True if object can be serialized, False otherwise
    """
    try:
        dump(obj)
        return True
    except Exception:
        return False

class JsonPortEncoder(json.JSONEncoder):
    """Custom encoder for special types with improved performance."""
    
    def default(self, obj: Any) -> Any:
        """
        Convert special types to JSON-serializable format.
        
        Args:
            obj: Object to encode
            
        Returns:
            JSON-serializable representation of the object
        """
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif is_dataclass(obj):
            return asdict(obj)
        elif isinstance(obj, set):
            return list(obj)
        return str(obj)

def _serialize_dataclass(obj: Any) -> dict:
    """
    Serialize a dataclass object to dictionary.
    
    Args:
        obj: Dataclass instance to serialize
        
    Returns:
        dict: Serialized dataclass as dictionary
        
    Raises:
        JsonPortError: If object is not a dataclass
    """
    if not is_dataclass(obj):
        raise JsonPortError("Object must be a dataclass")
    
    result = {}
    type_hints = _get_cached_type_hints(type(obj))
    
    for field_name, field_value in obj.__dict__.items():
        if field_name in type_hints:
            result[field_name] = _serialize_value(field_value, type_hints[field_name])
        else:
            result[field_name] = _serialize_value(field_value)
    
    return result

def _serialize_value(value: Any, expected_type: Optional[Type] = None) -> Any:
    """
    Serialize a value with type-aware conversion.
    
    Args:
        value: Value to serialize
        expected_type: Expected type for proper serialization
        
    Returns:
        Serialized value
    Raises:
        JsonPortError: If value is not serializable
    """
    if value is None:
        return None
    
    # Handle collections with type information
    if isinstance(value, list):
        item_type = get_args(expected_type)[0] if expected_type and get_origin(expected_type) is list else None
        return [_serialize_value(item, item_type) for item in value]
    
    if isinstance(value, tuple):
        if expected_type and get_origin(expected_type) is tuple:
            args = get_args(expected_type)
            if len(args) == len(value):
                return [_serialize_value(item, args[i]) for i, item in enumerate(value)]
        return [_serialize_value(item) for item in value]
    
    if isinstance(value, set):
        item_type = get_args(expected_type)[0] if expected_type and get_origin(expected_type) is set else None
        return [_serialize_value(item, item_type) for item in value]
    
    if isinstance(value, dict):
        key_type, val_type = (None, None)
        if expected_type and get_origin(expected_type) is dict:
            key_type, val_type = get_args(expected_type)
        return {_serialize_value(k, key_type): _serialize_value(v, val_type) for k, v in value.items()}
    
    # Handle special types
    if is_dataclass(value):
        return _serialize_dataclass(value)
    
    if isinstance(value, (str, int, float, bool)):
        return value
    
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    
    if isinstance(value, Enum):
        return value.value
    
    # If not serializable, raise error
    raise JsonPortError(f"Type {type(value).__name__} is not serializable by JsonPort")

def _deserialize_value(value: Any, target_type: Type) -> Any:
    """
    Deserialize a value to the target type.
    
    Args:
        value: Value to deserialize
        target_type: Target type for deserialization
        
    Returns:
        Deserialized value of the target type
    """
    if value is None:
        return None
    
    base_type = _get_cached_optional_type(target_type)
    
    # Handle primitive types
    if base_type in (str, int, float, bool):
        return base_type(value)
    
    # Handle datetime types
    if base_type == datetime.datetime:
        if isinstance(value, str):
            return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value
    
    if base_type == datetime.date:
        if isinstance(value, str):
            return datetime.date.fromisoformat(value)
        return value
    
    if base_type == datetime.time:
        if isinstance(value, str):
            return datetime.time.fromisoformat(value)
        return value
    
    # Handle collections
    if get_origin(base_type) is list:
        item_type = get_args(base_type)[0]
        return [_deserialize_value(item, item_type) for item in value]
    
    if get_origin(base_type) is tuple:
        args = get_args(base_type)
        if len(args) == len(value):
            return tuple(_deserialize_value(item, args[i]) for i, item in enumerate(value))
        return tuple(_deserialize_value(item, args[0]) for item in value)
    
    if get_origin(base_type) is set:
        item_type = get_args(base_type)[0]
        return set(_deserialize_value(item, item_type) for item in value)
    
    if get_origin(base_type) is dict:
        key_type, val_type = get_args(base_type)
        return {_deserialize_value(k, key_type): _deserialize_value(v, val_type) for k, v in value.items()}
    
    # Handle dataclasses and enums
    if is_dataclass(base_type):
        return _deserialize_dataclass(value, base_type)
    
    if isinstance(base_type, type) and issubclass(base_type, Enum):
        return base_type(value)
    
    return value

def _deserialize_dataclass(data: dict, target_class: Type[T]) -> T:
    """
    Deserialize a dictionary to a dataclass instance.
    
    Args:
        data: Dictionary data to deserialize
        target_class: Target dataclass type
        
    Returns:
        Instance of the target dataclass
        
    Raises:
        JsonPortError: If target class is not a dataclass
    """
    if not is_dataclass(target_class):
        raise JsonPortError("Target class must be a dataclass")
    
    type_hints = _get_cached_type_hints(target_class)
    kwargs = {}
    
    for field_name, field_type in type_hints.items():
        if field_name in data:
            kwargs[field_name] = _deserialize_value(data[field_name], field_type)
    
    return target_class(**kwargs)

def dump(obj: Any) -> Any:
    """
    Serialize a Python object to a JSON-serializable dictionary.
    
    This function handles complex Python objects including dataclasses, 
    collections, datetime objects, and enums, converting them to 
    JSON-compatible formats.
    
    Args:
        obj: Object to serialize (can be dataclass, list, tuple, set, dict, or primitive)
        
    Returns:
        JSON-serializable dictionary, list, or primitive value
        
    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>> user = User("John", 30)
        >>> dump(user)
        {'name': 'John', 'age': 30}
    """
    if is_dataclass(obj):
        return _serialize_dataclass(obj)
    elif isinstance(obj, (list, tuple, set)):
        return [_serialize_value(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _serialize_value(v) for k, v in obj.items()}
    else:
        return _serialize_value(obj)

def load(data: Any, target_class: Type[T]) -> T:
    """
    Deserialize a JSON dictionary/list to a Python object.
    
    This function reconstructs Python objects from JSON data, 
    handling type conversion and nested structures.
    
    Args:
        data: Dictionary/list to deserialize
        target_class: Target class for deserialization
        
    Returns:
        Instance of the target class
        
    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>> data = {'name': 'John', 'age': 30}
        >>> user = load(data, User)
        >>> user.name
        'John'
    """
    if is_dataclass(target_class):
        return _deserialize_dataclass(data, target_class)
    else:
        return _deserialize_value(data, target_class)

def dump_file(obj: Any, path: str, overwrite: bool = True) -> None:
    """
    Serialize a Python object and save it to a JSON file.
    
    Creates directories if they don't exist and supports both regular JSON
    and gzipped JSON files (.gz extension).
    
    Args:
        obj: Object to serialize
        path: Path to the JSON file
        overwrite: If False, raises error when file already exists
        
    Raises:
        JsonPortError: If file exists and overwrite=False, or if path is invalid
        
    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Config:
        ...     api_key: str
        ...     timeout: int
        >>> config = Config("abc123", 30)
        >>> dump_file(config, "config.json")
        >>> dump_file(config, "config.json.gz")  # Compressed file
    """
    data = dump(obj)
    
    # Create directory if it doesn't exist (only if path has directory)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    if not overwrite and os.path.exists(path):
        raise JsonPortError(f"File already exists: {path}")
    
    if path.endswith('.gz'):
        with gzip.open(path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def load_file(path: str, target_class: Type[T]) -> T:
    """
    Load a JSON file (or gzipped JSON) and deserialize to the desired type.
    
    Automatically detects gzipped files by .gz extension and handles
    decompression transparently.
    
    Args:
        path: Path to the JSON file
        target_class: Target class for deserialization
        
    Returns:
        Instance of the target class
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        JsonPortError: If deserialization fails
        
    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Config:
        ...     api_key: str
        ...     timeout: int
        >>> config = load_file("config.json", Config)
        >>> config = load_file("config.json.gz", Config)  # Compressed file
    """
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    return load(data, target_class) 