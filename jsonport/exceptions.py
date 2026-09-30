"""
Exceptions hierarchy for the JsonPort library.
"""

from typing import Any, Optional, Type


class JsonPortError(Exception):
    """Base exception for all jsonport errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message

    def __str__(self) -> str:
        return self.message


class SerializationError(JsonPortError):
    """Raised when serialization of an object fails."""

    def __init__(
        self,
        message: str,
        object_type: Optional[Type[Any]] = None,
        field: Optional[str] = None,
        path: str = "",
    ) -> None:
        super().__init__(message)
        self.object_type: Optional[Type[Any]] = object_type
        self.field: Optional[str] = field
        self.path: str = path

    def __str__(self) -> str:
        details = []
        if self.path:
            details.append(f"path: '{self.path}'")
        if self.field:
            details.append(f"field: '{self.field}'")
        if self.object_type is not None:
            details.append(
                f"type: {getattr(self.object_type, '__name__', str(self.object_type))}"
            )
        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class DeserializationError(JsonPortError):
    """Raised when deserialization of data fails."""

    def __init__(
        self,
        message: str,
        target_type: Optional[Type[Any]] = None,
        field: Optional[str] = None,
        path: str = "",
        value: Any = None,
    ) -> None:
        super().__init__(message)
        self.target_type: Optional[Type[Any]] = target_type
        self.field: Optional[str] = field
        self.path: str = path
        self.value: Any = value

    def __str__(self) -> str:
        details = []
        if self.path:
            details.append(f"path: '{self.path}'")
        if self.field:
            details.append(f"field: '{self.field}'")
        if self.target_type is not None:
            details.append(
                f"target_type: {getattr(self.target_type, '__name__', str(self.target_type))}"
            )
        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class ConfigurationError(JsonPortError):
    """Raised when configuration or registration is invalid."""

    pass
