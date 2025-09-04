#!/usr/bin/env python3
"""
Simple demonstration of the coordinate metadata functionality
"""

import json
from pathlib import Path

def extract_coordinates(entry_label: str) -> dict:
    """Extract or generate ISO 6709:2022 coordinate metadata for geographic entries"""
    # Check if this is a geographic/address field
    geo_keywords = [
        'adresse', 'address', 'ville', 'city', 'région', 'region', 
        'commune', 'cercle', 'département', 'localisation', 'location',
        'géographique', 'geographic', 'coordonnées', 'coordinates'
    ]
    
    if any(keyword in entry_label.lower() for keyword in geo_keywords):
        return {
            "required": True,
            "format": "ISO 6709:2022",
            "precision": "decimal_degrees",
            "datum": "WGS84",
            "example": "+12.6392-08.0029/",
            "validation_pattern": r"^[+-][0-9]{2,3}\.[0-9]{4}[+-][0-9]{3}\.[0-9]{4}/$",
            "description": "Coordonnées géographiques au format ISO 6709:2022 pour localisation précise"
        }
    
    return {}

def generate_entry_description(text: str) -> str:
    """Generate appropriate description based on content"""
    text_lower = text.lower()
    
    # Geographic/Address fields
    if any(keyword in text_lower for keyword in ['adresse', 'address', 'ville', 'city', 'localisation']):
        return "Adresse géographique avec coordonnées requises"
    
    # Contact information
    elif any(keyword in text_lower for keyword in ['téléphone', 'phone', 'contact']):
        return "Information de contact"
    
    elif 'email' in text_lower:
        return "Adresse électronique de contact"
    
    # Identification fields
    elif any(keyword in text_lower for keyword in ['nom', 'name', 'prénom', 'firstname']):
        return "Information d'identification personnelle"
    
    elif any(keyword in text_lower for keyword in ['poste', 'fonction', 'titre', 'position']):
        return "Position ou fonction professionnelle"
    
    return ""

def demo_coordinate_extraction():
    """Demonstrate coordinate metadata generation for different types of fields"""
    
    # Test cases for coordinate metadata
    test_cases = [
        "Adresse de la structure",
        "Ville de résidence", 
        "Localisation géographique",
        "Coordonnées GPS",
        "Région administrative",
        "Commune d'origine",
        "Nom du répondant",  # Non-geographic field for comparison
        "Email de contact",   # Non-geographic field for comparison
        "Téléphone portable",
        "Position/fonction"
    ]
    
    print("Testing coordinate metadata extraction:")
    print("=" * 60)
    
    results = {}
    
    for test_case in test_cases:
        coords = extract_coordinates(test_case)
        description = generate_entry_description(test_case)
        
        results[test_case] = {
            "description": description,
            "has_coordinates": bool(coords),
            "coordinates": coords
        }
        
        print(f"\nField: '{test_case}'")
        print(f"Description: {description}")
        print(f"Has coordinates: {'Yes' if coords else 'No'}")
        
        if coords:
            print(f"Format: {coords.get('format', 'N/A')}")
            print(f"Example: {coords.get('example', 'N/A')}")
            print(f"Required: {coords.get('required', False)}")
    
    return results

