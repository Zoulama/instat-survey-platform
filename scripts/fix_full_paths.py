#!/usr/bin/env python3
"""
Script to fix incorrect entryFullPath values in survey structure JSON files.

Issues to fix:
1. Truncated paths ending with "..."
2. Inconsistent context section paths
3. Missing proper hierarchy in paths
4. Long text truncation making paths unclear
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
import re


def fix_full_path(path: str, max_segment_length: int = 80) -> str:
    """
    Fix a full path by removing truncation and ensuring proper formatting.
    
    Args:
        path: The current path (potentially truncated)
        max_segment_length: Maximum length for each path segment
    
    Returns:
        Fixed path string
    """
    # Remove truncation indicators
    path = path.replace("...", "")
    
    # Split path into segments
    segments = [seg.strip() for seg in path.split("/") if seg.strip()]
    
    # Clean up each segment
    cleaned_segments = []
    for segment in segments:
        # Remove common truncation artifacts
        segment = re.sub(r'\s+', ' ', segment.strip())
        
        # Truncate cleanly if too long (but keep meaningful text)
        if len(segment) > max_segment_length:
            # Try to break at word boundary
            truncated = segment[:max_segment_length]
            last_space = truncated.rfind(' ')
            if last_space > max_segment_length * 0.7:  # If we can break at a reasonable point
                segment = truncated[:last_space]
            else:
                segment = truncated
        
        cleaned_segments.append(segment)
    
    # Rebuild path
    return "/" + "/".join(cleaned_segments)


def build_proper_path(section_title: str, subsection_title: str = None, 
                     question_text: str = None, option_text: str = None) -> str:
    """
    Build a proper hierarchical path.
    
    Args:
        section_title: Title of the section
        subsection_title: Title of subsection (optional)
        question_text: Text of the question (optional)
        option_text: Text of the option (optional)
    
    Returns:
        Properly formatted hierarchical path
    """
    path_parts = []
    
    if section_title:
        path_parts.append(section_title.strip())
    
    if subsection_title:
        path_parts.append(subsection_title.strip())
        
    if question_text:
        # Truncate question text smartly
        q_text = question_text.strip()
        if len(q_text) > 60:
            # Find a good break point
            truncated = q_text[:60]
            last_space = truncated.rfind(' ')
            last_punct = max(truncated.rfind('.'), truncated.rfind('?'), truncated.rfind('!'))
            
            if last_punct > 40:  # Break at punctuation if reasonable
                q_text = q_text[:last_punct + 1]
            elif last_space > 40:  # Break at word boundary
                q_text = truncated[:last_space]
            else:
                q_text = truncated
        
        path_parts.append(q_text)
    
    if option_text:
        path_parts.append(option_text.strip())
    
    return "/" + "/".join(path_parts)


def fix_question_paths(questions: List[Dict], section_title: str, subsection_title: str = None):
    """Fix paths for questions and their options."""
    for question in questions:
        if "metadata" in question and "entryFullPath" in question["metadata"]:
            # Build proper question path
            proper_path = build_proper_path(
                section_title, 
                subsection_title, 
                question.get("text", "")
            )
            question["metadata"]["entryFullPath"] = proper_path
        
        # Fix option paths
        for option in question.get("options", []):
            if "metadata" in option and "entryFullPath" in option["metadata"]:
                proper_path = build_proper_path(
                    section_title,
                    subsection_title,
                    question.get("text", ""),
                    option.get("text", "")
                )
                option["metadata"]["entryFullPath"] = proper_path


def fix_survey_structure(survey_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fix all entryFullPath values in a survey structure.
    
    Args:
        survey_data: The survey structure dictionary
        
    Returns:
        Fixed survey structure
    """
    print(f"Fixing paths for survey: {survey_data.get('title', 'Unknown')}")
    
    sections = survey_data.get("sections", [])
    
    for section in sections:
        section_title = section.get("title", "")
        
        # Fix section path
        if "metadata" in section and "entryFullPath" in section["metadata"]:
            section["metadata"]["entryFullPath"] = f"/{section_title}"
        
        # Fix section questions
        fix_question_paths(section.get("questions", []), section_title)
        
        # Fix subsections
        for subsection in section.get("subsections", []):
            subsection_title = subsection.get("title", "")
            
            # Fix subsection path
            if "metadata" in subsection and "entryFullPath" in subsection["metadata"]:
                subsection["metadata"]["entryFullPath"] = f"/{section_title}/{subsection_title}"
            
            # Fix subsection questions
            fix_question_paths(subsection.get("questions", []), section_title, subsection_title)
    
    return survey_data


def process_json_file(file_path: Path) -> bool:
    """
    Process a single JSON file to fix paths.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nProcessing: {file_path.name}")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Fix the structure
        fixed_data = fix_survey_structure(data)
        
        # Create backup
        backup_path = file_path.with_suffix('.json.backup')
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Created backup: {backup_path.name}")
        
        # Write fixed data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Fixed paths in: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function to fix all JSON structure files."""
    
    # Find all JSON files in the generated directory
    base_dir = Path("/Users/sileymanedjimera/workplace/trainings/poc/instat-survey-platform")
    generated_dir = base_dir / "generated"
    
    if not generated_dir.exists():
        print(f"Generated directory not found: {generated_dir}")
        return
    
    # Find all structure JSON files
    json_files = list(generated_dir.glob("*_structure.json"))
    
    if not json_files:
        print("No structure JSON files found to process")
        return
    
    print(f"Found {len(json_files)} JSON structure files to process")
    
    success_count = 0
    for json_file in json_files:
        if process_json_file(json_file):
            success_count += 1
    
    print(f"\n✓ Successfully processed {success_count}/{len(json_files)} files")
    
    if success_count > 0:
        print("\nPath fixing completed! The following issues were addressed:")
        print("  • Removed truncated paths ending with '...'")
        print("  • Fixed inconsistent context section paths")
        print("  • Rebuilt proper hierarchical paths")
        print("  • Improved path readability while maintaining structure")
        print("\nBackup files (.json.backup) were created for safety.")


if __name__ == "__main__":
    main()
