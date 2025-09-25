"""
Enhanced Excel parser for INSTAT structured survey files
Handles the specific format used in MODELISATION files with hierarchical survey structure
"""
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)


class INSTATExcelParser:
    """Parse INSTAT Excel files with structured survey data"""

    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
        self.entry_types = {
            'Survey': 'survey',
            'Context': 'context', 
            'Section': 'section',
            'SubSection': 'subsection',
            'Question': 'question',
            'Response': 'response'
        }

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse INSTAT Excel file and return survey structure"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        try:
            # Read all sheets from Excel file
            excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            
            survey_structure = None
            
            # Process each sheet
            for sheet_name, df in excel_data.items():
                parsed_survey = self._parse_structured_sheet(sheet_name, df, file_path)
                if parsed_survey:
                    survey_structure = parsed_survey
                    break  # Use the first valid survey found
            
            if not survey_structure:
                # Fallback to basic parsing if structured parsing fails
                survey_structure = {
                    "title": file_path.stem,
                    "description": f"Survey generated from {file_path.name}",
                    "sections": []
                }
                
                for sheet_name, df in excel_data.items():
                    section = self._parse_sheet_basic(sheet_name, df)
                    if section:
                        survey_structure["sections"].append(section)

            return survey_structure

        except Exception as e:
            logger.error(f"Error parsing Excel file {file_path}: {str(e)}")
            raise

    def _parse_structured_sheet(self, sheet_name: str, df: pd.DataFrame, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse sheet with INSTAT structured format"""
        if df.empty or len(df.columns) < 5:
            return None

        # Check if this looks like a structured INSTAT file
        if not self._is_structured_format(df):
            return None

        logger.info(f"Parsing structured INSTAT format for sheet: {sheet_name}")

        # Map the DataFrame columns to expected structure
        df_clean = df.copy()
        
        # Handle different column naming patterns
        if 'entryLabel' in df.iloc[0].values:
            # Header is in first row
            header_row = 0
            for i, val in enumerate(df.iloc[header_row]):
                if pd.notna(val):
                    if 'entryLabel' in str(val):
                        df_clean = df_clean.rename(columns={df.columns[i]: 'entryLabel'})
                    elif 'entryName' in str(val):
                        df_clean = df_clean.rename(columns={df.columns[i]: 'entryName'})
                    elif 'entryParentIndex' in str(val):
                        df_clean = df_clean.rename(columns={df.columns[i]: 'entryParentIndex'})
                    elif 'entryIndex' in str(val):
                        df_clean = df_clean.rename(columns={df.columns[i]: 'entryIndex'})
            # Remove header row
            df_clean = df_clean.iloc[1:].reset_index(drop=True)
        else:
            # Use positional mapping based on observed patterns
            col_mapping = {}
            if len(df.columns) >= 5:
                col_mapping[df.columns[1]] = 'entryLabel'  # Column 1: Label
                col_mapping[df.columns[2]] = 'entryName'   # Column 2: Type
                col_mapping[df.columns[3]] = 'entryParentIndex'  # Column 3: Parent
                col_mapping[df.columns[4]] = 'entryIndex'  # Column 4: Index
            df_clean = df_clean.rename(columns=col_mapping)

        # Parse the hierarchical structure
        survey_structure = self._build_survey_structure(df_clean, file_path)
        return self._validate_and_fix_metadata(survey_structure)

    def _is_structured_format(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame has INSTAT structured format"""
        if len(df) < 3:
            return False
        
        # Look for key indicators in the data
        indicators = ['Survey', 'Section', 'Question', 'Response', 'Context']
        found_indicators = 0
        
        # Check first 20 rows for structure indicators
        for i in range(min(20, len(df))):
            row_text = ' '.join([str(val) for val in df.iloc[i] if pd.notna(val)])
            for indicator in indicators:
                if indicator in row_text:
                    found_indicators += 1
                    break
        
        return found_indicators >= 3

    def _build_survey_structure(self, df: pd.DataFrame, file_path: Path) -> Dict[str, Any]:
        """Build survey structure from parsed DataFrame"""
        
        # Initialize the survey structure
        survey_structure = {
            "title": file_path.stem,
            "description": f"Survey generated from {file_path.name}",
            "sections": [],
            "metadata": {
                "source_file": file_path.name,
                "total_rows": len(df)
            }
        }

        # Track hierarchy
        current_section = None
        current_subsection = None
        current_question = None
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                entry_type = self._get_entry_type(row)
                entry_label = self._get_entry_label(row)
                parent_index = self._get_parent_index(row)
                entry_index = self._get_entry_index(row)
                
                if not entry_label or not entry_type:
                    continue

                logger.debug(f"Processing row {idx}: {entry_type} - {entry_label[:50]}...")

                if entry_type == 'survey':
                    # Update survey title if found
                    survey_structure["title"] = entry_label
                    survey_structure["description"] = f"Survey: {entry_label}"

                elif entry_type == 'section':
                    # Create new section
                    current_section = {
                        "title": entry_label,
                        "subsections": [],
                        "questions": [],
                        "metadata": {
                            "entry_index": entry_index,
                            "parent_index": parent_index,
                            "entryFullPath": f"/{entry_label}",
                            "entryDescription": self._extract_entry_description(row, entry_label),
                            "entryAnnotation": self._extract_entry_annotation(row, entry_label),
                            "caution": self._extract_caution_info(row, entry_label),
                            "existingConditions": self._extract_existing_conditions(row, entry_label),
                            "JumpToEntry": "",
                            "coordinates": self._extract_coordinates(entry_label)
                        }
                    }
                    survey_structure["sections"].append(current_section)
                    current_subsection = None  # Reset subsection
                    current_question = None

                elif entry_type == 'subsection':
                    # Create subsection within current section
                    if current_section:
                        current_subsection = {
                            "title": entry_label,
                            "questions": [],
                            "metadata": {
                                "entry_index": entry_index,
                                "parent_index": parent_index,
                                "entryFullPath": self._build_subsection_path(current_section, entry_label),
                                "entryDescription": self._extract_entry_description(row, entry_label),
                                "entryAnnotation": self._extract_entry_annotation(row, entry_label),
                                "caution": self._extract_caution_info(row, entry_label),
                                "existingConditions": self._extract_existing_conditions(row, entry_label),
                                "JumpToEntry": "",
                                "coordinates": self._extract_coordinates(entry_label)
                            }
                        }
                        current_section["subsections"].append(current_subsection)
                    current_question = None

                elif entry_type == 'question':
                    # Create question
                    question = {
                        "text": entry_label,
                        "type": self._detect_question_type(entry_label),
                        "options": [],
                        "metadata": {
                            "entry_index": entry_index,
                            "parent_index": parent_index,
                            "table_reference": self._extract_table_reference(entry_label),
                            "entryFullPath": self._build_entry_path(current_section, current_subsection, entry_label),
                            "entryDescription": self._extract_entry_description(row, entry_label),
                            "entryAnnotation": self._extract_entry_annotation(row, entry_label),
                            "caution": self._extract_caution_info(row, entry_label),
                            "existingConditions": self._extract_existing_conditions(row, entry_label),
                            "JumpToEntry": "",
                            "coordinates": self._extract_coordinates(entry_label)
                        },
                        "is_required": self._is_required_question(entry_label)
                    }
                    
                    # Add question to appropriate container
                    if current_subsection:
                        current_subsection["questions"].append(question)
                    elif current_section:
                        current_section["questions"].append(question)
                    
                    current_question = question

                elif entry_type == 'response':
                    # Add response option to current question
                    if current_question:
                        response_option = {
                            "text": entry_label,
                            "value": entry_label,
                            "metadata": {
                                "entry_index": entry_index,
                                "parent_index": parent_index,
                                "entryFullPath": self._build_option_path(current_section, current_subsection, current_question, entry_label),
                                "entryDescription": self._extract_entry_description(row, entry_label),
                                "entryAnnotation": self._extract_entry_annotation(row, entry_label),
                                "caution": self._extract_caution_info(row, entry_label),
                                "existingConditions": self._extract_existing_conditions(row, entry_label),
                                "JumpToEntry": "",
                                "coordinates": self._extract_coordinates(entry_label)
                            }
                        }
                        current_question["options"].append(response_option)
                        
                        # Update question type based on responses
                        if len(current_question["options"]) > 1:
                            current_question["type"] = "single_choice"

                elif entry_type == 'context':
                    # Handle context information (can be converted to section or metadata)
                    if not current_section:
                        section_title = f"Context: {entry_label}"
                        current_section = {
                            "title": section_title,
                            "subsections": [],
                            "questions": [],
                            "metadata": {
                                "entry_index": entry_index,
                                "parent_index": parent_index,
                                "type": "context",
                                "entryFullPath": f"/{section_title}",
                                "entryDescription": "Section contextuelle contenant des informations de base",
                                "entryAnnotation": self._extract_entry_annotation(row, entry_label),
                                "caution": self._extract_caution_info(row, entry_label),
                                "existingConditions": self._extract_existing_conditions(row, entry_label),
                                "JumpToEntry": "",
                                "coordinates": self._extract_coordinates(entry_label)
                            }
                        }
                        survey_structure["sections"].append(current_section)

            except Exception as e:
                logger.warning(f"Error processing row {idx}: {e}")
                continue

        return survey_structure

    def _get_entry_type(self, row) -> Optional[str]:
        """Extract entry type from row"""
        if 'entryName' in row:
            entry_name = str(row['entryName']).strip()
            return entry_name.lower() if entry_name and entry_name != 'nan' else None
        
        # Fallback: check all columns for type indicators
        for col in row.index:
            val = str(row[col]).strip()
            if val.lower() in ['survey', 'section', 'subsection', 'question', 'response', 'context']:
                return val.lower()
        return None

    def _get_entry_label(self, row) -> Optional[str]:
        """Extract entry label from row"""
        if 'entryLabel' in row:
            label = str(row['entryLabel']).strip()
            return label if label and label != 'nan' else None
        
        # Fallback: use first non-empty column after ID
        for col in row.index[1:]:  # Skip first column (ID)
            val = str(row[col]).strip()
            if val and val != 'nan' and len(val) > 2:
                return val
        return None

    def _get_parent_index(self, row) -> Optional[int]:
        """Extract parent index from row"""
        if 'entryParentIndex' in row:
            try:
                parent = row['entryParentIndex']
                return int(parent) if pd.notna(parent) and parent != -1 else None
            except:
                return None
        return None

    def _get_entry_index(self, row) -> Optional[int]:
        """Extract entry index from row"""
        if 'entryIndex' in row:
            try:
                return int(row['entryIndex']) if pd.notna(row['entryIndex']) else None
            except:
                return None
        return None

    def _parse_sheet_basic(self, sheet_name: str, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Basic parsing fallback for non-structured sheets"""
        if df.empty:
            return None

        section = {
            "title": sheet_name.replace('_', ' ').title(),
            "subsections": [],
            "questions": []
        }

        # Try to extract questions from any recognizable text
        for idx, row in df.iterrows():
            row_data = row.dropna()
            if row_data.empty:
                continue

            for col_val in row_data:
                text = str(col_val).strip()
                if len(text) > 10 and self._looks_like_question(text):
                    question = {
                        "text": text,
                        "type": self._detect_question_type(text),
                        "options": [],
                        "metadata": {"source_row": idx}
                    }
                    section["questions"].append(question)

        return section if section["questions"] else None

    def _looks_like_question(self, text: str) -> bool:
        """Check if text looks like a question"""
        text_lower = text.lower()
        question_indicators = [
            '?', 'quel', 'quelle', 'quels', 'quelles', 'comment', 'où', 'quand',
            'combien', 'pourquoi', 'êtes-vous', 'avez-vous', 'faites-vous',
            'disposez-vous', 'utilisez-vous'
        ]
        return any(indicator in text_lower for indicator in question_indicators)

    def _detect_question_type(self, question_text: str) -> str:
        """Detect question type based on text content"""
        text_lower = question_text.lower()

        # Check for table references first
        if self._extract_table_reference(question_text):
            return "table_reference"

        # Boolean/Yes-No questions
        if any(phrase in text_lower for phrase in ['oui ou non', 'oui/non', 'vrai/faux', 'disposez-vous']):
            return "boolean"

        # Multiple choice indicators
        if any(word in text_lower for word in ['sélectionner', 'choisir', 'cocher', 'options']):
            return "single_choice"

        # Number questions
        if any(word in text_lower for word in ['nombre', 'montant', 'quantité', 'combien', 'âge', 'pourcentage']):
            return "number"

        # Date questions
        if any(word in text_lower for word in ['date', 'quand', 'année', 'mois']):
            return "date"

        # Email
        if 'email' in text_lower or '@' in question_text:
            return "email"

        # Phone
        if any(word in text_lower for word in ['téléphone', 'phone', 'tél']):
            return "phone"

        # Default to text
        return "text"

    def _extract_table_reference(self, text: str) -> Optional[str]:
        """Extract table reference from question text"""
        # Look for TableRef patterns
        table_ref_patterns = [
            r'@?TableRef\s*:\s*(\d+)',
            r'TableRef\s*(\d+)',
            r'@TableRef:\s*(\d+)',
            r'liste\s+déroulante.*(\d+)',
            r'table\s+de\s+référence.*(\d+)'
        ]
        
        for pattern in table_ref_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"TableRef:{match.group(1).zfill(2)}"
        
        return None

    def _is_required_question(self, text: str) -> bool:
        """Determine if question is required"""
        required_indicators = ['obligatoire', 'requis', 'nécessaire', '*']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in required_indicators)

    def validate_structure(self, survey_structure: Dict[str, Any]) -> List[str]:
        """Validate parsed survey structure and return list of issues"""
        issues = []

        if not survey_structure.get("title"):
            issues.append("Survey title is missing")

        if not survey_structure.get("sections"):
            issues.append("No sections found in the survey")

        total_questions = 0
        sections_with_questions = 0
        empty_sections = []
        
        for i, section in enumerate(survey_structure.get("sections", [])):
            if not section.get("title"):
                issues.append(f"Section {i + 1} is missing a title")

            section_questions = len(section.get("questions", []))
            for subsection in section.get("subsections", []):
                section_questions += len(subsection.get("questions", []))
            
            total_questions += section_questions
            
            if section_questions > 0:
                sections_with_questions += 1
            else:
                empty_sections.append(section.get('title', f'Section {i + 1}'))

        # Only report issues if the survey has significant problems
        if total_questions == 0:
            issues.append("No questions found in the entire survey")
        elif total_questions < 5 and sections_with_questions < 2:
            issues.append(f"Survey appears to have very few questions ({total_questions} total)")
            
        # For INSTAT files, only report empty sections if they constitute a large portion
        # of the survey (more than 50% empty sections suggests a parsing problem)
        total_sections = len(survey_structure.get("sections", []))
        if len(empty_sections) > total_sections * 0.5 and total_questions > 0:
            issues.append(f"Many sections appear to be empty ({len(empty_sections)} out of {total_sections}). This might indicate a parsing issue.")

        return issues

    def extract_table_references(self, survey_structure: Dict[str, Any]) -> List[str]:
        """Extract all table references used in the survey"""
        table_refs = set()
        
        def extract_from_questions(questions):
            for question in questions:
                if question.get("metadata", {}).get("table_reference"):
                    table_refs.add(question["metadata"]["table_reference"])
        
        for section in survey_structure.get("sections", []):
            extract_from_questions(section.get("questions", []))
            for subsection in section.get("subsections", []):
                extract_from_questions(subsection.get("questions", []))
        
        return sorted(list(table_refs))

    def _build_entry_path(self, current_section, current_subsection, entry_label: str) -> str:
        """Build full path for an entry"""
        path_parts = []
        
        if current_section:
            section_title = current_section.get("title", "Unknown Section")
            path_parts.append(section_title)
            
        if current_subsection:
            subsection_title = current_subsection.get("title", "Unknown Subsection")
            path_parts.append(subsection_title)
            
        # Truncate entry label smartly if too long
        label = entry_label.strip()
        if len(label) > 60:
            # Find a good break point
            truncated = label[:60]
            last_space = truncated.rfind(' ')
            last_punct = max(truncated.rfind('.'), truncated.rfind('?'), truncated.rfind('!'))
            
            if last_punct > 40:  # Break at punctuation if reasonable
                label = label[:last_punct + 1]
            elif last_space > 40:  # Break at word boundary
                label = truncated[:last_space]
            else:
                label = truncated
        
        path_parts.append(label)
        
        return "/" + "/".join(path_parts)

    def _build_subsection_path(self, current_section, entry_label: str) -> str:
        """Build full path for a subsection"""
        if current_section:
            return f"/{current_section.get('title', 'Unknown Section')}/{entry_label}"
        return f"/{entry_label}"

    def _build_option_path(self, current_section, current_subsection, current_question, entry_label: str) -> str:
        """Build full path for an option"""
        path_parts = []
        
        if current_section:
            section_title = current_section.get("title", "Unknown Section")
            path_parts.append(section_title)
            
        if current_subsection:
            subsection_title = current_subsection.get("title", "Unknown Subsection")
            path_parts.append(subsection_title)
            
        if current_question:
            question_text = current_question.get("text", "Unknown Question")
            # Truncate question text smartly if too long
            if len(question_text) > 60:
                # Find a good break point
                truncated = question_text[:60]
                last_space = truncated.rfind(' ')
                last_punct = max(truncated.rfind('.'), truncated.rfind('?'), truncated.rfind('!'))
                
                if last_punct > 40:  # Break at punctuation if reasonable
                    question_text = question_text[:last_punct + 1]
                elif last_space > 40:  # Break at word boundary
                    question_text = truncated[:last_space]
                else:
                    question_text = truncated
            
            path_parts.append(question_text)
            
        path_parts.append(entry_label)
        
        return "/" + "/".join(path_parts)

    def _extract_entry_description(self, row, entry_label: str) -> str:
        """Extract description from additional columns in the row"""
        # Look for description in common description columns
        description_columns = ['description', 'desc', 'annotation', 'note', 'comment', 'entryDescription']
        
        for col in row.index:
            col_name = str(col).lower()
            if any(desc_col in col_name for desc_col in description_columns):
                val = str(row[col]).strip()
                if val and val != 'nan' and val != entry_label:
                    return val
        
        # Default description based on entry content
        if 'adresse' in entry_label.lower():
            return "Adresse géographique avec coordonnées requises"
        elif 'ville' in entry_label.lower() or 'city' in entry_label.lower():
            return "Ville ou entité géographique"
        elif any(word in entry_label.lower() for word in ['téléphone', 'phone', 'contact']):
            return "Information de contact"
        elif 'email' in entry_label.lower():
            return "Adresse électronique de contact"
        
        return ""

    def _extract_entry_annotation(self, row, entry_label: str) -> str:
        """Extract annotation from additional columns in the row"""
        # Look for annotation in specific columns
        annotation_columns = ['annotation', 'note', 'remark', 'entryAnnotation', 'comment']
        
        for col in row.index:
            col_name = str(col).lower()
            if any(ann_col in col_name for ann_col in annotation_columns):
                val = str(row[col]).strip()
                if val and val != 'nan' and val != entry_label:
                    return val
        
        # Auto-generate annotation for specific types
        if self._extract_table_reference(entry_label):
            return "Référence à une table de données externe"
        elif 'obligatoire' in entry_label.lower() or '*' in entry_label:
            return "Champ obligatoire à remplir"
            
        return ""

    def _extract_caution_info(self, row, entry_label: str) -> str:
        """Extract caution/warning information"""
        # Look for caution in specific columns
        caution_columns = ['caution', 'warning', 'attention', 'avertissement']
        
        for col in row.index:
            col_name = str(col).lower()
            if any(caut_col in col_name for caut_col in caution_columns):
                val = str(row[col]).strip()
                if val and val != 'nan':
                    return val
        
        # Auto-generate caution for sensitive data
        sensitive_keywords = ['confidentiel', 'personnel', 'privé', 'sensible']
        if any(keyword in entry_label.lower() for keyword in sensitive_keywords):
            return "Information sensible - manipuler avec précaution"
        
        return ""

    def _extract_existing_conditions(self, row, entry_label: str) -> str:
        """Extract existing conditions for the entry"""
        # Look for conditions in specific columns
        condition_columns = ['condition', 'prerequis', 'requirement', 'existingConditions']
        
        for col in row.index:
            col_name = str(col).lower()
            if any(cond_col in col_name for cond_col in condition_columns):
                val = str(row[col]).strip()
                if val and val != 'nan':
                    return val
        
        # Auto-generate conditions based on question type
        if 'dépend' in entry_label.lower() or 'si' in entry_label.lower():
            return "Réponse conditionnelle basée sur une question précédente"
        elif self._extract_table_reference(entry_label):
            return "Nécessite l'accès à une table de référence externe"
            
        # Default to French conditional response text when no conditions found
        return "Réponse conditionnelle basée sur une question précédente"

    def _extract_coordinates(self, entry_label: str) -> dict:
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

    def determine_schema_name(self, filename: str) -> str:
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
            
    def _validate_and_fix_metadata(self, survey_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix metadata fields, ensuring existingConditions is never empty and paths are correct"""
        default_conditions = "Réponse conditionnelle basée sur une question précédente"
        
        def fix_metadata(metadata: Dict[str, Any]):
            """Fix existingConditions in metadata"""
            if "existingConditions" not in metadata or not metadata["existingConditions"]:
                metadata["existingConditions"] = default_conditions
        
        def build_proper_path(section_title: str, subsection_title: str = None, 
                             question_text: str = None, option_text: str = None) -> str:
            """Build a proper hierarchical path"""
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
        
        # Process all sections
        for section in survey_structure.get("sections", []):
            section_title = section.get("title", "")
            
            # Fix section metadata
            if "metadata" in section:
                fix_metadata(section["metadata"])
                # Fix section path
                section["metadata"]["entryFullPath"] = f"/{section_title}"
            
            # Fix questions in section
            for question in section.get("questions", []):
                if "metadata" in question:
                    fix_metadata(question["metadata"])
                    # Fix question path
                    proper_path = build_proper_path(section_title, None, question.get("text", ""))
                    question["metadata"]["entryFullPath"] = proper_path
                
                # Fix options in question
                for option in question.get("options", []):
                    if "metadata" in option:
                        fix_metadata(option["metadata"])
                        # Fix option path
                        proper_path = build_proper_path(
                            section_title, None, question.get("text", ""), option.get("text", "")
                        )
                        option["metadata"]["entryFullPath"] = proper_path
            
            # Fix subsections
            for subsection in section.get("subsections", []):
                subsection_title = subsection.get("title", "")
                
                if "metadata" in subsection:
                    fix_metadata(subsection["metadata"])
                    # Fix subsection path
                    subsection["metadata"]["entryFullPath"] = f"/{section_title}/{subsection_title}"
                
                # Fix questions in subsection
                for question in subsection.get("questions", []):
                    if "metadata" in question:
                        fix_metadata(question["metadata"])
                        # Fix question path
                        proper_path = build_proper_path(
                            section_title, subsection_title, question.get("text", "")
                        )
                        question["metadata"]["entryFullPath"] = proper_path
                    
                    # Fix options in subsection question
                    for option in question.get("options", []):
                        if "metadata" in option:
                            fix_metadata(option["metadata"])
                            # Fix option path
                            proper_path = build_proper_path(
                                section_title, subsection_title, 
                                question.get("text", ""), option.get("text", "")
                            )
                            option["metadata"]["entryFullPath"] = proper_path
        
        return survey_structure
