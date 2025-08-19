"""
Service for audit logging functionality
"""
import json
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from src.infrastructure.database.models import AuditLog
from schemas.audit_schemas import AuditLogResponse, AuditLogCreate


class AuditService:
    """
    Service for managing audit logs
    """

    def __init__(self, db: Session):
        self.db = db

    def log_action(
            self,
            user_id: int,
            username: str,
            action: str,
            resource: str,
            resource_id: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None,
            success: bool = True,
            error_message: Optional[str] = None
    ) -> AuditLog:
        """
        Log an administrative action
        """
        audit_log = AuditLog(
            UserID=user_id,
            Username=username,
            Action=action,
            Resource=resource,
            ResourceID=resource_id,
            Details=details,
            IPAddress=ip_address,
            UserAgent=user_agent,
            Success=success,
            ErrorMessage=error_message
        )

        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)

        return audit_log

    def get_audit_logs(
            self,
            skip: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
            action: Optional[str] = None,
            resource: Optional[str] = None,
            success: Optional[bool] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[AuditLog]:
        """
        Get audit logs with optional filters
        """
        query = self.db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.UserID == user_id)

        if action:
            query = query.filter(AuditLog.Action == action)

        if resource:
            query = query.filter(AuditLog.Resource == resource)

        if success is not None:
            query = query.filter(AuditLog.Success == success)

        if start_date:
            query = query.filter(AuditLog.Timestamp >= start_date)

        if end_date:
            query = query.filter(AuditLog.Timestamp <= end_date)

        return query.order_by(desc(AuditLog.Timestamp)).offset(skip).limit(limit).all()

    def get_audit_log_count(
            self,
            user_id: Optional[int] = None,
            action: Optional[str] = None,
            resource: Optional[str] = None,
            success: Optional[bool] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> int:
        """
        Get total count of audit logs with optional filters
        """
        query = self.db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.UserID == user_id)

        if action:
            query = query.filter(AuditLog.Action == action)

        if resource:
            query = query.filter(AuditLog.Resource == resource)

        if success is not None:
            query = query.filter(AuditLog.Success == success)

        if start_date:
            query = query.filter(AuditLog.Timestamp >= start_date)

        if end_date:
            query = query.filter(AuditLog.Timestamp <= end_date)

        return query.count()

    def get_recent_actions(self, limit: int = 50) -> List[AuditLog]:
        """
        Get most recent audit actions
        """
        return self.db.query(AuditLog).order_by(
            desc(AuditLog.Timestamp)
        ).limit(limit).all()

    def get_user_actions(self, user_id: int, limit: int = 100) -> List[AuditLog]:
        """
        Get actions performed by a specific user
        """
        return self.db.query(AuditLog).filter(
            AuditLog.UserID == user_id
        ).order_by(desc(AuditLog.Timestamp)).limit(limit).all()

    def get_failed_actions(self, limit: int = 100) -> List[AuditLog]:
        """
        Get failed actions
        """
        return self.db.query(AuditLog).filter(
            AuditLog.Success == False
        ).order_by(desc(AuditLog.Timestamp)).limit(limit).all()

    def get_action_statistics(self) -> Dict[str, Any]:
        """
        Get audit log statistics
        """
        total_actions = self.db.query(AuditLog).count()
        successful_actions = self.db.query(AuditLog).filter(
            AuditLog.Success == True
        ).count()
        failed_actions = self.db.query(AuditLog).filter(
            AuditLog.Success == False
        ).count()

        # Get action type counts
        action_counts = self.db.query(
            AuditLog.Action,
            self.db.func.count(AuditLog.LogID).label('count')
        ).group_by(AuditLog.Action).all()

        # Get resource counts
        resource_counts = self.db.query(
            AuditLog.Resource,
            self.db.func.count(AuditLog.LogID).label('count')
        ).group_by(AuditLog.Resource).all()

        return {
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "failed_actions": failed_actions,
            "success_rate": (successful_actions / total_actions * 100) if total_actions > 0 else 0,
            "action_types": dict(action_counts),
            "resource_types": dict(resource_counts)
        }


# Audit logging decorator
def audit_action(action: str, resource: str):
    """
    Decorator to automatically log actions
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract database session and user info from kwargs if available
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')

            if db and current_user:
                audit_service = AuditService(db)

                try:
                    result = func(*args, **kwargs)

                    # Log successful action
                    audit_service.log_action(
                        user_id=current_user.user_id,
                        username=current_user.username,
                        action=action,
                        resource=resource,
                        success=True
                    )

                    return result

                except Exception as e:
                    # Log failed action
                    audit_service.log_action(
                        user_id=current_user.user_id,
                        username=current_user.username,
                        action=action,
                        resource=resource,
                        success=False,
                        error_message=str(e)
                    )
                    raise
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
