# Enhanced Survey Metadata Implementation

## Overview

This document describes the implementation of missing metadata fields for the INSTAT survey platform JSON structure. The following fields have been added to complete the survey metadata specification:

## Added Metadata Fields

### 1. `entryFullPath`
- **Type**: `string`
- **Description**: Full hierarchical path to the entry
- **Format**: `/Section/Subsection/Question` or `/Section/Question`
- **Example**: `"/Informations de contact/Adresse de votre bureau principal"`
- **Purpose**: Enables precise navigation and referencing within the survey structure

### 2. `entryDescription` 
- **Type**: `string`
- **Description**: Contextual description based on content type
- **Auto-generated based on field content**:
  - Geographic/Address fields: "Adresse géographique avec coordonnées requises"
  - Contact information: "Information de contact"
  - Email fields: "Adresse électronique de contact"
  - Name/ID fields: "Information d'identification personnelle"
  - Position fields: "Position ou fonction professionnelle"
  - Context sections: "Section contextuelle contenant des informations de base"

### 3. `entryAnnotation`
- **Type**: `string`
- **Description**: Additional annotation information
- **Auto-generated for**:
  - Table references: "Référence à une table de données externe"
  - Required fields: "Champ obligatoire à remplir"
  - Conditional questions: "Question conditionnelle basée sur une réponse précédente"
  - Multiple choice: "Sélection parmi les options proposées"

### 4. `caution`
- **Type**: `string`
- **Description**: Warning/caution information for sensitive or important fields
- **Auto-generated for**:
  - Sensitive data: "Information sensible - manipuler avec précaution"
  - Financial data: "Information financière - vérifier la précision"
  - Date fields: "Vérifier la validité des dates saisies"

### 5. `existingConditions`
- **Type**: `string`
- **Description**: Prerequisites or conditions for the entry
- **Auto-generated for**:
  - Conditional dependencies: "Réponse conditionnelle basée sur une question précédente"
  - Table references: "Nécessite l'accès à une table de référence externe"
  - Required fields: "Champ obligatoire - ne peut être vide"
  - Geographic fields: "Coordonnées géographiques requises pour la localisation"

### 6. `JumpToEntry`
- **Type**: `string`
- **Description**: Navigation field for survey flow control
- **Default**: `""` (empty string)
- **Purpose**: Can be populated later by the Survey manager to enable conditional navigation and skip logic

### 7. `coordinates`
- **Type**: `object`
- **Description**: ISO 6709:2022 coordinate metadata for geographic entries
- **Applied to fields containing keywords**: `adresse`, `address`, `ville`, `city`, `région`, `region`, `commune`, `cercle`, `département`, `localisation`, `location`, `géographique`, `geographic`, `coordonnées`, `coordinates`

#### Coordinate Object Structure:
```json
{
  "required": true,
  "format": "ISO 6709:2022",
  "precision": "decimal_degrees",
  "datum": "WGS84",
  "example": "+12.6392-08.0029/",
  "validation_pattern": "^[+-][0-9]{2,3}\\.[0-9]{4}[+-][0-9]{3}\\.[0-9]{4}/$",
  "description": "Coordonnées géographiques au format ISO 6709:2022 pour localisation précise"
}
```

## Implementation Details

### Files Modified/Created

1. **Enhanced Parser**: `src/utils/instat_excel_parser.py`
   - Updated to generate all missing metadata fields during JSON creation
   - Intelligent field detection based on content analysis
   - Automatic coordinate metadata generation for geographic fields

2. **Metadata Updater**: `scripts/update_survey_metadata.py`
   - Script to update existing JSON files with missing metadata
   - Preserves existing data while adding new fields
   - Handles all survey structure levels (sections, subsections, questions, options)

3. **Test/Demo Scripts**:
   - `scripts/demo_coordinate_metadata.py`: Demonstrates the coordinate functionality
   - `scripts/test_coordinate_metadata.py`: Tests the parser integration

### JSON Structure Enhancement

#### Before (Original):
```json
{
  "text": "Adresse",
  "type": "text",
  "metadata": {
    "entry_index": 1,
    "parent_index": 1,
    "table_reference": null
  }
}
```

#### After (Enhanced):
```json
{
  "text": "Adresse de votre bureau principal",
  "type": "text",
  "metadata": {
    "entry_index": 1,
    "parent_index": 1,
    "table_reference": null,
    "entryFullPath": "/Informations de contact/Adresse de votre bureau principal",
    "entryDescription": "Adresse géographique avec coordonnées requises",
    "entryAnnotation": "",
    "caution": "",
    "existingConditions": "Coordonnées géographiques requises pour la localisation",
    "JumpToEntry": "",
    "coordinates": {
      "required": true,
      "format": "ISO 6709:2022",
      "precision": "decimal_degrees",
      "datum": "WGS84",
      "example": "+12.6392-08.0029/",
      "validation_pattern": "^[+-][0-9]{2,3}\\.[0-9]{4}[+-][0-9]{3}\\.[0-9]{4}/$",
      "description": "Coordonnées géographiques au format ISO 6709:2022 pour localisation précise"
    }
  }
}
```

## ISO 6709:2022 Compliance

For address and geographic location fields, the system now includes comprehensive coordinate metadata that follows the ISO 6709:2022 standard for geographic location representation:

- **Format**: Standard coordinates representation
- **Precision**: Decimal degrees for high accuracy
- **Datum**: WGS84 (World Geodetic System 1984)
- **Validation**: Regular expression pattern for format validation
- **Example**: `+12.6392-08.0029/` (Mali coordinates format)

## Usage

### Automatic Processing
All future survey imports will automatically include the enhanced metadata.

### Existing Files Update
Run the update script to add missing fields to existing JSON files:
```bash
python3 scripts/update_survey_metadata.py
```

### Manual Implementation
For new surveys, the metadata fields are automatically populated by the enhanced parser based on content analysis.

## Benefits

1. **Complete Metadata**: All required fields now present in the JSON structure
2. **Geographic Compliance**: ISO 6709:2022 standard compliance for location data
3. **Enhanced Navigation**: Full path tracking for survey manager operations
4. **Content Intelligence**: Automatic field classification and description generation
5. **Quality Control**: Built-in cautions and conditions for data validation
6. **Future Extensibility**: JumpToEntry field ready for complex survey flow logic

## Files Updated

The following existing survey JSON files have been successfully updated with the missing metadata:

1. `MODELISATION_FICHIER_BILAN_ACTIVITES_2024_V28072025_structure.json`
2. `MODELISATION_FICHIER_DIAGNOSTIC_SSN_SDS4_DEVELOPPEMENT_V1.0.0_structure.json`
3. `MODELISATION_Fiche_De_Programmation_DES_Activites_Pour_2025_structure.json`

## Status

✅ **Complete**: All missing metadata fields have been successfully implemented and integrated into the INSTAT survey platform.

The survey manager can now perform JumpTo operations and access complete metadata for all survey elements, including precise geographic coordinates for address and location fields.
