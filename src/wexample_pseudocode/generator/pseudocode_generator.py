from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import yaml

from wexample_pseudocode.parser.module_parser import parse_module_constants
from wexample_pseudocode.generator.abstract_generator import AbstractGenerator


@dataclass
class PseudocodeGenerator(AbstractGenerator):
    """Minimal generator focusing on Python module-level constants -> YAML pseudocode.

    Public API kept close to the PHP lib naming:
    - generate_config_data(source_code: str) -> dict
    - dump_pseudocode(data: dict) -> str
    """

    def generate_config_data(self, source_code: str) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = []

        for const in parse_module_constants(source_code):
            items.append(
                {
                    "type": "constant",
                    "name": const.name,
                    "value": const.value,
                    **({"description": const.description} if const.description else {}),
                }
            )

        return {"items": items}
