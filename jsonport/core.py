"""
Core module for JsonPort 2.0.
High-performance serialization and deserialization library for Python.
"""

import json
from typing import Any, Optional, Type, TypeVar, Union

from .deserializers import _deserialize_dataclass, deserialize
from .exceptions import (
    ConfigurationError,
    DeserializationError,
    JsonPortError,
    SerializationError,
)
from .file_io import dump_file, dump_stream, load_file, load_stream
from .inspection import (
    get_cached_type_hints,
    unwrap_optional,
)
from .registry import (
    Registry,
    clear_registry,
    default_registry,
    deserializer,
    get_default_registry,
    get_deserializer,
    get_serializer,
    register_deserializer,
    register_serializer,
    serializer,
)
from .serializers import JsonPortEncoder, _serialize_dataclass, serialize

T = TypeVar("T")

# Backward compatibility aliases for internal functions
_get_cached_type_hints = get_cached_type_hints
_get_cached_optional_type = unwrap_optional
_serialize_value = serialize
_deserialize_value = deserialize


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


def dump(obj: Any, **kwargs: Any) -> Any:
    """
    Serialize a Python object to a JSON-serializable structure (dict, list, primitive).

    This function handles complex Python objects including dataclasses,
    collections, datetime objects, enums, UUID, Decimal, Path, bytes, IP, etc.,
    converting them to JSON-compatible formats.

    Args:
        obj: Object to serialize
        **kwargs: Optional serialization parameters

    Returns:
        JSON-serializable dictionary, list, or primitive value
    """
    return serialize(obj, **kwargs)


def dumps(
    obj: Any,
    *,
    indent: Optional[int] = None,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> str:
    """
    Serialize a Python object directly to a JSON string.

    Args:
        obj: Object to serialize
        indent: Indentation level for pretty-printing (None for compact)
        ensure_ascii: Whether to escape non-ASCII characters
        **kwargs: Optional serialization parameters

    Returns:
        str: JSON formatted string
    """
    data = serialize(obj, **kwargs)
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def load(data: Any, target_class: Type[T], **kwargs: Any) -> T:
    """
    Deserialize a JSON data structure (dict, list, primitive) to a Python object.

    Args:
        data: Data structure to deserialize
        target_class: Target class for deserialization
        **kwargs: Optional deserialization parameters (e.g. strict=True)

    Returns:
        Instance of the target class
    """
    return deserialize(data, target_class, **kwargs)  # type: ignore[no-any-return]


def loads(
    s: Union[str, bytes],
    target_class: Type[T],
    **kwargs: Any,
) -> T:
    """
    Deserialize a JSON string directly to an instance of target_class.

    Args:
        s: JSON string or bytes to deserialize
        target_class: Target class for deserialization
        **kwargs: Optional deserialization parameters (e.g. strict=True)

    Returns:
        Instance of the target class
    """
    data = json.loads(s)
    return deserialize(data, target_class, **kwargs)  # type: ignore[no-any-return]


__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "dump_file",
    "load_file",
    "dump_stream",
    "load_stream",
    "is_serializable",
    "register_serializer",
    "register_deserializer",
    "serializer",
    "deserializer",
    "get_serializer",
    "get_deserializer",
    "clear_registry",
    "Registry",
    "get_default_registry",
    "JsonPortEncoder",
    "JsonPortError",
    "SerializationError",
    "DeserializationError",
    "ConfigurationError",
]
