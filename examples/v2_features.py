#!/usr/bin/env python3
"""
JsonPort 2.0 Feature Showcase.

Demonstrates:
- dumps() and loads() string APIs
- Stream operations with io.StringIO
- Extended types (UUID, Decimal, Path, bytes, IP addresses, timedelta)
- Dataclass field metadata (alias, exclude, per-field serializer/deserializer)
- Custom @serializer and @deserializer decorators and Registry
- Strict mode and rich error diagnostics
- NamedTuple and TypedDict support
"""

import datetime
import decimal
import io
import ipaddress
import pathlib
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple, TypedDict

from jsonport import (
    DeserializationError,
    Registry,
    deserializer,
    dump_stream,
    dumps,
    load_stream,
    loads,
    serializer,
)


# ============================================================================
# 1. Extended Types & Field Metadata
# ============================================================================
class Environment(Enum):
    PRODUCTION = "prod"
    STAGING = "stage"
    DEVELOPMENT = "dev"


@dataclass
class ServiceInstance:
    id: uuid.UUID
    cost_per_hour: decimal.Decimal
    log_dir: pathlib.Path
    ip: ipaddress.IPv4Address
    uptime: datetime.timedelta
    environment: Environment
    # Map external JSON field 'host_name' to internal 'hostname'
    hostname: str = field(metadata={"alias": "host_name"})
    # Custom field formatting
    timestamp: datetime.datetime = field(
        metadata={
            "serializer": lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),
            "deserializer": lambda s: datetime.datetime.strptime(
                s, "%Y-%m-%d %H:%M:%S"
            ),
        }
    )
    # Exclude API key from output (provide default for deserialization)
    api_key: str = field(default="", metadata={"exclude": True})


def demo_extended_types():
    print("--- 1. Extended Types & Field Metadata ---")
    instance = ServiceInstance(
        id=uuid.uuid4(),
        cost_per_hour=decimal.Decimal("0.0450"),
        log_dir=pathlib.Path("/var/log/services"),
        ip=ipaddress.IPv4Address("10.0.1.25"),
        uptime=datetime.timedelta(days=3, hours=14, minutes=22),
        environment=Environment.PRODUCTION,
        api_key="sk-live-secret-token",
        hostname="node-01.internal",
        timestamp=datetime.datetime(2026, 9, 30, 8, 30, 0),
    )

    # Serialize to JSON string
    json_str = dumps(instance, indent=2)
    print("Serialized JSON:")
    print(json_str)

    # Deserialize back
    restored = loads(json_str, ServiceInstance)
    assert restored.id == instance.id
    assert restored.cost_per_hour == instance.cost_per_hour
    assert restored.log_dir == instance.log_dir
    assert restored.ip == instance.ip
    assert restored.uptime == instance.uptime
    assert restored.hostname == "node-01.internal"
    print("Successfully roundtripped extended types and metadata!\n")


# ============================================================================
# 2. Stream Operations
# ============================================================================
def demo_stream_operations():
    print("--- 2. Stream Operations ---")
    stream = io.StringIO()
    payload = {"records": [1, 2, 3], "status": "ok"}

    dump_stream(payload, stream, indent=2)
    stream.seek(0)

    loaded = load_stream(stream, dict)
    print("Loaded from stream:", loaded)
    print()


# ============================================================================
# 3. Custom Type Registry
# ============================================================================
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    def __repr__(self) -> str:
        return f"{self.celsius:.1f}°C"


@serializer(Temperature)
def serialize_temp(t: Temperature) -> str:
    return f"{t.celsius:.1f}C"


@deserializer(Temperature)
def deserialize_temp(val: str) -> Temperature:
    celsius = float(val.rstrip("C"))
    return Temperature(celsius)


def demo_custom_registry():
    print("--- 3. Custom Registry ---")
    temp = Temperature(23.5)
    serialized = dumps(temp)
    print(f"Serialized Temperature: {serialized}")

    restored = loads(serialized, Temperature)
    print(f"Deserialized Temperature: {restored}")
    print()


# ============================================================================
# 4. Strict Mode & Error Path Reporting
# ============================================================================
def demo_strict_mode():
    print("--- 4. Strict Mode & Error Reporting ---")
    raw_data = '{"id": "not-a-valid-uuid", "extra_unexpected_field": 123}'

    @dataclass
    class Node:
        id: uuid.UUID

    # Deserialization error with detailed message
    try:
        loads(raw_data, Node, strict=True)
    except DeserializationError as err:
        print(f"Caught DeserializationError: {err}")
        print(f"Target Type: {err.target_type}")
        print()


# ============================================================================
# 5. NamedTuple and TypedDict
# ============================================================================
class GeoPoint(NamedTuple):
    lat: float
    lon: float
    description: str = "GPS Location"


class ConfigDict(TypedDict):
    retries: int
    debug: bool


def demo_namedtuple_and_typeddict():
    print("--- 5. NamedTuple & TypedDict ---")
    # Deserializing NamedTuple from sequence
    point = loads("[37.7749, -122.4194]", GeoPoint)
    print(f"NamedTuple from list: {point}")

    # Deserializing TypedDict
    config = loads('{"retries": 3, "debug": true}', ConfigDict)
    print(f"TypedDict: {config}")
    print()


if __name__ == "__main__":
    demo_extended_types()
    demo_stream_operations()
    demo_custom_registry()
    demo_strict_mode()
    demo_namedtuple_and_typeddict()
