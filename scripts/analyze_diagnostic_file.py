#!/usr/bin/env python3
"""
Analyze the diagnostic Excel file to understand its structure
"""
import sys
import os
from pathlib import Path
import pandas as pd

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_excel_structure(file_path):
    """Analyze Excel file structure"""
    print(f"🔍 Analyzing: {file_path}")
    print("=" * 80)
    
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        
        for sheet_name, df in excel_data.items():
            print(f"\n📄 Sheet: '{sheet_name}'")
            print(f"   Size: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Show first few rows with content
            print(f"   First 15 non-empty cells:")
            found_content = []
            for idx, row in df.iterrows():
                for col_idx, cell in enumerate(row):
                    if pd.notna(cell) and str(cell).strip():
                        content = str(cell).strip()
                        found_content.append(f"   Row {idx+1}, Col {col_idx+1}: {content[:80]}")
                        if len(found_content) >= 15:
                            break
                if len(found_content) >= 15:
                    break
            
            for content in found_content:
                print(content)
                
            # Look for question patterns specifically
            print(f"\n   Looking for question-like content:")
            question_count = 0
            for idx, row in df.iterrows():
                for col_idx, cell in enumerate(row):
                    if pd.notna(cell):
                        text = str(cell).strip()
                        if len(text) > 10:
                            # More comprehensive question detection
                            text_lower = text.lower()
                            if any(pattern in text_lower for pattern in [
                                '?', 'quel', 'quelle', 'comment', 'où', 'quand', 'combien',
                                'pourquoi', 'indiquez', 'précisez', 'avez-vous', 'êtes-vous',
                                'disposez-vous', 'utilisez-vous', 'nombre', 'total'
                            ]):
                                print(f"      Q{question_count+1}: Row {idx+1}, Col {col_idx+1}: {text[:100]}")
                                question_count += 1
                                if question_count >= 10:  # Limit output
                                    break
                if question_count >= 10:
                    break
            
            if question_count == 0:
                print("      ❌ No obvious questions found")
            else:
                print(f"      ✅ Found {question_count} potential questions")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    file_path = "analysis/MODELISATION_FICHIER_DIAGNOSTIC_SSN_SDS4_DEVELOPPEMENT_V1.0.0.xlsx"
    if os.path.exists(file_path):
        analyze_excel_structure(file_path)
    else:
        print(f"❌ File not found: {file_path}")
