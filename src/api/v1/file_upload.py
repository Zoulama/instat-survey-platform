"""
File upload API for INSTAT Survey Platform
"""
import os
import shutil
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
import config
from ...utils.excel_parser import ExcelParser
from ...infrastructure.database.connection import get_db
from ...domain.survey import survey_service
from ...domain.instat.instat_services import get_template_service, TemplateService
from ...infrastructure.auth.oauth2 import UserInToken, require_scopes
from ...services.audit_service import AuditService
from src.infrastructure.database.models import ParsingResult, ParsingStatistics
from schemas import survey as survey_schema
from schemas.instat_domains import SurveyTemplateCreate, INSTATDomain, SurveyCategory
from schemas.responses import FileUploadResponse
from schemas.errors import (
    BadRequestErrorResponse,
    ValidationErrorResponse,
    InternalErrorResponse
)

router = APIRouter(
    tags=["File Upload"],
    prefix="/v1/api/files"
)

excel_parser = ExcelParser()


def _convert_sections_to_schema(sections_data):
    """Convert parsed sections data to schema format"""
    sections = []
    for section_data in sections_data:
        # Convert subsections
        subsections = []
        for subsection_data in section_data.get("subsections", []):
            questions = _convert_questions_to_schema(subsection_data.get("questions", []))
            if questions:  # Only add subsection if it has questions
                subsections.append(survey_schema.SubsectionCreate(
                    Title=subsection_data.get("title", "Untitled Subsection"),
                    Questions=questions
                ))

        # Convert direct questions in section
        questions = _convert_questions_to_schema(section_data.get("questions", []))

        # Only add section if it has questions or subsections
        if questions or subsections:
            sections.append(survey_schema.SectionCreate(
                Title=section_data.get("title", "Untitled Section"),
                Subsections=subsections,
                Questions=questions
            ))

    return sections


def _convert_questions_to_schema(questions_data):
    """Convert parsed questions data to schema format"""
    questions = []
    for question_data in questions_data:
        # Convert answer options
        options = []
        for option in question_data.get("options", []):
            if isinstance(option, dict):
                option_text = option.get("text", str(option))
            else:
                option_text = str(option)

            if option_text and option_text.strip():
                options.append(survey_schema.AnswerOptionCreate(
                    OptionText=option_text.strip()
                ))

        # Create question only if it has valid text
        question_text = question_data.get("text", "Untitled Question").strip()
        if question_text and len(question_text) > 2:  # Only add valid questions
            questions.append(survey_schema.QuestionCreate(
                QuestionText=question_text,
                QuestionType=question_data.get("type", "text"),
                AnswerOptions=options,
                IsRequired=question_data.get("is_required", False)
            ))

    return questions


