# generate_config_data parses source_code three times

**Source**: `packages/pseudocode/src/wexample_pseudocode/generator/pseudocode_generator.py:42-101`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`generate_config_data` calls `parse_module_constants`, `parse_module_classes`, and `parse_module_functions` sequentially with the same `source_code` string, likely running `ast.parse` (or equivalent) three times on the same input.

## Suggested direction
Introduce a single combined parse step that returns all three result sets from one AST walk, or accept a pre-parsed AST node as an optional argument so callers can amortize the parse cost.
