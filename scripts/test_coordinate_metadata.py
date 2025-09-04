#!/usr/bin/env python3
"""
Test script to demonstrate the coordinate functionality for address fields
"""

import json
import sys
from pathlib import Path

# Add src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.instat_excel_parser import INSTATExcelParser

def test_coordinate_extraction():
    """Test coordinate metadata generation for different types of fields"""
    
    parser = INSTATExcelParser()
    
    # Test cases for coordinate metadata
    test_cases = [
        "Adresse de la structure",
        "Ville de résidence",
        "Localisation géographique",
        "Coordonnées GPS",
        "Région administrative",
        "Commune d'origine",
        "Nom du répondant",  # Non-geographic field for comparison
        "Email de contact"   # Non-geographic field for comparison
    ]
    
    print("Testing coordinate metadata extraction:")
    print("=" * 60)
    
    for test_case in test_cases:
        coords = parser._extract_coordinates(test_case)
        description = parser._extract_entry_description(None, test_case)  # Pass None for row since we don't have one
        
        print(f"\nField: '{test_case}'")
        print(f"Description: {description}")
        print(f"Has coordinates: {'Yes' if coords else 'No'}")
        
        if coords:
            print(f"Format: {coords.get('format', 'N/A')}")
            print(f"Example: {coords.get('example', 'N/A')}")
            print(f"Required: {coords.get('required', False)}")

def create_sample_survey_with_addresses():
    """Create a sample survey structure with address fields to test the complete functionality"""
    
    sample_survey = {
        "title": "Test Survey with Address Fields",
        "description": "Sample survey demonstrating coordinate metadata",
        "sections": [
            {
                "title": "Informations géographiques",
                "subsections": [],
                "questions": [
                    {
                        "text": "Adresse de votre bureau principal",
                        "type": "text",
                        "options": [],
                        "metadata": {
                            "entry_index": 1,
                            "parent_index": 1,
                            "table_reference": None
                        },
                        "is_required": True
                    },
                    {
                        "text": "Ville de résidence",
                        "type": "text", 
                        "options": [],
                        "metadata": {
                            "entry_index": 2,
                            "parent_index": 1,
                            "table_reference": None
                        },
                        "is_required": False
                    },
                    {
                        "text": "Nom du responsable",
                        "type": "text",
                        "options": [],
                        "metadata": {
                            "entry_index": 3,
                            "parent_index": 1,
                            "table_reference": None
                        },
                        "is_required": False
                    }
                ],
                "metadata": {
                    "entry_index": 1,
                    "parent_index": 1
                }
            }
        ]
    }
    
    # Update with metadata using our updater
    sys.path.insert(0, str(Path(__file__).parent))
    from update_survey_metadata import SurveyMetadataUpdater
    
    updater = SurveyMetadataUpdater()
    updated_survey = updater._update_survey_structure(sample_survey)
    
    # Save to file
    output_file = Path(__file__).parent.parent / "generated" / "sample_address_survey.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_survey, f, ensure_ascii=False, indent=2)
    
    print(f"\nSample survey with address metadata created: {output_file}")
    
    # Display the first address question to show the coordinate metadata
    address_question = updated_survey["sections"][0]["questions"][0]
    print("\nAddress question metadata:")
    print(json.dumps(address_question["metadata"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_coordinate_extraction()
    create_sample_survey_with_addresses()
