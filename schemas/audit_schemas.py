"""
Schemas for audit logging
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    """Schema for creating audit logs"""
    user_id: int = Field(..., description="ID of the user who performed the action")
    username: str = Field(..., description="Username for easy reference")
    action: str = Field(..., description="Type of action performed")
    resource: str = Field(..., description="Resource affected")
    resource_id: Optional[str] = Field(None, description="ID of the affected resource")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details in JSON format")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    success: bool = Field(True, description="Whether the action was successful")
    error_message: Optional[str] = Field(None, description="Error message if action failed")


class AuditLogResponse(BaseModel):
    """Schema for audit log responses"""
    LogID: int = Field(..., alias="LogID")
    UserID: int = Field(..., alias="UserID")
    Username: str = Field(..., alias="Username")
    Action: str = Field(..., alias="Action")
    Resource: str = Field(..., alias="Resource")
    ResourceID: Optional[str] = Field(None, alias="ResourceID")
    Details: Optional[Dict[str, Any]] = Field(None, alias="Details")
    IPAddress: Optional[str] = Field(None, alias="IPAddress")
    UserAgent: Optional[str] = Field(None, alias="UserAgent")
    Timestamp: datetime = Field(..., alias="Timestamp")
    Success: bool = Field(..., alias="Success")
    ErrorMessage: Optional[str] = Field(None, alias="ErrorMessage")

    class Config:
        allow_population_by_field_name = True
        from_attributes = True


class AuditLogFilter(BaseModel):
    """Schema for audit log filtering"""
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource: Optional[str] = None
    success: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 100


class AuditStatistics(BaseModel):
    """Schema for audit log statistics"""
    total_actions: int
    successful_actions: int
    failed_actions: int
    success_rate: float
    action_types: Dict[str, int]
    resource_types: Dict[str, int]


class UserProfile(BaseModel):
    """Schema for user profile information"""
    username: str
    email: str
    role: str
    user_id: int
    scopes: list[str]


class PasswordChange(BaseModel):
    """Schema for password change request"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    def validate_passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
