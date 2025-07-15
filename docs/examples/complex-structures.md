# Complex Structures

JsonPort excels at handling complex nested data structures with full type preservation and automatic serialization/deserialization.

## Nested Dataclasses

### Simple Nesting

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from jsonport import dump, load

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str

@dataclass
class Contact:
    email: str
    phone: str
    website: Optional[str] = None

@dataclass
class Company:
    name: str
    address: Address
    contact: Contact
    founded_year: int

# Create nested structure
company = Company(
    name="TechCorp",
    address=Address("123 Main St", "San Francisco", "CA", "94105"),
    contact=Contact("info@techcorp.com", "+1-555-0123", "https://techcorp.com"),
    founded_year=2020
)

# Serialize
data = dump(company)
print(data)
# Output:
# {
#   "name": "TechCorp",
#   "address": {
#     "street": "123 Main St",
#     "city": "San Francisco",
#     "state": "CA",
#     "zip_code": "94105"
#   },
#   "contact": {
#     "email": "info@techcorp.com",
#     "phone": "+1-555-0123",
#     "website": "https://techcorp.com"
#   },
#   "founded_year": 2020
# }

# Deserialize
restored_company = load(data, Company)
print(restored_company.address.city)  # "San Francisco"
print(restored_company.contact.email)  # "info@techcorp.com"
```

### Deep Nesting

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Skill:
    name: str
    level: str
    years_experience: int

@dataclass
class Education:
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None

@dataclass
class WorkExperience:
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    responsibilities: List[str]

@dataclass
class Resume:
    personal_info: dict
    skills: List[Skill]
    education: List[Education]
    experience: List[WorkExperience]
    created_at: datetime

# Create complex resume
resume = Resume(
    personal_info={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-555-0123"
    },
    skills=[
        Skill("Python", "Advanced", 5),
        Skill("JavaScript", "Intermediate", 3),
        Skill("SQL", "Advanced", 4)
    ],
    education=[
        Education("BS Computer Science", "University of Tech", 2020, 3.8),
        Education("MS Data Science", "Tech Institute", 2022, 3.9)
    ],
    experience=[
        WorkExperience(
            "TechCorp",
            "Senior Developer",
            datetime(2022, 1, 1),
            None,
            ["Lead development team", "Architect solutions", "Mentor junior developers"]
        ),
        WorkExperience(
            "StartupXYZ",
            "Developer",
            datetime(2020, 6, 1),
            datetime(2021, 12, 31),
            ["Full-stack development", "API design", "Database optimization"]
        )
    ],
    created_at=datetime.now()
)

# Serialize
data = dump(resume)
print(data)
# Output:
# {
#   "personal_info": {
#     "name": "John Doe",
#     "email": "john@example.com",
#     "phone": "+1-555-0123"
#   },
#   "skills": [
#     {
#       "name": "Python",
#       "level": "Advanced",
#       "years_experience": 5
#     },
#     {
#       "name": "JavaScript",
#       "level": "Intermediate",
#       "years_experience": 3
#     },
#     {
#       "name": "SQL",
#       "level": "Advanced",
#       "years_experience": 4
#     }
#   ],
#   "education": [
#     {
#       "degree": "BS Computer Science",
#       "institution": "University of Tech",
#       "graduation_year": 2020,
#       "gpa": 3.8
#     },
#     {
#       "degree": "MS Data Science",
#       "institution": "Tech Institute",
#       "graduation_year": 2022,
#       "gpa": 3.9
#     }
#   ],
#   "experience": [
#     {
#       "company": "TechCorp",
#       "position": "Senior Developer",
#       "start_date": "2022-01-01T00:00:00",
#       "end_date": null,
#       "responsibilities": [
#         "Lead development team",
#         "Architect solutions",
#         "Mentor junior developers"
#       ]
#     },
#     {
#       "company": "StartupXYZ",
#       "position": "Developer",
#       "start_date": "2020-06-01T00:00:00",
#       "end_date": "2021-12-31T00:00:00",
#       "responsibilities": [
#         "Full-stack development",
#         "API design",
#         "Database optimization"
#       ]
#     }
#   ],
#   "created_at": "2025-01-14T10:30:00"
# }

# Deserialize
restored_resume = load(data, Resume)
print(len(restored_resume.skills))  # 3
print(restored_resume.experience[0].company)  # "TechCorp"
```

