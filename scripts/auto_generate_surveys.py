#!/usr/bin/env python3
"""
Automatic survey generation script from analysis files
Parses Excel files in the analysis folder and creates surveys automatically
"""
import sys
import os
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from src.infrastructure.database.connection import db_manager
from src.utils.instat_excel_parser import INSTATExcelParser
from src.domain.survey import survey_service
from schemas import survey as survey_schema
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_sections_to_schema(sections_data):
    """Convert parsed sections data to schema format"""
    sections = []
    for section_data in sections_data:
        # Convert subsections
        subsections = []
        for subsection_data in section_data.get("subsections", []):
            questions = convert_questions_to_schema(subsection_data.get("questions", []))
            if questions:  # Only add subsection if it has questions
                subsections.append(survey_schema.SubsectionCreate(
                    Title=subsection_data.get("title", "Untitled Subsection"),
                    Questions=questions
                ))
        
        # Convert direct questions in section
        questions = convert_questions_to_schema(section_data.get("questions", []))
        
        # Only add section if it has questions or subsections
        if questions or subsections:
            sections.append(survey_schema.SectionCreate(
                Title=section_data.get("title", "Untitled Section"),
                Subsections=subsections,
                Questions=questions
            ))
    
    return sections


def convert_questions_to_schema(questions_data):
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
        
        # Create question
        question_text = question_data.get("text", "Untitled Question").strip()
        if question_text and len(question_text) > 2:  # Only add valid questions
            questions.append(survey_schema.QuestionCreate(
                QuestionText=question_text,
                QuestionType=question_data.get("type", "text"),
                AnswerOptions=options,
                IsRequired=question_data.get("is_required", False)
            ))
    
    return questions


def determine_schema_name(filename):
    """Determine appropriate schema name based on filename"""
    filename_lower = filename.lower()
    
    if "bilan" in filename_lower or "activites" in filename_lower:
        return "survey_balance"
    elif "diagnostic" in filename_lower:
        return "survey_diagnostic"
    elif "programme" in filename_lower or "programming" in filename_lower:
        return "survey_program"
    else:
        return "survey_balance"  # default


def auto_generate_surveys():
    """Automatically generate surveys from analysis files"""
    analysis_dir = project_root / "analysis"
    parser = INSTATExcelParser()
    
    if not analysis_dir.exists():
        logger.error(f"Analysis directory not found: {analysis_dir}")
        return
    
    # Find Excel files in analysis directory
    excel_files = list(analysis_dir.glob("*.xlsx")) + list(analysis_dir.glob("*.xls"))
    
    if not excel_files:
        logger.warning("No Excel files found in analysis directory")
        return
    
    logger.info(f"Found {len(excel_files)} Excel files to process")
    
    # Process each Excel file
    for file_path in excel_files:
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {file_path.name}")
        logger.info(f"{'='*80}")
        
        try:
            # Parse the file
            survey_structure = parser.parse_file(file_path)
            validation_issues = parser.validate_structure(survey_structure)
            
            # Show parsing results
            logger.info(f"Parsed survey: {survey_structure.get('title', 'Unknown')}")
            logger.info(f"Sections found: {len(survey_structure.get('sections', []))}")
            
            # Count total questions
            total_questions = 0
            for section in survey_structure.get("sections", []):
                total_questions += len(section.get("questions", []))
                for subsection in section.get("subsections", []):
                    total_questions += len(subsection.get("questions", []))
            
            logger.info(f"Total questions found: {total_questions}")
            
            # Extract table references
            table_refs = parser.extract_table_references(survey_structure)
            if table_refs:
                logger.info(f"Table references found: {table_refs}")
            
            if validation_issues:
                logger.warning(f"Validation issues: {validation_issues}")
                
                # If there are no questions, skip creating the survey
                if total_questions == 0:
                    logger.warning("Skipping survey creation - no questions found")
                    continue
            
            # Determine schema name
            schema_name = determine_schema_name(file_path.name)
            logger.info(f"Using schema: {schema_name}")
            
            # Convert to schema format
            sections = convert_sections_to_schema(survey_structure.get("sections", []))
            
            if not sections:
                logger.warning("No valid sections to create - skipping")
                continue
            
            # Create survey data
            survey_data = survey_schema.SurveyCreate(
                Title=survey_structure.get("title", file_path.stem),
                Description=survey_structure.get("description", f"Auto-generated survey from {file_path.name}"),
                Status="Draft",
                Sections=sections
            )
            
            # Create the survey in the database
            session = db_manager.SessionLocal()
            try:
                created_survey = survey_service.create_survey(
                    db=session, 
                    survey=survey_data, 
                    schema_name=schema_name
                )
                
                logger.info(f"✅ Successfully created survey:")
                logger.info(f"   - ID: {created_survey.SurveyID}")
                logger.info(f"   - Title: {created_survey.Title}")
                logger.info(f"   - Sections: {len(sections)}")
                logger.info(f"   - Questions: {total_questions}")
                
                # Save detailed structure to JSON for review
                output_dir = project_root / "generated"
                output_dir.mkdir(exist_ok=True)
                
                structure_file = output_dir / f"{file_path.stem}_structure.json"
                with open(structure_file, 'w', encoding='utf-8') as f:
                    json.dump(survey_structure, f, indent=2, ensure_ascii=False, default=str)
                
                logger.info(f"   - Structure saved to: {structure_file}")
                
                session.commit()
                
            except Exception as db_error:
                session.rollback()
                logger.error(f"❌ Failed to create survey in database: {db_error}")
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"❌ Error processing {file_path.name}: {e}")
            import traceback
            logger.debug(traceback.format_exc())


