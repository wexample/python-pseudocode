from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Type


class WithConfigRegistry:
    """Minimal registry to map pseudocode items to config loader classes.

    Mirrors the PHP trait `WithConfigRegistry` for our limited scope (constants only).
    """

    _registry: Dict[str, Type]

    def __init__(self) -> None:
        # Register supported item types here
        from wexample_pseudocode.config.constant_config import ConstantConfig  # local import to avoid cycles
        from wexample_pseudocode.config.class_config import ClassConfig
        from wexample_pseudocode.config.function_config import FunctionConfig

        self._registry = {
            "constant": ConstantConfig,
            "class": ClassConfig,
            "function": FunctionConfig,
        }

    def get_config_registry(self) -> WithConfigRegistry:
        return self

    def find_matching_config_loader(self, data: dict) -> Optional[Type]:
        item_type = data.get("type")
        if not item_type:
            return None
        return self._registry.get(item_type)
