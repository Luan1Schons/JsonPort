"""
Edge cases and comprehensive coverage tests for JsonPort 2.0.
"""

import datetime
import decimal
import io
import ipaddress
import json
import os
import pathlib
import re
import tempfile
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
    cast,
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
from jsonport.deserializers import _deserialize_dataclass
from jsonport.inspection import (
    get_cached_type_hints,
    get_dataclass_fields,
    get_literal_args,
    get_union_args,
    is_dataclass_instance,
    is_dataclass_type,
    is_extended_instance,
    is_extended_type,
    is_literal,
    is_namedtuple_instance,
    is_namedtuple_type,
    is_optional,
    is_typeddict_instance,
    is_typeddict_type,
    is_union,
    safe_issubclass,
    unwrap_optional,
)
from jsonport.serializers import _serialize_dataclass, serialize, serialize_key


# ============================================================================
# 1. Strict Mode Tests
# ============================================================================
class TestStrictModeEdgeCases:
    """Test strict mode behaviors with extra keys, nested objects, and aliases."""

    def test_strict_mode_rejects_extra_fields(self):
        @dataclass
        class Simple:
            x: int

        with pytest.raises(DeserializationError) as exc_info:
            load({"x": 1, "extra1": "foo", "extra2": "bar"}, Simple, strict=True)
        err = exc_info.value
        assert "Extra keys not permitted" in str(err)
        assert err.target_type is Simple

    def test_strict_mode_accepts_alias(self):
        @dataclass
        class Aliased:
            internal_name: str = field(metadata={"alias": "external_name"})

        obj = load({"external_name": "val"}, Aliased, strict=True)
        assert obj.internal_name == "val"

        # Also internal name is accepted if strict
        obj2 = load({"internal_name": "val2"}, Aliased, strict=True)
        assert obj2.internal_name == "val2"

    def test_non_strict_mode_ignores_extra_fields(self):
        @dataclass
        class Simple:
            x: int

        obj = load({"x": 42, "unwanted": "ignored"}, Simple, strict=False)
        assert obj.x == 42


# ============================================================================
# 2. Custom Field Serializer & Deserializer in Dataclass Metadata
# ============================================================================
class TestFieldMetadataEdgeCases:
    """Test field serializer and deserializer edge cases."""

    def test_custom_field_serializer_and_deserializer_success(self):
        @dataclass
        class FormattedRecord:
            timestamp: datetime.datetime = field(
                metadata={
                    "serializer": lambda dt: dt.strftime("%Y/%m/%d %H:%M:%S"),
                    "deserializer": lambda s: datetime.datetime.strptime(
                        s, "%Y/%m/%d %H:%M:%S"
                    ),
                }
            )

        dt = datetime.datetime(2026, 9, 30, 12, 0, 0)
        rec = FormattedRecord(timestamp=dt)

        dumped = dump(rec)
        assert dumped["timestamp"] == "2026/09/30 12:00:00"

        restored = load(dumped, FormattedRecord)
        assert restored.timestamp == dt

    def test_custom_field_serializer_failure_raises_serialization_error(self):
        def bad_serializer(val: Any) -> Any:
            raise ValueError("boom serializer")

        @dataclass
        class BadModel:
            val: str = field(metadata={"serializer": bad_serializer})

        model = BadModel(val="test")
        with pytest.raises(SerializationError) as exc_info:
            dump(model)

        err = exc_info.value
        assert "Custom serializer failed for field 'val'" in str(err)
        assert err.field == "val"
        assert err.object_type is BadModel

    def test_custom_field_deserializer_failure_raises_deserialization_error(self):
        def bad_deserializer(val: Any) -> Any:
            raise ValueError("boom deserializer")

        @dataclass
        class BadModel:
            val: str = field(metadata={"deserializer": bad_deserializer})

        with pytest.raises(DeserializationError) as exc_info:
            load({"val": "test"}, BadModel)

        err = exc_info.value
        assert "Custom deserializer failed for field 'val'" in str(err)
        assert err.field == "val"
        assert err.target_type is BadModel
        assert err.value == "test"


