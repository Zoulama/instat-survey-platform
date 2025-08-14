"""INSTAT-specific API routes."""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.domain.instat.instat_services import (
    INSTATSurveyService, TemplateService, MetricsService, ExportService,
    get_instat_survey_service, get_template_service, 
    get_metrics_service, get_export_service
)
from schemas.instat_domains import (
    INSTATSurveyCreate, INSTATSurveyResponse, INSTATSurveyUpdate,
    SurveyTemplateCreate, SurveyTemplateResponse, 
    SurveyMetricsResponse, DataExportCreate, DataExportResponse,
    SurveyDomain, SurveyCategory, WorkflowStatus, ReportingCycle
)
from schemas.responses import (
    BaseResponse, PaginatedResponse, DeleteResponse
)
from schemas.errors import (
    NotFoundErrorResponse, ValidationErrorResponse
)

router = APIRouter(prefix="/v1/instat", tags=["INSTAT"])


# INSTAT Survey Routes
@router.post(
    "/surveys",
    response_model=BaseResponse[INSTATSurveyResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create INSTAT Survey",
    description="Create a new INSTAT survey with domain-specific metadata"
)
async def create_instat_survey(
    survey_data: INSTATSurveyCreate,
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> BaseResponse[INSTATSurveyResponse]:
    """Create a new INSTAT survey."""
    survey = service.create_survey(survey_data)
    return BaseResponse[INSTATSurveyResponse](
        success=True,
        message="Survey created successfully",
        data=survey
    )


@router.get(
    "/surveys/{survey_id}",
    response_model=BaseResponse[INSTATSurveyResponse],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get INSTAT Survey",
    description="Retrieve a specific INSTAT survey by ID"
)
async def get_instat_survey(
    survey_id: int,
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> BaseResponse[INSTATSurveyResponse]:
    """Get INSTAT survey by ID."""
    survey = service.get_survey(survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found"
        )
    
    return BaseResponse[INSTATSurveyResponse](
        success=True,
        message="Survey retrieved successfully",
        data=survey
    )


@router.get(
    "/surveys",
    response_model=PaginatedResponse[INSTATSurveyResponse],
    summary="List INSTAT Surveys",
    description="List all INSTAT surveys with optional filtering"
)
async def list_instat_surveys(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    domain: Optional[SurveyDomain] = Query(None, description="Filter by survey domain"),
    category: Optional[SurveyCategory] = Query(None, description="Filter by survey category"),
    status: Optional[WorkflowStatus] = Query(None, description="Filter by survey status"),
    fiscal_year: Optional[int] = Query(None, description="Filter by fiscal year"),
    reporting_cycle: Optional[ReportingCycle] = Query(None, description="Filter by reporting cycle"),
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> PaginatedResponse[INSTATSurveyResponse]:
    """List INSTAT surveys with filtering."""
    return service.list_surveys(
        skip=skip,
        limit=limit,
        domain=domain,
        category=category,
        status=status,
        fiscal_year=fiscal_year,
        reporting_cycle=reporting_cycle
    )


@router.put(
    "/surveys/{survey_id}",
    response_model=BaseResponse[INSTATSurveyResponse],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Update INSTAT Survey",
    description="Update an existing INSTAT survey"
)
async def update_instat_survey(
    survey_id: int,
    survey_update: INSTATSurveyUpdate,
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> BaseResponse[INSTATSurveyResponse]:
    """Update INSTAT survey."""
    survey = service.update_survey(survey_id, survey_update)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found"
        )
    
    return BaseResponse[INSTATSurveyResponse](
        success=True,
        message="Survey updated successfully",
        data=survey
    )


@router.delete(
    "/surveys/{survey_id}",
    response_model=DeleteResponse,
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Delete INSTAT Survey",
    description="Delete an INSTAT survey"
)
async def delete_instat_survey(
    survey_id: int,
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> DeleteResponse:
    """Delete INSTAT survey."""
    deleted = service.delete_survey(survey_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found"
        )
    
    return DeleteResponse(
        success=True,
        message="Survey deleted successfully",
        deleted_id=survey_id
    )


# Template Routes
@router.post(
    "/templates",
    response_model=BaseResponse[SurveyTemplateResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Survey Template",
    description="Create a new reusable survey template"
)
async def create_survey_template(
    template_data: SurveyTemplateCreate,
    service: TemplateService = Depends(get_template_service)
) -> BaseResponse[SurveyTemplateResponse]:
    """Create a new survey template."""
    template = service.create_template(template_data)
    return BaseResponse[SurveyTemplateResponse](
        success=True,
        message="Template created successfully",
        data=template
    )


@router.get(
    "/templates/dashboard",
    response_model=Dict[str, Any],
    summary="Get Template Dashboard",
    description="Get template statistics and overview for dashboard display"
)
async def get_template_dashboard(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of recent templates to return"),
    service: TemplateService = Depends(get_template_service)
) -> Dict[str, Any]:
    """Get template dashboard with statistics and recent templates."""
    return service.list_templates_with_stats(skip=skip, limit=limit)


@router.get(
    "/templates/{template_id}",
    response_model=BaseResponse[SurveyTemplateResponse],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Survey Template",
    description="Retrieve a specific survey template by ID"
)
async def get_survey_template(
    template_id: int,
    service: TemplateService = Depends(get_template_service)
) -> BaseResponse[SurveyTemplateResponse]:
    """Get survey template by ID."""
    template = service.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return BaseResponse[SurveyTemplateResponse](
        success=True,
        message="Template retrieved successfully",
        data=template
    )


@router.get(
    "/templates/{template_id}/details",
    response_model=Dict[str, Any],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Template with Section Details",
    description="Get template with detailed section and question analysis for display"
)
async def get_template_details(
    template_id: int,
    service: TemplateService = Depends(get_template_service)
) -> Dict[str, Any]:
    """Get template with detailed analysis including section/question counts."""
    template_details = service.get_template_with_sections(template_id)
    if not template_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return {
        "success": True,
        "message": "Template details retrieved successfully",
        "data": template_details
    }


@router.get(
    "/templates",
    response_model=PaginatedResponse[SurveyTemplateResponse],
    summary="List Survey Templates",
    description="List all survey templates with optional filtering"
)
async def list_survey_templates(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    domain: Optional[SurveyDomain] = Query(None, description="Filter by domain"),
    category: Optional[SurveyCategory] = Query(None, description="Filter by category"),
    service: TemplateService = Depends(get_template_service)
) -> PaginatedResponse[SurveyTemplateResponse]:
    """List survey templates with filtering."""
    return service.list_templates(
        skip=skip,
        limit=limit,
        domain=domain,
        category=category
    )


# Metrics Routes
@router.get(
    "/surveys/{survey_id}/metrics",
    response_model=BaseResponse[SurveyMetricsResponse],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Survey Metrics",
    description="Get performance metrics for a specific survey"
)
async def get_survey_metrics(
    survey_id: int,
    service: MetricsService = Depends(get_metrics_service)
) -> BaseResponse[SurveyMetricsResponse]:
    """Get survey metrics."""
    metrics = service.get_survey_metrics(survey_id)
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metrics not found for survey"
        )
    
    return BaseResponse[SurveyMetricsResponse](
        success=True,
        message="Metrics retrieved successfully",
        data=metrics
    )


@router.put(
    "/surveys/{survey_id}/metrics",
    response_model=BaseResponse[SurveyMetricsResponse],
    summary="Update Survey Metrics",
    description="Update or create performance metrics for a survey"
)
async def update_survey_metrics(
    survey_id: int,
    metrics_data: Dict[str, Any],
    service: MetricsService = Depends(get_metrics_service)
) -> BaseResponse[SurveyMetricsResponse]:
    """Update survey metrics."""
    metrics = service.update_survey_metrics(survey_id, metrics_data)
    return BaseResponse[SurveyMetricsResponse](
        success=True,
        message="Metrics updated successfully",
        data=metrics
    )


# Export Routes
@router.post(
    "/exports",
    response_model=BaseResponse[DataExportResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Export Configuration",
    description="Create a new data export configuration"
)
async def create_export_config(
    export_data: DataExportCreate,
    service: ExportService = Depends(get_export_service)
) -> BaseResponse[DataExportResponse]:
    """Create export configuration."""
    export_config = service.create_export_config(export_data)
    return BaseResponse[DataExportResponse](
        success=True,
        message="Export configuration created successfully",
        data=export_config
    )


@router.get(
    "/exports",
    response_model=PaginatedResponse[DataExportResponse],
    summary="List Export Configurations",
    description="List all export configurations with optional filtering"
)
async def list_export_configs(
    survey_id: Optional[int] = Query(None, description="Filter by survey ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: ExportService = Depends(get_export_service)
) -> PaginatedResponse[DataExportResponse]:
    """List export configurations."""
    return service.list_export_configs(
        survey_id=survey_id,
        skip=skip,
        limit=limit
    )


# Dashboard and Analytics Routes
@router.get(
    "/dashboard/summary",
    response_model=Dict[str, Any],
    summary="Get Dashboard Summary",
    description="Get summary statistics for INSTAT dashboard"
)
async def get_dashboard_summary(
    service: INSTATSurveyService = Depends(get_instat_survey_service)
) -> Dict[str, Any]:
    """Get dashboard summary statistics."""
    # Get surveys by status
    total_surveys_response = service.list_surveys(limit=1)
    total_surveys = total_surveys_response.pagination.get("total", 0)
    
    draft_surveys_response = service.list_surveys(limit=1, status=WorkflowStatus.DRAFT)
    draft_surveys = draft_surveys_response.pagination.get("total", 0)
    
    published_surveys_response = service.list_surveys(limit=1, status=WorkflowStatus.PUBLISHED)
    published_surveys = published_surveys_response.pagination.get("total", 0)
    
    # Get surveys by domain
    program_surveys_response = service.list_surveys(limit=1, domain=SurveyDomain.PROGRAM_REVIEW)
    program_surveys = program_surveys_response.pagination.get("total", 0)
    
    sds_surveys_response = service.list_surveys(limit=1, domain=SurveyDomain.SDS)
    sds_surveys = sds_surveys_response.pagination.get("total", 0)
    
    diagnostic_surveys_response = service.list_surveys(limit=1, domain=SurveyDomain.DIAGNOSTIC)
    diagnostic_surveys = diagnostic_surveys_response.pagination.get("total", 0)
    
    # Get recent activity
    recent_created_response = service.list_surveys(limit=5)
    recent_updated_response = service.list_surveys(limit=5)
    
    return {
        "total_surveys": total_surveys,
        "draft_surveys": draft_surveys,
        "published_surveys": published_surveys,
        "surveys_by_domain": {
            "program": program_surveys,
            "sds": sds_surveys,
            "diagnostic": diagnostic_surveys
        },
        "recent_activity": {
            "last_created": recent_created_response.data[:5],
            "last_updated": recent_updated_response.data[:5]
        }
    }
