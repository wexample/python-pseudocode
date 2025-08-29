from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from wexample_pseudocode.config.method_parameter_config import MethodParameterConfig
from wexample_pseudocode.common.type_normalizer import to_python_type


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
        py_ret = to_python_type(self.return_type)
        ret = f" -> {py_ret}" if py_ret else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: List[str] = []
        # Build docstring with optional param/return sections
        if self.description or any(p.description for p in self.parameters) or self.return_description:
            lines: List[str] = [self.description] if self.description else []
            has_details = any(p.description for p in self.parameters) or self.return_description
            if has_details and lines:
                lines.append("")
            for p in self.parameters:
                if p.description:
                    lines.append(f":param {p.name}: {p.description}")
            if self.return_description:
                lines.append(f":return: {self.return_description}")
            body_lines.append('"""' + "\n".join(lines) + '"""')
        body_lines.append("pass")
        inner_indent = indent * 2
        body = "\n".join(inner_indent + line for line in body_lines)
        return f"{indent}{header}\n{body}"