# ============================================================================
# 3. Unions with Multiple Non-Dataclass Types and Fallback
# ============================================================================
class TestUnionEdgeCases:
    """Test union types handling and fallback."""

    def test_multi_primitive_union(self):
        @dataclass
        class Container:
            val: Union[int, str, List[int]]

        c1 = load({"val": 42}, Container)
        assert c1.val == 42
        assert isinstance(c1.val, int)

        c2 = load({"val": "hello"}, Container)
        assert c2.val == "hello"
        assert isinstance(c2.val, str)

        c3 = load({"val": [1, 2, 3]}, Container)
        assert c3.val == [1, 2, 3]

    def test_union_failure_raises_deserialization_error(self):
        @dataclass
        class Container:
            val: Union[int, float]

        with pytest.raises(DeserializationError) as exc_info:
            load({"val": "not-a-number"}, Container)

        err = exc_info.value
        assert "Cannot deserialize value into any variant of Union" in str(err)

    def test_optional_union_with_none(self):
        @dataclass
        class OptionalContainer:
            val: Optional[Union[int, str]] = None

        c_none = load({"val": None}, OptionalContainer)
        assert c_none.val is None

        c_int = load({"val": 99}, OptionalContainer)
        assert c_int.val == 99

        c_str = load({"val": "sample"}, OptionalContainer)
        assert c_str.val == "sample"


# ============================================================================
# 4. Invalid JSON Strings in loads()
# ============================================================================
class TestLoadsInvalidJson:
    """Test handling of invalid JSON input."""

    def test_loads_invalid_syntax(self):
        @dataclass
        class Simple:
            x: int

        with pytest.raises(
            ValueError
        ):  # json.JSONDecodeError is a subclass of ValueError
            loads("{invalid json string", Simple)

    def test_loads_empty_string(self):
        @dataclass
        class Simple:
            x: int

        with pytest.raises(ValueError):
            loads("", Simple)


# ============================================================================
# 5. dump_stream and load_stream Operations
# ============================================================================
class TestStreamOperationsExtended:
    """Test streaming with StringIO, file objects, indent, and ensure_ascii."""

    def test_stringio_stream_with_formatting(self):
        @dataclass
        class Item:
            id: uuid.UUID
            name: str
            price: decimal.Decimal

        u = uuid.uuid4()
        d = decimal.Decimal("19.99")
        item = Item(id=u, name="Café", price=d)

        stream = io.StringIO()
        dump_stream(item, stream, indent=2, ensure_ascii=False)
        content = stream.getvalue()

        assert "Café" in content
        assert "\n" in content

        stream.seek(0)
        restored = load_stream(stream, Item)
        assert restored.id == u
        assert restored.name == "Café"
        assert restored.price == d

    def test_file_stream_operations(self):
        @dataclass
        class Record:
            title: str
            count: int

        rec = Record("Inventory", 150)
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
            temp_path = f.name
            try:
                dump_stream(rec, f)
                f.seek(0)
                restored = load_stream(f, Record)
                assert restored.title == "Inventory"
                assert restored.count == 150
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)


# ============================================================================
# 6. JsonPortEncoder with standard json.dumps()
# ============================================================================
class TestJsonPortEncoderExtended:
    """Test JsonPortEncoder with standard json.dumps() across extended types."""

    class Status(Enum):
        ACTIVE = "active"
        PENDING = "pending"

    def test_encoder_extended_types(self):
        u = uuid.uuid4()
        dec = decimal.Decimal("45.67")
        dt = datetime.datetime(2026, 9, 30, 15, 30)
        d = datetime.date(2026, 9, 30)
        t = datetime.time(15, 30)
        td = datetime.timedelta(days=1, hours=2)
        p = pathlib.Path("/tmp/test")
        ip = ipaddress.IPv4Address("192.168.1.1")
        s = {1, 2, 3}
        fs = frozenset(["a", "b"])

        data = {
            "uuid": u,
            "decimal": dec,
            "datetime": dt,
            "date": d,
            "time": t,
            "timedelta": td,
            "enum": self.Status.ACTIVE,
            "path": p,
            "ip": ip,
            "set": s,
            "frozenset": fs,
        }

        json_text = json.dumps(data, cls=JsonPortEncoder)
        assert str(u) in json_text
        assert "45.67" in json_text
        assert "active" in json_text
        assert "192.168.1.1" in json_text

    def test_encoder_fallback(self):
        class CustomNonSerializable:
            def __str__(self):
                return "CustomStrRepresentation"

        val = CustomNonSerializable()
        encoded = json.dumps({"obj": val}, cls=JsonPortEncoder)
        assert "CustomStrRepresentation" in encoded


