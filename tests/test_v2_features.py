"""
Comprehensive test suite for JsonPort 2.0 new features and capabilities.
"""

import base64
import datetime
import decimal
import io
import ipaddress
import pathlib
import re
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    TypedDict,
    Union,
)

import pytest

from jsonport import (
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
    is_serializable,
    load,
    load_file,
    load_stream,
    loads,
    register_deserializer,
    register_serializer,
    serializer,
)


class TestExtendedTypes:
    """Test extended types support in JsonPort 2.0."""

    def test_uuid_serialization_deserialization(self):
        @dataclass
        class ModelWithUUID:
            id: uuid.UUID
            name: str

        test_id = uuid.uuid4()
        model = ModelWithUUID(id=test_id, name="Test Item")

        data = dump(model)
        assert data["id"] == str(test_id)
        assert isinstance(data["id"], str)

        restored = load(data, ModelWithUUID)
        assert restored.id == test_id
        assert isinstance(restored.id, uuid.UUID)

    def test_decimal_serialization_deserialization(self):
        @dataclass
        class Account:
            balance: decimal.Decimal

        acc = Account(balance=decimal.Decimal("12345.6789"))
        data = dump(acc)
        assert data["balance"] == "12345.6789"

        restored = load(data, Account)
        assert restored.balance == decimal.Decimal("12345.6789")

    def test_path_serialization_deserialization(self):
        @dataclass
        class ConfigFile:
            path: pathlib.Path

        cfg = ConfigFile(path=pathlib.Path("/etc/jsonport/config.json"))
        data = dump(cfg)
        assert data["path"] == "/etc/jsonport/config.json"

        restored = load(data, ConfigFile)
        assert restored.path == pathlib.Path("/etc/jsonport/config.json")

    def test_bytes_serialization_deserialization(self):
        @dataclass
        class BinaryPayload:
            raw_data: bytes

        raw = b"\x00\x01\x02\xff\xfe"
        payload = BinaryPayload(raw_data=raw)
        data = dump(payload)
        expected_b64 = base64.b64encode(raw).decode("ascii")
        assert data["raw_data"] == expected_b64

        restored = load(data, BinaryPayload)
        assert restored.raw_data == raw

    def test_ip_addresses(self):
        @dataclass
        class NetworkNode:
            ipv4: ipaddress.IPv4Address
            ipv6: ipaddress.IPv6Address

        node = NetworkNode(
            ipv4=ipaddress.IPv4Address("192.168.1.1"),
            ipv6=ipaddress.IPv6Address("2001:db8::1"),
        )
        data = dump(node)
        assert data["ipv4"] == "192.168.1.1"
        assert data["ipv6"] == "2001:db8::1"

        restored = load(data, NetworkNode)
        assert restored.ipv4 == ipaddress.IPv4Address("192.168.1.1")
        assert restored.ipv6 == ipaddress.IPv6Address("2001:db8::1")

    def test_timedelta(self):
        @dataclass
        class Task:
            duration: datetime.timedelta

        task = Task(duration=datetime.timedelta(hours=2, minutes=30, seconds=15))
        data = dump(task)
        assert data["duration"] == 9015.0

        restored = load(data, Task)
        assert restored.duration == datetime.timedelta(seconds=9015.0)

    def test_pattern(self):
        @dataclass
        class Rule:
            pattern: re.Pattern

        rule = Rule(pattern=re.compile(r"^[a-z0-9_-]+$"))
        data = dump(rule)
        assert data["pattern"] == r"^[a-z0-9_-]+$"

        restored = load(data, Rule)
        assert restored.pattern.pattern == r"^[a-z0-9_-]+$"


class TestFieldMetadata:
    """Test alias, exclude, and custom field serializers."""

    def test_alias(self):
        @dataclass
        class ApiUser:
            user_id: int = field(metadata={"alias": "id"})
            user_name: str = field(metadata={"alias": "screen_name"})

        u = ApiUser(user_id=42, user_name="alice")
        data = dump(u)
        assert "id" in data
        assert "screen_name" in data
        assert data["id"] == 42
        assert data["screen_name"] == "alice"

        restored = load(data, ApiUser)
        assert restored.user_id == 42
        assert restored.user_name == "alice"

    def test_exclude(self):
        @dataclass
        class SensitiveData:
            public_id: int
            secret_key: str = field(metadata={"exclude": True})

        s = SensitiveData(public_id=1, secret_key="super_secret")
        data = dump(s)
        assert "public_id" in data
        assert "secret_key" not in data

    def test_field_custom_serializer_deserializer(self):
        @dataclass
        class EncryptedModel:
            code: str = field(
                metadata={
                    "serializer": lambda val: val.upper(),
                    "deserializer": lambda val: val.lower(),
                }
            )

        m = EncryptedModel(code="hello")
        data = dump(m)
        assert data["code"] == "HELLO"

        restored = load(data, EncryptedModel)
        assert restored.code == "hello"


