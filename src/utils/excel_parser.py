"""
Enhanced Excel file parser for INSTAT Survey Platform
Parses Excel files with both structured INSTAT format and basic Excel format
to extract survey structure and generate forms automatically
"""
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)


class ExcelParser:
    """Enhanced parser for Excel files with INSTAT structured survey data"""

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
        """Parse Excel file and return survey structure"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        try:
            # Read all sheets from Excel file
            excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            
            survey_structure = None
            
            # First try structured INSTAT parsing for each sheet
            for sheet_name, df in excel_data.items():
                parsed_survey = self._parse_structured_sheet(sheet_name, df, file_path)
                if parsed_survey:
                    survey_structure = parsed_survey
                    logger.info(f"Successfully parsed structured format from sheet: {sheet_name}")
                    break  # Use the first valid survey found
            
            # Fallback to basic parsing if structured parsing fails
            if not survey_structure:
                logger.info("Structured parsing failed, falling back to basic parsing")
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

    def _parse_sheet(self, sheet_name: str, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Parse individual sheet to extract section structure"""
        if df.empty:
            return None

        section = {
            "title": sheet_name,
            "subsections": [],
            "questions": []
        }

        # Look for hierarchical structure in the data
        current_subsection = None

        for idx, row in df.iterrows():
            row_data = row.dropna()

            if row_data.empty:
                continue

            # Detect if this is a subsection header (heuristic based)
            if self._is_subsection_header(row_data):
                current_subsection = {
                    "title": str(row_data.iloc[0]),
                    "questions": []
                }
                section["subsections"].append(current_subsection)

            # Detect if this is a question
            elif self._is_question(row_data):
                question = self._parse_question(row_data)
                if question:
                    if current_subsection:
                        current_subsection["questions"].append(question)
                    else:
                        section["questions"].append(question)

        return section

    def _is_subsection_header(self, row_data: pd.Series) -> bool:
        """Heuristic to detect subsection headers"""
        if len(row_data) == 1:
            text = str(row_data.iloc[0]).strip()
            # Look for typical subsection patterns
            if (text.isupper() or
                    text.startswith(('SECTION', 'PART', 'PARTIE', 'PARTI', 'CHAPTER',  'CHAPITRE', 'SUBSECTION')) or
                    len(text.split()) <= 5):
                return True
        return False

    def _is_question(self, row_data: pd.Series) -> bool:
        """Heuristic to detect questions"""
        if len(row_data) >= 1:
            text = str(row_data.iloc[0]).strip()
            # Look for question patterns
            if (text.endswith('?') or
                    text.startswith(
                        ('Nombre', 'Numero', 'Quelles', 'Quelle', 'Quels', 'Quel')) or
                    'question' in text.lower() or
                    len(text.split()) > 3):
                return True
        return False

    def _parse_question(self, row_data: pd.Series) -> Dict[str, Any]:
        """Parse question from row data"""
        question_text = str(row_data.iloc[0]).strip()

        question = {
            "text": question_text,
            "type": self._detect_question_type(question_text),
            "options": []
        }

        # If there are additional columns, treat them as options
        if len(row_data) > 1:
            for option in row_data.iloc[1:]:
                if pd.notna(option) and str(option).strip():
                    question["options"].append(str(option).strip())

        return question

    def _detect_question_type(self, question_text: str) -> str:
        """Detect question type based on text content"""
        text_lower = question_text.lower()

        # Multiple choice indicators
        if any(word in text_lower for word in ['select', 'checkbox','choix', 'choose', 'pick', 'option']):
            return "multiple_choice"

        # Yes/No questions
        if any(phrase in text_lower for phrase in
               ['oui ou nom', 'oui/non', 'vrai/faux']):
            return "boolean"

        # Number questions
        if any(word in text_lower for word in
               ['nombre', 'montant', 'quantite', 'compte', 'age']):
            return "number"

        # Date questions
        if any(word in text_lower for word in ['date', 'quand', 'temps']):
            return "date"

        # Default to text
        return "text"

    def validate_structure(self, survey_structure: Dict[str, Any]) -> List[str]:
        """Validate parsed survey structure and return list of issues"""
        issues = []

        if not survey_structure.get("title"):
            issues.append("Survey title is missing")

        if not survey_structure.get("sections"):
            issues.append("No sections found in the survey")

        # Count total questions across all sections
        total_survey_questions = 0
        sections_with_questions = 0
        
        for i, section in enumerate(survey_structure.get("sections", [])):
            if not section.get("title"):
                issues.append(f"Section {i + 1} is missing a title")

            # Count questions in this section
            section_questions = len(section.get("questions", []))
            for subsection in section.get("subsections", []):
                section_questions += len(subsection.get("questions", []))
            
            total_survey_questions += section_questions
            if section_questions > 0:
                sections_with_questions += 1

        # Only report issues if the entire survey has very few questions
        # Individual sections can be empty in structured formats (they might be context/headers)
        if total_survey_questions == 0:
            issues.append("No questions found in the entire survey")
        elif total_survey_questions < 5 and sections_with_questions < 2:
            issues.append(f"Survey appears to have very few questions ({total_survey_questions} total)")

        return issues

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
        return self._build_survey_structure(df_clean, file_path)

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

                logger.debug(f"Processing row {idx}: {entry_type} - {entry_label[:50] if len(entry_label) > 50 else entry_label}")

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
                            "parent_index": parent_index
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
                                "parent_index": parent_index
                            }
                        }
                        current_section["subsections"].append(current_subsection)
                    current_question = None

                elif entry_type == 'question':
                    # Create question
                    question = {
                        "text": entry_label,
                        "type": self._detect_question_type_enhanced(entry_label),
                        "options": [],
                        "metadata": {
                            "entry_index": entry_index,
                            "parent_index": parent_index,
                            "table_reference": self._extract_table_reference(entry_label)
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
                                "parent_index": parent_index
                            }
                        }
                        current_question["options"].append(response_option)
                        
                        # Update question type based on responses
                        if len(current_question["options"]) > 1:
                            current_question["type"] = "single_choice"

                elif entry_type == 'context':
                    # Handle context information (can be converted to section or metadata)
                    if not current_section:
                        current_section = {
                            "title": f"Context: {entry_label}",
                            "subsections": [],
                            "questions": [],
                            "metadata": {
                                "entry_index": entry_index,
                                "parent_index": parent_index,
                                "type": "context"
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
                        "type": self._detect_question_type_enhanced(text),
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

    def _detect_question_type_enhanced(self, question_text: str) -> str:
        """Enhanced question type detection based on text content"""
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
