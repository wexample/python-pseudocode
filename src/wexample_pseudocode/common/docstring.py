from __future__ import annotations

import re

PARAM_RE = re.compile(
    r"^\s*:param\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<desc>.+)\s*$"
)
RETURN_RE = re.compile(r"^\s*:return[s]?\s*:\s*(?P<desc>.+)\s*$")


def parse_docstring(doc: str | None) -> dict[str, dict[str, str]]:
    """Extract simple parameter and return descriptions from a docstring.

    Supported styles (single-line only):
    - reST/Sphinx: ":param name: desc" and ":return: desc"
    - Google/NumPy minimal: "Args:"/"Parameters:" block with lines "name: desc"
    """
    result: dict[str, dict[str, str]] = {"params": {}, "return": {}}
    if not doc:
        return result

    lines = [l.strip() for l in doc.splitlines()]

    # Single pass: reST directives + block-header index collection
    header_map: dict[str, int] = {}
    for idx, line in enumerate(lines):
        m = PARAM_RE.match(line)
        if m:
            result["params"][m.group("name")] = m.group("desc").strip()
            continue
        m = RETURN_RE.match(line)
        if m:
            result["return"]["description"] = m.group("desc").strip()
            continue
        low = line.lower()
        if low.startswith("args:"):
            header_map.setdefault("args:", idx)
        elif low.startswith("parameters:"):
            header_map.setdefault("parameters:", idx)
        elif low.startswith("returns:"):
            header_map.setdefault("returns:", idx)

    # Google/NumPy minimal blocks
    def parse_block(header: str, is_params: bool) -> None:
        start = header_map.get(header)
        if start is None:
            return
        i = start + 1
        n = len(lines)
        while i < n:
            s = lines[i]  # already stripped
            if not s:
                i += 1
                continue
            # stop at next section header (simple heuristic: ends with ':')
            if s.endswith(":"):
                break
            if ":" in s:
                name, desc = s.split(":", 1)
                name = name.strip()
                desc = desc.strip()
                if is_params:
                    if name:
                        result["params"][name] = desc
                elif desc and "description" not in result["return"]:
                    result["return"]["description"] = (
                        f"{name}: {desc}" if name else desc
                    )
            i += 1

    parse_block("args:", True)
    parse_block("parameters:", True)
    parse_block("returns:", False)

    return result
