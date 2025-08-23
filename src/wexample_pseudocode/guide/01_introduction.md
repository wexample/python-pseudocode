# Guide de création d'une configuration de migration

Ce guide explique comment créer une configuration de migration pour automatiser des modifications de code à grande échelle.

## Objectif

Une configuration de migration doit :
1. Être réutilisable pour des cas similaires
2. Automatiser les tâches répétitives
3. Guider les développeurs/IA pour les tâches complexes
4. Valider que toutes les étapes ont été complétées correctement

## Structure des fichiers

La configuration est divisée en plusieurs fichiers YAML :
1. `migrations/*.yml` - Les migrations spécifiques
2. `patterns.yml` - Les patterns réutilisables
3. `validations.yml` - Les validations communes
4. `actions.yml` - Les actions communes

Cette séparation permet de :
- Réutiliser les patterns/validations/actions entre différentes migrations
- Maintenir la configuration plus facilement
- Ajouter de nouvelles migrations sans dupliquer du code
