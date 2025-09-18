#!/usr/bin/env python3
"""
Fix empty existingConditions fields in survey structures
Replaces empty existingConditions with "Réponse conditionnelle basée sur une question précédente"
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_CONDITIONS = "Réponse conditionnelle basée sur une question précédente"

def fix_metadata_conditions(metadata: Dict[str, Any]) -> bool:
    """Fix existingConditions in metadata if empty or missing"""
    changed = False
    
    if "existingConditions" not in metadata or not metadata["existingConditions"]:
        metadata["existingConditions"] = DEFAULT_CONDITIONS
        changed = True
    
    return changed

def fix_section_conditions(section: Dict[str, Any]) -> bool:
    """Fix existingConditions in a section and its contents"""
    changed = False
    
    # Fix section metadata
    if "metadata" in section:
        if fix_metadata_conditions(section["metadata"]):
            changed = True
    
    # Fix questions in section
    for question in section.get("questions", []):
        if "metadata" in question:
            if fix_metadata_conditions(question["metadata"]):
                changed = True
        
        # Fix options in question
        for option in question.get("options", []):
            if "metadata" in option:
                if fix_metadata_conditions(option["metadata"]):
                    changed = True
    
    # Fix subsections
    for subsection in section.get("subsections", []):
        if "metadata" in subsection:
            if fix_metadata_conditions(subsection["metadata"]):
                changed = True
        
        # Fix questions in subsection
        for question in subsection.get("questions", []):
            if "metadata" in question:
                if fix_metadata_conditions(question["metadata"]):
                    changed = True
            
            # Fix options in subsection question
            for option in question.get("options", []):
                if "metadata" in option:
                    if fix_metadata_conditions(option["metadata"]):
                        changed = True
    
    return changed

def fix_survey_conditions(survey_data: Dict[str, Any]) -> bool:
    """Fix empty existingConditions in survey structure"""
    changed = False
    
    # Process each section
    for section in survey_data.get("sections", []):
        if fix_section_conditions(section):
            changed = True
    
    return changed

def process_json_file(file_path: Path) -> bool:
    """Process a single JSON file and fix empty existingConditions"""
    try:
        logger.info(f"Processing file: {file_path}")
        
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            survey_data = json.load(f)
        
        # Fix empty existingConditions
        changed = fix_survey_conditions(survey_data)
        
        if changed:
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(survey_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Updated existingConditions in {file_path.name}")
        else:
            logger.info(f"ℹ️  No changes needed for {file_path.name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all survey JSON files"""
    # Set up paths
    project_root = Path(__file__).parent.parent
    generated_dir = project_root / "generated"
    
    if not generated_dir.exists():
        logger.error(f"Generated directory not found: {generated_dir}")
        return
    
    # Find all JSON structure files
    json_files = list(generated_dir.glob("*_structure.json"))
    
    if not json_files:
        logger.warning("No survey JSON files found to process")
        return
    
    logger.info(f"Found {len(json_files)} JSON files to process")
    
    # Process each file
    successful = 0
    failed = 0
    
    for json_file in json_files:
        if process_json_file(json_file):
            successful += 1
        else:
            failed += 1
    
    logger.info(f"Processing complete: {successful} successful, {failed} failed")
    logger.info(f"All empty existingConditions replaced with: '{DEFAULT_CONDITIONS}'")

if __name__ == "__main__":
    main()
