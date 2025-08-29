from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from wexample_pseudocode.config.generator_config import GeneratorConfig
from wexample_pseudocode.config.function_parameter_config import FunctionParameterConfig
from wexample_pseudocode.common.type_normalizer import to_python_type


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class FunctionConfig:
    name: str
    description: Optional[str] = None
    parameters: List[FunctionParameterConfig] = field(default_factory=list)
    return_type: Optional[str] = None
    return_description: Optional[str] = None

    @classmethod
    def from_config(
        cls,
        data: Dict[str, Any],
        global_config: Optional[GeneratorConfig] = None,
    ) -> "FunctionConfig":
        params = [FunctionParameterConfig.from_config(p) for p in (data.get("parameters") or [])]
        ret_type = None
        ret_desc = None
        if "return" in data:
            if isinstance(data["return"], dict):
                ret_type = (data["return"] or {}).get("type")
                ret_desc = (data["return"] or {}).get("description")
            else:
                ret_type = data["return"]
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            parameters=params,
            return_type=ret_type,
            return_description=ret_desc,
        )

    def to_code(self) -> str:
        params_src = ", ".join(p.to_code() for p in self.parameters)
        py_ret = to_python_type(self.return_type)
        ret = f" -> {py_ret}" if py_ret else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: List[str] = []
        # Build docstring with description, param and return sections when available
        doc_lines: List[str] = []
        if self.description:
            doc_lines.append(self.description)
        # parameter descriptions
        for p in self.parameters:
            if p.description:
                if not doc_lines:
                    doc_lines.append("")
                doc_lines.append("") if len(doc_lines) == 1 else None
                # ensure a blank line after short description
                pass
        # Rebuild properly to avoid tricky state
        if self.description and any(p.description for p in self.parameters) or (self.return_description):
            # Start with short desc
            lines: List[str] = [self.description] if self.description else []
            if any(p.description for p in self.parameters) or self.return_description:
                if lines:
                    lines.append("")
                for p in self.parameters:
                    if p.description:
                        lines.append(f":param {p.name}: {p.description}")
                if self.return_description:
                    lines.append(f":return: {self.return_description}")
            # emit as separate lines to preserve indentation
            if lines:
                body_lines.append('"""' + lines[0])
                for extra in lines[1:]:
                    body_lines.append(extra)
                body_lines.append('"""')
        elif self.description:
            body_lines.append('"""' + self.description + '"""')
        body_lines.append("pass")
        body = "\n".join("    " + line for line in body_lines)
        return f"{header}\n{body}"
