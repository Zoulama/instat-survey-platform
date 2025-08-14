"""
Custom exception handlers for INSTAT Survey Platform
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from datetime import datetime
import uuid

from schemas.errors import (
    ErrorResponse, 
    ErrorDetail, 
    ErrorType
)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    details = []
    for error in exc.errors():
        details.append(
            ErrorDetail(
                field=str(error["loc"][-1]),
                message=error["msg"],
                type=error["type"]
            )
        )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error_type=ErrorType.VALIDATION_ERROR,
            message="Validation failed",
            details=details,
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path,
            request_id=str(uuid.uuid4())
        ).dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_type=ErrorType.BAD_REQUEST,
            message=exc.detail,
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path,
            request_id=str(uuid.uuid4())
        ).dict()
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_type=ErrorType.INTERNAL_ERROR,
            message="An unexpected error occurred",
            details=[ErrorDetail(message=str(exc), type="unexpected_error")],
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path,
            request_id=str(uuid.uuid4())
        ).dict()
    )
