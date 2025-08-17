"""INSTAT-specific API services and endpoints."""

from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from src.infrastructure.database.connection import get_db
from src.infrastructure.database import models
from schemas.instat_domains import (
    INSTATSurveyCreate, INSTATSurveyResponse, INSTATSurveyUpdate,
    SurveyTemplateCreate, SurveyTemplateResponse, 
    INSTATQuestionCreate, INSTATQuestionResponse,
    SurveyMetricsResponse, DataExportCreate, DataExportResponse,
    SurveyDomain, SurveyCategory, WorkflowStatus, ReportingCycle
)
from schemas.responses import (
    BaseResponse, PaginatedResponse
)
from schemas.errors import (
    ErrorResponse, ValidationErrorResponse, NotFoundErrorResponse
)


class INSTATSurveyService:
    """Service for INSTAT survey management."""

    def __init__(self, db: Session):
        self.db = db

    def create_survey(self, survey_data: INSTATSurveyCreate) -> INSTATSurveyResponse:
        """Create a new INSTAT survey."""
        try:
            db_survey = models.INSTATSurvey(
                **survey_data.model_dump(),
                Status=WorkflowStatus.DRAFT.value
            )
            self.db.add(db_survey)
            self.db.commit()
            self.db.refresh(db_survey)
            
            return INSTATSurveyResponse(**db_survey.to_dict())
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create survey: {str(e)}"
            )

    def get_survey(self, survey_id: int) -> Optional[INSTATSurveyResponse]:
        """Get INSTAT survey by ID."""
        survey = self.db.query(models.INSTATSurvey).filter(
            models.INSTATSurvey.SurveyID == survey_id
        ).first()
        
        if not survey:
            return None
            
        return INSTATSurveyResponse(**survey.to_dict())

    def list_surveys(
        self, 
        skip: int = 0, 
        limit: int = 100,
        domain: Optional[SurveyDomain] = None,
        category: Optional[SurveyCategory] = None,
        status: Optional[WorkflowStatus] = None,
        fiscal_year: Optional[int] = None,
        reporting_cycle: Optional[ReportingCycle] = None
    ) -> PaginatedResponse[INSTATSurveyResponse]:
        """List INSTAT surveys with filtering."""
        query = self.db.query(models.INSTATSurvey)
        
        # Apply filters
        if domain:
            query = query.filter(models.INSTATSurvey.Domain == domain.value)
        if category:
            query = query.filter(models.INSTATSurvey.Category == category.value)
        if status:
            query = query.filter(models.INSTATSurvey.Status == status.value)
        if fiscal_year:
            query = query.filter(models.INSTATSurvey.FiscalYear == fiscal_year)
        if reporting_cycle:
            query = query.filter(models.INSTATSurvey.ReportingCycle == reporting_cycle.value)
        
        total = query.count()
        surveys = query.order_by(desc(models.INSTATSurvey.CreatedDate)).offset(skip).limit(limit).all()
        
        items = [INSTATSurveyResponse(**survey.to_dict()) for survey in surveys]
        
        return PaginatedResponse[INSTATSurveyResponse](
            success=True,
            message="Surveys retrieved successfully",
            data=items,
            pagination={
                "total": total,
                "page": skip // limit + 1 if limit > 0 else 1,
                "size": limit,
                "pages": (total + limit - 1) // limit if limit > 0 else 1,
                "has_next": skip + limit < total,
                "has_prev": skip > 0
            }
        )

    def update_survey(
        self, 
        survey_id: int, 
        survey_update: INSTATSurveyUpdate
    ) -> Optional[INSTATSurveyResponse]:
        """Update INSTAT survey."""
        survey = self.db.query(models.INSTATSurvey).filter(
            models.INSTATSurvey.SurveyID == survey_id
        ).first()
        
        if not survey:
            return None
        
        try:
            update_data = survey_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(survey, field, value)
            
            self.db.commit()
            self.db.refresh(survey)
            
            return INSTATSurveyResponse(**survey.to_dict())
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update survey: {str(e)}"
            )

    def delete_survey(self, survey_id: int) -> bool:
        """Delete INSTAT survey."""
        survey = self.db.query(models.INSTATSurvey).filter(
            models.INSTATSurvey.SurveyID == survey_id
        ).first()
        
        if not survey:
            return False
        
        try:
            self.db.delete(survey)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to delete survey: {str(e)}"
            )