# ============================================================================
# 7. Exceptions Attributes and Formatting
# ============================================================================
class TestExceptionsAttributesAndStr:
    """Test SerializationError and DeserializationError attributes and string formatting."""

    def test_serialization_error_str_formatting(self):
        # Empty details
        err1 = SerializationError("Serialization failed")
        assert str(err1) == "Serialization failed"

        # All details
        err2 = SerializationError(
            "Cannot serialize", object_type=dict, field="my_field", path="root.my_field"
        )
        s2 = str(err2)
        assert "path: 'root.my_field'" in s2
        assert "field: 'my_field'" in s2
        assert "type: dict" in s2
        assert err2.object_type is dict
        assert err2.field == "my_field"
        assert err2.path == "root.my_field"

    def test_deserialization_error_str_formatting(self):
        # Empty details
        err1 = DeserializationError("Deserialization failed")
        assert str(err1) == "Deserialization failed"

        # All details
        err2 = DeserializationError(
            "Type mismatch",
            target_type=int,
            field="age",
            path="user.age",
            value="abc",
        )
        s2 = str(err2)
        assert "path: 'user.age'" in s2
        assert "field: 'age'" in s2
        assert "target_type: int" in s2
        assert err2.target_type is int
        assert err2.field == "age"
        assert err2.path == "user.age"
        assert err2.value == "abc"

    def test_configuration_error(self):
        err = ConfigurationError("Invalid configuration")
        assert isinstance(err, JsonPortError)
        assert str(err) == "Invalid configuration"


# ============================================================================
# 8. Extended Types Deserialization Failures
# ============================================================================
class TestExtendedTypesFailurePaths:
    """Test error handling when deserializing invalid extended type data."""

    def test_invalid_uuid(self):
        with pytest.raises(DeserializationError) as exc_info:
            load("invalid-uuid-string", uuid.UUID)
        assert exc_info.value.target_type is uuid.UUID

    def test_invalid_decimal(self):
        with pytest.raises(DeserializationError) as exc_info:
            load("not_a_decimal", decimal.Decimal)
        assert exc_info.value.target_type is decimal.Decimal

    def test_invalid_bytes(self):
        # Bad base64
        with pytest.raises(DeserializationError):
            load("!@#$%^&*", bytes)
        # Not a string
        with pytest.raises(DeserializationError):
            load(12345, bytes)

    def test_invalid_ip_addresses(self):
        with pytest.raises(DeserializationError):
            load("999.999.999.999", ipaddress.IPv4Address)

        with pytest.raises(DeserializationError):
            load("invalid-ipv6", ipaddress.IPv6Address)

        with pytest.raises(DeserializationError):
            load("invalid-network", ipaddress.IPv4Network)

        with pytest.raises(DeserializationError):
            load("invalid-network", ipaddress.IPv6Network)

    def test_valid_ip_network(self):
        net4 = load("192.168.1.0/24", ipaddress.IPv4Network)
        assert net4 == ipaddress.IPv4Network("192.168.1.0/24")

        net6 = load("2001:db8::/32", ipaddress.IPv6Network)
        assert net6 == ipaddress.IPv6Network("2001:db8::/32")

    def test_invalid_regex_pattern(self):
        with pytest.raises(DeserializationError):
            load("[a-z", re.Pattern)

    class Color(Enum):
        RED = 1
        GREEN = 2

    def test_enum_deserialization_failures_and_names(self):
        # By value
        assert load(1, self.Color) == self.Color.RED
        # By name
        assert load("GREEN", self.Color) == self.Color.GREEN

        with pytest.raises(DeserializationError):
            load("BLUE", self.Color)

        with pytest.raises(DeserializationError):
            load(999, self.Color)

    def test_invalid_timedelta(self):
        with pytest.raises(DeserializationError):
            load("not_a_number", datetime.timedelta)

        with pytest.raises(DeserializationError):
            load([], datetime.timedelta)

    def test_invalid_datetime_and_date(self):
        with pytest.raises(DeserializationError):
            load("not-a-datetime", datetime.datetime)

        with pytest.raises(DeserializationError):
            load("not-a-date", datetime.date)

        with pytest.raises(DeserializationError):
            load("not-a-time", datetime.time)

        with pytest.raises(DeserializationError):
            load(12345, datetime.datetime)


