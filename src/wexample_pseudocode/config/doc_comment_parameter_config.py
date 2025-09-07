from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocCommentParameterConfig:
    description: str | None = None
    name: str
    type: str | None = None
