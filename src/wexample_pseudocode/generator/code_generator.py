from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml
from wexample_helpers.service.registry import Registry

from wexample_pseudocode.generator.abstract_generator import AbstractGenerator


def _build_config_loaders() -> Registry[type]:
    from wexample_pseudocode.config.class_config import ClassConfig
    from wexample_pseudocode.config.constant_config import ConstantConfig
    from wexample_pseudocode.config.function_config import FunctionConfig

    registry: Registry[type] = Registry()
    registry.register(ConstantConfig, key="constant")
    registry.register(ClassConfig, key="class")
    registry.register(FunctionConfig, key="function")
    return registry


@dataclass
class CodeGenerator(AbstractGenerator):
    """Generate Python code from pseudocode YAML.

    Mirrors the PHP CodeGenerator class but targets Python as the output language.
    Minimal scope: only constant items.
    """

    _config_loaders: Registry[type] = field(default_factory=_build_config_loaders)

    def generate(self, input_text: str) -> str:
        configs = self._generate_config(input_text)
        return "\n".join(cfg.to_code() for cfg in configs) + "\n" if configs else ""

    # Implement abstract method (not used directly in CodeGenerator flow)
    def generate_config_data(self, source_code: str) -> dict[str, Any]:
        raise NotImplementedError(
            "CodeGenerator does not parse source; it generates code from YAML"
        )

    def get_source_file_extension(self) -> str:
        return "yml"

    def get_target_file_extension(self) -> str:
        return "py"

    def _find_config_loader(self, item: dict) -> type | None:
        item_type = item.get("type")
        if not item_type:
            return None
        return self._config_loaders.get(item_type)

    def _generate_config(self, input_text: str):
        from wexample_pseudocode.config.generator_config import GeneratorConfig

        data = yaml.safe_load(input_text) or {}

        global_generator_config = (
            GeneratorConfig.from_config(data["generator"]) if "generator" in data else None
        )

        return [
            config_cls.from_config(item, global_generator_config)
            for item in data.get("items", []) or []
            if (config_cls := self._find_config_loader(item)) is not None
        ]
