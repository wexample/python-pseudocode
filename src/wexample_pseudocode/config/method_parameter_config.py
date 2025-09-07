from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MethodParameterConfig:
    description: str | None = None
    name: str
    type: str | None = None

    def to_code(self) -> str:
        return f"{self.name}: {self.type}" if self.type is not None else self.name
