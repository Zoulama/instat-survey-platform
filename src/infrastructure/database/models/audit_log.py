"""
Audit logging model for tracking administrative actions
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from ..base import Base


class AuditLog(Base):
    """
    Audit log table to track all administrative actions
    """
    __tablename__ = "audit_logs"

    LogID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, nullable=False, index=True)  # User who performed the action
    Username = Column(String(100), nullable=False)  # Username for easy reference
    Action = Column(String(100), nullable=False, index=True)  # Type of action performed
    Resource = Column(String(100), nullable=False)  # Resource affected (table/entity)
    ResourceID = Column(String(50), nullable=True)  # ID of the affected resource
    Details = Column(JSON, nullable=True)  # Additional details in JSON format
    IPAddress = Column(String(45), nullable=True)  # Client IP address
    UserAgent = Column(Text, nullable=True)  # Client user agent
    Timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    Success = Column(Boolean, default=True, nullable=False)  # Whether the action was successful
    ErrorMessage = Column(Text, nullable=True)  # Error message if action failed
    
    def __repr__(self):
        return f"<AuditLog(LogID={self.LogID}, User={self.Username}, Action={self.Action}, Resource={self.Resource})>"
