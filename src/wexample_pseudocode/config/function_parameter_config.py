from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class FunctionParameterConfig:
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    default: Any = None
    has_default: bool = False

    @classmethod
    def from_config(cls, data: Dict[str, Any]) -> "FunctionParameterConfig":
        return cls(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            default=data.get("default"),
            has_default=("default" in data),
        )

    def to_code(self) -> str:
        left = self.name if self.type is None else f"{self.name}: {self.type}"
        if self.has_default:
            if self.default is None:
                return f"{left} = None"
            return f"{left} = {_format_value(self.default)}"
        return left
