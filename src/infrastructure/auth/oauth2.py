"""
OAuth2 Authentication and Authorization for INSTAT Survey Platform
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, ValidationError

from src.infrastructure.database.connection import get_db
from src.infrastructure.database import models

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "muqObXpk89vWh_6YpNGYMv20iH8Lu7CLW5nh7FCi-o")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Security instances
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/token",
    scopes={
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
)


# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []


class UserInToken(BaseModel):
    username: str
    email: str
    role: str
    user_id: int
    scopes: list[str]


# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get password hash."""
    return pwd_context.hash(password)


# Token utilities
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None

        scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=scopes)
        return token_data
    except JWTError:
        return None


# models.User authentication
def authenticate_user(db: Session, username: str, password: str) -> Optional[Any]:
    """Authenticate user with username and password."""
    user = db.query(models.User).filter(models.User.Username == username).first()
    if not user:
        return None
    if not verify_password(password, user.HashedPassword):
        return None
    return user


def get_user_scopes(role: str) -> list[str]:
    """Get scopes based on user role."""
    role_scopes = {
        "admin": [
            "upload:write", "templates:write", "context:write",
            "context:read", "users:admin", "surveys:read",
            "surveys:write", "surveys:delete", "admin"
        ],
        "manager": [
            "upload:write", "templates:write", "context:write",
            "context:read", "surveys:read", "surveys:write"
        ],
        "data_scientist": [
            "context:read", "surveys:read", "upload:write"
        ],
        "readonly": [
            "context:read", "surveys:read"
        ],
        "write": [
            "upload:write", "templates:write", "surveys:write",
            "context:read", "surveys:read"
        ]
    }
    return role_scopes.get(role.lower(), ["context:read"])


# Dependencies
async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserInToken:
    """Get current authenticated user."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.Username == token_data.username).first()
    if user is None:
        raise credentials_exception

    user_scopes = get_user_scopes(user.Role)

    # Check if user has required scopes
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return UserInToken(
        username=user.Username,
        email=user.Email,
        role=user.Role,
        user_id=user.UserID,
        scopes=user_scopes
    )


async def get_current_active_user(
        current_user: UserInToken = Depends(get_current_user)
) -> UserInToken:
    """Get current active user (can add additional checks here)."""
    return current_user


def require_scopes(*scopes: str):
    """Decorator to require specific scopes."""
    
    # Create a dependency that requires the specified scopes
    async def get_scoped_user(
        security_scopes: SecurityScopes = SecurityScopes(scopes),
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> UserInToken:
        return await get_current_user(security_scopes, token, db)
    
    return Depends(get_scoped_user)


# Convenience functions for common permission checks
async def require_admin(current_user: UserInToken = Depends(get_current_user)) -> UserInToken:
    """Require admin role."""
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_read_access(current_user: UserInToken = Depends(get_current_user)) -> UserInToken:
    """Require read access."""
    if "context:read" not in current_user.scopes and "surveys:read" not in current_user.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Read access required"
        )
    return current_user


async def require_write_access(current_user: UserInToken = Depends(get_current_user)) -> UserInToken:
    """Require write access."""
    required_scopes = ["surveys:write", "upload:write", "templates:write"]
    if not any(scope in current_user.scopes for scope in required_scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Write access required"
        )
    return current_user
