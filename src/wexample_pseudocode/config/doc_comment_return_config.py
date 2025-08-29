from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocCommentReturnConfig:
    description: str | None = None
    type: str | None = None
