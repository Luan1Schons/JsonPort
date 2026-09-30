"""
Custom serializers and deserializers registry for JsonPort.
"""

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    overload,
)

SerializerFn = Callable[[Any], Any]
DeserializerFn = Callable[..., Any]
Predicate = Callable[[Any], bool]
TypeOrPredicate = Union[Type[Any], Predicate]


class Registry:
    """Isolated registry for custom serializers and deserializers."""

    def __init__(self) -> None:
        self._serializers: Dict[Any, SerializerFn] = {}
        self._predicate_serializers: List[Tuple[Predicate, SerializerFn]] = []
        self._deserializers: Dict[Any, DeserializerFn] = {}
        self._predicate_deserializers: List[Tuple[Predicate, DeserializerFn]] = []

    @overload
    def register_serializer(
        self,
        type_or_predicate: TypeOrPredicate,
        serializer_fn: SerializerFn,
    ) -> SerializerFn: ...

    @overload
    def register_serializer(
        self,
        type_or_predicate: TypeOrPredicate,
        serializer_fn: None = None,
    ) -> Callable[[SerializerFn], SerializerFn]: ...

    def register_serializer(
        self,
        type_or_predicate: TypeOrPredicate,
        serializer_fn: Optional[SerializerFn] = None,
    ) -> Any:
        def decorator(fn: SerializerFn) -> SerializerFn:
            if callable(type_or_predicate) and not isinstance(type_or_predicate, type):
                self._predicate_serializers.append((type_or_predicate, fn))
            else:
                self._serializers[type_or_predicate] = fn
            return fn

        if serializer_fn is not None:
            return decorator(serializer_fn)
        return decorator

    def serializer(
        self,
        type_or_predicate: TypeOrPredicate,
    ) -> Callable[[SerializerFn], SerializerFn]:
        """Decorator for registering a custom serializer."""
        return self.register_serializer(type_or_predicate)

    @overload
    def register_deserializer(
        self,
        type_or_predicate: TypeOrPredicate,
        deserializer_fn: DeserializerFn,
    ) -> DeserializerFn: ...

    @overload
    def register_deserializer(
        self,
        type_or_predicate: TypeOrPredicate,
        deserializer_fn: None = None,
    ) -> Callable[[DeserializerFn], DeserializerFn]: ...

    def register_deserializer(
        self,
        type_or_predicate: TypeOrPredicate,
        deserializer_fn: Optional[DeserializerFn] = None,
    ) -> Any:
        def decorator(fn: DeserializerFn) -> DeserializerFn:
            if callable(type_or_predicate) and not isinstance(type_or_predicate, type):
                self._predicate_deserializers.append((type_or_predicate, fn))
            else:
                self._deserializers[type_or_predicate] = fn
            return fn

        if deserializer_fn is not None:
            return decorator(deserializer_fn)
        return decorator

    def deserializer(
        self,
        type_or_predicate: TypeOrPredicate,
    ) -> Callable[[DeserializerFn], DeserializerFn]:
        """Decorator for registering a custom deserializer."""
        return self.register_deserializer(type_or_predicate)

    def get_serializer(self, obj_or_type: Any) -> Optional[SerializerFn]:
        """Lookup a registered serializer for an object or type."""
        target_cls = obj_or_type if isinstance(obj_or_type, type) else type(obj_or_type)
        if target_cls in self._serializers:
            return self._serializers[target_cls]

        # Check subclass match
        for reg_type, fn in self._serializers.items():
            if isinstance(reg_type, type):
                try:
                    if issubclass(target_cls, reg_type):
                        return fn
                except TypeError:
                    continue

        # Check predicates
        for pred, fn in self._predicate_serializers:
            try:
                if pred(obj_or_type):
                    return fn
            except Exception:
                continue

        return None

    def get_deserializer(self, target_type: Any) -> Optional[DeserializerFn]:
        """Lookup a registered deserializer for a target type."""
        if target_type in self._deserializers:
            return self._deserializers[target_type]

        if isinstance(target_type, type):
            for reg_type, fn in self._deserializers.items():
                if isinstance(reg_type, type):
                    try:
                        if issubclass(target_type, reg_type):
                            return fn
                    except TypeError:
                        continue

        for pred, fn in self._predicate_deserializers:
            try:
                if pred(target_type):
                    return fn
            except Exception:
                continue

        return None

    def clear(self) -> None:
        """Clear all registered serializers and deserializers."""
        self._serializers.clear()
        self._predicate_serializers.clear()
        self._deserializers.clear()
        self._predicate_deserializers.clear()


default_registry = Registry()


def get_default_registry() -> Registry:
    """Get the global default registry instance."""
    return default_registry


def register_serializer(
    type_or_predicate: TypeOrPredicate,
    serializer_fn: Optional[SerializerFn] = None,
) -> Any:
    """Register a custom serializer in the default registry."""
    return default_registry.register_serializer(type_or_predicate, serializer_fn)


def serializer(
    type_or_predicate: TypeOrPredicate,
) -> Callable[[SerializerFn], SerializerFn]:
    """Decorator to register a custom serializer in the default registry."""
    return default_registry.serializer(type_or_predicate)


def register_deserializer(
    type_or_predicate: TypeOrPredicate,
    deserializer_fn: Optional[DeserializerFn] = None,
) -> Any:
    """Register a custom deserializer in the default registry."""
    return default_registry.register_deserializer(type_or_predicate, deserializer_fn)


def deserializer(
    type_or_predicate: TypeOrPredicate,
) -> Callable[[DeserializerFn], DeserializerFn]:
    """Decorator to register a custom deserializer in the default registry."""
    return default_registry.deserializer(type_or_predicate)


def get_serializer(obj_or_type: Any) -> Optional[SerializerFn]:
    """Lookup a custom serializer in the default registry."""
    return default_registry.get_serializer(obj_or_type)


def get_deserializer(target_type: Any) -> Optional[DeserializerFn]:
    """Lookup a custom deserializer in the default registry."""
    return default_registry.get_deserializer(target_type)


def clear_registry() -> None:
    """Clear the default registry."""
    default_registry.clear()
