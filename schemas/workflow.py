"""
Workflow and status management for INSTAT surveys
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class SurveyStatus(str, Enum):
    """Survey workflow states"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class ActionType(str, Enum):
    """Types of actions in workflow"""
    CREATE = "create"
    UPDATE = "update"
    SUBMIT_FOR_REVIEW = "submit_for_review"
    APPROVE = "approve"
    REJECT = "reject"
    PUBLISH = "publish"
    ARCHIVE = "archive"
    COMMENT = "comment"


class WorkflowActionBase(BaseModel):
    UserID: Optional[str] = None
    ActionType: ActionType
    FromStatus: Optional[SurveyStatus] = None
    ToStatus: Optional[SurveyStatus] = None
    Comment: Optional[str] = None


class WorkflowActionCreate(WorkflowActionBase):
    SurveyID: int
    SchemaName: str


class WorkflowAction(WorkflowActionBase):
    ActionID: int
    Timestamp: datetime
    
    class Config:
        orm_mode = True


class SurveyWorkflow(BaseModel):
    """Complete survey workflow"""
    survey_id: int
    current_status: SurveyStatus
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Workflow history
    actions: List[WorkflowAction] = []
    
    # Review information
    reviewer_id: Optional[str] = None
    review_date: Optional[datetime] = None
    review_comments: Optional[str] = None
    
    # Approval information  
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    approval_comments: Optional[str] = None
    
    # Publication information
    published_by: Optional[str] = None
    published_at: Optional[datetime] = None
    publication_url: Optional[str] = None
    
    class Config:
        orm_mode = True


class WorkflowTransition(BaseModel):
    """Allowed workflow transitions"""
    from_status: SurveyStatus
    to_status: SurveyStatus
    required_role: Optional[str] = None
    requires_comment: bool = False


# Define allowed workflow transitions
WORKFLOW_TRANSITIONS = [
    WorkflowTransition(from_status=SurveyStatus.DRAFT, to_status=SurveyStatus.REVIEW),
    WorkflowTransition(from_status=SurveyStatus.DRAFT, to_status=SurveyStatus.ARCHIVED),
    
    WorkflowTransition(from_status=SurveyStatus.REVIEW, to_status=SurveyStatus.APPROVED, required_role="reviewer"),
    WorkflowTransition(from_status=SurveyStatus.REVIEW, to_status=SurveyStatus.REJECTED, required_role="reviewer", requires_comment=True),
    WorkflowTransition(from_status=SurveyStatus.REVIEW, to_status=SurveyStatus.DRAFT),
    
    WorkflowTransition(from_status=SurveyStatus.APPROVED, to_status=SurveyStatus.PUBLISHED, required_role="admin"),
    WorkflowTransition(from_status=SurveyStatus.APPROVED, to_status=SurveyStatus.REVIEW),
    
    WorkflowTransition(from_status=SurveyStatus.PUBLISHED, to_status=SurveyStatus.ARCHIVED, required_role="admin"),
    
    WorkflowTransition(from_status=SurveyStatus.REJECTED, to_status=SurveyStatus.DRAFT),
    WorkflowTransition(from_status=SurveyStatus.REJECTED, to_status=SurveyStatus.ARCHIVED),
]