# ============================================================================
# 9. Dictionary Keys Serialization & Deserialization
# ============================================================================
class TestDictKeySerializationAndDeserialization:
    """Test serialization and deserialization of dictionary keys."""

    class KeyEnum(Enum):
        A = "key_a"
        B = "key_b"

    def test_dict_keys_serialization(self):
        u = uuid.uuid4()
        dt = datetime.datetime(2026, 9, 30, 10, 0)
        p = pathlib.Path("/tmp/foo")
        ip = ipaddress.IPv4Address("10.0.0.1")

        data = {
            self.KeyEnum.A: "val1",
            u: "val2",
            dt: "val3",
            p: "val4",
            ip: "val5",
            123: "val6",
        }
        serialized = dump(data)
        assert serialized["key_a"] == "val1"
        assert serialized[str(u)] == "val2"
        assert serialized[dt.isoformat()] == "val3"
        assert serialized[str(p)] == "val4"
        assert serialized["10.0.0.1"] == "val5"
        assert serialized[123] == "val6"

    def test_dict_typed_key_deserialization(self):
        u = uuid.uuid4()
        raw = {str(u): 100}
        restored = load(raw, Dict[uuid.UUID, int])
        assert u in restored
        assert restored[u] == 100


# ============================================================================
# 10. Collections and Tuples
# ============================================================================
class TestCollectionsEdgeCases:
    """Test collections with mismatched types or lengths."""

    def test_list_type_error(self):
        with pytest.raises(DeserializationError):
            load("not_a_list", List[int])

        with pytest.raises(DeserializationError):
            load(["abc", "def"], List[int])

    def test_set_type_error(self):
        with pytest.raises(DeserializationError):
            load("not_a_set", Set[int])

        with pytest.raises(DeserializationError):
            load(["abc"], Set[int])

    def test_tuple_fixed_length(self):
        t: Tuple[int, str] = load([1, "hello"], cast(Any, Tuple[int, str]))
        assert t == (1, "hello")

        # Wrong length
        with pytest.raises(DeserializationError):
            load([1], cast(Any, Tuple[int, str]))

        # Wrong element type
        with pytest.raises(DeserializationError):
            load(["not_int", "hello"], cast(Any, Tuple[int, str]))

    def test_tuple_variable_length(self):
        t: Tuple[int, ...] = load([1, 2, 3], cast(Any, Tuple[int, ...]))
        assert t == (1, 2, 3)

        # Variable length tuple serialization
        s = serialize((1, 2, 3), expected_type=cast(Any, Tuple[int, ...]))
        assert s == [1, 2, 3]


# ============================================================================
# 11. NamedTuple & TypedDict Edge Cases
# ============================================================================
class TestNamedTupleAndTypedDictEdgeCases:
    """Test NamedTuple and TypedDict edge cases."""

    class Coordinate(NamedTuple):
        x: int
        y: int
        label: str = "origin"

    def test_namedtuple_from_sequence(self):
        c = load([10, 20], self.Coordinate)
        assert c.x == 10
        assert c.y == 20
        assert c.label == "origin"

    def test_namedtuple_with_defaults(self):
        c = load({"x": 5, "y": 15}, self.Coordinate)
        assert c.x == 5
        assert c.y == 15
        assert c.label == "origin"

    def test_namedtuple_missing_required(self):
        with pytest.raises(DeserializationError):
            load({"x": 5}, self.Coordinate)

    def test_namedtuple_invalid_input_type(self):
        with pytest.raises(DeserializationError):
            load(999, self.Coordinate)

    class UserProfile(TypedDict):
        username: str
        score: int

    def test_typeddict_invalid_input(self):
        with pytest.raises(DeserializationError):
            load("not_a_dict", self.UserProfile)

    def test_typeddict_serialization(self):
        profile = {"username": "alice", "score": 100}
        dumped = serialize(profile, expected_type=cast(Any, self.UserProfile))
        assert dumped == {"username": "alice", "score": 100}


