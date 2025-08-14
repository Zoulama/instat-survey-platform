# Mali Reference Tables System

This document describes the Mali Reference Tables system that supports TableRef 01-09 as specified in the INSTAT SDS Survey documentation.

## Overview

The Mali Reference Tables system provides structured reference data for the Institut National de la Statistique du Mali (INSTAT) Survey Platform. It supports 9 reference tables that can be used in survey questions and data validation.

## Reference Tables

### TableRef:01 - Strategic Axis Results
**Endpoint:** `GET /api/v1/mali-references/strategic-results`
- **Description:** Axe stratégique/Objectifs opérationnel/Résultats attendus du SDS
- **Fields:** result_id, strategic_axis, operational_objective, expected_result, activity

### TableRef:02 - INSTAT Structures  
**Endpoint:** `GET /api/v1/mali-references/structures`
- **Description:** Liste des Structures pour les revues SDS
- **Fields:** structure_id, structure_name, abbreviation, structure_type, responsible_for_collection

### TableRef:03 - CMR Indicators
**Endpoint:** `GET /api/v1/mali-references/cmr-indicators`
- **Description:** Indicateurs CMR (Cadre de Mesure de la Performance)
- **Fields:** indicator_id, indicator_name, category, measurement_unit, data_source, collection_frequency

### TableRef:04 - Operational Results
**Endpoint:** `GET /api/v1/mali-references/operational-results`
- **Description:** Résultat attendu par Objectif opérationnel et Axe
- **Fields:** result_code, axis_code, objective_code, result_description, performance_indicators

### TableRef:05 - Participating Structures
**Endpoint:** `GET /api/v1/mali-references/participating-structures`
- **Description:** Autres structures devant participer à l'activité
- **Fields:** structure_code, structure_name, participation_type, role, contact_info

### TableRef:06 - Monitoring Indicators
**Endpoint:** `GET /api/v1/mali-references/monitoring-indicators`
- **Description:** Indicateur de Suivi-évaluation
- **Fields:** indicator_code, indicator_name, category, measurement_method, reporting_frequency

### TableRef:07 - Financing Sources
**Endpoint:** `GET /api/v1/mali-references/financing-sources`
- **Description:** Sources de financement
- **Fields:** source_code, source_name, source_type, currency, min_amount, max_amount

### TableRef:08 - Mali Regions
**Endpoint:** `GET /api/v1/mali-references/regions`
- **Description:** Liste des régions selon le découpage administratif du Mali
- **Fields:** region_code, region_name, region_capital, population, surface
- **Example:** Bamako (09), Kayes (01), Koulikoro (02), Sikasso (03), etc.

### TableRef:09 - Mali Cercles
**Endpoint:** `GET /api/v1/mali-references/cercles`
- **Description:** Liste des cercles selon le découpage administratif du Mali
- **Fields:** cercle_code, cercle_name, region_code, cercle_capital, population, surface
- **Example:** Kati (0204), Bamako Commune I (0901), etc.

## Generic Lookup API

**Endpoint:** `POST /api/v1/mali-references/lookup`

### Request Format
```json
{
  "table_ref": "TableRef:08",
  "search_term": "Bamako",
  "limit": 10
}
```

### Response Format
```json
{
  "table_ref": "TableRef:08",
  "results": [
    {
      "region_code": "09",
      "region_name": "Bamako",
      "region_capital": "Bamako",
      "population": 2446000,
      "surface": 252.0
    }
  ],
  "total_found": 1,
  "filtered": true
}
```

## Validation API

**Endpoint:** `GET /api/v1/mali-references/validate-reference/{table_ref}/{reference_code}`

### Example
```
GET /api/v1/mali-references/validate-reference/TableRef:08/09
```

### Response
```json
{
  "table_ref": "TableRef:08",
  "reference_code": "09",
  "exists": true
}
```

## Usage in Surveys

### Survey Question with Table Reference
```json
{
  "question_text": "Quelle est la région de la structure?",
  "question_type": "single_choice",
  "table_reference": "TableRef:08",
  "is_required": true
}
```

### Survey Response with Table Reference
```json
{
  "survey_id": 1,
  "question_id": 5,
  "response_value": "Bamako",
  "table_reference": "TableRef:08",
  "reference_code": "09"
}
```

## Data Loading

To populate the reference tables with initial data:

```bash
python scripts/load_mali_reference_data.py
```

This will load:
- 11 Mali regions
- 26+ Mali cercles (major ones)
- 6 INSTAT structures
- 5 financing sources
- 3 monitoring indicators
- 3 CMR indicators
- 3 strategic axis results
- 2 operational results
- 2 participating structures

## API Parameters

All individual table endpoints support these query parameters:
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return (1-1000)
- `search`: Text search across searchable fields

Some endpoints have additional filters:
- `/regions`: No additional filters
- `/cercles`: `region_code` - filter by region
- `/structures`: `responsible_for_collection` - filter by collection responsibility
- `/cmr-indicators`: `category` - filter by indicator category
- `/monitoring-indicators`: `category` - filter by indicator category
- `/financing-sources`: `source_type` - filter by source type

## Integration with SDS Survey

The system is specifically designed to support the Mali SDS (Statistical Development Strategy) survey as documented in `MODELISATION_Fiche2_Programme_REVUE_SDS_version01_22072025_15h14.docx`.

### Survey Sections Supported

1. **Section 1: Identification de la fiche**
   - Q1.01: Region (TableRef:08)
   - Q1.02: Cercle (TableRef:09)
   - Q1.03: Implementing structure (TableRef:02)
   - Q1.04: Data collection structure (TableRef:02)
   - Q1.05: Activity title (TableRef:01)

2. **Section 2: Caractéristiques de l'activité**
   - Financial sources (TableRef:07)
   - Monitoring indicators (TableRef:06)

### Database Schema

The system uses PostgreSQL with JSON support for flexible data structures. All tables include:
- Unique identifiers and codes
- Multi-language support (French/English)
- Audit trails (created_at, updated_at)
- Soft deletion (is_active flag)
- Relationship constraints

### Performance Considerations

- All lookups are indexed on primary keys and codes
- Search operations use database-level text matching
- Results are paginated to prevent large data transfers
- Caching can be implemented at the API level

## Maintenance

### Adding New Reference Data

1. Update the appropriate data in `data/mali_reference_sample_data.py`
2. Run the data loader script
3. Verify the data through the API endpoints

### Updating Existing Data

Reference data should be updated through database migrations or administrative interfaces to maintain data integrity and audit trails.

### Backup and Recovery

All reference tables should be included in regular database backups. The reference data is critical for survey functionality and should be treated as core system data.