def list_analysis_files():
    """List all files in the analysis directory"""
    analysis_dir = project_root / "analysis"
    
    if not analysis_dir.exists():
        logger.error(f"Analysis directory not found: {analysis_dir}")
        return
    
    files = list(analysis_dir.iterdir())
    
    print(f"\n📁 Files in analysis directory ({len(files)} total):")
    print("="*80)
    
    for file_path in sorted(files):
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            file_type = "📊 Excel" if file_path.suffix.lower() in ['.xlsx', '.xls'] else "📄 Document"
            print(f"{file_type:<10} {file_path.name:<60} ({size_mb:.1f} MB)")


def test_single_file(filename):
    """Test parsing a single file"""
    analysis_dir = project_root / "analysis"
    file_path = analysis_dir / filename
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return
    
    logger.info(f"Testing single file: {filename}")
    
    parser = INSTATExcelParser()
    try:
        survey_structure = parser.parse_file(file_path)
        validation_issues = parser.validate_structure(survey_structure)
        
        print(f"\n📊 Parsing Results for {filename}")
        print("="*80)
        print(f"Title: {survey_structure.get('title', 'Unknown')}")
        print(f"Description: {survey_structure.get('description', 'None')}")
        print(f"Sections: {len(survey_structure.get('sections', []))}")
        
        total_questions = 0
        for i, section in enumerate(survey_structure.get("sections", [])):
            section_questions = len(section.get("questions", []))
            subsection_questions = sum(len(sub.get("questions", [])) for sub in section.get("subsections", []))
            total_section_questions = section_questions + subsection_questions
            total_questions += total_section_questions
            
            print(f"  Section {i+1}: {section.get('title', 'Untitled')} ({total_section_questions} questions)")
            for j, subsection in enumerate(section.get("subsections", [])):
                print(f"    Subsection {j+1}: {subsection.get('title', 'Untitled')} ({len(subsection.get('questions', []))} questions)")
        
        print(f"Total Questions: {total_questions}")
        
        if validation_issues:
            print(f"\n⚠️  Validation Issues:")
            for issue in validation_issues:
                print(f"  - {issue}")
        else:
            print(f"\n✅ No validation issues found")
        
        # Show table references
        table_refs = parser.extract_table_references(survey_structure)
        if table_refs:
            print(f"\n🔗 Table References Found: {table_refs}")
        
        # Show sample questions
        print(f"\n📝 Sample Questions (first 5):")
        question_count = 0
        for section in survey_structure.get("sections", []):
            for question in section.get("questions", []):
                if question_count < 5:
                    print(f"  Q{question_count+1}: {question.get('text', 'No text')[:100]}...")
                    if question.get('options'):
                        print(f"      Options: {len(question['options'])} choices")
                    question_count += 1
            for subsection in section.get("subsections", []):
                for question in subsection.get("questions", []):
                    if question_count < 5:
                        print(f"  Q{question_count+1}: {question.get('text', 'No text')[:100]}...")
                        if question.get('options'):
                            print(f"      Options: {len(question['options'])} choices")
                        question_count += 1
        
    except Exception as e:
        logger.error(f"Error testing file {filename}: {e}")
        import traceback
        logger.debug(traceback.format_exc())


if __name__ == "__main__":
    print("🚀 INSTAT Survey Auto-Generation Tool")
    print("="*80)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_analysis_files()
        elif command == "test" and len(sys.argv) > 2:
            test_single_file(sys.argv[2])
        elif command == "generate":
            auto_generate_surveys()
        else:
            print("Usage:")
            print("  python scripts/auto_generate_surveys.py list        # List analysis files")
            print("  python scripts/auto_generate_surveys.py test <file> # Test single file")
            print("  python scripts/auto_generate_surveys.py generate    # Generate all surveys")
    else:
        print("Usage:")
        print("  python scripts/auto_generate_surveys.py list        # List analysis files")
        print("  python scripts/auto_generate_surveys.py test <file> # Test single file")
        print("  python scripts/auto_generate_surveys.py generate    # Generate all surveys")
        print()
        print("Available commands:")
        print("  list     - Show all files in the analysis directory")
        print("  test     - Test parsing of a specific file")
        print("  generate - Auto-generate surveys from all Excel files")
