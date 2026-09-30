"""
Serialization engine for JsonPort.
Converts complex Python objects into JSON-serializable structures.
"""

import base64
import datetime
import decimal
import ipaddress
import json
import pathlib
import re
import uuid
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
    get_args,
    get_origin,
)

from .exceptions import JsonPortError, SerializationError
from .inspection import (
    FieldInfo,
    get_cached_type_hints,
    get_dataclass_fields,
    is_dataclass_instance,
    is_namedtuple_instance,
    is_typeddict_type,
)
from .registry import Registry, get_serializer


def serialize_key(
    key: Any,
    expected_type: Optional[Type[Any]] = None,
    registry: Optional[Registry] = None,
    path: str = "",
) -> Any:
    """Serialize a dictionary key to a JSON-compatible string or primitive."""
    if isinstance(key, Enum):
        return key.value
    if isinstance(key, (int, float, str, bool)):
        return key
    if isinstance(key, (datetime.datetime, datetime.date, datetime.time)):
        return key.isoformat()
    if isinstance(
        key,
        (
            pathlib.Path,
            pathlib.PurePath,
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
            uuid.UUID,
        ),
    ):
        return str(key)
    return serialize(key, expected_type=expected_type, registry=registry, path=path)


def _serialize_dataclass(
    obj: Any,
    registry: Optional[Registry] = None,
    path: str = "",
) -> Dict[str, Any]:
    """Serialize a dataclass instance to a dictionary."""
    if not is_dataclass_instance(obj):
        raise JsonPortError("Object must be a dataclass")

    fields_info = get_dataclass_fields(cast(Any, type(obj)))
    result: Dict[str, Any] = {}

    for name, info in fields_info.items():
        if info.exclude:
            continue

        field_path = f"{path}.{name}" if path else name
        val = getattr(obj, name, None)

        out_key = info.alias if info.alias is not None else name

        if info.serializer is not None:
            try:
                result[out_key] = info.serializer(val)
            except Exception as e:
                raise SerializationError(
                    f"Custom serializer failed for field '{name}': {e}",
                    object_type=type(obj),
                    field=name,
                    path=field_path,
                ) from e
        else:
            result[out_key] = serialize(
                val,
                expected_type=info.type,
                registry=registry,
                path=field_path,
            )

    # Include any dynamic attributes not in dataclass fields
    if hasattr(obj, "__dict__"):
        for key, val in obj.__dict__.items():
            if key not in fields_info and not key.startswith("_"):
                field_path = f"{path}.{key}" if path else key
                result[key] = serialize(
                    val,
                    registry=registry,
                    path=field_path,
                )

    return result


def serialize(
    obj: Any,
    expected_type: Optional[Type[Any]] = None,
    registry: Optional[Registry] = None,
    path: str = "",
) -> Any:
    """
    Serialize an object into JSON-compatible primitives, dicts, and lists.
    """
    if obj is None:
        return None

    # Check custom registry first
    custom_serializer = (
        registry.get_serializer(obj) if registry is not None else get_serializer(obj)
    )
    if custom_serializer is not None:
        try:
            return custom_serializer(obj)
        except Exception as e:
            raise SerializationError(
                f"Custom serializer error: {e}",
                object_type=type(obj),
                path=path,
            ) from e

    # Primitives
    if isinstance(obj, (str, int, float, bool)):
        return obj

    # Dataclasses
    if is_dataclass_instance(obj):
        return _serialize_dataclass(obj, registry=registry, path=path)

    # NamedTuple
    if is_namedtuple_instance(obj):
        return {
            field: serialize(
                getattr(obj, field),
                registry=registry,
                path=f"{path}.{field}" if path else field,
            )
            for field in obj._fields
        }

    # Extended types
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()

    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, decimal.Decimal):
        return str(obj)

    if isinstance(obj, uuid.UUID):
        return str(obj)

    if isinstance(
        obj,
        (
            pathlib.Path,
            pathlib.PurePath,
            ipaddress.IPv4Address,
            ipaddress.IPv6Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ),
    ):
        return str(obj)

    if isinstance(obj, (bytes, bytearray)):
        return base64.b64encode(obj).decode("ascii")

    if isinstance(obj, re.Pattern):
        return obj.pattern

    # Collections
    if isinstance(obj, list):
        item_type = None
        if expected_type and get_origin(expected_type) is list:
            args = get_args(expected_type)
            if args:
                item_type = args[0]
        return [
            serialize(
                item,
                expected_type=item_type,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(obj)
        ]

    if isinstance(obj, (set, frozenset)):
        item_type = None
        if expected_type and get_origin(expected_type) in (set, frozenset):
            args = get_args(expected_type)
            if args:
                item_type = args[0]
        return [
            serialize(
                item,
                expected_type=item_type,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(obj)
        ]

    if isinstance(obj, tuple):
        if expected_type and get_origin(expected_type) is tuple:
            args = get_args(expected_type)
            if len(args) == len(obj):
                return [
                    serialize(
                        item,
                        expected_type=args[i],
                        registry=registry,
                        path=f"{path}[{i}]",
                    )
                    for i, item in enumerate(obj)
                ]
            elif len(args) == 2 and args[1] is Ellipsis:
                return [
                    serialize(
                        item,
                        expected_type=args[0],
                        registry=registry,
                        path=f"{path}[{i}]",
                    )
                    for i, item in enumerate(obj)
                ]
        return [
            serialize(item, registry=registry, path=f"{path}[{i}]")
            for i, item in enumerate(obj)
        ]

    if isinstance(obj, dict):
        key_type, val_type = (None, None)
        if expected_type:
            if get_origin(expected_type) is dict:
                args = get_args(expected_type)
                if len(args) == 2:
                    key_type, val_type = args
            elif is_typeddict_type(expected_type):
                hints = get_cached_type_hints(cast(Any, expected_type))
                return {
                    str(k): serialize(
                        v,
                        expected_type=hints.get(str(k)),
                        registry=registry,
                        path=f"{path}[{k!r}]",
                    )
                    for k, v in obj.items()
                }

        return {
            serialize_key(
                k,
                expected_type=key_type,
                registry=registry,
                path=f"{path}.<key>",
            ): serialize(
                v,
                expected_type=val_type,
                registry=registry,
                path=f"{path}[{k!r}]",
            )
            for k, v in obj.items()
        }

    raise SerializationError(
        f"Type {type(obj).__name__} is not serializable by JsonPort",
        object_type=type(obj),
        path=path,
    )


class JsonPortEncoder(json.JSONEncoder):
    """Custom JSON encoder for JsonPort supporting dataclasses and extended types."""

    def default(self, obj: Any) -> Any:
        try:
            return serialize(obj)
        except Exception:
            return str(obj)
