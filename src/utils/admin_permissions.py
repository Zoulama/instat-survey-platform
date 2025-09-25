"""
Admin permission utilities for INSTAT Survey Platform
"""
from typing import List
from fastapi import HTTPException, status
from ..infrastructure.auth.oauth2 import UserInToken


class AdminPermissions:
    """Admin permission checker utility"""
    
    # Define admin roles and permissions
    ADMIN_ROLES = {"admin", "super_admin", "system_admin"}
    ADMIN_SCOPES = {"admin:read", "admin:write", "admin:delete"}
    
    # File upload specific permissions - include existing upload:write scope
    UPLOAD_ADMIN_SCOPES = {"admin:write", "upload:admin", "upload:write"}
    
    @classmethod
    def is_admin_user(cls, user: UserInToken) -> bool:
        """Check if user has admin role"""
        if not user:
            return False
        
        # Check if user has admin role - check both 'role' (singular) and 'roles' (plural)
        user_role = getattr(user, 'role', None)
        user_roles = getattr(user, 'roles', []) or []
        
        # Combine single role and roles list
        all_roles = []
        if user_role:
            all_roles.append(user_role)
        if isinstance(user_roles, str):
            all_roles.append(user_roles)
        elif isinstance(user_roles, list):
            all_roles.extend(user_roles)
        
        return any(role.lower() in cls.ADMIN_ROLES for role in all_roles)
    
    @classmethod
    def has_admin_scope(cls, user: UserInToken, required_scope: str = None) -> bool:
        """Check if user has admin scopes"""
        if not user:
            return False
        
        # Get user scopes
        user_scopes = getattr(user, 'scopes', []) or []
        if isinstance(user_scopes, str):
            user_scopes = [user_scopes]
        
        # Check specific scope if provided
        if required_scope:
            return required_scope in user_scopes
        
        # Check any admin scope
        return any(scope in cls.ADMIN_SCOPES for scope in user_scopes)
    
    @classmethod
    def can_upload_files(cls, user: UserInToken) -> bool:
        """Check if user can upload files (admin only)"""
        if not user:
            return False
        
        return (cls.is_admin_user(user) or 
                any(scope in cls.UPLOAD_ADMIN_SCOPES for scope in getattr(user, 'scopes', [])))
    
    @classmethod
    def can_view_all_uploads(cls, user: UserInToken) -> bool:
        """Check if user can view all uploads (admin only)"""
        if not user:
            return False
        
        return cls.is_admin_user(user) or cls.has_admin_scope(user, 'admin:read')
    
    @classmethod
    def can_manage_uploads(cls, user: UserInToken) -> bool:
        """Check if user can manage uploads (delete, cleanup, etc.)"""
        if not user:
            return False
        
        return cls.is_admin_user(user) or cls.has_admin_scope(user, 'admin:write')
    
    @classmethod
    def require_admin_access(cls, user: UserInToken, action: str = "perform this action") -> None:
        """Raise exception if user doesn't have admin access"""
        if not cls.is_admin_user(user) and not cls.has_admin_scope(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Admin access required to {action}. Contact your administrator for access."
            )
    
    @classmethod
    def require_upload_admin_access(cls, user: UserInToken) -> None:
        """Raise exception if user doesn't have upload admin access"""
        if not cls.can_upload_files(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required for file upload operations. Contact your administrator for access."
            )
    
    @classmethod
    def get_user_permission_level(cls, user: UserInToken) -> str:
        """Get user's permission level"""
        if not user:
            return "none"
        
        if cls.is_admin_user(user):
            return "admin"
        
        user_scopes = getattr(user, 'scopes', []) or []
        if 'admin:write' in user_scopes or 'upload:admin' in user_scopes:
            return "upload_admin"
        elif 'admin:read' in user_scopes:
            return "read_admin"
        elif 'upload:read' in user_scopes:
            return "user"
        else:
            return "basic"
    
    @classmethod
    def get_accessible_endpoints(cls, user: UserInToken) -> List[str]:
        """Get list of endpoints accessible to the user"""
        permission_level = cls.get_user_permission_level(user)
        
        endpoints = []
        
        if permission_level in ["admin", "upload_admin"]:
            endpoints.extend([
                "POST /v1/api/files/upload-excel-and-create-survey",
                "POST /v1/api/files/upload-excel-and-create-survey-with-template",
                "GET /v1/api/uploads/my-uploads"
            ])
        
        if permission_level in ["admin", "read_admin"]:
            endpoints.extend([
                "GET /v1/api/uploads/recent",
                "GET /v1/api/uploads/by-user/{username}",
                "GET /v1/api/uploads/by-date-range",
                "GET /v1/api/uploads/statistics",
                "GET /v1/api/uploads/today"
            ])
        
        if permission_level == "admin":
            endpoints.extend([
                "POST /v1/api/uploads/cleanup"
            ])
        
        if permission_level in ["user", "upload_admin", "read_admin", "admin"]:
            endpoints.extend([
                "GET /v1/api/uploads/my-uploads"
            ])
        
        return sorted(list(set(endpoints)))


# Singleton instance
admin_permissions = AdminPermissions()