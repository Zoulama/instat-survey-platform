"""
User service for user management operations
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import secrets
import string

from src.infrastructure.database import models
from src.infrastructure.auth.oauth2 import get_password_hash, verify_password
from schemas.user_schemas import UserCreate, UserUpdate, UserResponse, PasswordResetRequest, PasswordResetResponse


class UserService:
    """Service class for user management operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if user already exists
        existing_user = self.db.query(models.User).filter(
            (models.User.Username == user_data.username) |
            (models.User.Email == user_data.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user
        db_user = models.User(
            Username=user_data.username,
            Email=user_data.email,
            HashedPassword=hashed_password,
            Role=user_data.role,
            Status=user_data.status,
            Department=user_data.department
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return UserResponse(
                user_id=db_user.UserID,
                username=db_user.Username,
                email=db_user.Email,
                role=db_user.Role,
                status=db_user.Status,
                department=db_user.Department,
                CreatedAt=db_user.CreatedAt,
                UpdatedAt=db_user.UpdatedAt
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            )
    
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID"""
        user = self.db.query(models.User).filter(models.User.UserID == user_id).first()
        if not user:
            return None
            
        return UserResponse(
            user_id=user.UserID,
            username=user.Username,
            email=user.Email,
            role=user.Role,
            status=user.Status,
            department=user.Department,
            CreatedAt=user.CreatedAt,
            UpdatedAt=user.UpdatedAt
        )
    
    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """Get user by username"""
        user = self.db.query(models.User).filter(models.User.Username == username).first()
        if not user:
            return None
            
        return UserResponse(
            user_id=user.UserID,
            username=user.Username,
            email=user.Email,
            role=user.Role,
            status=user.Status,
            department=user.Department,
            CreatedAt=user.CreatedAt,
            UpdatedAt=user.UpdatedAt
        )
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """List all users with pagination"""
        users = self.db.query(models.User).offset(skip).limit(limit).all()
        return [
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
    
    def get_users(self, skip: int = 0, limit: int = 100, role: Optional[str] = None) -> List[models.User]:
        """Get users with optional role filtering (returns raw models for admin routes)"""
        query = self.db.query(models.User)
        
        if role:
            query = query.filter(models.User.Role == role)
            
        return query.offset(skip).limit(limit).all()
    
    def get_user_count(self, role: Optional[str] = None) -> int:
        """Get total count of users with optional role filtering"""
        query = self.db.query(models.User)
        
        if role:
            query = query.filter(models.User.Role == role)
            
        return query.count()
    
    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        """Get user by ID (returns raw model for admin routes)"""
        return self.db.query(models.User).filter(models.User.UserID == user_id).first()
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:
        """Update user information"""
        user = self.db.query(models.User).filter(models.User.UserID == user_id).first()
        if not user:
            return None
        
        # Update fields if provided
        if user_update.email:
            # Check if email is already taken by another user
            existing_user = self.db.query(models.User).filter(
                models.User.Email == user_update.email,
                models.User.UserID != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already taken by another user"
                )
            user.Email = user_update.email
        
        if user_update.role:
            user.Role = user_update.role
        
        if user_update.status:
            user.Status = user_update.status
        
        if user_update.department is not None:
            user.Department = user_update.department
        
        try:
            self.db.commit()
            self.db.refresh(user)
            
            return UserResponse(
                user_id=user.UserID,
                username=user.Username,
                email=user.Email,
                role=user.Role,
                status=user.Status,
                department=user.Department,
                CreatedAt=user.CreatedAt,
                UpdatedAt=user.UpdatedAt
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user: {str(e)}"
            )
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        user = self.db.query(models.User).filter(models.User.UserID == user_id).first()
        if not user:
            return False
        
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete user: {str(e)}"
            )
    
    async def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        """Change user password"""
        user = self.db.query(models.User).filter(models.User.UserID == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Verify current password
        if not verify_password(current_password, user.HashedPassword):
            raise ValueError("Current password is incorrect")
        
        # Hash new password
        hashed_new_password = get_password_hash(new_password)
        
        try:
            user.HashedPassword = hashed_new_password
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to change password: {str(e)}")
    
    def reset_user_password(self, user_id: int, reset_request: PasswordResetRequest) -> PasswordResetResponse:
        """Reset user password to a temporary password"""
        user = self.db.query(models.User).filter(models.User.UserID == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate temporary password
        temp_password = self._generate_temp_password(reset_request.temp_password_length or 12)
        
        # Hash the temporary password
        hashed_temp_password = get_password_hash(temp_password)
        
        try:
            # Update user's password
            user.HashedPassword = hashed_temp_password
            self.db.commit()
            self.db.refresh(user)
            
            # Create response
            reset_timestamp = datetime.utcnow().isoformat()
            
            return PasswordResetResponse(
                user_id=user.UserID,
                username=user.Username,
                temp_password=temp_password,
                reset_timestamp=reset_timestamp,
                message=f"Password successfully reset for user {user.Username}. Please provide the temporary password to the user."
            )
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reset password: {str(e)}"
            )
    
    def _generate_temp_password(self, length: int = 12) -> str:
        """Generate a secure temporary password"""
        # Include letters, digits, and some special characters
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        
        # Ensure at least one character from each category
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%&*")
        ]
        
        # Fill the rest randomly
        for _ in range(length - 4):
            password.append(secrets.choice(chars))
        
        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        total_users = self.db.query(models.User).count()
        
        # Get users by role
        from sqlalchemy import func
        role_counts = self.db.query(
            models.User.Role,
            func.count(models.User.UserID)
        ).group_by(models.User.Role).all()
        
        users_by_role = {role: count for role, count in role_counts}
        
        return {
            "total_users": total_users,
            "users_by_role": users_by_role,
            "active_users": total_users,  # For now, assume all users are active
            "recent_logins": 0  # Would need login tracking to implement this
        }
