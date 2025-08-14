# Modèle Conceptuel de Données (MCD) - Plateforme INSTAT

## Vue d'ensemble du Schéma de Base de Données

La base de données `instat_surveys` contient 28 tables organisées en plusieurs domaines fonctionnels :

### 1. **Domaine Principal - Enquêtes et Templates**

#### Tables d'Enquêtes
- **Survey** : Table principale des enquêtes génériques
- **INSTATSurveys** : Enquêtes INSTAT enrichies avec métadonnées spécifiques
- **SurveyTemplates** : Modèles d'enquêtes réutilisables

#### Structure Hiérarchique
- **Section** : Sections principales des enquêtes
- **Subsection** : Sous-sections dans les sections
- **Question** : Questions individuelles
- **INSTATQuestions** : Questions INSTAT avec enrichissements
- **AnswerOption** : Options de réponse pour questions à choix

#### Réponses et Collecte
- **Response** : Réponses soumises aux enquêtes
- **ResponseDetail** : Détails des réponses par question
- **survey_responses** : Réponses avec références aux tables Mali

### 2. **Domaine Utilisateurs et Sécurité**

- **Users** : Utilisateurs de la plateforme
- **Roles** : Rôles et permissions
- **WorkflowActions** : Actions de workflow et historique

### 3. **Domaine Métriques et Reporting**

- **SurveyMetrics** : Métriques de performance des enquêtes
- **DataExports** : Configuration et historique des exports

### 4. **Tables de Référence Mali (9 tables)**

#### Référentiels Géographiques
- **mali_regions** : 11 régions du Mali
- **mali_cercles** : 26 cercles du Mali

#### Référentiels Organisationnels
- **instat_structures** : Structures INSTAT
- **participating_structures** : Structures participantes
- **strategic_axis_results** : Résultats des axes stratégiques

#### Référentiels Techniques  
- **cmr_indicators** : Indicateurs CMR
- **operational_results** : Résultats opérationnels
- **monitoring_indicators** : Indicateurs de suivi
- **financing_sources** : Sources de financement

### 5. **Infrastructure et Métadonnées**

- **table_reference_mappings** : Mapping des tables de référence
- **sds_activity_surveys** : Enquêtes spécifiques SDS
- **alembic_version** : Versioning des migrations

## Relations Principales

### 1. **Hiérarchie Survey → Section → Subsection → Question**
```
Survey (1) ──── (N) Section (1) ──── (N) Subsection (1) ──── (N) Question
   │                                                              │
   └──── (N) Response (1) ──── (N) ResponseDetail ──── (1) ──────┘
```

### 2. **Templates et Réutilisabilité**
```
SurveyTemplates ──── JSON(Sections) ──── JSON(Questions)
      │
      └── Metadata (Domain, Category, UsageCount)
```

### 3. **Référentiels Mali**
```
mali_regions (1) ──── (N) mali_cercles
      │                      │
      └──── (N) sds_activity_surveys ──────┘
```

### 4. **Questions et Options**
```
Question (1) ──── (N) AnswerOption
    │                     │
    └── (N) ResponseDetail ──┘
```

## Statistiques de la Base de Données

### Contenu Actuel (2025-08-10)
- **Templates** : 12 templates (5 uniques, 7 doublons)
- **Enquêtes** : ~15 enquêtes créées
- **Régions Mali** : 11 régions
- **Cercles Mali** : 26 cercles
- **Mappings** : 9 mappings de tables de référence

### Domaines Couverts
- **SDS** (Schéma Directeur de la Statistique) : Prédominant
- **Diagnostic** : Développement des capacités
- **Bilan** : Activités programmées et réalisées
- **Programmation** : Planification d'activités futures

## Contraintes et Intégrité

### Clés Étrangères
- Cascade DELETE pour maintenir l'intégrité référentielle
- SET NULL pour les références optionnelles
- Index sur les colonnes de jointure

### Contraintes Métier
- Validation des domaines INSTAT (SSN, SDS, DES, etc.)
- Statuts d'enquête contrôlés (draft, review, approved, published)
- Versions sémantiques pour les templates

### Archivage et Audit
- Timestamps automatiques (created_at, updated_at)
- Workflow tracking dans WorkflowActions
- Soft delete avec colonnes is_active

## Performance et Optimisation

### Index Stratégiques
- Primary keys et foreign keys indexées
- Index sur les champs de recherche fréquents
- Index composites pour les requêtes complexes

### Stockage JSON
- Utilisation de JSON pour la flexibilité des structures
- Optimisation pour les requêtes sur metadata
- Compression automatique des gros objets JSON

## Sécurité des Données

### Contrôle d'Accès
- Authentification basée sur Users/Roles
- Audit trail complet des modifications
- Isolation par schéma pour différents types d'enquêtes

### Confidentialité
- Chiffrement des données sensibles
- Respect des normes INSTAT de confidentialité
- Policies de rétention des données

