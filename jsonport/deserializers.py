"""
Deserialization engine for JsonPort.
Converts JSON-compatible primitives, dicts, and lists into typed Python objects.
"""

import base64
import datetime
import decimal
import inspect
import ipaddress
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
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from .exceptions import DeserializationError, JsonPortError
from .inspection import (
    FieldInfo,
    get_cached_type_hints,
    get_dataclass_fields,
    get_literal_args,
    get_union_args,
    is_dataclass_type,
    is_literal,
    is_namedtuple_type,
    is_optional,
    is_typeddict_type,
    is_union,
    safe_issubclass,
    unwrap_optional,
)
from .registry import Registry, get_deserializer

T = TypeVar("T")


def _deserialize_dataclass(
    data: Dict[str, Any],
    target_class: Type[T],
    strict: bool = False,
    registry: Optional[Registry] = None,
    path: str = "",
) -> T:
    """Deserialize a dictionary to a dataclass instance."""
    if not is_dataclass_type(target_class):
        raise JsonPortError("Target class must be a dataclass")

    fields_info = get_dataclass_fields(cast(Any, target_class))
    kwargs: Dict[str, Any] = {}

    if strict:
        recognized_keys = set()
        for info in fields_info.values():
            recognized_keys.add(info.name)
            if info.alias:
                recognized_keys.add(info.alias)
        extra_keys = set(data.keys()) - recognized_keys
        if extra_keys:
            raise DeserializationError(
                f"Extra keys not permitted in strict mode for {target_class.__name__}: {sorted(extra_keys)}",
                target_type=target_class,
                path=path,
            )

    for name, info in fields_info.items():
        key_to_use = (
            info.alias
            if (info.alias is not None and info.alias in data)
            else (name if name in data else None)
        )

        field_path = f"{path}.{name}" if path else name

        if key_to_use is not None:
            raw_val = data[key_to_use]
            if info.deserializer is not None:
                try:
                    sig = inspect.signature(info.deserializer)
                    if len(sig.parameters) >= 2:
                        kwargs[name] = info.deserializer(raw_val, info.type)
                    else:
                        kwargs[name] = info.deserializer(raw_val)
                except Exception as e:
                    raise DeserializationError(
                        f"Custom deserializer failed for field '{name}': {e}",
                        target_type=target_class,
                        field=name,
                        path=field_path,
                        value=raw_val,
                    ) from e
            else:
                kwargs[name] = deserialize(
                    raw_val,
                    info.type,
                    strict=strict,
                    registry=registry,
                    path=field_path,
                )
        else:
            if not info.has_default:
                raise DeserializationError(
                    f"Missing required field '{name}' for dataclass {target_class.__name__}",
                    target_type=target_class,
                    field=name,
                    path=field_path,
                )

    return target_class(**kwargs)


