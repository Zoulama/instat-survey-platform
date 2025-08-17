"""
Survey API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from ...infrastructure.database.connection import get_db
from ...infrastructure.auth.oauth2 import UserInToken, require_scopes
from ...domain.survey import survey_service
from schemas import survey as survey_schema
from schemas.responses import BaseResponse, PaginatedResponse, DeleteResponse
from schemas.errors import (
    ErrorResponse, 
    ValidationErrorResponse, 
    NotFoundErrorResponse, 
    BadRequestErrorResponse,
    InternalErrorResponse
)


router = APIRouter(
    tags=["Surveys"],
    prefix="/v1/api"
)


@router.post(
    "/surveys/{schema_name}", 
    response_model=BaseResponse[survey_schema.Survey],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
def create_survey(
    schema_name: str,
    survey: survey_schema.SurveyCreate,
    current_user: UserInToken = require_scopes("surveys:write"),
    db: Session = Depends(get_db)
):
    """Create a new survey"""
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    created_survey = survey_service.create_survey(db=db, survey=survey, schema_name=schema_name)
    return BaseResponse(
        message="Survey created successfully",
        data=created_survey,
        timestamp=datetime.utcnow()
    )


@router.get(
    "/surveys/{schema_name}", 
    response_model=PaginatedResponse[survey_schema.Survey],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
def read_surveys(
    schema_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
):
    """Get all surveys"""
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    surveys = survey_service.get_surveys(db=db, schema_name=schema_name, skip=skip, limit=limit)
    total_count = len(surveys)  # This should be improved with actual count query
    
    return PaginatedResponse(
        message="Surveys retrieved successfully",
        data=surveys,
        pagination={
            "page": (skip // limit) + 1,
            "limit": limit,
            "total": total_count,
            "pages": (total_count + limit - 1) // limit,
            "has_next": skip + limit < total_count,
            "has_prev": skip > 0
        },
        timestamp=datetime.utcnow()
    )


@router.get(
    "/surveys/{schema_name}/{survey_id}", 
    response_model=BaseResponse[survey_schema.Survey],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
def read_survey(
    schema_name: str,
    survey_id: int,
    current_user: UserInToken = require_scopes("surveys:read"),
    db: Session = Depends(get_db)
):
    """Get survey by ID"""
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    db_survey = survey_service.get_survey(db=db, survey_id=survey_id, schema_name=schema_name)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return BaseResponse(
        message="Survey retrieved successfully",
        data=db_survey,
        timestamp=datetime.utcnow()
    )


@router.put(
    "/surveys/{schema_name}/{survey_id}", 
    response_model=BaseResponse[survey_schema.Survey],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
def update_survey(
    schema_name: str,
    survey_id: int,
    survey: survey_schema.SurveyCreate,
    current_user: UserInToken = require_scopes("surveys:write"),
    db: Session = Depends(get_db)
):
    """Update a survey"""
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    db_survey = survey_service.update_survey(db=db, survey_id=survey_id, survey=survey, schema_name=schema_name)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return BaseResponse(
        message="Survey updated successfully",
        data=db_survey,
        timestamp=datetime.utcnow()
    )


@router.delete(
    "/surveys/{schema_name}/{survey_id}",
    response_model=DeleteResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
def delete_survey(
    schema_name: str,
    survey_id: int,
    current_user: UserInToken = require_scopes("surveys:write"),
    db: Session = Depends(get_db)
):
    """Delete a survey"""
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    db_survey = survey_service.delete_survey(db=db, survey_id=survey_id, schema_name=schema_name)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return DeleteResponse(
        message="Survey deleted successfully",
        deleted_id=survey_id,
        timestamp=datetime.utcnow()
    )
