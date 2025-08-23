# Bonnes pratiques générales

## 1. Organisation des fichiers

```
migrations/
  ├── patterns.yml     # Patterns réutilisables
  ├── validations.yml  # Validations communes
  ├── actions.yml      # Actions communes
  └── migrations/      # Migrations spécifiques
      ├── migration1.yml
      └── migration2.yml
```

## 2. Conventions de nommage

1. Utiliser des noms descriptifs
```yaml
# ❌ Mauvais
m1:
  p1:
    f1: "..."

# ✅ Bon
migrations:
  prompt_response:
    patterns:
      files: "..."
```

2. Utiliser des verbes pour les actions
```yaml
# ❌ Mauvais
actions:
  file_move:
    ...

# ✅ Bon
actions:
  move_file:
    ...
```

## 3. Documentation

1. Documenter le pourquoi
```yaml
migrations:
  tree_response:
    description: "Migration du TreePromptResponse"
    why: "Standardisation de la structure des réponses"
    impact: "Amélioration de la maintenabilité"
```

2. Documenter les prérequis
```yaml
migrations:
  tree_response:
    requires:
      python: ">=3.8"
      packages:
        - "pydantic>=2.0"
```

## 4. Validation

1. Valider avant/après chaque étape
```yaml
operations:
  move_file:
    pre_validations:
      - check_source_exists
      - check_target_free
    post_validations:
      - check_target_exists
      - check_permissions
```

2. Prévoir des rollbacks
```yaml
operations:
  database_migration:
    steps:
      - backup_data
      - migrate_tables
    rollback:
      - restore_backup
```

## 5. Flexibilité

1. Utiliser des variables
```yaml
variables:
  base_dir: "wexample_prompt"
  response_types: ["tree", "title", "list"]

patterns:
  files:
    - "${base_dir}/responses/{type}_response.py"
```

2. Permettre la surcharge
```yaml
# Base
default_patterns:
  python_file: "{name}.py"

# Surcharge spécifique
custom_patterns:
  python_file: "custom_{name}.py"
```

## 6. Maintenance

1. Versionner les migrations
```yaml
version: "1.0"
compatibility:
  min_version: "0.5"
  max_version: "2.0"
```

2. Journaliser les changements
```yaml
changelog:
  - version: "1.0"
    date: "2024-01-01"
    changes:
      - "Ajout de la migration tree_response"
      - "Correction des patterns de test"
```
