from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from wexample_pseudocode.config.doc_comment_parameter_config import DocCommentParameterConfig
from wexample_pseudocode.config.doc_comment_return_config import DocCommentReturnConfig


@dataclass
class DocCommentConfig:
    description: Optional[str] = None
    parameters: List[DocCommentParameterConfig] = field(default_factory=list)
    returns: Optional[DocCommentReturnConfig] = None
