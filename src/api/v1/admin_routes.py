"""
Admin routes for audit logging and user management
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_db
from src.infrastructure.auth.oauth2 import require_admin, UserInToken
from src.services.audit_service import AuditService
from src.services.user_service import UserService
from schemas.audit_schemas import (
    AuditLogResponse, AuditLogFilter, AuditStatistics
)
from schemas.user_schemas import UserResponse, UserCreate, UserUpdate, PasswordResetRequest, PasswordResetResponse
from schemas.common_schemas import PaginatedResponse

router = APIRouter(prefix="/v1/api/admin", tags=["Administration"])


@router.get("/audit-logs", response_model=PaginatedResponse)
async def get_audit_logs(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        user_id: Optional[int] = Query(None),
        action: Optional[str] = Query(None),
        resource: Optional[str] = Query(None),
        success: Optional[bool] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Get audit logs with filtering (Admin only)
    """
    audit_service = AuditService(db)

    # Log this admin action
    audit_service.log_action(
        user_id=current_user.user_id,
        username=current_user.username,
        action="VIEW_AUDIT_LOGS",
        resource="audit_logs",
        details={
            "filters": {
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "success": success,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    )

    # Get audit logs
    logs = audit_service.get_audit_logs(
        skip=skip,
        limit=limit,
        user_id=user_id,
        action=action,
        resource=resource,
        success=success,
        start_date=start_date,
        end_date=end_date
    )

    total_count = audit_service.get_audit_log_count(
        user_id=user_id,
        action=action,
        resource=resource,
        success=success,
        start_date=start_date,
        end_date=end_date
    )

    # Convert to response schema
    log_responses = [AuditLogResponse.from_orm(log) for log in logs]

    return PaginatedResponse(
        data=log_responses,
        success=True,
        message=f"Retrieved {len(log_responses)} audit logs",
        pagination={
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit
        }
    )


@router.get("/audit-logs/statistics", response_model=AuditStatistics)
async def get_audit_statistics(
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Get audit log statistics (Admin only)
    """
    audit_service = AuditService(db)

    # Log this admin action
    audit_service.log_action(
        user_id=current_user.user_id,
        username=current_user.username,
        action="VIEW_AUDIT_STATISTICS",
        resource="audit_logs"
    )

    stats = audit_service.get_action_statistics()
    return AuditStatistics(**stats)


@router.get("/audit-logs/recent", response_model=List[AuditLogResponse])
async def get_recent_audit_logs(
        limit: int = Query(50, ge=1, le=200),
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Get most recent audit logs (Admin only)
    """
    audit_service = AuditService(db)

    # Log this admin action
    audit_service.log_action(
        user_id=current_user.user_id,
        username=current_user.username,
        action="VIEW_RECENT_AUDIT_LOGS",
        resource="audit_logs",
        details={"limit": limit}
    )

    recent_logs = audit_service.get_recent_actions(limit=limit)
    return [AuditLogResponse.from_orm(log) for log in recent_logs]


@router.get("/audit-logs/failed", response_model=List[AuditLogResponse])
async def get_failed_audit_logs(
        limit: int = Query(100, ge=1, le=500),
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Get failed audit actions (Admin only)
    """
    audit_service = AuditService(db)

    # Log this admin action
    audit_service.log_action(
        user_id=current_user.user_id,
        username=current_user.username,
        action="VIEW_FAILED_AUDIT_LOGS",
        resource="audit_logs",
        details={"limit": limit}
    )

    failed_logs = audit_service.get_failed_actions(limit=limit)
    return [AuditLogResponse.from_orm(log) for log in failed_logs]


@router.get("/users", response_model=PaginatedResponse)
async def get_all_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=500),
        role: Optional[str] = Query(None),
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Get all users (Admin only)
    """
    audit_service = AuditService(db)
    user_service = UserService(db)

    # Log this admin action
    audit_service.log_action(
        user_id=current_user.user_id,
        username=current_user.username,
        action="VIEW_USERS",
        resource="users",
        details={"role_filter": role}
    )

    users = user_service.get_users(skip=skip, limit=limit, role=role)
    total_count = user_service.get_user_count(role=role)

    user_responses = [
        UserResponse(
            user_id=user.UserID,
            username=user.Username,
            email=user.Email,
            role=user.Role,
            status=user.Status,
            department=user.Department,
            CreatedAt=user.CreatedAt,
            UpdatedAt=user.UpdatedAt
        )
        for user in users
    ]

    return PaginatedResponse(
        data=user_responses,
        success=True,
        message=f"Retrieved {len(user_responses)} users",
        pagination={
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit
        }
    )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate,
        request: Request,
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Create a new user (Admin only)
    """
    audit_service = AuditService(db)
    user_service = UserService(db)

    try:
        new_user = user_service.create_user(user_data)

        # Log successful user creation
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="CREATE_USER",
            resource="users",
            resource_id=str(new_user.user_id),
            details={
                "created_username": new_user.username,
                "created_email": new_user.email,
                "created_role": new_user.role
            },
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        return UserResponse(
            user_id=new_user.user_id,
            username=new_user.username,
            email=new_user.email,
            role=new_user.role,
            status=new_user.status,
            department=new_user.department,
            CreatedAt=new_user.CreatedAt,
            UpdatedAt=new_user.UpdatedAt
        )

    except Exception as e:
        # Log failed user creation
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="CREATE_USER",
            resource="users",
            details={
                "attempted_username": user_data.username,
                "attempted_email": user_data.email,
                "attempted_role": user_data.role
            },
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=False,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        request: Request,
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Update a user (Admin only)
    """
    audit_service = AuditService(db)
    user_service = UserService(db)

    try:
        updated_user = user_service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Log successful user update
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="UPDATE_USER",
            resource="users",
            resource_id=str(user_id),
            details={
                "updated_fields": user_data.dict(exclude_unset=True),
                "target_username": updated_user.username
            },
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        return UserResponse(
            user_id=updated_user.user_id,
            username=updated_user.username,
            email=updated_user.email,
            role=updated_user.role,
            status=updated_user.status,
            department=updated_user.department,
            CreatedAt=updated_user.CreatedAt,
            UpdatedAt=updated_user.UpdatedAt
        )

    except Exception as e:
        # Log failed user update
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="UPDATE_USER",
            resource="users",
            resource_id=str(user_id),
            details={"attempted_updates": user_data.dict(exclude_unset=True)},
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=False,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/users/{user_id}/reset-password", response_model=PasswordResetResponse)
async def reset_user_password(
        user_id: int,
        reset_request: PasswordResetRequest,
        request: Request,
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Reset user password to a temporary password (Admin only)
    """
    audit_service = AuditService(db)
    user_service = UserService(db)

    try:
        # Reset the password
        reset_response = user_service.reset_user_password(user_id, reset_request)
        
        # Log successful password reset
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="RESET_USER_PASSWORD",
            resource="users",
            resource_id=str(user_id),
            details={
                "target_username": reset_response.username,
                "reset_timestamp": reset_response.reset_timestamp,
                "temp_password_length": reset_request.temp_password_length or 12
            },
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        return reset_response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log failed password reset
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="RESET_USER_PASSWORD",
            resource="users",
            resource_id=str(user_id),
            details={"error": str(e)},
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=False,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(e)}"
        )


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: int,
        request: Request,
        current_user: UserInToken = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """
    Delete a user (Admin only)
    """
    audit_service = AuditService(db)
    user_service = UserService(db)

    # Prevent self-deletion
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    try:
        # Get user info before deletion for audit log
        user_to_delete = user_service.get_user_by_id(user_id)
        if not user_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_service.delete_user(user_id)

        # Log successful user deletion
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="DELETE_USER",
            resource="users",
            resource_id=str(user_id),
            details={
                "deleted_username": user_to_delete.Username,
                "deleted_email": user_to_delete.Email,
                "deleted_role": user_to_delete.Role
            },
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        return {"message": f"User {user_to_delete.Username} deleted successfully"}

    except Exception as e:
        # Log failed user deletion
        audit_service.log_action(
            user_id=current_user.user_id,
            username=current_user.username,
            action="DELETE_USER",
            resource="users",
            resource_id=str(user_id),
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=False,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
