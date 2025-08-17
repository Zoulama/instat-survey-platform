"""
Common schemas used across different API endpoints
"""
from typing import Any, List, Optional, Dict
from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    """Schema for paginated responses"""
    data: List[Any]
    success: bool = True
    message: str = "Request successful"
    pagination: Dict[str, int]


class MessageResponse(BaseModel):
    """Schema for simple message responses"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
    success: bool = False


class HealthCheckResponse(BaseModel):
    """Schema for health check responses"""
    status: str
    timestamp: str
    version: str
    database: str
    redis: str
