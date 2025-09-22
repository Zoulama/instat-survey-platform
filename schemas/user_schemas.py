"""
User-related Pydantic schemas for API request/response models
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr  # Email serves as username
    first_name: str
    last_name: str
    role: str
    status: str = "active"
    department: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    department: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    user_id: int
    username: str  # Email that serves as username
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    status: str = "active"
    department: Optional[str] = None
    CreatedAt: Optional[datetime] = None
    UpdatedAt: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Schema for user profile information"""
    user_id: int
    username: str  # Email that serves as username
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    status: str = "active"
    department: Optional[str] = None
    scopes: List[str]
    CreatedAt: Optional[datetime] = None
    UpdatedAt: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for password change request"""
    current_password: str
    new_password: str


class UserLogin(BaseModel):
    """Schema for user login request"""
    username: str  # Email address used as username
    password: str


class UserStats(BaseModel):
    """Schema for user statistics"""
    total_users: int
    users_by_role: dict
    active_users: int
    recent_logins: int


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    generate_temp_password: bool = True
    temp_password_length: Optional[int] = 12
    send_email_notification: bool = False


class PasswordResetResponse(BaseModel):
    """Schema for password reset response"""
    user_id: int
    username: str
    first_name: str
    last_name: str
    temp_password: str
    reset_timestamp: str
    message: str
