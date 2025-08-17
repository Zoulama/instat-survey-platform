"""
Authentication routes for OAuth2 token management
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_db
from src.infrastructure.database import models
from src.infrastructure.auth.oauth2 import (
    authenticate_user, create_access_token, get_user_scopes,
    Token, UserInToken, get_current_user, require_admin
)
from schemas.user_schemas import (
    UserCreate, UserResponse, UserUpdate,
    PasswordChange, UserProfile
)
from src.services.user_service import UserService

router = APIRouter(prefix="/v1/api/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_scopes = get_user_scopes(user.Role)
    access_token_expires = timedelta(minutes=1440)  # 24 hours

    # Include scopes in the token
    token_data = {
        "sub": user.Username,
        "scopes": user_scopes,
        "role": user.Role,
        "user_id": user.UserID
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400,  # 24 hours in seconds
        "scope": " ".join(user_scopes)
    }


@router.get("/me", response_model=UserProfile)
async def read_users_me(
        current_user: UserInToken = Depends(get_current_user)
):
    """
    Get current user profile
    """
    return UserProfile(
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        user_id=current_user.user_id,
        scopes=current_user.scopes
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
        current_user: UserInToken = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Refresh access token
    """
    # Re-fetch user to get latest role/permissions
    user = db.query(models.User).filter(models.User.UserID == current_user.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_scopes = get_user_scopes(user.Role)
    access_token_expires = timedelta(minutes=1440)

    token_data = {
        "sub": user.Username,
        "scopes": user_scopes,
        "role": user.Role,
        "user_id": user.UserID
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400,
        "scope": " ".join(user_scopes)
    }


@router.post("/change-password")
async def change_password(
        password_data: PasswordChange,
        current_user: UserInToken = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Change user password
    """
    user_service = UserService(db)

    try:
        await user_service.change_password(
            current_user.user_id,
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/scopes")
async def get_available_scopes():
    """
    Get all available OAuth2 scopes
    """
    return {
        "upload:write": "Upload and manage files",
        "templates:write": "Create and manage templates",
        "context:write": "Modify backend context",
        "context:read": "Read survey data",
        "users:admin": "Manage users",
        "surveys:read": "Read surveys",
        "surveys:write": "Create and update surveys",
        "surveys:delete": "Delete surveys",
        "admin": "Full administrative access"
    }


@router.get("/roles")
async def get_available_roles(
        current_user: UserInToken = Security(require_admin)
):
    """
    Get all available user roles (admin only)
    """
    return {
        "admin": {
            "scopes": [
                "upload:write", "templates:write", "context:write",
                "context:read", "users:admin", "surveys:read",
                "surveys:write", "surveys:delete", "admin"
            ],
            "description": "Full administrative access"
        },
        "manager": {
            "scopes": [
                "upload:write", "templates:write", "context:write",
                "context:read", "surveys:read", "surveys:write"
            ],
            "description": "Management access with write permissions"
        },
        "data_scientist": {
            "scopes": [
                "context:read", "surveys:read", "upload:write"
            ],
            "description": "Data analysis and upload permissions"
        },
        "readonly": {
            "scopes": [
                "context:read", "surveys:read"
            ],
            "description": "Read-only access"
        },
        "write": {
            "scopes": [
                "upload:write", "templates:write", "surveys:write",
                "context:read", "surveys:read"
            ],
            "description": "General write access"
        }
    }