class TestCustomRegistry:
    """Test global and isolated custom serializer and deserializer registries."""

    def teardown_method(self):
        clear_registry()

    def test_custom_serializer_and_deserializer(self):
        class Coordinate:
            def __init__(self, x: float, y: float):
                self.x = x
                self.y = y

        @serializer(Coordinate)
        def serialize_coord(c: Coordinate):
            return f"{c.x},{c.y}"

        @deserializer(Coordinate)
        def deserialize_coord(val: str) -> Coordinate:
            x, y = map(float, val.split(","))
            return Coordinate(x, y)

        coord = Coordinate(10.5, 20.25)
        serialized = dump(coord)
        assert serialized == "10.5,20.25"

        restored = load(serialized, Coordinate)
        assert isinstance(restored, Coordinate)
        assert restored.x == 10.5
        assert restored.y == 20.25

    def test_isolated_registry(self):
        reg = Registry()

        class Money:
            def __init__(self, amount: float, currency: str):
                self.amount = amount
                self.currency = currency

        reg.register_serializer(Money, lambda m: f"{m.currency} {m.amount:.2f}")
        reg.register_deserializer(
            Money,
            lambda v: Money(float(v.split()[1]), v.split()[0]),
        )

        m = Money(99.5, "USD")
        # Global registry should not have Money
        with pytest.raises(JsonPortError):
            dump(m)

        # Using isolated registry directly
        ser = reg.get_serializer(Money)
        assert ser is not None
        serialized = ser(m)
        assert serialized == "USD 99.50"

        deser = reg.get_deserializer(Money)
        assert deser is not None
        restored = deser(serialized)
        assert restored.amount == 99.5
        assert restored.currency == "USD"


class TestModernTyping:
    """Test PEP 585, PEP 604, Union, and Literal support."""

    def test_literal_type(self):
        @dataclass
        class StatusModel:
            status: Literal["active", "inactive", "pending"]

        m = StatusModel(status="active")
        data = dump(m)
        assert data["status"] == "active"

        restored = load(data, StatusModel)
        assert restored.status == "active"

        with pytest.raises(DeserializationError):
            load({"status": "unknown"}, StatusModel)

    def test_union_types(self):
        @dataclass
        class Result:
            output: Union[int, str]

        r1 = Result(output=123)
        assert dump(r1) == {"output": 123}
        loaded1 = load({"output": 123}, Result)
        assert loaded1.output == 123

        r2 = Result(output="success")
        assert dump(r2) == {"output": "success"}
        loaded2 = load({"output": "success"}, Result)
        assert loaded2.output == "success"

    def test_intelligent_union_matching(self):
        @dataclass
        class Cat:
            meow: str

        @dataclass
        class Dog:
            bark: str

        @dataclass
        class Shelter:
            pet: Union[Cat, Dog]

        shelter_cat = load({"pet": {"meow": "purr"}}, Shelter)
        assert isinstance(shelter_cat.pet, Cat)
        assert shelter_cat.pet.meow == "purr"

        shelter_dog = load({"pet": {"bark": "woof"}}, Shelter)
        assert isinstance(shelter_dog.pet, Dog)
        assert shelter_dog.pet.bark == "woof"


class TestNamedTupleAndTypedDict:
    """Test NamedTuple and TypedDict serialization and deserialization."""

    def test_namedtuple(self):
        class Point(NamedTuple):
            x: int
            y: int

        p = Point(10, 20)
        data = dump(p)
        assert data == {"x": 10, "y": 20}

        restored = load(data, Point)
        assert restored == p

    def test_typeddict(self):
        class Movie(TypedDict):
            title: str
            year: int

        m: Movie = {"title": "Inception", "year": 2010}
        data = dump(m)
        assert data == {"title": "Inception", "year": 2010}

        restored = load(data, Movie)
        assert restored == m


class TestDumpsLoadsAndStreams:
    """Test direct dumps, loads, and stream operations."""

    def test_dumps_and_loads(self):
        @dataclass
        class Book:
            title: str
            pages: int

        b = Book("Clean Code", 464)
        json_str = dumps(b, indent=2)
        assert isinstance(json_str, str)
        assert '"title": "Clean Code"' in json_str

        restored = loads(json_str, Book)
        assert restored.title == "Clean Code"
        assert restored.pages == 464

    def test_stream_operations(self):
        @dataclass
        class Note:
            text: str

        note = Note("Remember to write tests")
        stream = io.StringIO()
        dump_stream(note, stream)

        stream.seek(0)
        restored = load_stream(stream, Note)
        assert restored.text == note.text


class TestErrorPathsAndStrict:
    """Test error reporting with paths and strict mode."""

    def test_missing_required_field_error(self):
        @dataclass
        class Address:
            city: str
            zip_code: str

        @dataclass
        class Person:
            name: str
            address: Address

        data = {"name": "Bob", "address": {"city": "New York"}}

        with pytest.raises(DeserializationError) as exc_info:
            load(data, Person)

        err = exc_info.value
        assert err.field == "zip_code"
        assert "address.zip_code" in err.path or "zip_code" in str(err)

    def test_strict_mode(self):
        @dataclass
        class Settings:
            theme: str

        # Default allows extra keys
        s = load({"theme": "dark", "extra_option": 123}, Settings)
        assert s.theme == "dark"

        # Strict mode forbids extra keys
        with pytest.raises(DeserializationError, match="Extra keys not permitted"):
            load({"theme": "dark", "extra_option": 123}, Settings, strict=True)
