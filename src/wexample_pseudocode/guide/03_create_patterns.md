# Création des patterns

## Structure du fichier patterns.yml

```yaml
file_patterns:
  category_name:
    pattern1: "chemin/vers/{variable}/fichier.py"
    pattern2: "chemin/vers/{variable}/autre.py"

class_patterns:
  category_name:
    class1: "{Name}Suffix"
    class2: "Prefix{Name}"
```

## Bonnes pratiques

1. Utiliser des variables
```yaml
# ❌ Mauvais - Hardcodé
source: wexample_prompt/responses/data/tree_prompt_response.py

# ✅ Bon - Utilise des variables
source: wexample_prompt/responses/{category}/{name}_prompt_response.py
```

2. Regrouper par catégorie
```yaml
# ❌ Mauvais - Plat
patterns:
  source: "..."
  test: "..."
  mixin: "..."

# ✅ Bon - Groupé
file_patterns:
  prompt_response:
    source: "..."
    test: "..."
    mixin: "..."
```

3. Documenter les variables
```yaml
file_patterns:
  prompt_response:
    source: wexample_prompt/responses/{category}/{name}_prompt_response.py
    vars:
      category:
        description: "Catégorie du prompt (data, messages, etc.)"
        type: string
      name:
        description: "Nom du prompt (tree, title, etc.)"
        type: string
```

4. Prévoir la réutilisation
```yaml
# Définir des bases communes
base_patterns:
  python_file: "{name}.py"
  python_test: "test_{name}.py"

# Les réutiliser
file_patterns:
  prompt_response:
    source: "responses/${base_patterns.python_file}"
    test: "tests/${base_patterns.python_test}"
```