@router.post(
    "/upload-excel-and-create-survey",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
async def upload_excel_and_create_survey(
    *,
    file: UploadFile = File(..., description="Excel file to upload and parse"),
    create_template: bool = Query(True, description="Automatically create template from survey structure"),
    template_name: Optional[str] = Query(None, description="Name for the template (defaults to filename)"),
    schema_name: Optional[str] = Query(None, description="Override auto-detected schema"),
    request: Request = None,
    current_user: UserInToken = require_scopes("upload:write"),
    db: Session = Depends(get_db),
    template_service: TemplateService = Depends(get_template_service)
):
    # Auto-detect schema name if not provided
    if not schema_name:
        schema_name = excel_parser.determine_schema_name(file.filename)
    
    # Validate schema name
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in config.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types are: {config.ALLOWED_FILE_EXTENSIONS}"
        )
    
    # Ensure upload directory exists
    upload_dir = Path(config.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file to disk
    file_path = upload_dir / file.filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    # Parse the uploaded file with enhanced parser
    try:
        survey_structure = excel_parser.parse_file(file_path)
        validation_issues = excel_parser.validate_structure(survey_structure)
        
        if validation_issues:
            return FileUploadResponse(
                success=False,
                message="File uploaded, but with validation issues.",
                file_path=str(file_path),
                issues=validation_issues,
                survey_structure=survey_structure,
                timestamp=datetime.utcnow()
            )
        
        # Create survey from parsed structure
        survey_data = survey_schema.SurveyCreate(
            Title=survey_structure.get("title", file.filename),
            Description=survey_structure.get("description", f"Survey generated from {file.filename}"),
            Status="Draft",
            Sections=_convert_sections_to_schema(survey_structure.get("sections", []))
        )
        
        # Create the survey in the database
        created_survey = survey_service.create_survey(db=db, survey=survey_data, schema_name=schema_name)
        
        # Create template if requested
        created_template = None
        if create_template:
            try:
                # Prepare template data
                template_sections = _convert_survey_structure_to_template_sections(survey_structure)
                
                template_data = SurveyTemplateCreate(
                    TemplateName=template_name or f"Template_{os.path.splitext(file.filename)[0]}",
                    Domain=_determine_instat_domain_from_schema(schema_name),
                    Category=_determine_survey_category_from_schema(schema_name),
                    Version="1.0.0",
                    CreatedBy="System",
                    Sections=template_sections,
                    UsageGuidelines=f"Template created from {file.filename} upload",
                    ExampleImplementations=[f"Original file: {file.filename}"]
                )
                
                created_template = template_service.create_template(template_data)
            except Exception as template_error:
                # Template creation failed, but survey was created successfully
                # Log the error but don't fail the entire operation
                print(f"Template creation failed: {template_error}")
        
        # Prepare response data
        response_data = {
            "message": "File uploaded, parsed, and survey created successfully.",
            "file_path": str(file_path),
            "survey_structure": survey_structure,
            "created_survey": created_survey.to_dict(),
            "timestamp": datetime.utcnow()
        }
        
        # Add template info if created
        if created_template:
            response_data["message"] = "File uploaded, parsed, survey and template created successfully."
            response_data["created_template"] = created_template.model_dump()
        
        return FileUploadResponse(**response_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Excel file: {str(e)}"
        )


def _determine_instat_domain_from_schema(schema_name: str) -> INSTATDomain:
    """Determine INSTAT domain from schema name"""
    if "program" in schema_name.lower():
        return INSTATDomain.PROGRAM_REVIEW
    elif "balance" in schema_name.lower():
        return INSTATDomain.SDS
    elif "diagnostic" in schema_name.lower():
        return INSTATDomain.DIAGNOSTIC
    else:
        return INSTATDomain.DES


def _determine_survey_category_from_schema(schema_name: str) -> SurveyCategory:
    """Determine survey category from schema name"""
    if "program" in schema_name.lower():
        return SurveyCategory.PROGRAM_REVIEW
    elif "diagnostic" in schema_name.lower():
        return SurveyCategory.DIAGNOSTIC
    elif "balance" in schema_name.lower():
        return SurveyCategory.DEVELOPMENT_ASSESSMENT
    else:
        return SurveyCategory.ACTIVITY_REPORT


def _convert_survey_structure_to_template_sections(survey_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert survey structure to template-compatible sections format"""
    sections = []
    for section in survey_structure.get("sections", []):
        template_section = {
            "title": section.get("title", "Untitled Section"),
            "questions": [],
            "subsections": []
        }
        
        # Add direct questions
        for question in section.get("questions", []):
            template_section["questions"].append({
                "text": question.get("text", ""),
                "type": question.get("type", "text"),
                "is_required": question.get("is_required", False),
                "options": question.get("options", [])
            })
        
        # Add subsections
        for subsection in section.get("subsections", []):
            template_subsection = {
                "title": subsection.get("title", "Untitled Subsection"),
                "questions": []
            }
            
            for question in subsection.get("questions", []):
                template_subsection["questions"].append({
                    "text": question.get("text", ""),
                    "type": question.get("type", "text"),
                    "is_required": question.get("is_required", False),
                    "options": question.get("options", [])
                })
            
            template_section["subsections"].append(template_subsection)
        
        sections.append(template_section)
    
    return sections


@router.post(
    "/upload-excel-and-create-survey-with-template",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorResponse}
    }
)
async def upload_excel_and_create_survey_with_template(
    file: UploadFile = File(...), 
    create_template: bool = Query(True, description="Create template from survey structure"),
    template_name: Optional[str] = Query(None, description="Name for the template (defaults to filename)"),
    schema_name: Optional[str] = Query(None, description="Override auto-detected schema"),
    current_user: UserInToken = require_scopes("upload:write"),
    db: Session = Depends(get_db),
    template_service: TemplateService = Depends(get_template_service)
):
    """Upload Excel file, create survey, and optionally create reusable template"""
    # Auto-detect schema name if not provided
    if not schema_name:
        schema_name = excel_parser.determine_schema_name(file.filename)
    
    # Validate schema name
    if schema_name not in ["survey_program", "survey_balance", "survey_diagnostic"]:
        raise HTTPException(status_code=400, detail="Invalid schema name")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in config.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types are: {config.ALLOWED_FILE_EXTENSIONS}"
        )
    
    # Ensure upload directory exists
    upload_dir = Path(config.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file to disk
    file_path = upload_dir / file.filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    # Parse the uploaded file with enhanced parser
    try:
        survey_structure = excel_parser.parse_file(file_path)
        validation_issues = excel_parser.validate_structure(survey_structure)
        
        if validation_issues:
            return FileUploadResponse(
                success=False,
                message="File uploaded, but with validation issues.",
                file_path=str(file_path),
                issues=validation_issues,
                survey_structure=survey_structure,
                timestamp=datetime.utcnow()
            )
        
        # Create survey from parsed structure
        survey_data = survey_schema.SurveyCreate(
            Title=survey_structure.get("title", file.filename),
            Description=survey_structure.get("description", f"Survey generated from {file.filename}"),
            Status="Draft",
            Sections=_convert_sections_to_schema(survey_structure.get("sections", []))
        )
        
        # Create the survey in the database
        created_survey = survey_service.create_survey(db=db, survey=survey_data, schema_name=schema_name)
        
        created_template = None
        if create_template:
            try:
                # Prepare template data
                template_sections = _convert_survey_structure_to_template_sections(survey_structure)
                
                template_data = SurveyTemplateCreate(
                    TemplateName=template_name or f"Template_{os.path.splitext(file.filename)[0]}",
                    Domain=_determine_instat_domain_from_schema(schema_name),
                    Category=_determine_survey_category_from_schema(schema_name),
                    Version="1.0.0",
                    CreatedBy="System",
                    Sections=template_sections,
                    UsageGuidelines=f"Template created from {file.filename} upload",
                    ExampleImplementations=[f"Original file: {file.filename}"]
                )
                
                created_template = template_service.create_template(template_data)
            except Exception as template_error:
                # Template creation failed, but survey was created successfully
                # Log the error but don't fail the entire operation
                print(f"Template creation failed: {template_error}")
        
        response_data = {
            "message": "File uploaded, parsed, and survey created successfully.",
            "file_path": str(file_path),
            "survey_structure": survey_structure,
            "created_survey": created_survey.to_dict(),
            "timestamp": datetime.utcnow()
        }
        
        if created_template:
            response_data["message"] = "File uploaded, parsed, survey and template created successfully."
            response_data["created_template"] = created_template.model_dump()
        
        return FileUploadResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Excel file: {str(e)}"
        )

