"""
INSTAT Domain-Specific Schemas and Models
Supports SSN, SDS, DES activities and specialized survey types
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field


class INSTATDomain(str, Enum):
    """INSTAT Statistical Domains"""
    SSN = "ssn"  # Social Safety Net
    SDS = "sds"  # Statistical Development Strategy  
    DES = "des"  # Direction des Études et Statistiques
    PROGRAM_REVIEW = "program_review"
    ACTIVITY_REPORT = "activity_report"
    DIAGNOSTIC = "diagnostic"
    DEVELOPMENT = "development"


class SurveyCategory(str, Enum):
    """Survey Categories for INSTAT"""
    DIAGNOSTIC = "diagnostic"
    PROGRAM_REVIEW = "program_review"
    ACTIVITY_REPORT = "activity_report"
    DEVELOPMENT_ASSESSMENT = "development_assessment"
    STATISTICAL_PLANNING = "statistical_planning"
    MONITORING_EVALUATION = "monitoring_evaluation"


class ReportingCycle(str, Enum):
    """Reporting Cycles"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    AD_HOC = "ad_hoc"


class ActivityType(str, Enum):
    """Types of INSTAT Activities"""
    DATA_COLLECTION = "data_collection"
    DATA_ANALYSIS = "data_analysis"
    CAPACITY_BUILDING = "capacity_building"
    POLICY_SUPPORT = "policy_support"
    TECHNICAL_ASSISTANCE = "technical_assistance"
    INFRASTRUCTURE = "infrastructure"
    COORDINATION = "coordination"


# Enhanced Survey Models for INSTAT
class INSTATSurveyBase(BaseModel):
    """Base model for INSTAT surveys with domain-specific fields"""
    Title: str
    Description: Optional[str] = None
    Domain: INSTATDomain
    Category: SurveyCategory
    ReportingCycle: Optional[ReportingCycle] = None
    FiscalYear: Optional[int] = None
    TargetAudience: Optional[List[str]] = []
    GeographicScope: Optional[List[str]] = []  # Regions, provinces, etc.
    ImplementingUnit: Optional[str] = None  # Which INSTAT unit
    
    # Compliance and Standards
    ComplianceFramework: Optional[List[str]] = []  # SDS4, etc.
    InternationalStandards: Optional[List[str]] = []
    
    # Resource Requirements
    EstimatedDuration: Optional[int] = None  # in days
    RequiredSkills: Optional[List[str]] = []
    BudgetCategory: Optional[str] = None


class SSNDiagnosticSurvey(INSTATSurveyBase):
    """Social Safety Net Diagnostic Survey"""
    Domain: INSTATDomain = INSTATDomain.SSN
    Category: SurveyCategory = SurveyCategory.DIAGNOSTIC
    
    # SSN-specific fields
    BeneficiaryGroups: Optional[List[str]] = []
    ProgramTypes: Optional[List[str]] = []  # Cash transfers, food assistance, etc.
    VulnerabilityIndicators: Optional[List[str]] = []
    CoverageMetrics: Optional[Dict[str, Any]] = {}


class ProgramReviewSurvey(INSTATSurveyBase):
    """Program Review Survey for SDS"""
    Domain: INSTATDomain = INSTATDomain.SDS
    Category: SurveyCategory = SurveyCategory.PROGRAM_REVIEW
    
    # Program Review specific fields
    ProgramName: str
    ReviewPeriod: str  # e.g., "2024-2025"
    KeyPerformanceIndicators: Optional[List[str]] = []
    StakeholderGroups: Optional[List[str]] = []
    ReviewObjectives: Optional[List[str]] = []


class ActivityReportSurvey(INSTATSurveyBase):
    """Activity Report Survey"""
    Domain: INSTATDomain = INSTATDomain.DES
    Category: SurveyCategory = SurveyCategory.ACTIVITY_REPORT
    
    # Activity Report specific fields
    ActivityTypes: Optional[List[ActivityType]] = []
    ReportingPeriodStart: Optional[date] = None
    ReportingPeriodEnd: Optional[date] = None
    OutputIndicators: Optional[Dict[str, Any]] = {}
    OutcomeIndicators: Optional[Dict[str, Any]] = {}


# Advanced Question Types for INSTAT
class INSTATQuestionType(str, Enum):
    """INSTAT-specific question types"""
    # Standard types
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    
    # INSTAT-specific types
    PERCENTAGE_DISTRIBUTION = "percentage_distribution"
    BUDGET_ALLOCATION = "budget_allocation"
    GEOGRAPHIC_SELECTION = "geographic_selection"
    STAKEHOLDER_MATRIX = "stakeholder_matrix"
    TIMELINE_CHART = "timeline_chart"
    PERFORMANCE_SCALE = "performance_scale"
    COMPLIANCE_CHECKLIST = "compliance_checklist"
    RESOURCE_ALLOCATION = "resource_allocation"
    INDICATOR_TRACKING = "indicator_tracking"
    VULNERABILITY_ASSESSMENT = "vulnerability_assessment"


