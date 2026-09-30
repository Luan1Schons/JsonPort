# Types & Schema Support

JsonPort 2.0 provides native support for Python primitives, standard collections, dataclasses, modern typing constructs, and extended Python standard library types.

---

## Supported Types Overview

| Category | Supported Types |
|----------|-----------------|
| **Primitives** | `str`, `int`, `float`, `bool`, `None` |
| **Collections** | `list`, `tuple` (fixed & variable), `set`, `frozenset`, `dict` |
| **DateTime** | `datetime.datetime`, `datetime.date`, `datetime.time`, `datetime.timedelta` |
| **Extended Standard Library** | `uuid.UUID`, `decimal.Decimal`, `pathlib.Path`, `pathlib.PurePath`, `bytes`, `bytearray`, `re.Pattern`, `ipaddress.IPv4Address`, `IPv6Address`, `IPv4Network`, `IPv6Network` |
| **Modern Typing** | `typing.Literal`, `typing.Union` (PEP 604 `A | B`), `typing.Optional`, `typing.NamedTuple`, `typing.TypedDict` |
| **Data Models** | `dataclass` (with `alias`, `exclude`, field `serializer` / `deserializer`), `Enum`, `IntEnum` |

---

## Extended Standard Library Types

### UUID (`uuid.UUID`)

UUID objects are automatically serialized to standard hex-hyphenated strings and restored to `uuid.UUID` instances during deserialization.

```python
import uuid
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class Account:
    id: uuid.UUID
    email: str

acc = Account(id=uuid.uuid4(), email="dev@example.com")
json_str = dumps(acc)
# {"id": "12345678-1234-5678-1234-567812345678", "email": "dev@example.com"}

restored = loads(json_str, Account)
assert isinstance(restored.id, uuid.UUID)
```

### Decimal (`decimal.Decimal`)

`Decimal` instances preserve exact numeric precision by serializing to string representation, avoiding floating-point rounding errors.

```python
import decimal
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class Transaction:
    amount: decimal.Decimal

tx = Transaction(amount=decimal.Decimal("123456789.987654321"))
json_str = dumps(tx)
# {"amount": "123456789.987654321"}

restored = loads(json_str, Transaction)
assert restored.amount == decimal.Decimal("123456789.987654321")
```

### Filesystem Paths (`pathlib.Path`)

`pathlib.Path` and `pathlib.PurePath` serialize to standard string paths and deserialize back into `Path` instances:

```python
import pathlib
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class Config:
    log_dir: pathlib.Path

cfg = Config(log_dir=pathlib.Path("/var/log/app"))
json_str = dumps(cfg)
# {"log_dir": "/var/log/app"}

restored = loads(json_str, Config)
assert isinstance(restored.log_dir, pathlib.Path)
```

### Binary Data (`bytes` / `bytearray`)

Binary data is encoded to Base64 ASCII strings during serialization, and safely decoded with validation during deserialization:

```python
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class KeyStore:
    secret_bytes: bytes

ks = KeyStore(secret_bytes=b"super_secret_payload")
json_str = dumps(ks)
# {"secret_bytes": "c3VwZXJfc2VjcmV0X3BheWxvYWQ="}

restored = loads(json_str, KeyStore)
assert restored.secret_bytes == b"super_secret_payload"
```

### IP Addresses & Networks (`ipaddress`)

Supports `IPv4Address`, `IPv6Address`, `IPv4Network`, and `IPv6Network`:

```python
import ipaddress
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class NetworkNode:
    ip: ipaddress.IPv4Address
    subnet: ipaddress.IPv4Network

node = NetworkNode(
    ip=ipaddress.IPv4Address("192.168.1.10"),
    subnet=ipaddress.IPv4Network("192.168.1.0/24"),
)
json_str = dumps(node)
# {"ip": "192.168.1.10", "subnet": "192.168.1.0/24"}

restored = loads(json_str, NetworkNode)
assert restored.ip == ipaddress.IPv4Address("192.168.1.10")
```

### Timedelta (`datetime.timedelta`)

Serialized as total seconds (float or int):

```python
import datetime
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class Job:
    timeout: datetime.timedelta

job = Job(timeout=datetime.timedelta(minutes=5, seconds=30))
json_str = dumps(job)
# {"timeout": 330.0}

restored = loads(json_str, Job)
assert restored.timeout == datetime.timedelta(seconds=330)
```

### Regular Expression Patterns (`re.Pattern`)

```python
import re
from dataclasses import dataclass
from jsonport import dumps, loads

@dataclass
class Validator:
    rule: re.Pattern

val = Validator(rule=re.compile(r"^[A-Z0-9]+$"))
json_str = dumps(val)
# {"rule": "^[A-Z0-9]+$"}

restored = loads(json_str, Validator)
assert restored.rule.pattern == "^[A-Z0-9]+$"
```

---

## Modern Typing Support

### Literals (`typing.Literal`)

Enforces exact permitted literal values during deserialization:

```python
from typing import Literal
from dataclasses import dataclass
from jsonport import loads

@dataclass
class Deployment:
    stage: Literal["dev", "staging", "prod"]

dep = loads('{"stage": "prod"}', Deployment)
assert dep.stage == "prod"
```

### Unions & Intelligent Dataclass Matching (`typing.Union` / `|`)

JsonPort uses an intelligent matching algorithm for `Union` types:
1. Exact type matches are prioritized.
2. For dictionaries against multiple dataclasses in a Union, candidate dataclasses are ranked by key overlap (including `alias` metadata).
3. Fallback candidates are tested in definition order.

```python
from typing import Union
from dataclasses import dataclass
from jsonport import loads

@dataclass
class Cat:
    meow: str

@dataclass
class Dog:
    bark: str

@dataclass
class PetStore:
    pet: Union[Cat, Dog]

store = loads('{"pet": {"bark": "woof"}}', PetStore)
assert isinstance(store.pet, Dog)
```

### NamedTuples (`typing.NamedTuple`)

NamedTuples can be deserialized from both dictionaries and sequences (lists/tuples):

```python
from typing import NamedTuple
from jsonport import loads

class Point(NamedTuple):
    x: int
    y: int
    label: str = "origin"

# From dict
p1 = loads('{"x": 10, "y": 20}', Point)
assert p1.label == "origin"

# From list
p2 = loads('[10, 20]', Point)
assert p2.x == 10
```

### TypedDicts (`typing.TypedDict`)

```python
from typing import TypedDict
from jsonport import loads

class ServerStats(TypedDict):
    hostname: str
    cpu_percent: float

stats = loads('{"hostname": "srv-01", "cpu_percent": 12.5}', ServerStats)
assert stats["hostname"] == "srv-01"
```

---

## Dataclass Field Metadata

Use `dataclasses.field(metadata={...})` to customize behavior per-field:

```python
from dataclasses import dataclass, field
from jsonport import dumps, loads

@dataclass
class UserCredentials:
    # Rename external JSON key
    username: str = field(metadata={"alias": "user_id"})

    # Exclude from serialization
    hashed_password: str = field(metadata={"exclude": True})

    # Custom per-field serializer & deserializer
    created_at: str = field(
        metadata={
            "serializer": lambda val: val.upper(),
            "deserializer": lambda val: val.lower(),
        }
    )
```