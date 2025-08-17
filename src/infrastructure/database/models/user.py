"""
User models for authentication and authorization
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from ..base import Base


class User(Base):
    """User model"""
    __tablename__ = "Users"
    __table_args__ = {'schema': 'public'}
    
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(255), unique=True, nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    Role = Column(String(50), nullable=False)
    
    def to_dict(self):
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'Email': self.Email,
            'Role': self.Role
        }


class Role(Base):
    """Role model"""
    __tablename__ = "Roles"
    __table_args__ = {'schema': 'public'}
    
    RoleID = Column(Integer, primary_key=True, index=True)
    RoleName = Column(String(50), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            'RoleID': self.RoleID,
            'RoleName': self.RoleName
        }
