#!/usr/bin/env python3
"""
Debug script to see what the parser is actually creating
"""
import sys
import os
from pathlib import Path
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.excel_parser import ExcelParser

def debug_parser_output():
    """Debug what the parser creates"""
    file_path = Path("analysis/MODELISATION_FICHIER_DIAGNOSTIC_SSN_SDS4_DEVELOPPEMENT_V1.0.0.xlsx")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    parser = ExcelParser()
    
    try:
        print("🔍 Parsing Excel file...")
        survey_structure = parser.parse_file(file_path)
        
        print(f"\n📊 Survey Structure:")
        print(f"   Title: {survey_structure.get('title')}")
        print(f"   Description: {survey_structure.get('description')}")
        print(f"   Total sections: {len(survey_structure.get('sections', []))}")
        
        for i, section in enumerate(survey_structure.get('sections', []), 1):
            print(f"\n📄 Section {i}: '{section.get('title')}'")
            print(f"   Direct questions: {len(section.get('questions', []))}")
            print(f"   Subsections: {len(section.get('subsections', []))}")
            
            # Show first few questions
            for j, question in enumerate(section.get('questions', [])[:3], 1):
                print(f"   Q{j}: {question.get('text', '')[:80]}")
            
            # Show subsections
            for j, subsection in enumerate(section.get('subsections', [])[:3], 1):
                print(f"   Sub {j}: '{subsection.get('title')}' ({len(subsection.get('questions', []))} questions)")
                for k, question in enumerate(subsection.get('questions', [])[:2], 1):
                    print(f"      Q{k}: {question.get('text', '')[:60]}")
        
        print(f"\n🔍 Validation Issues:")
        validation_issues = parser.validate_structure(survey_structure)
        for issue in validation_issues:
            print(f"   ❌ {issue}")
        
        if not validation_issues:
            print("   ✅ No validation issues!")
            
        # Show extracted table references
        table_refs = parser.extract_table_references(survey_structure)
        if table_refs:
            print(f"\n📋 Table References Found: {table_refs}")
        
    except Exception as e:
        print(f"❌ Parser error: {e}")

if __name__ == "__main__":
    debug_parser_output()
