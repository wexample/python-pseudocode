# Création des validations

## Structure du fichier validations.yml

Les validations définissent ce qui doit être vérifié :

```yaml
validations:
  # Groupes de validations
  group_name:
    - validation1
    - validation2
    
  # Validations avec paramètres
  specific_validations:
    validation_name:
      type: "type_validation"
      params:
        param1: "value1"
```

## Types de validations

1. Validations automatiques
```yaml
file_structure:
  - check_file_exists  # Le programme peut vérifier
  - check_permissions  # Le programme peut vérifier
```

2. Validations semi-automatiques
```yaml
code_quality:
  - check_method_signatures:  # Le programme peut vérifier la syntaxe
      params:
        required_params: ["self", "data"]
        return_type: "str"
```

3. Validations manuelles
```yaml
code_review:
  - check_logic:  # Requiert une revue humaine/IA
      description: "Vérifier que la logique métier est correcte"
      checklist:
        - "Les cas d'erreur sont gérés"
        - "Le code est optimisé"
```

## Bonnes pratiques

1. Grouper par type
```yaml
validations:
  syntax:    # Validations de syntaxe
  structure: # Validations de structure
  quality:   # Validations de qualité
```

2. Définir des prérequis
```yaml
validations:
  check_imports:
    requires:
      - check_file_exists
    steps:
      - verify_import_syntax
      - verify_import_exists
```

3. Paramétrer les validations
```yaml
validations:
  check_method:
    params:
      method_name: "get_example_class"
      required: true
      return_type: "Type[BaseExample]"
```

4. Documenter les validations
```yaml
validations:
  check_inheritance:
    description: "Vérifie l'héritage correct des classes"
    error_message: "La classe doit hériter de BaseClass"
    fix_suggestion: "Ajouter 'class MyClass(BaseClass):'"
```