## Self-Referencing Structures

### Tree Structures

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TreeNode:
    value: str
    children: List['TreeNode'] = field(default_factory=list)
    parent: Optional['TreeNode'] = None

@dataclass
class Tree:
    root: TreeNode
    node_count: int

# Create tree structure
root = TreeNode("Root")
child1 = TreeNode("Child 1")
child2 = TreeNode("Child 2")
grandchild1 = TreeNode("Grandchild 1")
grandchild2 = TreeNode("Grandchild 2")

# Build relationships
root.children = [child1, child2]
child1.children = [grandchild1, grandchild2]
child1.parent = root
child2.parent = root
grandchild1.parent = child1
grandchild2.parent = child1

tree = Tree(root, 5)

# Serialize
data = dump(tree)
print(data)
# Output:
# {
#   "root": {
#     "value": "Root",
#     "children": [
#       {
#         "value": "Child 1",
#         "children": [
#           {
#             "value": "Grandchild 1",
#             "children": [],
#             "parent": null
#           },
#           {
#             "value": "Grandchild 2",
#             "children": [],
#             "parent": null
#           }
#         ],
#         "parent": null
#       },
#       {
#         "value": "Child 2",
#         "children": [],
#         "parent": null
#       }
#     ],
#     "parent": null
#   },
#   "node_count": 5
# }

# Deserialize
restored_tree = load(data, Tree)
print(restored_tree.root.value)  # "Root"
print(len(restored_tree.root.children))  # 2
print(restored_tree.root.children[0].value)  # "Child 1"
```

### Graph Structures

```python
from dataclasses import dataclass, field
from typing import List, Set, Dict

@dataclass
class GraphNode:
    id: str
    data: dict
    neighbors: List[str] = field(default_factory=list)

@dataclass
class Graph:
    nodes: Dict[str, GraphNode]
    edges: List[tuple]

