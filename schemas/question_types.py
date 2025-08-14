"""
Enhanced question types for INSTAT Survey Platform
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import date


class QuestionTypeEnum(str, Enum):
    """Enhanced question types for INSTAT forms"""
    # Basic types
    TEXT = "text"
    TEXTAREA = "textarea" 
    NUMBER = "number"
    EMAIL = "email"
    PHONE = "phone"
    
    # Date/Time types
    DATE = "date"
    DATE_RANGE = "date_range"
    DATETIME = "datetime"
    
    # Selection types
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    
    # Advanced types for INSTAT
    RATING_SCALE = "rating_scale"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    CALCULATION_FIELD = "calculation_field"
    
    # Grid/Matrix types
    MULTI_SELECT_GRID = "multi_select_grid"
    RATING_GRID = "rating_grid"
    
    # File types
    FILE_UPLOAD = "file_upload"
    IMAGE_UPLOAD = "image_upload"
    
    # Signature
    SIGNATURE_FIELD = "signature_field"
    
    # Conditional
    CONDITIONAL_SECTION = "conditional_section"
    
    # Geographic
    COUNTRY = "country"
    REGION = "region"
    ADDRESS = "address"


class ValidationRule(BaseModel):
    """Validation rules for questions"""
    type: str  # required, min_length, max_length, min_value, max_value, pattern
    value: Optional[Any] = None
    message: Optional[str] = None


class ConditionalLogic(BaseModel):
    """Conditional display logic"""
    trigger_question_id: int
    condition: str  # equals, not_equals, greater_than, less_than, contains
    value: Any
    action: str  # show, hide, required, optional


class QuestionOptions(BaseModel):
    """Extended question options"""
    # Basic options
    required: bool = False
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    
    # Advanced options
    validation_rules: List[ValidationRule] = []
    conditional_logic: List[ConditionalLogic] = []
    
    # Rating scale specific
    scale_min: Optional[int] = None
    scale_max: Optional[int] = None
    scale_labels: Optional[Dict[str, str]] = None
    
    # Grid specific
    grid_rows: Optional[List[str]] = None
    grid_columns: Optional[List[str]] = None
    
    # Calculation specific
    calculation_formula: Optional[str] = None
    calculation_dependencies: Optional[List[int]] = None
    
    # File upload specific
    max_file_size: Optional[int] = None  # in bytes
    allowed_file_types: Optional[List[str]] = None
    
    # Multilingual
    translations: Optional[Dict[str, str]] = None  # language code -> translated text


class EnhancedQuestion(BaseModel):
    """Enhanced question model for INSTAT"""
    QuestionID: Optional[int] = None
    SectionID: int
    SubsectionID: Optional[int] = None
    QuestionText: str
    QuestionType: QuestionTypeEnum
    Order: int = 0
    
    # Enhanced options
    options: QuestionOptions = QuestionOptions()
    
    # Multilingual support
    question_text_fr: Optional[str] = None  # French
    question_text_en: Optional[str] = None  # English
    
    class Config:
        orm_mode = True
