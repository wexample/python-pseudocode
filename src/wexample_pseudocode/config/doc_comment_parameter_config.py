from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocCommentParameterConfig:
    name: str
    description: str | None = None
    type: str | None = None
