"""
Survey Management API endpoints for statistics, exports, search, and general survey operations
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import time

from src.infrastructure.auth.oauth2 import UserInToken, require_scopes
from src.infrastructure.database.connection import get_db
from schemas.survey_extensions import (
    SurveyStatistics, QuestionStatistics, SectionStatistics,
    ExportRequest, ExportResult, ExportFormat,
    SurveySearchQuery, SurveySearchResult, SurveySearchResponse
)
from schemas.survey import Survey
from schemas.instat_domains import INSTATSurveyResponse, SurveyDomain, SurveyCategory, WorkflowStatus
from schemas.responses import BaseResponse, PaginatedResponse
from schemas.errors import NotFoundErrorResponse, BadRequestErrorResponse

router = APIRouter(prefix="/v1/api/surveys", tags=["Survey Management"])


@router.get(
    "",
    response_model=PaginatedResponse[INSTATSurveyResponse],
    summary="List All Surveys",
    description="Get all surveys across all schemas with filtering"
)
async def list_all_surveys(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    domain: Optional[SurveyDomain] = Query(None, description="Filter by domain"),
    category: Optional[SurveyCategory] = Query(None, description="Filter by category"),
    status: Optional[WorkflowStatus] = Query(None, description="Filter by status"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    fiscal_year: Optional[int] = Query(None, description="Filter by fiscal year"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[INSTATSurveyResponse]:
    """List all surveys with advanced filtering capabilities."""
    
    # In a real implementation, query all survey schemas
    # surveys = query_all_surveys(db, skip, limit, domain, category, status, created_by, fiscal_year, search)
    
    # Mock survey data
    mock_surveys = [
        INSTATSurveyResponse(
            SurveyID=i,
            Title=f"Survey {i}: {['Diagnostic', 'Program Review', 'Activity Report'][i % 3]}",
            Description=f"Survey {i} description for testing purposes",
            Domain=['diagnostic', 'program_review', 'des'][i % 3],
            Category=['diagnostic', 'program_review', 'activity_report'][i % 3],
            FiscalYear=2024,
            CreatedDate=datetime.utcnow(),
            Status='draft' if i % 2 == 0 else 'published',
            CreatedBy=f"user_{(i % 5) + 1}",
            TargetAudience=["internal", "departments"],
            GeographicScope=["national", "all_regions"],
            ComplianceFramework=["ISO", "SDS4"]
        ) for i in range(skip + 1, skip + min(limit, 50) + 1)
    ]
    
    return PaginatedResponse[INSTATSurveyResponse](
        success=True,
        message=f"Retrieved {len(mock_surveys)} surveys",
        data=mock_surveys,
        pagination={
            "total": 250,  # Mock total count
            "skip": skip,
            "limit": limit,
            "pages": 25,
            "has_next": skip + limit < 250,
            "has_prev": skip > 0
        }
    )


@router.get(
    "/{survey_id}/statistics",
    response_model=BaseResponse[SurveyStatistics],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Survey Statistics",
    description="Get comprehensive statistics for a survey including responses and completion rates"
)
async def get_survey_statistics(
    survey_id: int,
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[SurveyStatistics]:
    """Get comprehensive survey statistics."""
    
    # In a real implementation, query survey and calculate statistics
    # survey = get_survey_by_id(db, survey_id)
    # if not survey:
    #     raise HTTPException(status_code=404, detail="Survey not found")
    
    # Mock statistics data
    question_stats = [
        QuestionStatistics(
            question_id=i,
            question_text=f"Question {i}: Sample question text",
            question_type=["text", "single_choice", "multiple_choice", "number"][i % 4],
            total_responses=150,
            response_rate=0.85 + (i % 10) * 0.01,
            most_common_answer="Option A" if i % 4 == 1 else None,
            answer_distribution={"Option A": 45, "Option B": 30, "Option C": 25} if i % 4 == 1 else {},
            average_time_spent=30.5 + (i % 20)
        ) for i in range(1, 16)
    ]
    
    section_stats = [
        SectionStatistics(
            section_id=i,
            section_title=f"Section {i}: Sample Section",
            total_questions=5,
            completion_rate=0.88 - (i * 0.02),
            average_time_spent=5.5 + (i * 0.5),
            questions=question_stats[(i-1)*5:i*5]
        ) for i in range(1, 4)
    ]
    
    statistics = SurveyStatistics(
        survey_id=survey_id,
        survey_title=f"Survey {survey_id} Statistics",
        total_responses=150,
        completed_responses=132,
        completion_rate=0.88,
        average_completion_time=15.5,
        response_rate_by_day={
            "2024-01-01": 15,
            "2024-01-02": 23,
            "2024-01-03": 18,
            "2024-01-04": 31,
            "2024-01-05": 27
        },
        geographic_distribution={
            "Bamako": 45,
            "Sikasso": 28,
            "Koulikoro": 22,
            "Kayes": 19,
            "Mopti": 15,
            "Tombouctou": 12,
            "Gao": 9
        },
        demographic_breakdown={
            "age_groups": {"18-25": 25, "26-35": 45, "36-45": 35, "46+": 45},
            "gender": {"male": 72, "female": 78},
            "education": {"primary": 20, "secondary": 60, "tertiary": 70}
        },
        sections=section_stats,
        last_updated=datetime.utcnow()
    )
    
    return BaseResponse[SurveyStatistics](
        success=True,
        message="Survey statistics retrieved successfully",
        data=statistics
    )


@router.post(
    "/{survey_id}/export",
    response_model=BaseResponse[ExportResult],
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        404: {"model": NotFoundErrorResponse},
        400: {"model": BadRequestErrorResponse}
    },
    summary="Export Survey Data",
    description="Export survey data in various formats (PDF, Excel, CSV, JSON)"
)
async def export_survey_data(
    survey_id: int,
    export_request: ExportRequest,
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[ExportResult]:
    """Export survey data in the requested format."""
    
    # In a real implementation, check if survey exists
    # survey = get_survey_by_id(db, survey_id)
    # if not survey:
    #     raise HTTPException(status_code=404, detail="Survey not found")
    
    # Generate unique export ID
    export_id = str(uuid.uuid4())
    
    # In a real implementation, queue the export job
    # queue_export_job(export_id, survey_id, export_request, current_user.username)
    
    # Mock export result
    export_result = ExportResult(
        export_id=export_id,
        survey_id=survey_id,
        format=export_request.format,
        file_name=f"survey_{survey_id}_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{export_request.format.lower()}",
        status="processing",
        created_at=datetime.utcnow(),
        download_count=0
    )
    
    # In a real implementation, this would be processed asynchronously
    # For demo purposes, we'll simulate immediate completion for some formats
    if export_request.format in [ExportFormat.CSV, ExportFormat.JSON]:
        export_result.status = "completed"
        export_result.completed_at = datetime.utcnow()
        export_result.file_size = 1024 * 50  # 50KB
        export_result.file_url = f"/downloads/exports/{export_id}/{export_result.file_name}"
    
    return BaseResponse[ExportResult](
        success=True,
        message="Export request submitted successfully" if export_result.status == "processing" else "Export completed successfully",
        data=export_result
    )


@router.get(
    "/search",
    response_model=BaseResponse[SurveySearchResponse],
    summary="Advanced Survey Search",
    description="Search surveys with advanced filtering and full-text search"
)
async def search_surveys(
    query: Optional[str] = Query(None, description="Text search query"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    created_date_from: Optional[str] = Query(None, description="Filter by creation date from (YYYY-MM-DD)"),
    created_date_to: Optional[str] = Query(None, description="Filter by creation date to (YYYY-MM-DD)"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    has_responses: Optional[bool] = Query(None, description="Filter by response existence"),
    min_completion_rate: Optional[float] = Query(None, description="Minimum completion rate"),
    fiscal_year: Optional[int] = Query(None, description="Filter by fiscal year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    sort_by: str = Query("created_date", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)"),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[SurveySearchResponse]:
    """Advanced search for surveys with multiple filters and full-text search."""
    
    search_start_time = time.time()
    
    # Parse tags if provided
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else None
    
    # Build search query object
    search_query = SurveySearchQuery(
        query=query,
        domain=domain,
        category=category,
        status=status,
        created_date_from=datetime.fromisoformat(created_date_from) if created_date_from else None,
        created_date_to=datetime.fromisoformat(created_date_to) if created_date_to else None,
        created_by=created_by,
        tags=tag_list,
        has_responses=has_responses,
        min_completion_rate=min_completion_rate,
        fiscal_year=fiscal_year,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    # In a real implementation, execute search query with database/search engine
    # search_results = execute_search_query(db, search_query)
    
    # Mock search results
    mock_results = [
        SurveySearchResult(
            survey_id=i,
            title=f"Survey {i}: {query or 'Sample'} Survey",
            description=f"Description for survey {i} matching search criteria",
            domain=domain or ['diagnostic', 'program_review', 'des'][i % 3],
            category=category or ['diagnostic', 'program_review', 'activity_report'][i % 3],
            status=status or ['draft', 'published', 'archived'][i % 3],
            created_date=datetime.utcnow(),
            created_by=created_by or f"user_{i % 5}",
            total_responses=i * 10,
            completion_rate=0.75 + (i % 20) * 0.01,
            tags=tag_list or [f"tag{i}", f"category{i % 3}"],
            relevance_score=0.95 - (i * 0.02)
        ) for i in range(1, min(limit + 1, 21))  # Return up to 20 results
    ]
    
    query_time = time.time() - search_start_time
    
    # Mock facets for filtering UI
    facets = {
        "domain": {"diagnostic": 45, "program_review": 32, "des": 28},
        "category": {"diagnostic": 42, "program_review": 35, "activity_report": 28},
        "status": {"draft": 55, "published": 35, "archived": 15},
        "created_by": {"user_1": 25, "user_2": 20, "user_3": 18, "user_4": 15, "user_5": 12}
    }
    
    search_response = SurveySearchResponse(
        results=mock_results,
        total_results=len(mock_results),
        query_time=query_time,
        suggestions=["diagnostic survey", "program evaluation", "activity assessment"] if query else None,
        facets=facets,
        pagination={
            "total": 105,  # Mock total
            "skip": skip,
            "limit": limit,
            "pages": 11,
            "has_next": skip + limit < 105,
            "has_prev": skip > 0
        }
    )
    
    return BaseResponse[SurveySearchResponse](
        success=True,
        message=f"Found {len(mock_results)} surveys in {query_time:.3f} seconds",
        data=search_response
    )


@router.get(
    "/exports/{export_id}",
    response_model=BaseResponse[ExportResult],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Export Status",
    description="Check the status of a survey data export"
)
async def get_export_status(
    export_id: str,
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[ExportResult]:
    """Get the status of a survey data export."""
    
    # In a real implementation, query export status from database/job queue
    # export_result = get_export_by_id(db, export_id)
    # if not export_result:
    #     raise HTTPException(status_code=404, detail="Export not found")
    
    # Mock export result
    export_result = ExportResult(
        export_id=export_id,
        survey_id=1,  # Mock survey ID
        format=ExportFormat.EXCEL,
        file_name=f"survey_export_{export_id}.xlsx",
        file_size=1024 * 250,  # 250KB
        status="completed",
        created_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
        file_url=f"/downloads/exports/{export_id}/survey_export_{export_id}.xlsx",
        download_count=0
    )
    
    return BaseResponse[ExportResult](
        success=True,
        message="Export status retrieved successfully",
        data=export_result
    )


@router.get(
    "/{survey_id}/analytics",
    response_model=BaseResponse[Dict[str, Any]],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Survey Analytics",
    description="Get advanced analytics and insights for a survey"
)
async def get_survey_analytics(
    survey_id: int,
    time_period: str = Query("30d", description="Time period for analytics (7d, 30d, 90d, 1y)"),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[Dict[str, Any]]:
    """Get advanced analytics for a survey."""
    
    # Mock analytics data
    analytics = {
        "survey_id": survey_id,
        "time_period": time_period,
        "response_trends": {
            "daily_responses": [5, 8, 12, 15, 11, 9, 14, 18, 22, 16],
            "completion_trends": [0.65, 0.68, 0.72, 0.74, 0.71, 0.69, 0.75, 0.78, 0.82, 0.79],
            "abandonment_points": {
                "section_1": 0.05,
                "section_2": 0.12,
                "section_3": 0.18,
                "section_4": 0.08
            }
        },
        "user_engagement": {
            "average_session_duration": 8.5,  # minutes
            "bounce_rate": 0.15,
            "return_rate": 0.23,
            "mobile_usage": 0.45
        },
        "quality_metrics": {
            "data_quality_score": 0.87,
            "validation_pass_rate": 0.93,
            "duplicate_responses": 3,
            "incomplete_responses": 18
        },
        "geographic_insights": {
            "top_regions": [
                {"region": "Bamako", "responses": 45, "completion_rate": 0.89},
                {"region": "Sikasso", "responses": 28, "completion_rate": 0.85},
                {"region": "Koulikoro", "responses": 22, "completion_rate": 0.82}
            ],
            "coverage_gaps": ["Tombouctou", "Gao"]
        },
        "recommendations": [
            "Consider simplifying Section 3 as it has the highest abandonment rate",
            "Mobile optimization could improve completion rates",
            "Focus collection efforts in Tombouctou and Gao regions"
        ]
    }
    
    return BaseResponse[Dict[str, Any]](
        success=True,
        message="Survey analytics retrieved successfully",
        data=analytics
    )