# ============================================================================
# 12. Registry and Predicates
# ============================================================================
class TestRegistryEdgeCases:
    """Test Registry top-level helpers, predicates, and subclass lookup."""

    def test_global_registry_decorators_and_lookup(self):
        class CustomPoint:
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

        @serializer(CustomPoint)
        def ser_point(p: CustomPoint) -> str:
            return f"{p.x},{p.y}"

        @deserializer(CustomPoint)
        def deser_point(s: str) -> CustomPoint:
            x, y = map(int, s.split(","))
            return CustomPoint(x, y)

        assert get_serializer(CustomPoint) is not None
        assert get_deserializer(CustomPoint) is not None

        dumped = dump(CustomPoint(3, 4))
        assert dumped == "3,4"

        restored = load("3,4", CustomPoint)
        assert restored.x == 3
        assert restored.y == 4

        # Clear global registry and verify
        clear_registry()
        assert get_serializer(CustomPoint) is None
        assert get_deserializer(CustomPoint) is None

    def test_predicate_and_subclass_registration(self):
        reg = Registry()

        class Base:
            pass

        class Sub(Base):
            pass

        reg.register_serializer(Base, lambda b: "base_serialized")
        reg.register_deserializer(Base, lambda s: Sub())

        # Subclass lookup
        ser = reg.get_serializer(Sub)
        assert ser is not None
        assert ser(Sub()) == "base_serialized"

        deser = reg.get_deserializer(Sub)
        assert deser is not None
        assert isinstance(deser("val"), Sub)

        # Predicate registration
        reg.register_serializer(
            lambda obj: isinstance(obj, str) and obj.startswith("pre_"),
            lambda obj: f"converted_{obj}",
        )
        pred_ser = reg.get_serializer("pre_test")
        assert pred_ser is not None
        assert pred_ser("pre_test") == "converted_pre_test"

        # Predicate deserializer with 2 parameters (value, target_type)
        reg.register_deserializer(
            lambda t: t == "special_type",
            lambda v, t: f"result_{v}_{t}",
        )
        pred_deser = reg.get_deserializer("special_type")
        assert pred_deser is not None
        assert pred_deser("val", "special_type") == "result_val_special_type"

    def test_custom_serializer_error_wrapped(self):
        reg = Registry()

        class ErrorObj:
            pass

        reg.register_serializer(ErrorObj, lambda x: 1 / 0)

        with pytest.raises(SerializationError):
            serialize(ErrorObj(), registry=reg)

    def test_custom_deserializer_error_wrapped(self):
        reg = Registry()

        class ErrorObj:
            pass

        reg.register_deserializer(ErrorObj, lambda x: 1 / 0)

        with pytest.raises(DeserializationError):
            deserialize_error = reg.get_deserializer(ErrorObj)
            assert deserialize_error is not None
            load("foo", ErrorObj, registry=reg)


# ============================================================================
# 13. Dynamic Dataclass Attributes and is_serializable
# ============================================================================
class TestDynamicDataclassAttributesAndCanDump:
    """Test dynamic attributes added to dataclasses and is_serializable function."""

    def test_dynamic_attributes_serialized(self):
        @dataclass
        class Person:
            name: str

        p = Person("Alice")
        p.dynamic_note = "extra information"  # type: ignore[attr-defined]

        dumped = dump(p)
        assert dumped["name"] == "Alice"
        assert dumped["dynamic_note"] == "extra information"

    def test_is_serializable(self):
        @dataclass
        class Valid:
            a: int

        assert is_serializable(Valid(1)) is True
        assert is_serializable("hello") is True
        assert is_serializable([1, 2, 3]) is True

        class NonSerializable:
            pass

        assert is_serializable(NonSerializable()) is False


# ============================================================================
# 14. Direct Low-Level Functions & Inspection Helpers
# ============================================================================
class TestLowLevelAndInspectionHelpers:
    """Test edge cases of low-level helper functions for complete branch coverage."""

    def test_serialize_dataclass_non_dataclass_raises(self):
        with pytest.raises(JsonPortError, match="must be a dataclass"):
            _serialize_dataclass("not_a_dataclass")

    def test_deserialize_dataclass_non_dataclass_raises(self):
        with pytest.raises(JsonPortError, match="must be a dataclass"):
            _deserialize_dataclass({}, int)

    def test_none_for_non_optional_raises(self):
        with pytest.raises(
            DeserializationError, match="Expected <class 'int'> but got None"
        ):
            load(None, int)

    def test_literal_deserialization_invalid_value(self):
        with pytest.raises(DeserializationError):
            load("green", cast(Any, Literal["red", "blue"]))

    def test_safe_issubclass(self):
        assert safe_issubclass(int, (int, float)) is True
        assert safe_issubclass("not_a_class", int) is False
        assert safe_issubclass(Union[int, str], int) is False

    def test_inspection_helpers(self):
        assert is_extended_type(uuid.UUID) is True
        assert is_extended_type(int) is False
        assert is_extended_instance(uuid.uuid4()) is True
        assert is_extended_instance(123) is False

        assert is_typeddict_instance({"a": 1}) is True
        assert is_typeddict_instance("not_dict") is False

        assert get_union_args(int) == ()
        assert is_optional(int) is False
        assert get_literal_args(int) == ()
        assert get_dataclass_fields(int) == {}

        # unwrap_optional
        assert unwrap_optional(int) is int
        assert unwrap_optional(Optional[int]) is int
        assert is_union(unwrap_optional(Optional[Union[int, str]]))
