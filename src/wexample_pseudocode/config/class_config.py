from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from wexample_pseudocode.config.generator_config import GeneratorConfig
from wexample_pseudocode.config.class_property_config import ClassPropertyConfig
from wexample_pseudocode.config.method_parameter_config import MethodParameterConfig
from wexample_pseudocode.config.class_method_config import ClassMethodConfig


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)




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
    ) -> ClassConfig:
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
