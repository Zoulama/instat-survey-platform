#!/usr/bin/env python3
"""
Script to update existing survey JSON files with missing metadata fields
Adds: entryFullPath, entryDescription, entryAnnotation, caution, existingConditions, JumpToEntry, coordinates
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SurveyMetadataUpdater:
    """Updates existing survey JSON files with enhanced metadata"""
    
    def __init__(self):
        self.geo_keywords = [
            'adresse', 'address', 'ville', 'city', 'région', 'region', 
            'commune', 'cercle', 'département', 'localisation', 'location',
            'géographique', 'geographic', 'coordonnées', 'coordinates'
        ]
        
    def update_survey_file(self, file_path: Path) -> bool:
        """Update a single survey JSON file with enhanced metadata"""
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Read the existing JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                survey_data = json.load(f)
            
            # Update the survey structure
            updated_data = self._update_survey_structure(survey_data)
            
            # Write the updated JSON back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Successfully updated: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating {file_path}: {e}")
            return False
    
    def _update_survey_structure(self, survey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the survey structure with enhanced metadata"""
        
        # Process each section
        for section in survey_data.get("sections", []):
            self._update_section_metadata(section, survey_data.get("title", ""))
            
            # Process questions in the section
            for question in section.get("questions", []):
                self._update_question_metadata(question, section)
                
                # Process options in the question
                for option in question.get("options", []):
                    self._update_option_metadata(option, section, question)
            
            # Process subsections
            for subsection in section.get("subsections", []):
                self._update_subsection_metadata(subsection, section)
                
                # Process questions in the subsection
                for question in subsection.get("questions", []):
                    self._update_question_metadata(question, section, subsection)
                    
                    # Process options in the question
                    for option in question.get("options", []):
                        self._update_option_metadata(option, section, question, subsection)
        
        return survey_data
    
    def _update_section_metadata(self, section: Dict[str, Any], survey_title: str) -> None:
        """Update section metadata with missing fields"""
        if "metadata" not in section:
            section["metadata"] = {}
        
        metadata = section["metadata"]
        title = section.get("title", "")
        
        # Add missing fields if they don't exist
        if "entryFullPath" not in metadata:
            metadata["entryFullPath"] = f"/{title}"
        
        if "entryDescription" not in metadata:
            metadata["entryDescription"] = self._generate_entry_description(title, "section")
        
        if "entryAnnotation" not in metadata:
            metadata["entryAnnotation"] = self._generate_entry_annotation(title, "section")
        
        if "caution" not in metadata:
            metadata["caution"] = self._generate_caution_info(title)
        
        if "existingConditions" not in metadata:
            metadata["existingConditions"] = self._generate_existing_conditions(title)
        
        if "JumpToEntry" not in metadata:
            metadata["JumpToEntry"] = ""
        
        if "coordinates" not in metadata:
            metadata["coordinates"] = self._generate_coordinates(title)
    
    def _update_subsection_metadata(self, subsection: Dict[str, Any], parent_section: Dict[str, Any]) -> None:
        """Update subsection metadata with missing fields"""
        if "metadata" not in subsection:
            subsection["metadata"] = {}
        
        metadata = subsection["metadata"]
        title = subsection.get("title", "")
        parent_title = parent_section.get("title", "")
        
        # Add missing fields if they don't exist
        if "entryFullPath" not in metadata:
            metadata["entryFullPath"] = f"/{parent_title}/{title}"
        
        if "entryDescription" not in metadata:
            metadata["entryDescription"] = self._generate_entry_description(title, "subsection")
        
        if "entryAnnotation" not in metadata:
            metadata["entryAnnotation"] = self._generate_entry_annotation(title, "subsection")
        
        if "caution" not in metadata:
            metadata["caution"] = self._generate_caution_info(title)
        
        if "existingConditions" not in metadata:
            metadata["existingConditions"] = self._generate_existing_conditions(title)
        
        if "JumpToEntry" not in metadata:
            metadata["JumpToEntry"] = ""
        
        if "coordinates" not in metadata:
            metadata["coordinates"] = self._generate_coordinates(title)
    
    def _update_question_metadata(self, question: Dict[str, Any], parent_section: Dict[str, Any], 
                                 parent_subsection: Optional[Dict[str, Any]] = None) -> None:
        """Update question metadata with missing fields"""
        if "metadata" not in question:
            question["metadata"] = {}
        
        metadata = question["metadata"]
        text = question.get("text", "")
        section_title = parent_section.get("title", "")
        
        # Build full path
        path_parts = [section_title]
        if parent_subsection:
            path_parts.append(parent_subsection.get("title", ""))
        path_parts.append(text[:50] + ("..." if len(text) > 50 else ""))
        
        # Add missing fields if they don't exist
        if "entryFullPath" not in metadata:
            metadata["entryFullPath"] = "/" + "/".join(path_parts)
        
        if "entryDescription" not in metadata:
            metadata["entryDescription"] = self._generate_entry_description(text, "question")
        
        if "entryAnnotation" not in metadata:
            metadata["entryAnnotation"] = self._generate_entry_annotation(text, "question")
        
        if "caution" not in metadata:
            metadata["caution"] = self._generate_caution_info(text)
        
        if "existingConditions" not in metadata:
            metadata["existingConditions"] = self._generate_existing_conditions(text)
        
        if "JumpToEntry" not in metadata:
            metadata["JumpToEntry"] = ""
        
        if "coordinates" not in metadata:
            metadata["coordinates"] = self._generate_coordinates(text)
    
    def _update_option_metadata(self, option: Dict[str, Any], parent_section: Dict[str, Any], 
                               parent_question: Dict[str, Any], parent_subsection: Optional[Dict[str, Any]] = None) -> None:
        """Update option metadata with missing fields"""
        if "metadata" not in option:
            option["metadata"] = {}
        
        metadata = option["metadata"]
        text = option.get("text", "")
        section_title = parent_section.get("title", "")
        question_text = parent_question.get("text", "")[:30] + "..."
        
        # Build full path
        path_parts = [section_title]
        if parent_subsection:
            path_parts.append(parent_subsection.get("title", ""))
        path_parts.extend([question_text, text])
        
        # Add missing fields if they don't exist
        if "entryFullPath" not in metadata:
            metadata["entryFullPath"] = "/" + "/".join(path_parts)
        
        if "entryDescription" not in metadata:
            metadata["entryDescription"] = self._generate_entry_description(text, "option")
        
        if "entryAnnotation" not in metadata:
            metadata["entryAnnotation"] = self._generate_entry_annotation(text, "option")
        
        if "caution" not in metadata:
            metadata["caution"] = self._generate_caution_info(text)
        
        if "existingConditions" not in metadata:
            metadata["existingConditions"] = self._generate_existing_conditions(text)
        
        if "JumpToEntry" not in metadata:
            metadata["JumpToEntry"] = ""
        
        if "coordinates" not in metadata:
            metadata["coordinates"] = self._generate_coordinates(text)
    
    def _generate_entry_description(self, text: str, entry_type: str) -> str:
        """Generate appropriate description based on content and type"""
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
        
        # Context sections
        elif entry_type == "section" and "context" in text_lower:
            return "Section contextuelle contenant des informations de base"
        
        # Questions with table references
        elif "@TableRef" in text or "table de référence" in text_lower:
            return "Question avec référence à une table de données externe"
        
        # Required fields
        elif any(indicator in text_lower for indicator in ['obligatoire', 'requis', '*']):
            return "Champ obligatoire à remplir"
        
        return ""
    
    def _generate_entry_annotation(self, text: str, entry_type: str) -> str:
        """Generate appropriate annotation based on content and type"""
        text_lower = text.lower()
        
        # Table references
        if "@TableRef" in text or "tableau" in text_lower:
            return "Référence à une table de données externe"
        
        # Required fields
        elif any(indicator in text_lower for indicator in ['obligatoire', 'requis', '*']):
            return "Champ obligatoire à remplir"
        
        # Conditional questions
        elif any(word in text_lower for word in ['si', 'dépend', 'conditionnelle']):
            return "Question conditionnelle basée sur une réponse précédente"
        
        # Multiple choice
        elif any(word in text_lower for word in ['sélectionner', 'choisir', 'cocher']):
            return "Sélection parmi les options proposées"
        
        return ""
    
    def _generate_caution_info(self, text: str) -> str:
        """Generate caution information for sensitive or important fields"""
        text_lower = text.lower()
        
        # Sensitive data
        sensitive_keywords = ['confidentiel', 'personnel', 'privé', 'sensible', 'secret']
        if any(keyword in text_lower for keyword in sensitive_keywords):
            return "Information sensible - manipuler avec précaution"
        
        # Financial data
        elif any(keyword in text_lower for keyword in ['montant', 'budget', 'coût', 'financement', 'euros', 'fcfa']):
            return "Information financière - vérifier la précision"
        
        # Dates and deadlines
        elif any(keyword in text_lower for keyword in ['date', 'délai', 'échéance']):
            return "Vérifier la validité des dates saisies"
        
        return ""
    
    def _generate_existing_conditions(self, text: str) -> str:
        """Generate existing conditions for the entry"""
        text_lower = text.lower()
        
        # Conditional dependencies
        if any(word in text_lower for word in ['si', 'dépend', 'selon', 'en fonction']):
            return "Réponse conditionnelle basée sur une question précédente"
        
        # Table references
        elif "@TableRef" in text or "table de référence" in text_lower:
            return "Nécessite l'accès à une table de référence externe"
        
        # Required fields
        elif any(indicator in text_lower for indicator in ['obligatoire', 'requis', 'nécessaire']):
            return "Champ obligatoire - ne peut être vide"
        
        # Geographic fields
        elif any(keyword in text_lower for keyword in self.geo_keywords):
            return "Coordonnées géographiques requises pour la localisation"
        
        return ""
    
    def _generate_coordinates(self, text: str) -> dict:
        """Generate coordinate metadata for geographic entries"""
        text_lower = text.lower()
        
        # Check if this is a geographic/address field
        if any(keyword in text_lower for keyword in self.geo_keywords):
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
    
    # Initialize the updater
    updater = SurveyMetadataUpdater()
    
    # Process each file
    successful = 0
    failed = 0
    
    for json_file in json_files:
        if updater.update_survey_file(json_file):
            successful += 1
        else:
            failed += 1
    
    logger.info(f"Processing complete: {successful} successful, {failed} failed")


if __name__ == "__main__":
    main()
