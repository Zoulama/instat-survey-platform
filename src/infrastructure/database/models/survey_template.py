"""
Survey template models for INSTAT
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from ..base import Base


class SurveyTemplate(Base):
    """Survey template model for INSTAT standardization"""
    __tablename__ = "SurveyTemplates"
    __table_args__ = {'schema': 'public'}
    
    TemplateID = Column(Integer, primary_key=True, index=True)
    TemplateName = Column(String(255), nullable=False)
    Domain = Column(String(50), nullable=False)
    Category = Column(String(50), nullable=False)
    Version = Column(String(20), default="1.0.0")
    
    # Metadata
    CreatedBy = Column(String(100))
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    LastModified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ApprovedBy = Column(String(100))
    ApprovalDate = Column(DateTime)
    
    # Template structure (JSON)
    Sections = Column(JSON)
    DefaultQuestions = Column(JSON)
    
    # Usage tracking
    UsageCount = Column(Integer, default=0)
    LastUsed = Column(DateTime)
    
    # Documentation
    UsageGuidelines = Column(Text)
    ExampleImplementations = Column(JSON)
    
    def to_dict(self):
        return {
            'TemplateID': self.TemplateID,
            'TemplateName': self.TemplateName,
            'Domain': self.Domain,
            'Category': self.Category,
            'Version': self.Version,
            'CreatedBy': self.CreatedBy,
            'CreatedDate': self.CreatedDate,
            'LastModified': self.LastModified,
            'ApprovedBy': self.ApprovedBy,
            'ApprovalDate': self.ApprovalDate,
            'Sections': self.Sections,
            'DefaultQuestions': self.DefaultQuestions,
            'UsageCount': self.UsageCount,
            'LastUsed': self.LastUsed,
            'UsageGuidelines': self.UsageGuidelines,
            'ExampleImplementations': self.ExampleImplementations
        }
