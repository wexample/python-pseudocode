from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from wexample_pseudocode.config.generator_config import GeneratorConfig


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class FunctionParameterConfig:
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    default: Any = None
    has_default: bool = False

    @classmethod
    def from_config(cls, data: Dict[str, Any]) -> "FunctionParameterConfig":
        return cls(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            default=data.get("default"),
            has_default=("default" in data),
        )

    def to_code(self) -> str:
        left = self.name if self.type is None else f"{self.name}: {self.type}"
        if self.has_default:
            if self.default is None:
                return f"{left} = None"
            return f"{left} = {_format_value(self.default)}"
        return left


@dataclass
class FunctionConfig:
    name: str
    description: Optional[str] = None
    parameters: List[FunctionParameterConfig] = field(default_factory=list)
    return_type: Optional[str] = None

    @classmethod
    def from_config(
        cls,
        data: Dict[str, Any],
        global_config: Optional[GeneratorConfig] = None,
    ) -> "FunctionConfig":
        params = [FunctionParameterConfig.from_config(p) for p in (data.get("parameters") or [])]
        ret_type = None
        if "return" in data:
            ret_type = (data["return"] or {}).get("type") if isinstance(data["return"], dict) else data["return"]
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            parameters=params,
            return_type=ret_type,
        )

    def to_code(self) -> str:
        params_src = ", ".join(p.to_code() for p in self.parameters)
        ret = f" -> {self.return_type}" if self.return_type else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: List[str] = []
        if self.description:
            body_lines.append('"""' + self.description + '"""')
        body_lines.append("pass")
        body = "\n".join("    " + line for line in body_lines)
        return f"{header}\n{body}"
