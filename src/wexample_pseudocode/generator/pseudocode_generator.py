from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import yaml

from wexample_pseudocode.parser.module_parser import parse_module_constants
from wexample_pseudocode.generator.abstract_generator import AbstractGenerator
from wexample_pseudocode.parser.class_parser import parse_module_classes
from wexample_pseudocode.parser.function_parser import parse_module_functions


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

        for cls in parse_module_classes(source_code):
            item: Dict[str, Any] = {
                "type": "class",
                "name": cls.name,
            }
            if cls.description:
                item["description"] = cls.description

            if cls.properties:
                props: List[Dict[str, Any]] = []
                for p in cls.properties:
                    pd: Dict[str, Any] = {"name": p.name}
                    if p.type is not None:
                        pd["type"] = p.type
                    if p.description:
                        pd["description"] = p.description
                    if p.default is not None:
                        pd["default"] = p.default
                    props.append(pd)
                item["properties"] = props

            if cls.methods:
                methods: List[Dict[str, Any]] = []
                for m in cls.methods:
                    md: Dict[str, Any] = {"type": "method", "name": m.name}
                    if m.description:
                        md["description"] = m.description
                    if m.parameters:
                        params: List[Dict[str, Any]] = []
                        for a in m.parameters:
                            ad: Dict[str, Any] = {"name": a.name}
                            if a.type is not None:
                                ad["type"] = a.type
                            if a.description:
                                ad["description"] = a.description
                            params.append(ad)
                        md["parameters"] = params
                    if m.return_type is not None or m.return_description is not None:
                        rd: Dict[str, Any] = {}
                        if m.return_type is not None:
                            rd["type"] = m.return_type
                        if m.return_description:
                            rd["description"] = m.return_description
                        md["return"] = rd
                    methods.append(md)
                item["methods"] = methods

            items.append(item)

        for fn in parse_module_functions(source_code):
            item: Dict[str, Any] = {
                "type": "function",
                "name": fn.name,
            }
            if fn.description:
                item["description"] = fn.description
            if fn.parameters:
                params: List[Dict[str, Any]] = []
                for p in fn.parameters:
                    pd: Dict[str, Any] = {"name": p.name}
                    if p.type is not None:
                        pd["type"] = p.type
                    if getattr(p, "has_default", False):
                        default_val = _literal_eval_safe(p.default)
                        # explicit None default (null)
                        if isinstance(getattr(p, "default", None), type(None)) or default_val is None:
                            pd["optional"] = True
                            pd["default"] = None
                        else:
                            pd["default"] = default_val
                    params.append(pd)
                item["parameters"] = params
            if fn.return_type is not None:
                item["return"] = {"type": fn.return_type}
            items.append(item)

        return {"items": items}


def _literal_eval_safe(node):
    try:
        import ast as _ast

        if node is None:
            return None
        return _ast.literal_eval(node)
    except Exception:
        try:
            import ast as _ast

            return _ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:
            return None
