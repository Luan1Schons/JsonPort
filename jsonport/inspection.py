"""
Type introspection and metadata extraction for jsonport.
"""

import dataclasses
import datetime
import decimal
import ipaddress
import pathlib
import re
import types
import typing
import uuid
from dataclasses import dataclass, is_dataclass
from enum import Enum
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)


@dataclass(frozen=True)
class FieldInfo:
    """Introspected metadata for a dataclass field."""

    name: str
    type: Any
    default: Any
    default_factory: Any
    has_default: bool
    alias: Optional[str]
    exclude: bool
    serializer: Optional[Callable[[Any], Any]]
    deserializer: Optional[Callable[..., Any]]


@lru_cache(maxsize=1024)
def get_cached_type_hints(cls: Any) -> Dict[str, Any]:
    """
    Safely get and cache type hints for a class.
    Handles forward references and resolves them using module globals.
    """
    try:
        return get_type_hints(cls)
    except Exception:
        return getattr(cls, "__annotations__", {}).copy()


def safe_issubclass(tp: Any, cls: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
    """Safely check issubclass without failing on GenericAlias or typing constructs."""
    if not isinstance(tp, type):
        return False
    try:
        return issubclass(tp, cls)
    except TypeError:
        return False


def is_dataclass_type(tp: Any) -> bool:
    """Check if a type is a dataclass class (not an instance)."""
    return isinstance(tp, type) and is_dataclass(tp)


def is_dataclass_instance(obj: Any) -> bool:
    """Check if an object is an instance of a dataclass."""
    return is_dataclass(obj) and not isinstance(obj, type)


@lru_cache(maxsize=1024)
def get_dataclass_fields(cls: Any) -> Dict[str, FieldInfo]:
    """
    Get introspected field metadata for a dataclass type, cached for performance.
    """
    if not is_dataclass_type(cls):
        return {}

    hints = get_cached_type_hints(cast(Any, cls))
    raw_fields = dataclasses.fields(cls)
    result: Dict[str, FieldInfo] = {}

    for f in raw_fields:
        f_type = hints.get(f.name, f.type)
        metadata: Dict[str, Any] = dict(f.metadata) if f.metadata else {}
        has_default = (
            f.default is not dataclasses.MISSING
            or f.default_factory is not dataclasses.MISSING
        )
        alias = metadata.get("alias")
        exclude = bool(metadata.get("exclude", False))
        serializer = metadata.get("serializer")
        deserializer = metadata.get("deserializer")

        result[f.name] = FieldInfo(
            name=f.name,
            type=f_type,
            default=f.default,
            default_factory=f.default_factory,
            has_default=has_default,
            alias=alias if isinstance(alias, str) else None,
            exclude=exclude,
            serializer=serializer if callable(serializer) else None,
            deserializer=deserializer if callable(deserializer) else None,
        )
    return result


def is_union(tp: Any) -> bool:
    """Check if a type is a typing.Union or PEP 604 Union (type | type)."""
    origin = get_origin(tp)
    if origin is Union:
        return True
    if hasattr(types, "UnionType") and origin is types.UnionType:
        return True
    return False


def get_union_args(tp: Any) -> Tuple[Any, ...]:
    """Get the member types of a Union."""
    if is_union(tp):
        return get_args(tp)
    return ()


def is_optional(tp: Any) -> bool:
    """Check if a type is an Optional (Union including None)."""
    if is_union(tp):
        return type(None) in get_args(tp)
    return False


def unwrap_optional(tp: Any) -> Any:
    """
    Unwrap Optional[T] into T.
    If Union contains None and multiple types, returns Union without None.
    If not optional, returns original type.
    """
    if is_optional(tp):
        args = [arg for arg in get_args(tp) if arg is not type(None)]
        if len(args) == 1:
            return args[0]
        elif len(args) > 1:
            return typing.Union[tuple(args)]
    return tp


def is_literal(tp: Any) -> bool:
    """Check if a type is a typing.Literal."""
    return get_origin(tp) is typing.Literal


def get_literal_args(tp: Any) -> Tuple[Any, ...]:
    """Get allowed values for a Literal type."""
    if is_literal(tp):
        return get_args(tp)
    return ()


def is_namedtuple_type(tp: Any) -> bool:
    """Check if a type is a typing.NamedTuple or collections.namedtuple."""
    return (
        safe_issubclass(tp, tuple)
        and hasattr(tp, "_fields")
        and hasattr(tp, "_field_defaults")
    )


def is_namedtuple_instance(obj: Any) -> bool:
    """Check if an object is an instance of a NamedTuple."""
    return is_namedtuple_type(type(obj))


def is_typeddict_type(tp: Any) -> bool:
    """Check if a type is a TypedDict."""
    if hasattr(typing, "is_typeddict"):
        return typing.is_typeddict(tp)
    return (
        safe_issubclass(tp, dict)
        and hasattr(tp, "__annotations__")
        and hasattr(tp, "__total__")
    )


def is_typeddict_instance(obj: Any) -> bool:
    """Check if an object can represent a TypedDict (dict at runtime)."""
    return isinstance(obj, dict)


EXTENDED_TYPES: Tuple[Type[Any], ...] = (
    datetime.datetime,
    datetime.date,
    datetime.time,
    datetime.timedelta,
    uuid.UUID,
    decimal.Decimal,
    pathlib.Path,
    pathlib.PurePath,
    bytes,
    bytearray,
    ipaddress.IPv4Address,
    ipaddress.IPv6Address,
    ipaddress.IPv4Network,
    ipaddress.IPv6Network,
    re.Pattern,
    Enum,
)


def is_extended_type(tp: Any) -> bool:
    """Check if a type is one of the extended supported types."""
    return safe_issubclass(tp, EXTENDED_TYPES)


def is_extended_instance(obj: Any) -> bool:
    """Check if an object is an instance of an extended supported type."""
    return isinstance(obj, EXTENDED_TYPES)
