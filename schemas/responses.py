"""
Response models for INSTAT Survey Platform API
"""
from typing import Optional, List, Any, Dict, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    """Base response model for all API responses"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    timestamp: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {},
                "timestamp": "2025-08-05T21:23:40Z"
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    success: bool = True
    message: Optional[str] = None
    data: List[T] = []
    pagination: Dict[str, Any] = {}
    timestamp: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Data retrieved successfully",
                "data": [],
                "pagination": {
                    "page": 1,
                    "limit": 20,
                    "total": 100,
                    "pages": 5,
                    "has_next": True,
                    "has_prev": False
                },
                "timestamp": "2025-08-05T21:23:40Z"
            }
        }


class SurveyResponse(BaseResponse):
    """Survey-specific response model"""
    pass


class SurveyListResponse(PaginatedResponse):
    """Survey list response model"""
    pass


class FileUploadResponse(BaseModel):
    """File upload response model"""
    success: bool = True
    message: str
    file_path: Optional[str] = None
    survey_structure: Optional[Dict[str, Any]] = None
    created_survey: Optional[Dict[str, Any]] = None
    created_template: Optional[Dict[str, Any]] = None
    issues: Optional[List[str]] = None
    upload_info: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "File 'survey_20240925_152348.xlsx' uploaded at 2024-09-25 15:23:48 UTC, parsed, and survey created successfully",
                "file_path": "/uploads/survey_20240925_152348.xlsx",
                "survey_structure": {
                    "title": "Sample Survey",
                    "description": "A sample survey",
                    "sections": []
                },
                "created_survey": {
                    "SurveyID": 1,
                    "Title": "Sample Survey",
                    "Status": "Draft"
                },
                "upload_info": {
                    "original_filename": "survey.xlsx",
                    "timestamped_filename": "survey_20240925_152348.xlsx",
                    "upload_timestamp": "2024-09-25T15:23:48.123456",
                    "uploaded_by": "admin@instat.gov.ml",
                    "file_size": 102400,
                    "file_path": "/uploads/survey_20240925_152348.xlsx"
                },
                "timestamp": "2024-09-25T15:23:48.123456Z"
            }
        }


class DeleteResponse(BaseModel):
    """Delete operation response model"""
    success: bool = True
    message: str = "Resource deleted successfully"
    deleted_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Survey deleted successfully",
                "deleted_id": 123,
                "timestamp": "2025-08-05T21:23:40Z"
            }
        }