# Create graph
graph = Graph(
    nodes={
        "A": GraphNode("A", {"name": "Node A"}, ["B", "C"]),
        "B": GraphNode("B", {"name": "Node B"}, ["A", "D"]),
        "C": GraphNode("C", {"name": "Node C"}, ["A", "D"]),
        "D": GraphNode("D", {"name": "Node D"}, ["B", "C"])
    },
    edges=[("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
)

# Serialize
data = dump(graph)
print(data)
# Output:
# {
#   "nodes": {
#     "A": {
#       "id": "A",
#       "data": {"name": "Node A"},
#       "neighbors": ["B", "C"]
#     },
#     "B": {
#       "id": "B",
#       "data": {"name": "Node B"},
#       "neighbors": ["A", "D"]
#     },
#     "C": {
#       "id": "C",
#       "data": {"name": "Node C"},
#       "neighbors": ["A", "D"]
#     },
#     "D": {
#       "id": "D",
#       "data": {"name": "Node D"},
#       "neighbors": ["B", "C"]
#     }
#   },
#   "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"]]
# }

# Deserialize
restored_graph = load(data, Graph)
print(len(restored_graph.nodes))  # 4
print(restored_graph.nodes["A"].neighbors)  # ["B", "C"]
```

## Mixed Data Types

### Complex Collections

```python
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

@dataclass
class ComplexData:
    # Basic types
    name: str
    count: int
    is_valid: bool
    score: float
    
    # Collections
    tags: Set[str]
    coordinates: Tuple[float, float]
    metadata: Dict[str, str]
    items: List[Dict[str, any]]
    
    # Optional fields
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    status: Optional[Status] = None
    
    # Nested structures
    nested_data: Optional[Dict[str, List[Dict[str, any]]]] = None

# Create complex data structure
complex_data = ComplexData(
    name="Complex Object",
    count=42,
    is_valid=True,
    score=95.5,
    tags={"python", "json", "complex"},
    coordinates=(10.5, 20.3),
    metadata={"version": "1.0", "author": "John Doe"},
    items=[
        {"id": 1, "name": "Item 1", "active": True},
        {"id": 2, "name": "Item 2", "active": False},
        {"id": 3, "name": "Item 3", "active": True}
    ],
    description="A complex data structure example",
    created_at=datetime.now(),
    status=Status.ACTIVE,
    nested_data={
        "group1": [
            {"sub_id": 1, "value": "A"},
            {"sub_id": 2, "value": "B"}
        ],
        "group2": [
            {"sub_id": 3, "value": "C"}
        ]
    }
)

# Serialize
data = dump(complex_data)
print(data)
# Output:
# {
#   "name": "Complex Object",
#   "count": 42,
#   "is_valid": true,
#   "score": 95.5,
#   "tags": ["complex", "json", "python"],
#   "coordinates": [10.5, 20.3],
#   "metadata": {
#     "version": "1.0",
#     "author": "John Doe"
#   },
#   "items": [
#     {"id": 1, "name": "Item 1", "active": true},
#     {"id": 2, "name": "Item 2", "active": false},
#     {"id": 3, "name": "Item 3", "active": true}
#   ],
#   "description": "A complex data structure example",
#   "created_at": "2025-01-14T10:30:00",
#   "status": "active",
#   "nested_data": {
#     "group1": [
#       {"sub_id": 1, "value": "A"},
#       {"sub_id": 2, "value": "B"}
#     ],
#     "group2": [
#       {"sub_id": 3, "value": "C"}
#     ]
#   }
# }

# Deserialize
restored_data = load(data, ComplexData)
print(restored_data.name)  # "Complex Object"
print(len(restored_data.items))  # 3
print(restored_data.status)  # Status.ACTIVE
print(restored_data.nested_data["group1"][0]["value"])  # "A"
```

## API Response Structures

### REST API Response

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class Pagination:
    page: int
    per_page: int
    total: int
    total_pages: int

@dataclass
class ApiError:
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class ApiResponse:
    success: bool
    data: Optional[Any] = None
    error: Optional[ApiError] = None
    pagination: Optional[Pagination] = None
    timestamp: datetime = None
    version: str = "1.0"

# Success response
success_response = ApiResponse(
    success=True,
    data={
        "users": [
            {"id": 1, "name": "John", "email": "john@example.com"},
            {"id": 2, "name": "Jane", "email": "jane@example.com"}
        ]
    },
    pagination=Pagination(page=1, per_page=10, total=2, total_pages=1),
    timestamp=datetime.now()
)

# Error response
error_response = ApiResponse(
    success=False,
    error=ApiError(
        code="VALIDATION_ERROR",
        message="Invalid input data",
        details={"field": "email", "issue": "Invalid email format"}
    ),
    timestamp=datetime.now()
)

# Serialize success response
success_data = dump(success_response)
print(success_data)
# Output:
# {
#   "success": true,
#   "data": {
#     "users": [
#       {"id": 1, "name": "John", "email": "john@example.com"},
#       {"id": 2, "name": "Jane", "email": "jane@example.com"}
#     ]
#   },
#   "error": null,
#   "pagination": {
#     "page": 1,
#     "per_page": 10,
#     "total": 2,
#     "total_pages": 1
#   },
#   "timestamp": "2025-01-14T10:30:00",
#   "version": "1.0"
# }

# Serialize error response
error_data = dump(error_response)
print(error_data)
# Output:
# {
#   "success": false,
#   "data": null,
#   "error": {
#     "code": "VALIDATION_ERROR",
#     "message": "Invalid input data",
#     "details": {
#       "field": "email",
#       "issue": "Invalid email format"
#     }
#   },
#   "pagination": null,
#   "timestamp": "2025-01-14T10:30:00",
#   "version": "1.0"
# }

# Deserialize
restored_success = load(success_data, ApiResponse)
restored_error = load(error_data, ApiResponse)

print(restored_success.success)  # True
print(restored_error.error.code)  # "VALIDATION_ERROR"
```

## Configuration Structures

### Application Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"

@dataclass
class DatabaseConfig:
    type: DatabaseType
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10
    timeout: int = 30

@dataclass
class LoggingConfig:
    level: LogLevel
    file_path: str
    max_size: int
    backup_count: int
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

@dataclass
class SecurityConfig:
    secret_key: str
    allowed_hosts: List[str]
    cors_origins: List[str]
    session_timeout: int = 3600
    max_login_attempts: int = 5

@dataclass
class AppConfig:
    name: str
    version: str
    debug: bool
    database: DatabaseConfig
    logging: LoggingConfig
    security: SecurityConfig
    features: Dict[str, bool] = field(default_factory=dict)
    metadata: Optional[Dict[str, str]] = None

# Create configuration
config = AppConfig(
    name="MyApp",
    version="1.0.0",
    debug=True,
    database=DatabaseConfig(
        type=DatabaseType.POSTGRESQL,
        host="localhost",
        port=5432,
        database="myapp",
        username="admin",
        password="secret123"
    ),
    logging=LoggingConfig(
        level=LogLevel.INFO,
        file_path="/var/log/myapp.log",
        max_size=10485760,  # 10MB
        backup_count=5
    ),
    security=SecurityConfig(
        secret_key="super-secret-key-123",
        allowed_hosts=["localhost", "127.0.0.1"],
        cors_origins=["http://localhost:3000", "https://myapp.com"]
    ),
    features={
        "api": True,
        "websocket": True,
        "caching": False,
        "monitoring": True
    },
    metadata={
        "environment": "development",
        "deployment": "local"
    }
)

# Serialize
data = dump(config)
print(data)
# Output:
# {
#   "name": "MyApp",
#   "version": "1.0.0",
#   "debug": true,
#   "database": {
#     "type": "postgresql",
#     "host": "localhost",
#     "port": 5432,
#     "database": "myapp",
#     "username": "admin",
#     "password": "secret123",
#     "pool_size": 10,
#     "timeout": 30
#   },
#   "logging": {
#     "level": "info",
#     "file_path": "/var/log/myapp.log",
#     "max_size": 10485760,
#     "backup_count": 5,
#     "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#   },
#   "security": {
#     "secret_key": "super-secret-key-123",
#     "allowed_hosts": ["localhost", "127.0.0.1"],
#     "cors_origins": ["http://localhost:3000", "https://myapp.com"],
#     "session_timeout": 3600,
#     "max_login_attempts": 5
#   },
#   "features": {
#     "api": true,
#     "websocket": true,
#     "caching": false,
#     "monitoring": true
#   },
#   "metadata": {
#     "environment": "development",
#     "deployment": "local"
#   }
# }

# Deserialize
restored_config = load(data, AppConfig)
print(restored_config.name)  # "MyApp"
print(restored_config.database.type)  # DatabaseType.POSTGRESQL
print(restored_config.features["api"])  # True
```

## Performance Considerations

### Large Complex Structures

```python
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class LargeStructure:
    items: List[Dict[str, any]]
    metadata: Dict[str, any]

# Create large structure
large_data = LargeStructure(
    items=[{"id": i, "data": f"item_{i}", "value": i * 1.5} for i in range(10000)],
    metadata={f"key_{i}": f"value_{i}" for i in range(1000)}
)

# Measure performance
start_time = time.time()
data = dump(large_data)
serialization_time = time.time() - start_time

start_time = time.time()
restored_data = load(data, LargeStructure)
deserialization_time = time.time() - start_time

print(f"Serialization time: {serialization_time:.3f}s")
print(f"Deserialization time: {deserialization_time:.3f}s")
print(f"Items count: {len(restored_data.items)}")
print(f"Metadata keys: {len(restored_data.metadata)}")
```

This comprehensive guide demonstrates how to work with complex data structures in JsonPort, including nested objects, self-referencing structures, mixed data types, and real-world examples like API responses and configuration management. 