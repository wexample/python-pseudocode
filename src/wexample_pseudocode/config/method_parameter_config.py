from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MethodParameterConfig:
    name: str

    description: str | None = None
    type: str | None = None

    def to_code(self) -> str:
        name, param_type = self.name, self.type
        return f"{name}: {param_type}" if param_type is not None else name
