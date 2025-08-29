from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from wexample_pseudocode.config.method_parameter_config import MethodParameterConfig


@dataclass
class ClassMethodConfig:
    name: str
    description: Optional[str] = None
    parameters: List[MethodParameterConfig] = field(default_factory=list)
    return_type: Optional[str] = None
    return_description: Optional[str] = None

    @classmethod
    def from_config(cls, data: Dict[str, Any]) -> "ClassMethodConfig":
        params = []
        for p in (data.get("parameters") or []):
            params.append(
                MethodParameterConfig(
                    name=p.get("name"),
                    type=p.get("type"),
                    description=p.get("description"),
                )
            )
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            parameters=params,
            return_type=(data.get("return") or {}).get("type"),
            return_description=(data.get("return") or {}).get("description"),
        )

    def to_code(self, indent: str = "    ") -> str:
        params_src = ", ".join(["self"] + [p.to_code() for p in self.parameters])
        ret = f" -> {self.return_type}" if self.return_type else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: List[str] = []
        if self.description:
            body_lines.append('"""' + self.description + '"""')
        body_lines.append("pass")
        inner_indent = indent * 2
        body = "\n".join(inner_indent + line for line in body_lines)
        return f"{indent}{header}\n{body}"
