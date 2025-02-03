# Analyse des besoins

Avant de créer une configuration de migration, suivez ces étapes :

## 1. Identifier les patterns

Analysez votre codebase pour identifier :

### Patterns de nommage
- Fichiers sources/tests qui suivent une convention
- Classes/méthodes qui suivent une convention
- Dossiers qui suivent une structure commune

Exemple :
```yaml
# Dans notre cas :
source: "{name}_prompt_response.py"
test: "test_{name}_prompt_response.py"
```

### Patterns d'opérations
- Actions répétitives (déplacer des fichiers, créer des mixins)
- Validations communes (vérifier l'héritage, les imports)
- Tests à exécuter

## 2. Séparer les responsabilités

Pour chaque opération, déterminez qui doit l'exécuter :

### Programme
- Déplacer/créer des fichiers
- Vérifier la présence de fichiers/dossiers
- Exécuter des commandes
- Valider la syntaxe

### Développeur/IA
- Implémenter des méthodes
- Revoir la logique du code
- Corriger des bugs
- Adapter le code au contexte

## 3. Définir les dépendances

Identifiez l'ordre des opérations :
1. Validations préalables
2. Création/déplacement de fichiers
3. Modifications de code
4. Tests
5. Validations finales
