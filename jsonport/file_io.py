"""
File and stream I/O operations with automatic gzip support.
"""

import gzip
import json
import os
from typing import Any, IO, Optional, Type, TypeVar, Union

from .deserializers import deserialize
from .exceptions import JsonPortError
from .serializers import serialize

T = TypeVar("T")


def dump_stream(
    obj: Any,
    fp: IO[str],
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> None:
    """
    Serialize an object and write it as JSON to an open text stream.

    Args:
        obj: Object to serialize
        fp: File-like object open for writing text
        indent: Indentation level for formatting
        ensure_ascii: Whether to escape non-ASCII characters
        **kwargs: Extra arguments passed to serializer
    """
    data = serialize(obj, **kwargs)
    json.dump(data, fp, indent=indent, ensure_ascii=ensure_ascii)


def load_stream(
    fp: IO[str],
    target_class: Type[T],
    **kwargs: Any,
) -> T:
    """
    Read JSON from an open text stream and deserialize to target_class.

    Args:
        fp: File-like object open for reading text
        target_class: Target class for deserialization
        **kwargs: Extra arguments passed to deserializer

    Returns:
        Deserialized instance of target_class
    """
    data = json.load(fp)
    return deserialize(data, target_class, **kwargs)  # type: ignore[no-any-return]


def dump_file(
    obj: Any,
    path: Union[str, os.PathLike[str]],
    overwrite: bool = True,
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> None:
    """
    Serialize a Python object and save it to a JSON file.
    Creates directories if they don't exist and supports both regular JSON
    and gzipped JSON files (.gz extension).

    Args:
        obj: Object to serialize
        path: Path to the JSON file
        overwrite: If False, raises error when file already exists
        indent: Indentation level for formatting
        ensure_ascii: Whether to escape non-ASCII characters
        **kwargs: Extra arguments passed to serializer

    Raises:
        JsonPortError: If file exists and overwrite=False
    """
    path_str = os.fspath(path)
    directory = os.path.dirname(path_str)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if not overwrite and os.path.exists(path_str):
        raise JsonPortError(f"File already exists: {path_str}")

    if path_str.endswith(".gz"):
        with gzip.open(path_str, "wt", encoding="utf-8") as f:
            dump_stream(
                obj,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                **kwargs,
            )
    else:
        with open(path_str, "w", encoding="utf-8") as f:
            dump_stream(
                obj,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                **kwargs,
            )


def load_file(
    path: Union[str, os.PathLike[str]],
    target_class: Type[T],
    **kwargs: Any,
) -> T:
    """
    Load a JSON file (or gzipped JSON) and deserialize to target_class.

    Automatically detects gzipped files by .gz extension and handles
    decompression transparently.

    Args:
        path: Path to the JSON file
        target_class: Target class for deserialization
        **kwargs: Extra arguments passed to deserializer

    Returns:
        Instance of the target class

    Raises:
        FileNotFoundError: If the file doesn't exist
        JsonPortError: If deserialization fails
    """
    path_str = os.fspath(path)
    if path_str.endswith(".gz"):
        with gzip.open(path_str, "rt", encoding="utf-8") as f:
            return load_stream(
                f,
                target_class,
                **kwargs,
            )
    else:
        with open(path_str, "r", encoding="utf-8") as f:
            return load_stream(
                f,
                target_class,
                **kwargs,
            )
