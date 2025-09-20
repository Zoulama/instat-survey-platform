"""
User-related Pydantic schemas for API request/response models
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str
    email: EmailStr
    role: str
    status: str = "active"
    department: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    status: Optional[str] = None
    department: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response (without password)"""
    user_id: int
    
    class Config:
        from_attributes = True


class UserProfile(UserBase):
    """Schema for user profile information"""
    user_id: int
    scopes: List[str]
    
    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for password change request"""
    current_password: str
    new_password: str


class UserLogin(BaseModel):
    """Schema for user login request"""
    username: str
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
    temp_password: str
    reset_timestamp: str
    message: str
