"""
API Routes for Mali Reference Tables (TableRef 01-09)
Supports the INSTAT SDS Survey System with table reference lookups
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.infrastructure.database.connection import get_db
from src.infrastructure.database.mali_ref_models import (
    StrategicAxisResultModel, INSTATStructureModel, CMRIndicatorModel,
    OperationalResultModel, ParticipatingStructureModel, MonitoringIndicatorModel,
    FinancingSourceModel, MaliRegionModel, MaliCercleModel, TableReferenceMapping
)
from schemas.mali_reference_tables import (
    StrategicAxisResult, INSTATStructure, CMRIndicator, OperationalResult,
    ParticipatingStructure, MonitoringIndicator, FinancingSource, MaliRegion,
    MaliCercle, TableRefLookupRequest, TableRefLookupResponse, ReferenceTableResponse
)

router = APIRouter(prefix="/api/v1/mali-references", tags=["Mali Reference Tables"])


# Table Reference Mapping
TABLE_REF_MAPPING = {
    "TableRef:01": {
        "model": StrategicAxisResultModel,
        "schema": StrategicAxisResult,
        "name": "Axe stratégique/Objectifs opérationnel/Résultats attendus du SDS",
        "search_fields": ["strategic_axis", "operational_objective", "expected_result"],
        "display_fields": ["result_id", "strategic_axis", "operational_objective"]
    },
    "TableRef:02": {
        "model": INSTATStructureModel,
        "schema": INSTATStructure,
        "name": "Liste des Structures pour les revues SDS",
        "search_fields": ["structure_name", "abbreviation"],
        "display_fields": ["structure_id", "structure_name", "abbreviation"]
    },
    "TableRef:03": {
        "model": CMRIndicatorModel,
        "schema": CMRIndicator,
        "name": "Indicateurs CMR",
        "search_fields": ["indicator_name", "category"],
        "display_fields": ["indicator_id", "indicator_name", "category"]
    },
    "TableRef:04": {
        "model": OperationalResultModel,
        "schema": OperationalResult,
        "name": "Résultat attendu par Objectif opérationnel et Axe",
        "search_fields": ["result_description"],
        "display_fields": ["result_code", "result_description"]
    },
    "TableRef:05": {
        "model": ParticipatingStructureModel,
        "schema": ParticipatingStructure,
        "name": "Autres structures devant participer à l'activité",
        "search_fields": ["structure_name", "participation_type"],
        "display_fields": ["structure_code", "structure_name", "participation_type"]
    },
    "TableRef:06": {
        "model": MonitoringIndicatorModel,
        "schema": MonitoringIndicator,
        "name": "Indicateur de Suivi-évaluation",
        "search_fields": ["indicator_name", "category"],
        "display_fields": ["indicator_code", "indicator_name", "category"]
    },
    "TableRef:07": {
        "model": FinancingSourceModel,
        "schema": FinancingSource,
        "name": "Sources de financement",
        "search_fields": ["source_name", "source_type"],
        "display_fields": ["source_code", "source_name", "source_type"]
    },
    "TableRef:08": {
        "model": MaliRegionModel,
        "schema": MaliRegion,
        "name": "Liste des régions selon le découpage administratif du Mali",
        "search_fields": ["region_name", "region_capital"],
        "display_fields": ["region_code", "region_name", "region_capital"]
    },
    "TableRef:09": {
        "model": MaliCercleModel,
        "schema": MaliCercle,
        "name": "Liste des cercles selon le découpage administratif du Mali",
        "search_fields": ["cercle_name", "cercle_capital"],
        "display_fields": ["cercle_code", "cercle_name", "region_code"]
    }
}


# Generic Table Reference Lookup
@router.post("/lookup", response_model=TableRefLookupResponse)
async def lookup_table_reference(
    request: TableRefLookupRequest,
    db: Session = Depends(get_db)
):
    """
    Generic table reference lookup endpoint
    Supports all TableRef:01 through TableRef:09
    """
    if request.table_ref not in TABLE_REF_MAPPING:
        raise HTTPException(status_code=400, detail=f"Invalid table reference: {request.table_ref}")
    
    mapping = TABLE_REF_MAPPING[request.table_ref]
    model = mapping["model"]
    search_fields = mapping["search_fields"]
    
    # Build base query
    query = db.query(model).filter(model.is_active == True)
    
    # Apply search filter if provided
    if request.search_term:
        search_conditions = []
        for field in search_fields:
            if hasattr(model, field):
                search_conditions.append(
                    getattr(model, field).ilike(f"%{request.search_term}%")
                )
        
        if search_conditions:
            query = query.filter(or_(*search_conditions))
    
    # Apply limit
    if request.limit:
        query = query.limit(request.limit)
    
    # Execute query
    results = query.all()
    
    # Convert to dictionaries
    result_dicts = []
    for result in results:
        result_dict = {}
        for column in model.__table__.columns:
            if column.name not in ['created_at', 'updated_at', 'is_active']:
                result_dict[column.name] = getattr(result, column.name)
        result_dicts.append(result_dict)
    
    return TableRefLookupResponse(
        table_ref=request.table_ref,
        results=result_dicts,
        total_found=len(result_dicts),
        filtered=bool(request.search_term)
    )


# Individual table endpoints

# TableRef:01 - Strategic Axis Results
@router.get("/strategic-results", response_model=List[StrategicAxisResult])
async def get_strategic_results(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get strategic axis results (TableRef:01)"""
    query = db.query(StrategicAxisResultModel).filter(StrategicAxisResultModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                StrategicAxisResultModel.strategic_axis.ilike(f"%{search}%"),
                StrategicAxisResultModel.operational_objective.ilike(f"%{search}%"),
                StrategicAxisResultModel.expected_result.ilike(f"%{search}%")
            )
        )
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:02 - INSTAT Structures
@router.get("/structures", response_model=List[INSTATStructure])
async def get_instat_structures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    responsible_for_collection: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get INSTAT structures (TableRef:02)"""
    query = db.query(INSTATStructureModel).filter(INSTATStructureModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                INSTATStructureModel.structure_name.ilike(f"%{search}%"),
                INSTATStructureModel.abbreviation.ilike(f"%{search}%")
            )
        )
    
    if responsible_for_collection is not None:
        query = query.filter(INSTATStructureModel.responsible_for_collection == responsible_for_collection)
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:03 - CMR Indicators
@router.get("/cmr-indicators", response_model=List[CMRIndicator])
async def get_cmr_indicators(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get CMR indicators (TableRef:03)"""
    query = db.query(CMRIndicatorModel).filter(CMRIndicatorModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                CMRIndicatorModel.indicator_name.ilike(f"%{search}%"),
                CMRIndicatorModel.category.ilike(f"%{search}%")
            )
        )
    
    if category:
        query = query.filter(CMRIndicatorModel.category == category)
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:06 - Monitoring Indicators
@router.get("/monitoring-indicators", response_model=List[MonitoringIndicator])
async def get_monitoring_indicators(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get monitoring indicators (TableRef:06)"""
    query = db.query(MonitoringIndicatorModel).filter(MonitoringIndicatorModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                MonitoringIndicatorModel.indicator_name.ilike(f"%{search}%"),
                MonitoringIndicatorModel.category.ilike(f"%{search}%")
            )
        )
    
    if category:
        query = query.filter(MonitoringIndicatorModel.category == category)
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:07 - Financing Sources
@router.get("/financing-sources", response_model=List[FinancingSource])
async def get_financing_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    source_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get financing sources (TableRef:07)"""
    query = db.query(FinancingSourceModel).filter(FinancingSourceModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                FinancingSourceModel.source_name.ilike(f"%{search}%"),
                FinancingSourceModel.source_type.ilike(f"%{search}%")
            )
        )
    
    if source_type:
        query = query.filter(FinancingSourceModel.source_type == source_type)
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:08 - Mali Regions
@router.get("/regions", response_model=List[MaliRegion])
async def get_mali_regions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get Mali regions (TableRef:08)"""
    query = db.query(MaliRegionModel).filter(MaliRegionModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                MaliRegionModel.region_name.ilike(f"%{search}%"),
                MaliRegionModel.region_capital.ilike(f"%{search}%")
            )
        )
    
    results = query.offset(skip).limit(limit).all()
    return results


# TableRef:09 - Mali Cercles
@router.get("/cercles", response_model=List[MaliCercle])
async def get_mali_cercles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    region_code: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get Mali cercles (TableRef:09)"""
    query = db.query(MaliCercleModel).filter(MaliCercleModel.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                MaliCercleModel.cercle_name.ilike(f"%{search}%"),
                MaliCercleModel.cercle_capital.ilike(f"%{search}%")
            )
        )
    
    if region_code:
        query = query.filter(MaliCercleModel.region_code == region_code)
    
    results = query.offset(skip).limit(limit).all()
    return results


