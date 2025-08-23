# Création des actions

## Structure du fichier actions.yml

Les actions définissent ce qui doit être fait :

```yaml
actions:
  # Groupes d'actions
  group_name:
    action1:
      description: "..."
      steps: [...]
    
  # Actions avec paramètres
  specific_actions:
    action_name:
      type: "action_type"
      params: {...}
```

## Types d'actions

1. Actions automatiques
```yaml
file_operations:
  move_file:
    type: "command"
    command: "mv {source} {target}"
```

2. Actions semi-automatiques
```yaml
code_modifications:
  implement_method:
    type: "template"
    template: "templates/method.py.j2"
    requires_review: true
```

3. Actions manuelles
```yaml
code_review:
  review_logic:
    type: "manual"
    instructions: "Vérifier la logique métier"
    checklist: [...]
```

## Bonnes pratiques

1. Définir des dépendances
```yaml
actions:
  implement_class:
    requires:
      - create_file
      - add_imports
    steps:
      - add_class_definition
      - implement_methods
```

2. Utiliser des templates
```yaml
actions:
  create_mixin:
    template: templates/mixin.py.j2
    variables:
      class_name: "{Name}Mixin"
      methods: ["method1", "method2"]
```

3. Prévoir les rollbacks
```yaml
actions:
  move_file:
    command: "mv {source} {target}"
    rollback: "mv {target} {source}"
```

4. Gérer les erreurs
```yaml
actions:
  compile_code:
    on_error:
      - log_error
      - notify_developer
      - suggest_fix
```
