"""
Upload tracking API endpoints for INSTAT Survey Platform
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends, status
from pydantic import BaseModel
from ...utils.upload_tracker import upload_tracker
from ...utils.admin_permissions import admin_permissions
from ...infrastructure.auth.oauth2 import UserInToken, require_scopes


router = APIRouter(
    tags=["Upload Tracking"],
    prefix="/v1/api/uploads"
)


class UploadStatistics(BaseModel):
    """Upload statistics response model"""
    total_uploads: int
    unique_users: int
    total_file_size: int
    average_file_size: float
    uploads_today: int
    uploads_this_week: int
    uploads_this_month: int
    most_active_user: Optional[str]


class UploadRecord(BaseModel):
    """Upload record response model"""
    id: int
    timestamp: str
    original_filename: str
    timestamped_filename: str
    upload_timestamp: str
    uploaded_by: str
    file_size: int
    file_path: str


class CleanupResult(BaseModel):
    """File cleanup result model"""
    files_deleted: int
    message: str


class UserPermissions(BaseModel):
    """User permissions response model"""
    username: str
    permission_level: str
    can_upload_files: bool
    can_view_all_uploads: bool
    can_manage_uploads: bool
    accessible_endpoints: List[str]


@router.get(
    "/recent",
    response_model=List[UploadRecord],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def get_recent_uploads(
    limit: int = Query(50, ge=1, le=100, description="Number of recent uploads to retrieve"),
    current_user: UserInToken = require_scopes("admin:read")
) -> List[UploadRecord]:
    """Get recent file uploads"""
    try:
        uploads = upload_tracker.get_recent_uploads(limit)
        return [UploadRecord(**upload) for upload in uploads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve recent uploads: {str(e)}"
        )


@router.get(
    "/by-user/{username}",
    response_model=List[UploadRecord],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def get_uploads_by_user(
    username: str,
    limit: int = Query(50, ge=1, le=100, description="Number of uploads to retrieve"),
    current_user: UserInToken = require_scopes("admin:read")
) -> List[UploadRecord]:
    """Get file uploads by specific user"""
    try:
        uploads = upload_tracker.get_uploads_by_user(username, limit)
        return [UploadRecord(**upload) for upload in uploads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve uploads for user {username}: {str(e)}"
        )


@router.get(
    "/by-date-range",
    response_model=List[UploadRecord],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def get_uploads_by_date_range(
    start_date: datetime = Query(..., description="Start date for the range"),
    end_date: datetime = Query(..., description="End date for the range"),
    current_user: UserInToken = require_scopes("admin:read")
) -> List[UploadRecord]:
    """Get file uploads within a date range"""
    try:
        if start_date >= end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
        
        # Limit date range to prevent too large queries
        max_days = 90
        if (end_date - start_date).days > max_days:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Date range cannot exceed {max_days} days"
            )
        
        uploads = upload_tracker.get_uploads_by_date_range(start_date, end_date)
        return [UploadRecord(**upload) for upload in uploads]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve uploads by date range: {str(e)}"
        )


@router.get(
    "/statistics",
    response_model=UploadStatistics,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def get_upload_statistics(
    current_user: UserInToken = require_scopes("admin:read")
) -> UploadStatistics:
    """Get upload statistics and metrics"""
    try:
        stats = upload_tracker.get_upload_statistics()
        
        if "error" in stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to calculate statistics: {stats['error']}"
            )
        
        return UploadStatistics(**stats)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve upload statistics: {str(e)}"
        )


@router.post(
    "/cleanup",
    response_model=CleanupResult,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def cleanup_old_files(
    days_old: int = Query(30, ge=1, le=365, description="Delete files older than this many days"),
    current_user: UserInToken = require_scopes("upload:admin")
) -> CleanupResult:
    """Clean up uploaded files older than specified days (Admin only)"""
    try:
        files_deleted = upload_tracker.cleanup_old_files(days_old)
        
        return CleanupResult(
            files_deleted=files_deleted,
            message=f"Successfully deleted {files_deleted} files older than {days_old} days"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanup old files: {str(e)}"
        )


@router.get(
    "/my-uploads",
    response_model=List[UploadRecord],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"}
    }
)
async def get_my_uploads(
    limit: int = Query(50, ge=1, le=100, description="Number of uploads to retrieve"),
    current_user: UserInToken = require_scopes("upload:read")
) -> List[UploadRecord]:
    """Get uploads for the current authenticated user"""
    try:
        uploads = upload_tracker.get_uploads_by_user(current_user.username, limit)
        return [UploadRecord(**upload) for upload in uploads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve your uploads: {str(e)}"
        )


@router.get(
    "/today",
    response_model=List[UploadRecord],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
    }
)
async def get_today_uploads(
    current_user: UserInToken = require_scopes("admin:read")
) -> List[UploadRecord]:
    """Get all uploads from today"""
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        uploads = upload_tracker.get_uploads_by_date_range(today, tomorrow)
        return [UploadRecord(**upload) for upload in uploads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve today's uploads: {str(e)}"
        )


@router.get(
    "/permissions",
    response_model=UserPermissions,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"}
    }
)
async def get_user_permissions(
    current_user: UserInToken = require_scopes("upload:read")
) -> UserPermissions:
    """Get current user's permissions for upload operations"""
    try:
        return UserPermissions(
            username=current_user.username,
            permission_level=admin_permissions.get_user_permission_level(current_user),
            can_upload_files=admin_permissions.can_upload_files(current_user),
            can_view_all_uploads=admin_permissions.can_view_all_uploads(current_user),
            can_manage_uploads=admin_permissions.can_manage_uploads(current_user),
            accessible_endpoints=admin_permissions.get_accessible_endpoints(current_user)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user permissions: {str(e)}"
        )