class TemplateService:
    """Service for survey template management."""

    def __init__(self, db: Session):
        self.db = db

    def create_template(self, template_data: SurveyTemplateCreate) -> SurveyTemplateResponse:
        """Create a new survey template."""
        try:
            db_template = models.SurveyTemplate(**template_data.model_dump())
            self.db.add(db_template)
            self.db.commit()
            self.db.refresh(db_template)
            
            return SurveyTemplateResponse(**db_template.to_dict())
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create template: {str(e)}"
            )

    def get_template(self, template_id: int) -> Optional[SurveyTemplateResponse]:
        """Get survey template by ID."""
        template = self.db.query(models.SurveyTemplate).filter(
            models.SurveyTemplate.TemplateID == template_id
        ).first()
        
        if not template:
            return None
            
        return SurveyTemplateResponse(**template.to_dict())

    def list_templates(
        self,
        skip: int = 0,
        limit: int = 100,
        domain: Optional[SurveyDomain] = None,
        category: Optional[SurveyCategory] = None
    ) -> PaginatedResponse[SurveyTemplateResponse]:
        """List survey templates with filtering."""
        query = self.db.query(models.SurveyTemplate)
        
        if domain:
            query = query.filter(models.SurveyTemplate.Domain == domain.value)
        if category:
            query = query.filter(models.SurveyTemplate.Category == category.value)
        
        total = query.count()
        templates = query.order_by(asc(models.SurveyTemplate.TemplateName)).offset(skip).limit(limit).all()
        
        items = [SurveyTemplateResponse(**template.to_dict()) for template in templates]
        
        return PaginatedResponse[SurveyTemplateResponse](
            data=items,
            pagination={
                "total": total,
                "page": skip // limit + 1 if limit > 0 else 1,
                "size": limit,
                "pages": (total + limit - 1) // limit if limit > 0 else 1
            }
        )
        
    def get_template_with_sections(self, template_id: int) -> Optional[Dict[str, Any]]:
        """Get template with detailed sections and questions for display."""
        template = self.db.query(models.SurveyTemplate).filter(
            models.SurveyTemplate.TemplateID == template_id
        ).first()
        
        if not template:
            return None
            
        template_dict = template.to_dict()
        
        # Parse sections to count questions and subsections
        sections = template_dict.get('Sections', [])
        total_questions = 0
        total_subsections = 0
        
        for section in sections:
            section_questions = section.get('questions', [])
            section_subsections = section.get('subsections', [])
            total_questions += len(section_questions)
            total_subsections += len(section_subsections)
            
            # Count questions in subsections too
            for subsection in section_subsections:
                subsection_questions = subsection.get('questions', [])
                total_questions += len(subsection_questions)
        
        # Add computed metadata
        template_dict['metadata'] = {
            'total_sections': len(sections),
            'total_subsections': total_subsections,
            'total_questions': total_questions,
            'template_complexity': 'High' if total_questions > 50 else 'Medium' if total_questions > 20 else 'Low'
        }
        
        return template_dict
        
    def list_templates_with_stats(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List templates with statistical information for better display."""
        templates = self.db.query(models.SurveyTemplate).offset(skip).limit(limit).all()
        total = self.db.query(models.SurveyTemplate).count()
        
        template_list = []
        for template in templates:
            template_dict = template.to_dict()
            
            # Calculate metadata
            sections = template_dict.get('Sections', [])
            question_count = 0
            section_count = len(sections)
            
            for section in sections:
                questions = section.get('questions', [])
                subsections = section.get('subsections', [])
                question_count += len(questions)
                
                for subsection in subsections:
                    sub_questions = subsection.get('questions', [])
                    question_count += len(sub_questions)
            
            # Add computed fields
            template_dict['question_count'] = question_count
            template_dict['section_count'] = section_count
            template_dict['complexity_level'] = (
                'High' if question_count > 50 else 
                'Medium' if question_count > 20 else 
                'Low'
            )
            
            template_list.append(template_dict)
            
        return {
            'templates': template_list,
            'pagination': {
                'total': total,
                'page': skip // limit + 1 if limit > 0 else 1,
                'size': limit,
                'pages': (total + limit - 1) // limit if limit > 0 else 1
            },
            'summary': {
                'total_templates': total,
                'templates_by_domain': self._get_templates_by_domain(),
                'templates_by_category': self._get_templates_by_category()
            }
        }
        
    def _get_templates_by_domain(self) -> Dict[str, int]:
        """Get template count by domain."""
        from sqlalchemy import func
        result = self.db.query(
            models.SurveyTemplate.Domain, 
            func.count(models.SurveyTemplate.TemplateID)
        ).group_by(models.SurveyTemplate.Domain).all()
        return {domain: count for domain, count in result}
        
    def _get_templates_by_category(self) -> Dict[str, int]:
        """Get template count by category."""
        from sqlalchemy import func
        result = self.db.query(
            models.SurveyTemplate.Category, 
            func.count(models.SurveyTemplate.TemplateID)
        ).group_by(models.SurveyTemplate.Category).all()
        return {category: count for category, count in result}


class MetricsService:
    """Service for survey metrics management."""

    def __init__(self, db: Session):
        self.db = db

    def get_survey_metrics(self, survey_id: int) -> Optional[SurveyMetricsResponse]:
        """Get metrics for a specific survey."""
        metrics = self.db.query(models.SurveyMetrics).filter(
            models.SurveyMetrics.SurveyID == survey_id
        ).first()
        
        if not metrics:
            return None
            
        return SurveyMetricsResponse(**metrics.to_dict())

    def update_survey_metrics(self, survey_id: int, metrics_data: Dict[str, Any]) -> SurveyMetricsResponse:
        """Update or create survey metrics."""
        metrics = self.db.query(models.SurveyMetrics).filter(
            models.SurveyMetrics.SurveyID == survey_id
        ).first()
        
        try:
            if metrics:
                for field, value in metrics_data.items():
                    if hasattr(metrics, field):
                        setattr(metrics, field, value)
            else:
                metrics = models.SurveyMetrics(SurveyID=survey_id, **metrics_data)
                self.db.add(metrics)
            
            self.db.commit()
            self.db.refresh(metrics)
            
            return SurveyMetricsResponse(**metrics.to_dict())
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update metrics: {str(e)}"
            )


class ExportService:
    """Service for data export management."""

    def __init__(self, db: Session):
        self.db = db

    def create_export_config(self, export_data: DataExportCreate) -> DataExportResponse:
        """Create a new export configuration."""
        try:
            db_export = models.DataExport(**export_data.model_dump())
            self.db.add(db_export)
            self.db.commit()
            self.db.refresh(db_export)
            
            return DataExportResponse(**db_export.to_dict())
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create export config: {str(e)}"
            )

    def list_export_configs(
        self,
        survey_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> PaginatedResponse[DataExportResponse]:
        """List export configurations."""
        query = self.db.query(models.DataExport)
        
        if survey_id:
            query = query.filter(models.DataExport.SurveyID == survey_id)
        
        total = query.count()
        exports = query.order_by(desc(models.DataExport.CreatedDate)).offset(skip).limit(limit).all()
        
        items = [DataExportResponse(**export.to_dict()) for export in exports]
        
        return PaginatedResponse[DataExportResponse](
            items=items,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit,
            pages=(total + limit - 1) // limit if limit > 0 else 1
        )


# Service factory functions
def get_instat_survey_service(db: Session = Depends(get_db)) -> INSTATSurveyService:
    """Get INSTAT survey service."""
    return INSTATSurveyService(db)


def get_template_service(db: Session = Depends(get_db)) -> TemplateService:
    """Get template service."""
    return TemplateService(db)


def get_metrics_service(db: Session = Depends(get_db)) -> MetricsService:
    """Get metrics service."""
    return MetricsService(db)


def get_export_service(db: Session = Depends(get_db)) -> ExportService:
    """Get export service."""
    return ExportService(db)
