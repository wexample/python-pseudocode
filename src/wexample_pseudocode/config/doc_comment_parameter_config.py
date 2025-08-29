from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocCommentParameterConfig:
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
