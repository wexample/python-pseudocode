# Création de la migration

## Structure du fichier de migration

```yaml
name: nom_migration
description: "Description détaillée"
version: "1.0"

imports:
  - patterns.yml
  - validations.yml
  - actions.yml

migrations:
  migration_name:
    patterns: {...}
    operations: [...]
```

## Étapes de création

1. Identifier le scope
```yaml
migrations:
  tree_prompt_response:  # Migration spécifique
    patterns:
      files: ["*_prompt_response.py"]
      
  all_prompt_responses:  # Migration générique
    patterns:
      files: ["responses/**/*.py"]
```

2. Définir les patterns
```yaml
patterns:
  source_files:
    - pattern: "{type}_prompt_response.py"
      vars:
        type: ["tree", "title", "list"]
```

3. Lister les opérations
```yaml
operations:
  - name: "verify_location"
    type: "validation"
  - name: "move_file"
    type: "action"
```

4. Ordonner les étapes
```yaml
steps:
  1_preparation:
    - verify_files
    - backup_files
  2_migration:
    - move_files
    - update_code
  3_validation:
    - run_tests
    - verify_examples
```

## Bonnes pratiques

1. Documenter chaque étape
```yaml
operations:
  - name: "update_imports"
    description: "Mise à jour des imports pour le nouveau chemin"
    why: "Les chemins ont changé suite au déplacement"
    how: "Utiliser le template d'imports"
```

2. Définir des points de contrôle
```yaml
checkpoints:
  after_move:
    - verify_files_exist
    - verify_permissions
  after_update:
    - verify_syntax
    - run_tests
```

3. Prévoir la parallélisation
```yaml
operations:
  - name: "update_all"
    parallel:
      - update_file_1
      - update_file_2
    wait_for_all: true
```

4. Gérer les dépendances
```yaml
operations:
  - name: "implement_class"
    requires:
      files:
        - "base_class.py"
      operations:
        - "create_mixin"
```
