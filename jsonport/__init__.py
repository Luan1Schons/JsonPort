"""
JsonPort - High-performance serialization and deserialization library for Python.
"""

from .core import (
    ConfigurationError,
    DeserializationError,
    JsonPortEncoder,
    JsonPortError,
    Registry,
    SerializationError,
    clear_registry,
    deserializer,
    dump,
    dump_file,
    dump_stream,
    dumps,
    get_default_registry,
    get_deserializer,
    get_serializer,
    is_serializable,
    load,
    load_file,
    load_stream,
    loads,
    register_deserializer,
    register_serializer,
    serializer,
)

__version__ = "2.0.0"

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
    "__version__",
]
