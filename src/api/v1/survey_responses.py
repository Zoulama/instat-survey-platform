"""
Survey Response API endpoints for handling survey responses, progress tracking, and validation
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from src.infrastructure.auth.oauth2 import UserInToken, require_scopes
from src.infrastructure.database.connection import get_db
from schemas.survey_extensions import (
    SurveyResponseCreate, SurveyResponseUpdate, SurveyResponseData,
    SurveyProgress, ValidationResult, SurveyValidationRequest,
    ResponseStatus, ValidationSeverity, ValidationIssue
)
from schemas.responses import BaseResponse, PaginatedResponse
from schemas.errors import NotFoundErrorResponse, ValidationErrorResponse, BadRequestErrorResponse

router = APIRouter(prefix="/v1/api/surveys", tags=["Survey Responses"])


@router.post(
    "/{survey_id}/responses",
    response_model=BaseResponse[SurveyResponseData],
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse}
    },
    summary="Save Survey Response",
    description="Save partial or complete survey responses"
)
async def save_survey_response(
    survey_id: int,
    response_data: SurveyResponseCreate,
    current_user: UserInToken = require_scopes("surveys:write"),
    db: Session = Depends(get_db)
) -> BaseResponse[SurveyResponseData]:
    """Save survey response - supports both partial and complete submissions."""
    
    # Validate survey exists
    # In a real implementation, you would check if survey exists in database
    # survey = get_survey_by_id(db, survey_id)
    # if not survey:
    #     raise HTTPException(status_code=404, detail="Survey not found")
    
    # Calculate completion percentage
    total_questions = len(response_data.responses) if response_data.responses else 0
    answered_questions = len([r for r in response_data.responses if r.value is not None]) if response_data.responses else 0
    completion_percentage = (answered_questions / total_questions * 100) if total_questions > 0 else 0
    
    # Create response record
    response_id = int(str(uuid.uuid4().int)[:10])  # Simulate database ID
    
    saved_response = SurveyResponseData(
        response_id=response_id,
        survey_id=survey_id,
        respondent_id=response_data.respondent_id or current_user.username,
        respondent_metadata=response_data.respondent_metadata or {},
        responses=response_data.responses,
        status=response_data.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        completion_percentage=completion_percentage
    )
    
    # In a real implementation, save to database here
    # db_response = save_response_to_db(db, saved_response)
    
    return BaseResponse[SurveyResponseData](
        success=True,
        message=f"Survey response {'saved as draft' if response_data.save_as_draft else 'submitted'} successfully",
        data=saved_response
    )


@router.get(
    "/{survey_id}/progress",
    response_model=BaseResponse[SurveyProgress],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Get Survey Progress",
    description="Get completion progress for a survey"
)
async def get_survey_progress(
    survey_id: int,
    respondent_id: Optional[str] = Query(None, description="Specific respondent ID"),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[SurveyProgress]:
    """Get survey completion progress for a respondent."""
    
    # In a real implementation, fetch from database
    # survey = get_survey_by_id(db, survey_id)
    # if not survey:
    #     raise HTTPException(status_code=404, detail="Survey not found")
    
    # Mock progress data - replace with actual database queries
    respondent = respondent_id or current_user.username
    
    # Simulate fetching progress from database
    progress = SurveyProgress(
        survey_id=survey_id,
        respondent_id=respondent,
        total_questions=25,  # From database
        answered_questions=18,  # From responses table
        completion_percentage=72.0,
        current_section_id=3,
        current_section_title="Section 3: Personal Information",
        last_activity=datetime.utcnow(),
        estimated_time_remaining=8,  # minutes
        sections_progress=[
            {"section_id": 1, "section_title": "Basic Info", "completed": True, "questions_answered": 5, "total_questions": 5},
            {"section_id": 2, "section_title": "Demographics", "completed": True, "questions_answered": 8, "total_questions": 8},
            {"section_id": 3, "section_title": "Personal Information", "completed": False, "questions_answered": 5, "total_questions": 12}
        ]
    )
    
    return BaseResponse[SurveyProgress](
        success=True,
        message="Survey progress retrieved successfully",
        data=progress
    )


@router.post(
    "/{survey_id}/validate",
    response_model=BaseResponse[ValidationResult],
    responses={
        404: {"model": NotFoundErrorResponse},
        400: {"model": BadRequestErrorResponse}
    },
    summary="Validate Survey",
    description="Validate survey structure or response data before submission"
)
async def validate_survey(
    survey_id: int,
    validation_request: SurveyValidationRequest,
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> BaseResponse[ValidationResult]:
    """Validate survey structure or response data."""
    
    # In a real implementation, fetch survey from database
    # survey = get_survey_by_id(db, survey_id)
    # if not survey:
    #     raise HTTPException(status_code=404, detail="Survey not found")
    
    issues = []
    
    # Mock validation logic - replace with actual validation
    if validation_request.validate_structure:
        # Structure validation
        if survey_id == 999:  # Mock invalid survey
            issues.append(ValidationIssue(
                field="survey_structure",
                severity=ValidationSeverity.ERROR,
                message="Survey structure is incomplete",
                suggested_fix="Add required sections and questions",
                error_code="STRUCT_001"
            ))
    
    if validation_request.validate_data and validation_request.response_id:
        # Data validation
        issues.append(ValidationIssue(
            field="responses",
            question_id=5,
            severity=ValidationSeverity.WARNING,
            message="Response value seems unusually high",
            suggested_fix="Please verify the entered value",
            error_code="DATA_001"
        ))
    
    if validation_request.validate_business_rules:
        # Business rules validation
        if survey_id in [1, 2, 3]:  # Mock business rule
            issues.append(ValidationIssue(
                field="fiscal_year",
                section_id=1,
                severity=ValidationSeverity.INFO,
                message="Fiscal year should be current year for active surveys",
                suggested_fix="Update fiscal year to 2024",
                error_code="BIZ_001"
            ))
    
    # Count issues by severity
    errors = len([i for i in issues if i.severity == ValidationSeverity.ERROR])
    warnings = len([i for i in issues if i.severity == ValidationSeverity.WARNING])
    info = len([i for i in issues if i.severity == ValidationSeverity.INFO])
    
    validation_result = ValidationResult(
        is_valid=errors == 0,
        total_issues=len(issues),
        errors=errors,
        warnings=warnings,
        info=info,
        issues=issues,
        validation_timestamp=datetime.utcnow(),
        validated_by=current_user.username
    )
    
    return BaseResponse[ValidationResult](
        success=True,
        message=f"Validation completed with {len(issues)} issues found",
        data=validation_result
    )


@router.get(
    "/{survey_id}/responses",
    response_model=PaginatedResponse[SurveyResponseData],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="List Survey Responses",
    description="Get all responses for a survey with pagination"
)
async def list_survey_responses(
    survey_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: Optional[ResponseStatus] = Query(None, description="Filter by response status"),
    respondent_id: Optional[str] = Query(None, description="Filter by respondent ID"),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[SurveyResponseData]:
    """List all responses for a survey."""
    
    # In a real implementation, query database with filters
    # responses = query_survey_responses(db, survey_id, skip, limit, status, respondent_id)
    
    # Mock response data
    mock_responses = [
        SurveyResponseData(
            response_id=i,
            survey_id=survey_id,
            respondent_id=f"user_{i}",
            respondent_metadata={"source": "web", "device": "desktop"},
            responses=[],
            status=ResponseStatus.COMPLETED if i % 2 == 0 else ResponseStatus.IN_PROGRESS,
            created_at=datetime.utcnow(),
            completion_percentage=100.0 if i % 2 == 0 else 65.0
        ) for i in range(skip + 1, skip + limit + 1)
    ]
    
    return PaginatedResponse[SurveyResponseData](
        success=True,
        message=f"Retrieved {len(mock_responses)} survey responses",
        data=mock_responses,
        pagination={
            "total": 150,  # Mock total count
            "skip": skip,
            "limit": limit,
            "pages": 15,
            "has_next": skip + limit < 150,
            "has_prev": skip > 0
        }
    )


@router.put(
    "/{survey_id}/responses/{response_id}",
    response_model=BaseResponse[SurveyResponseData],
    responses={
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse}
    },
    summary="Update Survey Response",
    description="Update an existing survey response"
)
async def update_survey_response(
    survey_id: int,
    response_id: int,
    response_update: SurveyResponseUpdate,
    current_user: UserInToken = require_scopes("surveys:write"),
    db: Session = Depends(get_db)
) -> BaseResponse[SurveyResponseData]:
    """Update an existing survey response."""
    
    # In a real implementation, fetch existing response
    # existing_response = get_response_by_id(db, response_id)
    # if not existing_response or existing_response.survey_id != survey_id:
    #     raise HTTPException(status_code=404, detail="Response not found")
    
    # Mock updated response
    updated_response = SurveyResponseData(
        response_id=response_id,
        survey_id=survey_id,
        respondent_id=current_user.username,
        respondent_metadata=response_update.respondent_metadata or {},
        responses=response_update.responses or [],
        status=response_update.status or ResponseStatus.IN_PROGRESS,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        completion_percentage=85.0
    )
    
    return BaseResponse[SurveyResponseData](
        success=True,
        message="Survey response updated successfully",
        data=updated_response
    )


@router.delete(
    "/{survey_id}/responses/{response_id}",
    response_model=BaseResponse[Dict[str, Any]],
    responses={404: {"model": NotFoundErrorResponse}},
    summary="Delete Survey Response",
    description="Delete a survey response"
)
async def delete_survey_response(
    survey_id: int,
    response_id: int,
    current_user: UserInToken = require_scopes("surveys:delete"),
    db: Session = Depends(get_db)
) -> BaseResponse[Dict[str, Any]]:
    """Delete a survey response."""
    
    # In a real implementation, check if response exists and belongs to survey
    # response = get_response_by_id(db, response_id)
    # if not response or response.survey_id != survey_id:
    #     raise HTTPException(status_code=404, detail="Response not found")
    
    # Delete the response
    # delete_response(db, response_id)
    
    return BaseResponse[Dict[str, Any]](
        success=True,
        message="Survey response deleted successfully",
        data={"deleted_id": response_id, "survey_id": survey_id}
    )