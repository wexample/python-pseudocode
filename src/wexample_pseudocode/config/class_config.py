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
class ClassPropertyConfig:
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    default: Any = None

    def to_code(self) -> str:
        if self.type is not None:
            left = f"{self.name}: {self.type}"
        else:
            left = self.name
        code = left
        if self.default is not None:
            code += f" = {_format_value(self.default)}"
        if self.description:
            code += f"  # {self.description}"
        return code


@dataclass
class MethodParameterConfig:
    name: str
    type: Optional[str] = None

    def to_code(self) -> str:
        if self.type is not None:
            return f"{self.name}: {self.type}"
        return self.name


@dataclass
class ClassMethodConfig:
    name: str
    description: Optional[str] = None
    parameters: List[MethodParameterConfig] = field(default_factory=list)
    return_type: Optional[str] = None

    @classmethod
    def from_config(cls, data: Dict[str, Any]) -> "ClassMethodConfig":
        params = [
            MethodParameterConfig(name=p.get("name"), type=p.get("type"))
            for p in (data.get("parameters") or [])
        ]
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            parameters=params,
            return_type=(data.get("return") or {}).get("type"),
        )

    def to_code(self, indent: str = "    ") -> str:
        params_src = ", ".join(["self"] + [p.to_code() for p in self.parameters])
        ret = f" -> {self.return_type}" if self.return_type else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: List[str] = []
        if self.description:
            # Single-line docstring like in fixture
            body_lines.append('"""' + self.description + '"""')
        body_lines.append("pass")
        # Inside a class, method body should be indented two levels total
        inner_indent = indent * 2
        body = "\n".join(inner_indent + line for line in body_lines)
        return f"{indent}{header}\n{body}"


@dataclass
class ClassConfig:
    name: str
    description: Optional[str] = None
    properties: List[ClassPropertyConfig] = field(default_factory=list)
    methods: List[ClassMethodConfig] = field(default_factory=list)

    @classmethod
    def from_config(
        cls,
        data: Dict[str, Any],
        global_config: Optional[GeneratorConfig] = None,
    ) -> "ClassConfig":
        props = [
            ClassPropertyConfig(
                name=p.get("name"),
                type=p.get("type"),
                description=p.get("description"),
                default=p.get("default"),
            )
            for p in (data.get("properties") or [])
        ]
        methods = [ClassMethodConfig.from_config(m) for m in (data.get("methods") or [])]
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            properties=props,
            methods=methods,
        )

    def to_code(self) -> str:
        lines: List[str] = [f"class {self.name}:"]
        if self.description:
            lines.append(f'    """{self.description}"""')
            lines.append("")
        for p in self.properties:
            lines.append("    " + p.to_code())
        if self.properties and self.methods:
            lines.append("")
        for m in self.methods:
            lines.append(m.to_code(indent="    "))
        if not self.properties and not self.methods and not self.description:
            lines.append("    pass")
        return "\n".join(lines)
