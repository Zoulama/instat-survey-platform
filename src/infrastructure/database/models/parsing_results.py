"""
Enhanced parsing results storage model for rolling retention
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.sql import func
from ..base import Base


class ParsingResult(Base):
    """
    Store parsing results with rolling retention (last 100 uploads)
    """
    __tablename__ = "parsing_results"

    ResultID = Column(Integer, primary_key=True, index=True)
    FileName = Column(String(255), nullable=False)  # Original filename
    FileSize = Column(Integer, nullable=True)  # File size in bytes
    FileHash = Column(String(64), nullable=True)  # SHA-256 hash of file content
    UserID = Column(Integer, nullable=False, index=True)  # User who uploaded the file
    Username = Column(String(100), nullable=False)  # Username for easy reference
    
    # Parsing details
    ParsedStructure = Column(JSON, nullable=False)  # Full parsed structure in JSON
    ParsingMethod = Column(String(50), nullable=False)  # 'structured' or 'basic'
    SurveyCreated = Column(Boolean, default=False)  # Whether survey was created
    TemplateCreated = Column(Boolean, default=False)  # Whether template was created
    SurveyID = Column(Integer, nullable=True)  # ID of created survey (if any)
    TemplateID = Column(Integer, nullable=True)  # ID of created template (if any)
    
    # Metadata
    Domain = Column(String(50), nullable=True)  # Survey domain
    Category = Column(String(50), nullable=True)  # Survey category
    SectionsCount = Column(Integer, default=0)  # Number of sections parsed
    SubsectionsCount = Column(Integer, default=0)  # Number of subsections parsed
    QuestionsCount = Column(Integer, default=0)  # Number of questions parsed
    
    # Status and timing
    Status = Column(String(20), default='completed')  # 'completed', 'failed', 'partial'
    ProcessingTimeMs = Column(Float, nullable=True)  # Processing time in milliseconds
    ErrorMessage = Column(Text, nullable=True)  # Error message if parsing failed
    ValidationIssues = Column(JSON, nullable=True)  # Validation issues found
    
    # Timestamps
    UploadedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ProcessedAt = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<ParsingResult(ResultID={self.ResultID}, FileName={self.FileName}, Status={self.Status})>"


class ParsingStatistics(Base):
    """
    Store parsing statistics and metrics
    """
    __tablename__ = "parsing_statistics"
    
    StatID = Column(Integer, primary_key=True, index=True)
    Date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    TotalUploads = Column(Integer, default=0)
    SuccessfulParses = Column(Integer, default=0)
    FailedParses = Column(Integer, default=0)
    StructuredParses = Column(Integer, default=0)
    BasicParses = Column(Integer, default=0)
    SurveysCreated = Column(Integer, default=0)
    TemplatesCreated = Column(Integer, default=0)
    AverageProcessingTime = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<ParsingStatistics(Date={self.Date}, TotalUploads={self.TotalUploads})>"
