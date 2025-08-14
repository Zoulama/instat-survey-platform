"""
SQLAlchemy models for INSTAT Survey Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from .base import Base


class Survey(Base):
    """Survey model for all schemas"""
    __tablename__ = "Survey"
    
    SurveyID = Column(Integer, primary_key=True, index=True)
    Title = Column(String(255), nullable=False)
    Description = Column(Text)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    UpdatedDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    Status = Column(String(50), default="draft")
    CreatedBy = Column(String(100))
    ReviewedBy = Column(String(100))
    ApprovedBy = Column(String(100))
    PublishedBy = Column(String(100))
    ReviewDate = Column(DateTime)
    ApprovalDate = Column(DateTime)
    PublicationDate = Column(DateTime)
    Language = Column(String(10), default="fr")
    Version = Column(Integer, default=1)
    IsTemplate = Column(Boolean, default=False)
    
    # Relationships
    sections = relationship("Section", back_populates="survey", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="survey", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SurveyID': self.SurveyID,
            'Title': self.Title,
            'Description': self.Description,
            'CreatedDate': self.CreatedDate,
            'UpdatedDate': self.UpdatedDate,
            'Status': self.Status,
            'CreatedBy': self.CreatedBy,
            'ReviewedBy': self.ReviewedBy,
            'ApprovedBy': self.ApprovedBy,
            'PublishedBy': self.PublishedBy,
            'ReviewDate': self.ReviewDate,
            'ApprovalDate': self.ApprovalDate,
            'PublicationDate': self.PublicationDate,
            'Language': self.Language,
            'Version': self.Version,
            'IsTemplate': self.IsTemplate
        }


class Section(Base):
    """Section model for all schemas"""
    __tablename__ = "Section"
    
    SectionID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, ForeignKey("Survey.SurveyID", ondelete="CASCADE"))
    Title = Column(String(255), nullable=False)
    
    # Relationships
    survey = relationship("Survey", back_populates="sections")
    subsections = relationship("Subsection", back_populates="section", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="section", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SectionID': self.SectionID,
            'SurveyID': self.SurveyID,
            'Title': self.Title
        }


class Subsection(Base):
    """Subsection model for all schemas"""
    __tablename__ = "Subsection"
    
    SubsectionID = Column(Integer, primary_key=True, index=True)
    SectionID = Column(Integer, ForeignKey("Section.SectionID", ondelete="CASCADE"))
    Title = Column(String(255), nullable=False)
    
    # Relationships
    section = relationship("Section", back_populates="subsections")
    questions = relationship("Question", back_populates="subsection", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SubsectionID': self.SubsectionID,
            'SectionID': self.SectionID,
            'Title': self.Title
        }


class Question(Base):
    """Question model for all schemas"""
    __tablename__ = "Question"
    
    QuestionID = Column(Integer, primary_key=True, index=True)
    SectionID = Column(Integer, ForeignKey("Section.SectionID", ondelete="CASCADE"))
    SubsectionID = Column(Integer, ForeignKey("Subsection.SubsectionID", ondelete="CASCADE"), nullable=True)
    QuestionText = Column(Text, nullable=False)
    QuestionType = Column(String(50))
    
    # Relationships
    section = relationship("Section", back_populates="questions")
    subsection = relationship("Subsection", back_populates="questions")
    answer_options = relationship("AnswerOption", back_populates="question", cascade="all, delete-orphan")
    response_details = relationship("ResponseDetail", back_populates="question", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'QuestionID': self.QuestionID,
            'SectionID': self.SectionID,
            'SubsectionID': self.SubsectionID,
            'QuestionText': self.QuestionText,
            'QuestionType': self.QuestionType
        }


class AnswerOption(Base):
    """Answer option model for all schemas"""
    __tablename__ = "AnswerOption"
    
    OptionID = Column(Integer, primary_key=True, index=True)
    QuestionID = Column(Integer, ForeignKey("Question.QuestionID", ondelete="CASCADE"))
    OptionText = Column(Text, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="answer_options")
    response_details = relationship("ResponseDetail", back_populates="selected_option")
    
    def to_dict(self):
        return {
            'OptionID': self.OptionID,
            'QuestionID': self.QuestionID,
            'OptionText': self.OptionText
        }


class Response(Base):
    """Response model for all schemas"""
    __tablename__ = "Response"
    
    ResponseID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, ForeignKey("Survey.SurveyID", ondelete="CASCADE"))
    RespondentID = Column(Integer)
    SubmittedDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    survey = relationship("Survey", back_populates="responses")
    response_details = relationship("ResponseDetail", back_populates="response", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'ResponseID': self.ResponseID,
            'SurveyID': self.SurveyID,
            'RespondentID': self.RespondentID,
            'SubmittedDate': self.SubmittedDate
        }


class ResponseDetail(Base):
    """Response detail model for all schemas"""
    __tablename__ = "ResponseDetail"
    
    ResponseDetailID = Column(Integer, primary_key=True, index=True)
    ResponseID = Column(Integer, ForeignKey("Response.ResponseID", ondelete="CASCADE"))
    QuestionID = Column(Integer, ForeignKey("Question.QuestionID", ondelete="CASCADE"))
    SelectedOptionID = Column(Integer, ForeignKey("AnswerOption.OptionID", ondelete="SET NULL"), nullable=True)
    AnswerText = Column(Text)
    
    # Relationships
    response = relationship("Response", back_populates="response_details")
    question = relationship("Question", back_populates="response_details")
    selected_option = relationship("AnswerOption", back_populates="response_details")
    
    def to_dict(self):
        return {
            'ResponseDetailID': self.ResponseDetailID,
            'ResponseID': self.ResponseID,
            'QuestionID': self.QuestionID,
            'SelectedOptionID': self.SelectedOptionID,
            'AnswerText': self.AnswerText
        }


# Workflow management model
class WorkflowAction(Base):
    """Workflow action model for tracking survey state changes"""
    __tablename__ = "WorkflowActions"
    __table_args__ = {'schema': 'public'}
    
    ActionID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, nullable=False)
    SchemaName = Column(String(50), nullable=False)
    UserID = Column(String(100))
    ActionType = Column(String(50), nullable=False)
    FromStatus = Column(String(50))
    ToStatus = Column(String(50))
    Comment = Column(Text)
    Timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'ActionID': self.ActionID,
            'SurveyID': self.SurveyID,
            'SchemaName': self.SchemaName,
            'UserID': self.UserID,
            'ActionType': self.ActionType,
            'FromStatus': self.FromStatus,
            'ToStatus': self.ToStatus,
            'Comment': self.Comment,
            'Timestamp': self.Timestamp
        }


# User management models
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


# INSTAT-specific models
class INSTATSurvey(Base):
    """Enhanced survey model with INSTAT-specific fields"""
    __tablename__ = "INSTATSurveys"
    __table_args__ = {'schema': 'public'}
    
    SurveyID = Column(Integer, primary_key=True, index=True)
    Title = Column(String(255), nullable=False)
    Description = Column(Text)
    Domain = Column(String(50), nullable=False)  # SSN, SDS, DES, etc.
    Category = Column(String(50), nullable=False)  # diagnostic, program_review, etc.
    
    # Temporal fields
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    UpdatedDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    Status = Column(String(50), default="draft")
    FiscalYear = Column(Integer)
    ReportingCycle = Column(String(50))
    
    # Personnel fields
    CreatedBy = Column(String(100))
    ReviewedBy = Column(String(100))
    ApprovedBy = Column(String(100))
    PublishedBy = Column(String(100))
    ImplementingUnit = Column(String(100))
    
    # Timestamps for workflow
    ReviewDate = Column(DateTime)
    ApprovalDate = Column(DateTime)
    PublicationDate = Column(DateTime)
    
    # Configuration
    Language = Column(String(10), default="fr")
    Version = Column(String(20), default="1.0.0")
    IsTemplate = Column(Boolean, default=False)
    
    # INSTAT-specific fields (JSON for flexibility)
    TargetAudience = Column(JSON)  # List of target groups
    GeographicScope = Column(JSON)  # List of regions/provinces
    ComplianceFramework = Column(JSON)  # SDS4, etc.
    InternationalStandards = Column(JSON)
    RequiredSkills = Column(JSON)
    BudgetCategory = Column(String(100))
    EstimatedDuration = Column(Integer)  # in days
    
    # Domain-specific fields (flexible JSON)
    DomainSpecificFields = Column(JSON)  # For SSN, SDS, DES specific data
    
    def to_dict(self):
        return {
            'SurveyID': self.SurveyID,
            'Title': self.Title,
            'Description': self.Description,
            'Domain': self.Domain,
            'Category': self.Category,
            'CreatedDate': self.CreatedDate,
            'UpdatedDate': self.UpdatedDate,
            'Status': self.Status,
            'FiscalYear': self.FiscalYear,
            'ReportingCycle': self.ReportingCycle,
            'CreatedBy': self.CreatedBy,
            'ReviewedBy': self.ReviewedBy,
            'ApprovedBy': self.ApprovedBy,
            'PublishedBy': self.PublishedBy,
            'ImplementingUnit': self.ImplementingUnit,
            'ReviewDate': self.ReviewDate,
            'ApprovalDate': self.ApprovalDate,
            'PublicationDate': self.PublicationDate,
            'Language': self.Language,
            'Version': self.Version,
            'IsTemplate': self.IsTemplate,
            'TargetAudience': self.TargetAudience,
            'GeographicScope': self.GeographicScope,
            'ComplianceFramework': self.ComplianceFramework,
            'InternationalStandards': self.InternationalStandards,
            'RequiredSkills': self.RequiredSkills,
            'BudgetCategory': self.BudgetCategory,
            'EstimatedDuration': self.EstimatedDuration,
            'DomainSpecificFields': self.DomainSpecificFields
        }


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


class INSTATQuestion(Base):
    """Enhanced question model with INSTAT-specific features"""
    __tablename__ = "INSTATQuestions"
    __table_args__ = {'schema': 'public'}
    
    QuestionID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, nullable=False)
    SectionID = Column(Integer, nullable=True)
    SubsectionID = Column(Integer, nullable=True)
    
    # Basic question fields
    QuestionText = Column(Text, nullable=False)
    QuestionType = Column(String(50), nullable=False)
    IsRequired = Column(Boolean, default=False)
    
    # INSTAT-specific fields
    IndicatorCode = Column(String(100))  # Links to national indicators
    DataSource = Column(String(255))
    CollectionMethod = Column(String(100))
    QualityRequirements = Column(JSON)
    
    # Validation and logic
    ValidationRules = Column(JSON)
    DependsOnQuestion = Column(Integer)  # Question ID for conditional logic
    
    # Multilingual support
    QuestionTextEN = Column(Text)
    QuestionTextFR = Column(Text)
    
    # Metadata
    Tags = Column(JSON)
    Priority = Column(String(20), default="medium")
    
    def to_dict(self):
        return {
            'QuestionID': self.QuestionID,
            'SurveyID': self.SurveyID,
            'SectionID': self.SectionID,
            'SubsectionID': self.SubsectionID,
            'QuestionText': self.QuestionText,
            'QuestionType': self.QuestionType,
            'IsRequired': self.IsRequired,
            'IndicatorCode': self.IndicatorCode,
            'DataSource': self.DataSource,
            'CollectionMethod': self.CollectionMethod,
            'QualityRequirements': self.QualityRequirements,
            'ValidationRules': self.ValidationRules,
            'DependsOnQuestion': self.DependsOnQuestion,
            'QuestionTextEN': self.QuestionTextEN,
            'QuestionTextFR': self.QuestionTextFR,
            'Tags': self.Tags,
            'Priority': self.Priority
        }


class SurveyMetrics(Base):
    """Survey metrics for INSTAT reporting and analytics"""
    __tablename__ = "SurveyMetrics"
    __table_args__ = {'schema': 'public'}
    
    MetricID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, nullable=False)
    
    # Response metrics
    TotalResponses = Column(Integer, default=0)
    CompletionRate = Column(Float, default=0.0)
    AverageCompletionTime = Column(Float)  # in minutes
    
    # Quality metrics
    DataQualityScore = Column(Float)
    ValidationErrorRate = Column(Float)
    IncompleteResponses = Column(Integer, default=0)
    
    # Geographic and temporal data (JSON)
    ResponseByRegion = Column(JSON)
    ResponseTrend = Column(JSON)
    
    # Resource metrics
    DataCollectionCost = Column(Float)
    TimeToComplete = Column(Integer)  # in days
    CoverageRate = Column(Float)
    
    # Timestamps
    LastUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'MetricID': self.MetricID,
            'SurveyID': self.SurveyID,
            'TotalResponses': self.TotalResponses,
            'CompletionRate': self.CompletionRate,
            'AverageCompletionTime': self.AverageCompletionTime,
            'DataQualityScore': self.DataQualityScore,
            'ValidationErrorRate': self.ValidationErrorRate,
            'IncompleteResponses': self.IncompleteResponses,
            'ResponseByRegion': self.ResponseByRegion,
            'ResponseTrend': self.ResponseTrend,
            'DataCollectionCost': self.DataCollectionCost,
            'TimeToComplete': self.TimeToComplete,
            'CoverageRate': self.CoverageRate,
            'LastUpdated': self.LastUpdated
        }


class DataExport(Base):
    """Data export configuration and tracking"""
    __tablename__ = "DataExports"
    __table_args__ = {'schema': 'public'}
    
    ExportID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, nullable=False)
    ExportFormat = Column(String(20), nullable=False)  # excel, csv, json, xml, pdf
    ExportType = Column(String(50), nullable=False)  # raw_data, analysis, report, dashboard
    
    # Configuration (JSON)
    ExportConfig = Column(JSON)  # includes filters, metadata options, etc.
    
    # Scheduling
    IsScheduled = Column(Boolean, default=False)
    ScheduleFrequency = Column(String(50))
    NextExport = Column(DateTime)
    
    # Delivery
    DeliveryMethod = Column(String(50), default="download")
    Recipients = Column(JSON)
    
    # Tracking
    CreatedBy = Column(String(100))
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    LastExported = Column(DateTime)
    ExportCount = Column(Integer, default=0)
    
    def to_dict(self):
        return {
            'ExportID': self.ExportID,
            'SurveyID': self.SurveyID,
            'ExportFormat': self.ExportFormat,
            'ExportType': self.ExportType,
            'ExportConfig': self.ExportConfig,
            'IsScheduled': self.IsScheduled,
            'ScheduleFrequency': self.ScheduleFrequency,
            'NextExport': self.NextExport,
            'DeliveryMethod': self.DeliveryMethod,
            'Recipients': self.Recipients,
            'CreatedBy': self.CreatedBy,
            'CreatedDate': self.CreatedDate,
            'LastExported': self.LastExported,
            'ExportCount': self.ExportCount
        }
