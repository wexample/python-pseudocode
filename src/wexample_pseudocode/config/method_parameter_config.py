from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MethodParameterConfig:
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

    def to_code(self) -> str:
        return f"{self.name}: {self.type}" if self.type is not None else self.name
