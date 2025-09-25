"""
Extended schemas for survey responses, progress tracking, validation, and statistics
"""
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ResponseStatus(str, Enum):
    """Status of survey responses"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"
    SUBMITTED = "submitted"
    REJECTED = "rejected"


class ValidationSeverity(str, Enum):
    """Validation issue severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ExportFormat(str, Enum):
    """Export format options"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    XML = "xml"


# Survey Response Models
class SurveyResponseValue(BaseModel):
    """Individual response value"""
    question_id: int
    value: Union[str, int, float, List[str], Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = {}


class SurveyResponseCreate(BaseModel):
    """Create/update survey response"""
    survey_id: int
    respondent_id: Optional[str] = None
    respondent_metadata: Optional[Dict[str, Any]] = {}
    responses: List[SurveyResponseValue]
    status: ResponseStatus = ResponseStatus.DRAFT
    save_as_draft: bool = True
    section_id: Optional[int] = None  # For partial saves


class SurveyResponseUpdate(BaseModel):
    """Update existing survey response"""
    responses: Optional[List[SurveyResponseValue]] = None
    status: Optional[ResponseStatus] = None
    respondent_metadata: Optional[Dict[str, Any]] = None


class SurveyResponseData(BaseModel):
    """Survey response data"""
    response_id: int
    survey_id: int
    respondent_id: Optional[str] = None
    respondent_metadata: Optional[Dict[str, Any]] = {}
    responses: List[SurveyResponseValue]
    status: ResponseStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    completion_percentage: float = 0.0
    
    class Config:
        orm_mode = True


# Progress Tracking Models
class SurveyProgress(BaseModel):
    """Survey completion progress"""
    survey_id: int
    respondent_id: Optional[str] = None
    total_questions: int
    answered_questions: int
    completion_percentage: float
    current_section_id: Optional[int] = None
    current_section_title: Optional[str] = None
    last_activity: Optional[datetime] = None
    estimated_time_remaining: Optional[int] = None  # in minutes
    sections_progress: List[Dict[str, Any]] = []
    
    class Config:
        orm_mode = True


# Validation Models
class ValidationIssue(BaseModel):
    """Individual validation issue"""
    field: str
    question_id: Optional[int] = None
    section_id: Optional[int] = None
    severity: ValidationSeverity
    message: str
    suggested_fix: Optional[str] = None
    error_code: Optional[str] = None


class ValidationResult(BaseModel):
    """Validation result for survey or response"""
    is_valid: bool
    total_issues: int
    errors: int
    warnings: int
    info: int
    issues: List[ValidationIssue]
    validation_timestamp: datetime
    validated_by: Optional[str] = None


class SurveyValidationRequest(BaseModel):
    """Request for survey validation"""
    survey_id: Optional[int] = None
    response_id: Optional[int] = None
    validate_structure: bool = True
    validate_data: bool = True
    validate_business_rules: bool = True
    section_id: Optional[int] = None  # Validate specific section only


# Statistics Models
class QuestionStatistics(BaseModel):
    """Statistics for individual question"""
    question_id: int
    question_text: str
    question_type: str
    total_responses: int
    response_rate: float
    most_common_answer: Optional[str] = None
    answer_distribution: Dict[str, Any] = {}
    average_time_spent: Optional[float] = None  # in seconds


class SectionStatistics(BaseModel):
    """Statistics for survey section"""
    section_id: int
    section_title: str
    total_questions: int
    completion_rate: float
    average_time_spent: Optional[float] = None  # in minutes
    questions: List[QuestionStatistics] = []


class SurveyStatistics(BaseModel):
    """Complete survey statistics"""
    survey_id: int
    survey_title: str
    total_responses: int
    completed_responses: int
    completion_rate: float
    average_completion_time: Optional[float] = None  # in minutes
    response_rate_by_day: Dict[str, int] = {}
    geographic_distribution: Dict[str, int] = {}
    demographic_breakdown: Dict[str, Any] = {}
    sections: List[SectionStatistics] = []
    last_updated: datetime
    
    class Config:
        orm_mode = True


# Export Models
class ExportRequest(BaseModel):
    """Request for data export"""
    survey_id: int
    format: ExportFormat
    include_metadata: bool = True
    include_raw_data: bool = True
    include_statistics: bool = False
    date_range: Optional[Dict[str, str]] = None  # {"start": "2024-01-01", "end": "2024-12-31"}
    filters: Optional[Dict[str, Any]] = {}
    sections: Optional[List[int]] = None  # Export specific sections only
    questions: Optional[List[int]] = None  # Export specific questions only


class ExportResult(BaseModel):
    """Export result"""
    export_id: str
    survey_id: int
    format: ExportFormat
    file_url: Optional[str] = None
    file_name: str
    file_size: Optional[int] = None  # in bytes
    status: str  # "processing", "completed", "failed"
    created_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    download_count: int = 0
    error_message: Optional[str] = None
    
    class Config:
        orm_mode = True


# Search Models
class SurveySearchQuery(BaseModel):
    """Advanced search query for surveys"""
    query: Optional[str] = None  # Text search
    domain: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    created_date_from: Optional[datetime] = None
    created_date_to: Optional[datetime] = None
    created_by: Optional[str] = None
    tags: Optional[List[str]] = None
    has_responses: Optional[bool] = None
    min_completion_rate: Optional[float] = None
    fiscal_year: Optional[int] = None
    
    # Pagination and sorting
    skip: int = 0
    limit: int = 100
    sort_by: str = "created_date"
    sort_order: str = "desc"  # "asc" or "desc"


class SurveySearchResult(BaseModel):
    """Search result item"""
    survey_id: int
    title: str
    description: Optional[str] = None
    domain: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    created_date: datetime
    created_by: Optional[str] = None
    total_responses: int = 0
    completion_rate: float = 0.0
    tags: List[str] = []
    relevance_score: Optional[float] = None
    
    class Config:
        orm_mode = True


class SurveySearchResponse(BaseModel):
    """Search response with results and metadata"""
    results: List[SurveySearchResult]
    total_results: int
    query_time: float  # in seconds
    suggestions: Optional[List[str]] = None
    facets: Optional[Dict[str, Dict[str, int]]] = None  # For filtering UI
    pagination: Dict[str, Any]


# Template Action Models
class TemplateAction(BaseModel):
    """Available action for a template"""
    action_id: str
    action_name: str
    description: str
    requires_permission: Optional[str] = None
    is_available: bool = True
    parameters: Optional[Dict[str, Any]] = {}


class TemplateActions(BaseModel):
    """All available actions for a template"""
    template_id: int
    template_name: str
    actions: List[TemplateAction]
    user_permissions: List[str]


# Template Duplication Models
class TemplateDuplicateRequest(BaseModel):
    """Request to duplicate a template"""
    new_name: str
    copy_questions: bool = True
    copy_sections: bool = True
    copy_metadata: bool = False
    target_domain: Optional[str] = None
    target_category: Optional[str] = None


class TemplateDuplicateResult(BaseModel):
    """Result of template duplication"""
    original_template_id: int
    new_template_id: int
    new_template_name: str
    items_copied: Dict[str, int]  # {"sections": 5, "questions": 20, etc.}
    created_at: datetime
    
    class Config:
        orm_mode = True


# Template Preview Models
class FormField(BaseModel):
    """Form field for preview"""
    field_id: str
    field_type: str
    label: str
    required: bool = False
    options: Optional[List[str]] = None
    validation: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}


class FormSection(BaseModel):
    """Form section for preview"""
    section_id: str
    title: str
    description: Optional[str] = None
    fields: List[FormField]
    is_repeatable: bool = False


class TemplatePreview(BaseModel):
    """Template preview for form rendering"""
    template_id: int
    template_name: str
    description: Optional[str] = None
    total_fields: int
    estimated_time: Optional[int] = None  # in minutes
    sections: List[FormSection]
    styling: Optional[Dict[str, Any]] = {}
    configuration: Optional[Dict[str, Any]] = {}
    
    class Config:
        orm_mode = True