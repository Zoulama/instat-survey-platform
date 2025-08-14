"""
Error and exception models for INSTAT Survey Platform API
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel
from enum import Enum


class ErrorType(str, Enum):
    """Error types for categorizing different kinds of errors"""
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"
    CONFLICT = "conflict"
    UNAUTHORIZED = "unauthorized"


class ErrorDetail(BaseModel):
    """Individual error detail"""
    field: Optional[str] = None
    message: str
    type: str
    context: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "field": "title",
                "message": "Title is required",
                "type": "missing",
                "context": {"min_length": 1}
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error_type: ErrorType
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None
    request_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error_type": "validation_error",
                "message": "Validation failed",
                "details": [
                    {
                        "field": "title",
                        "message": "Title is required",
                        "type": "missing"
                    }
                ],
                "timestamp": "2025-08-05T21:23:40Z",
                "path": "/v1/surveys/survey_program",
                "request_id": "req_12345"
            }
        }


class ValidationErrorResponse(ErrorResponse):
    """Validation error response"""
    error_type: ErrorType = ErrorType.VALIDATION_ERROR


class NotFoundErrorResponse(ErrorResponse):
    """Not found error response"""
    error_type: ErrorType = ErrorType.NOT_FOUND


class BadRequestErrorResponse(ErrorResponse):
    """Bad request error response"""
    error_type: ErrorType = ErrorType.BAD_REQUEST


class InternalErrorResponse(ErrorResponse):
    """Internal server error response"""
    error_type: ErrorType = ErrorType.INTERNAL_ERROR


class UnauthorizedErrorResponse(ErrorResponse):
    """Unauthorized error response"""
    error_type: ErrorType = ErrorType.UNAUTHORIZED


class ConflictErrorResponse(ErrorResponse):
    """Conflict error response"""
    error_type: ErrorType = ErrorType.CONFLICT