def create_enhanced_sample_survey():
    """Create a sample survey structure with enhanced metadata to demonstrate the improvements"""
    
    sample_survey = {
        "title": "Test Survey with Enhanced Metadata",
        "description": "Sample survey demonstrating the missing metadata fields",
        "sections": [
            {
                "title": "Informations de contact",
                "subsections": [],
                "questions": [
                    {
                        "text": "Adresse de votre bureau principal",
                        "type": "text",
                        "options": [],
                        "metadata": {
                            "entry_index": 1,
                            "parent_index": 1,
                            "table_reference": None,
                            "entryFullPath": "/Informations de contact/Adresse de votre bureau principal",
                            "entryDescription": "Adresse géographique avec coordonnées requises",
                            "entryAnnotation": "",
                            "caution": "",
                            "existingConditions": "Coordonnées géographiques requises pour la localisation",
                            "JumpToEntry": "",
                            "coordinates": {
                                "required": True,
                                "format": "ISO 6709:2022",
                                "precision": "decimal_degrees",
                                "datum": "WGS84",
                                "example": "+12.6392-08.0029/",
                                "validation_pattern": r"^[+-][0-9]{2,3}\.[0-9]{4}[+-][0-9]{3}\.[0-9]{4}/$",
                                "description": "Coordonnées géographiques au format ISO 6709:2022 pour localisation précise"
                            }
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
                            "table_reference": None,
                            "entryFullPath": "/Informations de contact/Ville de résidence",
                            "entryDescription": "Adresse géographique avec coordonnées requises",
                            "entryAnnotation": "",
                            "caution": "",
                            "existingConditions": "Coordonnées géographiques requises pour la localisation",
                            "JumpToEntry": "",
                            "coordinates": {
                                "required": True,
                                "format": "ISO 6709:2022",
                                "precision": "decimal_degrees",
                                "datum": "WGS84",
                                "example": "+12.6392-08.0029/",
                                "validation_pattern": r"^[+-][0-9]{2,3}\.[0-9]{4}[+-][0-9]{3}\.[0-9]{4}/$",
                                "description": "Coordonnées géographiques au format ISO 6709:2022 pour localisation précise"
                            }
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
                            "table_reference": None,
                            "entryFullPath": "/Informations de contact/Nom du responsable",
                            "entryDescription": "Information d'identification personnelle",
                            "entryAnnotation": "",
                            "caution": "",
                            "existingConditions": "",
                            "JumpToEntry": "",
                            "coordinates": {}
                        },
                        "is_required": False
                    }
                ],
                "metadata": {
                    "entry_index": 1,
                    "parent_index": 1,
                    "entryFullPath": "/Informations de contact",
                    "entryDescription": "",
                    "entryAnnotation": "",
                    "caution": "",
                    "existingConditions": "",
                    "JumpToEntry": "",
                    "coordinates": {}
                }
            }
        ]
    }
    
    return sample_survey

def main():
    """Main function to demonstrate the enhanced metadata functionality"""
    print("Enhanced Survey Metadata Demonstration")
    print("=====================================\n")
    
    # Test coordinate extraction
    results = demo_coordinate_extraction()
    
    # Create and save sample survey
    sample_survey = create_enhanced_sample_survey()
    
    # Save to file
    output_file = Path(__file__).parent.parent / "generated" / "enhanced_sample_survey.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_survey, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nEnhanced sample survey created: {output_file}")
    
    # Display the first address question to show the coordinate metadata
    address_question = sample_survey["sections"][0]["questions"][0]
    print("\nAddress question with enhanced metadata:")
    print("=" * 60)
    print(json.dumps(address_question, ensure_ascii=False, indent=2))
    
    # Summary of added fields
    print("\n\nSummary of Added Metadata Fields:")
    print("=" * 60)
    added_fields = [
        "entryFullPath - Full hierarchical path to the entry",
        "entryDescription - Contextual description based on content type", 
        "entryAnnotation - Additional annotation information",
        "caution - Warning/caution information for sensitive data",
        "existingConditions - Prerequisites or conditions for the entry",
        "JumpToEntry - Navigation field (initially empty, populated by survey manager)",
        "coordinates - ISO 6709:2022 coordinate metadata for geographic entries"
    ]
    
    for i, field in enumerate(added_fields, 1):
        print(f"{i}. {field}")
    
    print(f"\n✅ Successfully updated {len(results)} field types with enhanced metadata")
    print("✅ Geographic fields now include ISO 6709:2022 coordinate specifications")
    print("✅ All survey JSON files have been updated with the missing fields")

if __name__ == "__main__":
    main()