class INSTATQuestion(BaseModel):
    """Enhanced question model for INSTAT surveys"""
    QuestionText: str
    QuestionType: INSTATQuestionType
    IsRequired: bool = False
    
    # INSTAT-specific fields
    IndicatorCode: Optional[str] = None  # Links to national indicators
    DataSource: Optional[str] = None
    CollectionMethod: Optional[str] = None
    QualityRequirements: Optional[Dict[str, Any]] = {}
    
    # Validation rules
    ValidationRules: Optional[Dict[str, Any]] = {}
    DependsOnQuestion: Optional[int] = None  # Conditional logic
    
    # Multilingual support
    QuestionTextEN: Optional[str] = None
    QuestionTextFR: Optional[str] = None
    
    # Metadata
    Tags: Optional[List[str]] = []
    Priority: Optional[str] = "medium"  # high, medium, low


# Template Management
class SurveyTemplate(BaseModel):
    """Survey Template for INSTAT standardization"""
    TemplateID: Optional[int] = None
    TemplateName: str
    Domain: INSTATDomain
    Category: SurveyCategory
    Version: str = "1.0.0"
    
    # Template metadata
    CreatedBy: Optional[str] = None
    CreatedDate: Optional[datetime] = None
    LastModified: Optional[datetime] = None
    ApprovedBy: Optional[str] = None
    ApprovalDate: Optional[datetime] = None
    
    # Template structure
    Sections: Optional[List[Dict[str, Any]]] = []
    DefaultQuestions: Optional[List[INSTATQuestion]] = []
    
    # Usage tracking
    UsageCount: Optional[int] = 0
    LastUsed: Optional[datetime] = None
    
    # Documentation
    UsageGuidelines: Optional[str] = None
    ExampleImplementations: Optional[List[str]] = []
    
    class Config:
        orm_mode = True


# Reporting and Analytics
class SurveyMetrics(BaseModel):
    """Survey metrics for INSTAT reporting"""
    SurveyID: int
    
    # Response metrics
    TotalResponses: int = 0
    CompletionRate: float = 0.0
    AverageCompletionTime: Optional[float] = None  # in minutes
    
    # Quality metrics
    DataQualityScore: Optional[float] = None
    ValidationErrorRate: Optional[float] = None
    IncompleteResponses: int = 0
    
    # Geographic distribution
    ResponseByRegion: Optional[Dict[str, int]] = {}
    CoverageRate: Optional[float] = None
    
    # Temporal metrics
    ResponseTrend: Optional[Dict[str, int]] = {}  # responses over time
    
    # Resource metrics
    DataCollectionCost: Optional[float] = None
    TimeToComplete: Optional[int] = None  # in days
    
    class Config:
        orm_mode = True


# Workflow enhancements for INSTAT
class INSTATWorkflowStage(str, Enum):
    """INSTAT-specific workflow stages"""
    DESIGN = "design"
    TECHNICAL_REVIEW = "technical_review"
    METHODOLOGICAL_REVIEW = "methodological_review"
    PILOT_TEST = "pilot_test"
    FIELD_PREPARATION = "field_preparation"
    DATA_COLLECTION = "data_collection"
    DATA_PROCESSING = "data_processing"
    QUALITY_ASSURANCE = "quality_assurance"
    ANALYSIS = "analysis"
    REPORT_DRAFTING = "report_drafting"
    VALIDATION = "validation"
    PUBLICATION = "publication"
    DISSEMINATION = "dissemination"


class INSTATWorkflowTransition(BaseModel):
    """INSTAT workflow transition with specific requirements"""
    FromStage: INSTATWorkflowStage
    ToStage: INSTATWorkflowStage
    RequiredRole: Optional[str] = None
    RequiredDocuments: Optional[List[str]] = []
    QualityChecks: Optional[List[str]] = []
    EstimatedDuration: Optional[int] = None  # in days
    RequiredApprovals: Optional[List[str]] = []


# Integration models
class ExternalSystem(BaseModel):
    """External systems integration for INSTAT"""
    SystemName: str
    SystemType: str  # database, api, file_system, etc.
    ConnectionDetails: Dict[str, Any]
    DataMapping: Optional[Dict[str, str]] = {}
    SyncFrequency: Optional[str] = None
    LastSync: Optional[datetime] = None


class DataExport(BaseModel):
    """Data export configuration"""
    ExportID: Optional[int] = None
    SurveyID: int
    ExportFormat: str  # excel, csv, json, xml, pdf
    ExportType: str  # raw_data, analysis, report, dashboard
    
    # Export configuration
    IncludeMetadata: bool = True
    IncludeValidation: bool = True
    FilterCriteria: Optional[Dict[str, Any]] = {}
    
    # Scheduling
    IsScheduled: bool = False
    ScheduleFrequency: Optional[str] = None
    NextExport: Optional[datetime] = None
    
    # Delivery
    DeliveryMethod: str = "download"  # download, email, ftp, api
    Recipients: Optional[List[str]] = []
    
    class Config:
        orm_mode = True
