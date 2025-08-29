from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocCommentReturnConfig:
    description: Optional[str] = None
    type: Optional[str] = None
