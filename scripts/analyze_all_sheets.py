#!/usr/bin/env python3
"""
Analyze all sheets in the diagnostic Excel file
"""
import sys
import os
from pathlib import Path
import pandas as pd

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_all_sheets(file_path):
    """Analyze all sheets in Excel file"""
    print(f"🔍 Analyzing: {file_path}")
    print("=" * 80)
    
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        
        print(f"📋 Found {len(excel_data.keys())} sheets:")
        for i, sheet_name in enumerate(excel_data.keys(), 1):
            print(f"  {i}. '{sheet_name}'")
        
        print("\n" + "=" * 80)
        
        for sheet_name, df in excel_data.items():
            print(f"\n📄 Sheet: '{sheet_name}'")
            print(f"   Size: {df.shape[0]} rows × {df.shape[1]} columns")
            
            if df.empty:
                print("   ❌ Sheet is empty")
                continue
            
            # Check if it looks like structured format
            has_entry_columns = any(col in ['entryLabel', 'entryName', 'entryParentIndex'] for col in df.columns)
            has_entry_in_first_row = any('entry' in str(val).lower() for val in df.iloc[0] if pd.notna(val))
            
            if has_entry_columns or has_entry_in_first_row:
                print("   ✅ Appears to be structured format")
                
                # Count entries by type
                entry_types = {}
                for idx, row in df.iterrows():
                    if 'entryName' in row:
                        entry_type = str(row['entryName']).strip().lower()
                        if entry_type and entry_type != 'nan':
                            entry_types[entry_type] = entry_types.get(entry_type, 0) + 1
                
                print(f"   Entry types found: {dict(entry_types)}")
                
                # Look for questions specifically
                question_count = 0
                for idx, row in df.iterrows():
                    if 'entryName' in row and str(row['entryName']).strip().lower() == 'question':
                        if 'entryLabel' in row and pd.notna(row['entryLabel']):
                            question_text = str(row['entryLabel']).strip()
                            if question_text and question_text != 'nan':
                                question_count += 1
                                if question_count <= 3:  # Show first 3
                                    print(f"      Q{question_count}: {question_text[:80]}")
                
                print(f"   ✅ Found {question_count} structured questions")
            else:
                print("   ⚠️  Non-structured format, checking for questions...")
                
                # Look for question-like content in any cell
                question_count = 0
                for idx, row in df.iterrows():
                    for col_idx, cell in enumerate(row):
                        if pd.notna(cell):
                            text = str(cell).strip()
                            if len(text) > 15:  # Longer text more likely to be questions
                                text_lower = text.lower()
                                if any(pattern in text_lower for pattern in [
                                    '?', 'quel', 'quelle', 'comment', 'où', 'quand', 'combien',
                                    'pourquoi', 'indiquez', 'précisez', 'avez-vous', 'êtes-vous',
                                    'disposez-vous', 'utilisez-vous', 'nombre total', 'information'
                                ]):
                                    question_count += 1
                                    if question_count <= 5:  # Show first 5
                                        print(f"      Q{question_count}: Row {idx+1}, Col {col_idx+1}: {text[:100]}")
                                    if question_count >= 20:  # Don't go crazy
                                        break
                    if question_count >= 20:
                        break
                
                if question_count == 0:
                    print("   ❌ No questions found")
                else:
                    print(f"   ✅ Found {question_count} potential questions")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    file_path = "analysis/MODELISATION_FICHIER_DIAGNOSTIC_SSN_SDS4_DEVELOPPEMENT_V1.0.0.xlsx"
    if os.path.exists(file_path):
        analyze_all_sheets(file_path)
    else:
        print(f"❌ File not found: {file_path}")
