"""
Business logic for survey management
"""
from sqlalchemy.orm import Session
from ...infrastructure.database import models
from schemas import survey as survey_schema


def create_survey(db: Session, survey: survey_schema.SurveyCreate, schema_name: str):
    """Create a new survey with all nested objects"""
    # Create the main survey
    db_survey = models.Survey(
        Title=survey.Title,
        Description=survey.Description,
        Status=survey.Status
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    
    # Create sections, subsections, questions, and answer options
    for section_data in survey.Sections:
        db_section = models.Section(
            SurveyID=db_survey.SurveyID,
            Title=section_data.Title
        )
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        
        # Create subsections
        for subsection_data in section_data.Subsections:
            db_subsection = models.Subsection(
                SectionID=db_section.SectionID,
                Title=subsection_data.Title
            )
            db.add(db_subsection)
            db.commit()
            db.refresh(db_subsection)
            
            # Create questions in subsection
            for question_data in subsection_data.Questions:
                db_question = models.Question(
                    SectionID=db_section.SectionID,
                    SubsectionID=db_subsection.SubsectionID,
                    QuestionText=question_data.QuestionText,
                    QuestionType=question_data.QuestionType
                )
                db.add(db_question)
                db.commit()
                db.refresh(db_question)
                
                # Create answer options
                for option_data in question_data.AnswerOptions:
                    db_option = models.AnswerOption(
                        QuestionID=db_question.QuestionID,
                        OptionText=option_data.OptionText
                    )
                    db.add(db_option)
                    db.commit()
        
        # Create questions directly in section (not in subsection)
        for question_data in section_data.Questions:
            db_question = models.Question(
                SectionID=db_section.SectionID,
                SubsectionID=None,  # No subsection
                QuestionText=question_data.QuestionText,
                QuestionType=question_data.QuestionType
            )
            db.add(db_question)
            db.commit()
            db.refresh(db_question)
            
            # Create answer options
            for option_data in question_data.AnswerOptions:
                db_option = models.AnswerOption(
                    QuestionID=db_question.QuestionID,
                    OptionText=option_data.OptionText
                )
                db.add(db_option)
                db.commit()
    
    return db_survey


def get_survey(db: Session, survey_id: int, schema_name: str):
    """Get survey by ID"""
    return db.query(models.Survey).filter(models.Survey.SurveyID == survey_id).first()


def get_surveys(db: Session, schema_name: str, skip: int = 0, limit: int = 100):
    """Get all surveys"""
    return db.query(models.Survey).offset(skip).limit(limit).all()


def update_survey(db: Session, survey_id: int, survey: survey_schema.SurveyCreate, schema_name: str):
    """Update a survey"""
    db_survey = db.query(models.Survey).filter(models.Survey.SurveyID == survey_id).first()
    if db_survey:
        db_survey.Title = survey.Title
        db_survey.Description = survey.Description
        db_survey.Status = survey.Status
        db.commit()
        db.refresh(db_survey)
    return db_survey


def delete_survey(db: Session, survey_id: int, schema_name: str):
    """Delete a survey"""
    db_survey = db.query(models.Survey).filter(models.Survey.SurveyID == survey_id).first()
    if db_survey:
        db.delete(db_survey)
        db.commit()
    return db_survey