def deserialize(
    value: Any,
    target_type: Any,
    strict: bool = False,
    registry: Optional[Registry] = None,
    path: str = "",
) -> Any:
    """
    Deserialize data into an instance of target_type.
    """
    if target_type is Any or target_type is object:
        return value

    # Check custom registry first
    custom_deserializer = (
        registry.get_deserializer(target_type)
        if registry is not None
        else get_deserializer(target_type)
    )
    if custom_deserializer is not None:
        try:
            sig = inspect.signature(custom_deserializer)
            if len(sig.parameters) >= 2:
                return custom_deserializer(value, target_type)
            return custom_deserializer(value)
        except Exception as e:
            raise DeserializationError(
                f"Custom deserializer error: {e}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            ) from e

    # None handling & Optional
    if value is None:
        if is_optional(target_type) or target_type is type(None):
            return None
        raise DeserializationError(
            f"Expected {target_type} but got None",
            target_type=target_type if isinstance(target_type, type) else None,
            path=path,
            value=value,
        )

    # Union & Optional handling
    if is_union(target_type):
        if is_optional(target_type):
            inner_type = unwrap_optional(target_type)
            return deserialize(
                value,
                inner_type,
                strict=strict,
                registry=registry,
                path=path,
            )

        union_args = get_union_args(target_type)

        # 1. Exact primitive / direct instance match
        for arg in union_args:
            if isinstance(arg, type) and isinstance(value, arg):
                return value

        # 2. Dict matching against dataclasses: score candidates by field overlap
        if isinstance(value, dict):
            scored_candidates = []
            for arg in union_args:
                if is_dataclass_type(arg):
                    dc_fields = get_dataclass_fields(cast(Any, arg))
                    keys = set(value.keys())
                    overlap = sum(
                        1
                        for f_name, f_info in dc_fields.items()
                        if f_name in keys or (f_info.alias and f_info.alias in keys)
                    )
                    scored_candidates.append((overlap, arg))
            if scored_candidates:
                scored_candidates.sort(key=lambda x: x[0], reverse=True)
                for _, arg in scored_candidates:
                    try:
                        return deserialize(
                            value,
                            arg,
                            strict=strict,
                            registry=registry,
                            path=path,
                        )
                    except DeserializationError:
                        continue

        # 3. Try each argument in order
        for arg in union_args:
            try:
                return deserialize(
                    value,
                    arg,
                    strict=strict,
                    registry=registry,
                    path=path,
                )
            except DeserializationError:
                continue

        raise DeserializationError(
            f"Cannot deserialize value into any variant of Union {target_type}",
            target_type=target_type if isinstance(target_type, type) else None,
            path=path,
            value=value,
        )

    # Literal types
    if is_literal(target_type):
        allowed = get_literal_args(target_type)
        if value in allowed:
            return value
        raise DeserializationError(
            f"Value {value!r} is not one of allowed literals {allowed}",
            target_type=target_type if isinstance(target_type, type) else None,
            path=path,
            value=value,
        )

    # Primitives
    if target_type is bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (dict, list, set, tuple)):
            raise DeserializationError(
                f"Expected bool, got {type(value).__name__}",
                target_type=bool,
                path=path,
                value=value,
            )
        if isinstance(value, str):
            v = value.strip().lower()
            if v in ("true", "1", "yes", "t"):
                return True
            if v in ("false", "0", "no", "f"):
                return False
        return bool(value)

    if target_type is int:
        try:
            return int(value)
        except Exception as e:
            raise DeserializationError(
                f"Cannot convert {value!r} to int: {e}",
                target_type=int,
                path=path,
                value=value,
            ) from e

    if target_type is float:
        try:
            return float(value)
        except Exception as e:
            raise DeserializationError(
                f"Cannot convert {value!r} to float: {e}",
                target_type=float,
                path=path,
                value=value,
            ) from e

    if target_type is str:
        if isinstance(value, (dict, list, set, tuple)):
            raise DeserializationError(
                f"Expected str, got {type(value).__name__}",
                target_type=str,
                path=path,
                value=value,
            )
        try:
            return str(value)
        except Exception as e:
            raise DeserializationError(
                f"Cannot convert {value!r} to str: {e}",
                target_type=str,
                path=path,
                value=value,
            ) from e

    # Dataclasses
    if is_dataclass_type(target_type):
        if not isinstance(value, dict):
            raise DeserializationError(
                f"Expected dict for dataclass {target_type.__name__}, got {type(value).__name__}",
                target_type=target_type,
                path=path,
                value=value,
            )
        return _deserialize_dataclass(
            value,
            target_type,
            strict=strict,
            registry=registry,
            path=path,
        )

    # NamedTuple
    if is_namedtuple_type(target_type):
        hints = get_cached_type_hints(cast(Any, target_type))
        nt_fields: Tuple[str, ...] = getattr(target_type, "_fields", ())
        if isinstance(value, dict):
            kwargs: Dict[str, Any] = {}
            for f in nt_fields:
                f_path = f"{path}.{f}" if path else f
                if f in value:
                    kwargs[f] = deserialize(
                        value[f],
                        hints.get(f, Any),
                        strict=strict,
                        registry=registry,
                        path=f_path,
                    )
                elif f in getattr(target_type, "_field_defaults", {}):
                    kwargs[f] = target_type._field_defaults[f]
                else:
                    raise DeserializationError(
                        f"Missing required field '{f}' for NamedTuple {target_type.__name__}",
                        target_type=target_type,
                        field=f,
                        path=f_path,
                    )
            return target_type(**kwargs)
        elif isinstance(value, (list, tuple)):
            items = [
                deserialize(
                    item,
                    hints.get(nt_fields[i], Any),
                    strict=strict,
                    registry=registry,
                    path=f"{path}[{i}]",
                )
                for i, item in enumerate(value)
            ]
            return target_type(*items)
        else:
            raise DeserializationError(
                f"Expected dict or list for NamedTuple, got {type(value).__name__}",
                target_type=target_type,
                path=path,
                value=value,
            )

    # TypedDict
    if is_typeddict_type(target_type):
        if not isinstance(value, dict):
            raise DeserializationError(
                f"Expected dict for TypedDict {getattr(target_type, '__name__', str(target_type))}, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        hints = get_cached_type_hints(cast(Any, target_type))
        res_dict = {}
        for k, v in value.items():
            if k in hints:
                res_dict[k] = deserialize(
                    v,
                    hints[k],
                    strict=strict,
                    registry=registry,
                    path=f"{path}[{k!r}]",
                )
            else:
                res_dict[k] = v
        return res_dict

    # Extended Types
    if target_type is datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            except Exception as e:
                raise DeserializationError(
                    f"Invalid datetime string '{value}': {e}",
                    target_type=datetime.datetime,
                    path=path,
                    value=value,
                ) from e
        raise DeserializationError(
            f"Expected datetime string, got {type(value).__name__}",
            target_type=datetime.datetime,
            path=path,
            value=value,
        )

    if target_type is datetime.date:
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, str):
            try:
                return datetime.date.fromisoformat(value)
            except Exception as e:
                raise DeserializationError(
                    f"Invalid date string '{value}': {e}",
                    target_type=datetime.date,
                    path=path,
                    value=value,
                ) from e
        raise DeserializationError(
            f"Expected date string, got {type(value).__name__}",
            target_type=datetime.date,
            path=path,
            value=value,
        )

    if target_type is datetime.time:
        if isinstance(value, datetime.time):
            return value
        if isinstance(value, str):
            try:
                return datetime.time.fromisoformat(value)
            except Exception as e:
                raise DeserializationError(
                    f"Invalid time string '{value}': {e}",
                    target_type=datetime.time,
                    path=path,
                    value=value,
                ) from e
        raise DeserializationError(
            f"Expected time string, got {type(value).__name__}",
            target_type=datetime.time,
            path=path,
            value=value,
        )

    if target_type is datetime.timedelta:
        if isinstance(value, datetime.timedelta):
            return value
        if isinstance(value, (int, float)):
            return datetime.timedelta(seconds=value)
        if isinstance(value, str):
            try:
                return datetime.timedelta(seconds=float(value))
            except Exception as e:
                raise DeserializationError(
                    f"Invalid timedelta string '{value}': {e}",
                    target_type=datetime.timedelta,
                    path=path,
                    value=value,
                ) from e
        raise DeserializationError(
            f"Expected timedelta number or string, got {type(value).__name__}",
            target_type=datetime.timedelta,
            path=path,
            value=value,
        )

    if target_type is uuid.UUID:
        if isinstance(value, uuid.UUID):
            return value
        try:
            return uuid.UUID(str(value))
        except Exception as e:
            raise DeserializationError(
                f"Invalid UUID string '{value}': {e}",
                target_type=uuid.UUID,
                path=path,
                value=value,
            ) from e

    if target_type is decimal.Decimal:
        if isinstance(value, decimal.Decimal):
            return value
        try:
            return decimal.Decimal(str(value))
        except Exception as e:
            raise DeserializationError(
                f"Invalid Decimal string '{value}': {e}",
                target_type=decimal.Decimal,
                path=path,
                value=value,
            ) from e

    if safe_issubclass(target_type, (pathlib.Path, pathlib.PurePath)):
        if isinstance(value, target_type):
            return value
        try:
            return target_type(value)
        except Exception as e:
            raise DeserializationError(
                f"Invalid Path value '{value}': {e}",
                target_type=target_type,
                path=path,
                value=value,
            ) from e

    if target_type in (bytes, bytearray):
        if isinstance(value, target_type):
            return value
        if isinstance(value, str):
            try:
                raw_bytes = base64.b64decode(value.encode("ascii"), validate=True)
                return target_type(raw_bytes)
            except Exception as e:
                raise DeserializationError(
                    f"Invalid base64 string for bytes: {e}",
                    target_type=target_type,
                    path=path,
                    value=value,
                ) from e
        raise DeserializationError(
            f"Expected base64 string for bytes, got {type(value).__name__}",
            target_type=target_type,
            path=path,
            value=value,
        )

    if target_type is ipaddress.IPv4Address:
        if isinstance(value, ipaddress.IPv4Address):
            return value
        try:
            return ipaddress.IPv4Address(value)
        except Exception as e:
            raise DeserializationError(
                f"Invalid IPv4Address: {e}",
                target_type=ipaddress.IPv4Address,
                path=path,
                value=value,
            ) from e

    if target_type is ipaddress.IPv6Address:
        if isinstance(value, ipaddress.IPv6Address):
            return value
        try:
            return ipaddress.IPv6Address(value)
        except Exception as e:
            raise DeserializationError(
                f"Invalid IPv6Address: {e}",
                target_type=ipaddress.IPv6Address,
                path=path,
                value=value,
            ) from e

    if target_type in (ipaddress.IPv4Network, ipaddress.IPv6Network):
        try:
            return target_type(value)
        except Exception as e:
            raise DeserializationError(
                f"Invalid IPNetwork: {e}",
                target_type=target_type,
                path=path,
                value=value,
            ) from e

    if target_type is re.Pattern or safe_issubclass(target_type, re.Pattern):
        if isinstance(value, re.Pattern):
            return value
        try:
            return re.compile(value)
        except Exception as e:
            raise DeserializationError(
                f"Invalid regex pattern: {e}",
                target_type=re.Pattern,
                path=path,
                value=value,
            ) from e

    if safe_issubclass(target_type, Enum):
        if isinstance(value, target_type):
            return value
        try:
            return target_type(value)
        except (ValueError, KeyError):
            try:
                return target_type[value]
            except (KeyError, TypeError) as e:
                raise DeserializationError(
                    f"Value {value!r} is not a valid {target_type.__name__}",
                    target_type=target_type,
                    path=path,
                    value=value,
                ) from e

    # Collections
    origin = get_origin(target_type)

    if origin is list or target_type is list:
        if not isinstance(value, (list, tuple)):
            raise DeserializationError(
                f"Expected list, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        args = get_args(target_type)
        item_type = args[0] if args else Any
        return [
            deserialize(
                item,
                item_type,
                strict=strict,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(value)
        ]

    if origin is set or target_type is set:
        if not isinstance(value, (list, tuple, set)):
            raise DeserializationError(
                f"Expected list/set, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        args = get_args(target_type)
        item_type = args[0] if args else Any
        return {
            deserialize(
                item,
                item_type,
                strict=strict,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(value)
        }

    if origin is frozenset or target_type is frozenset:
        if not isinstance(value, (list, tuple, set, frozenset)):
            raise DeserializationError(
                f"Expected list/set, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        args = get_args(target_type)
        item_type = args[0] if args else Any
        return frozenset(
            deserialize(
                item,
                item_type,
                strict=strict,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(value)
        )

    if origin is tuple or target_type is tuple:
        if not isinstance(value, (list, tuple)):
            raise DeserializationError(
                f"Expected tuple/list, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        args = get_args(target_type)
        if not args:
            return tuple(value)
        if len(args) == 2 and args[1] is Ellipsis:
            item_type = args[0]
            return tuple(
                deserialize(
                    item,
                    item_type,
                    strict=strict,
                    registry=registry,
                    path=f"{path}[{i}]",
                )
                for i, item in enumerate(value)
            )
        if len(args) != len(value):
            raise DeserializationError(
                f"Tuple length mismatch: expected {len(args)}, got {len(value)}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        return tuple(
            deserialize(
                item,
                args[i],
                strict=strict,
                registry=registry,
                path=f"{path}[{i}]",
            )
            for i, item in enumerate(value)
        )

    if origin is dict or target_type is dict:
        if not isinstance(value, dict):
            raise DeserializationError(
                f"Expected dict, got {type(value).__name__}",
                target_type=target_type if isinstance(target_type, type) else None,
                path=path,
                value=value,
            )
        args = get_args(target_type)
        key_type, val_type = (args[0], args[1]) if len(args) == 2 else (Any, Any)
        return {
            deserialize(
                k,
                key_type,
                strict=strict,
                registry=registry,
                path=f"{path}.<key>",
            ): deserialize(
                v,
                val_type,
                strict=strict,
                registry=registry,
                path=f"{path}[{k!r}]",
            )
            for k, v in value.items()
        }

    return value
