from __future__ import annotations

_TYPING_PREFIX_LEN: int = 7  # len("typing.")
_OPTIONAL_PREFIX_LEN: int = 9  # len("Optional[")

_ARRAY_TYPES: frozenset[str] = frozenset(
    {"list", "List", "Sequence", "MutableSequence", "dict", "Dict", "Mapping"}
)
_PRIMITIVE_TYPES: frozenset[str] = frozenset(
    {"int", "float", "str", "bool", "mixed", "void", "None"}
)

# Single-lookup table used by to_python_type; "void" maps to None intentionally.
_TO_PYTHON: dict[str, str | None] = {
    "array": "list",
    "callable": "typing.Callable",
    "mixed": "typing.Any",
    "void": None,
}


def normalize_type(type_str: str | None) -> str | None:
    if type_str is None:
        return None
    t = type_str.strip()

    # Strip leading 'typing.' for readability
    if t.startswith("typing."):
        t = t[_TYPING_PREFIX_LEN:]

    # Optional[...] -> inner + marker handled by caller
    if t.startswith("Optional[") and t.endswith("]"):
        inner = t[_OPTIONAL_PREFIX_LEN:-1].strip()
        return normalize_type(inner)

    # Common aliases across languages
    # Python -> schema (PHP uses 'array')
    if t in _ARRAY_TYPES:
        return "array"

    if t == "Callable":
        return "callable"

    # Primitives stay as-is
    if t in _PRIMITIVE_TYPES:
        return t if t != "None" else None

    return t


def to_python_type(type_str: str | None) -> str | None:
    if type_str is None:
        return None
    t = type_str.strip()
    if t in _TO_PYTHON:
        return _TO_PYTHON[t]
    return t