# Utility endpoints
@router.get("/table-mappings", response_model=Dict[str, Dict[str, Any]])
async def get_table_mappings():
    """Get all table reference mappings"""
    mappings = {}
    for table_ref, mapping in TABLE_REF_MAPPING.items():
        mappings[table_ref] = {
            "name": mapping["name"],
            "search_fields": mapping["search_fields"],
            "display_fields": mapping["display_fields"]
        }
    return mappings


@router.get("/validate-reference/{table_ref}/{reference_code}")
async def validate_table_reference(
    table_ref: str,
    reference_code: str,
    db: Session = Depends(get_db)
):
    """Validate if a reference code exists in the specified table"""
    if table_ref not in TABLE_REF_MAPPING:
        raise HTTPException(status_code=400, detail=f"Invalid table reference: {table_ref}")
    
    mapping = TABLE_REF_MAPPING[table_ref]
    model = mapping["model"]
    
    # Determine the primary code field based on the model
    if hasattr(model, 'region_code'):
        code_field = model.region_code
    elif hasattr(model, 'cercle_code'):
        code_field = model.cercle_code
    elif hasattr(model, 'structure_id'):
        code_field = model.structure_id
    elif hasattr(model, 'result_id'):
        code_field = model.result_id
    elif hasattr(model, 'indicator_id'):
        code_field = model.indicator_id
    elif hasattr(model, 'source_code'):
        code_field = model.source_code
    else:
        # Default to first column that contains 'code' or 'id'
        for column in model.__table__.columns:
            if 'code' in column.name or 'id' in column.name:
                code_field = getattr(model, column.name)
                break
        else:
            raise HTTPException(status_code=500, detail="Unable to determine code field for validation")
    
    # Check if the reference exists
    exists = db.query(model).filter(
        and_(
            code_field == reference_code,
            model.is_active == True
        )
    ).first() is not None
    
    return {
        "table_ref": table_ref,
        "reference_code": reference_code,
        "exists": exists
    }
