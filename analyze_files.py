#!/usr/bin/env python3
"""
Analyze INSTAT modeling files to understand structure and requirements
"""
import pandas as pd
import openpyxl
from pathlib import Path
import json
from typing import Dict, List, Any


def analyze_excel_file(file_path: Path) -> Dict[str, Any]:
    """Analyze Excel file structure"""
    try:
        print(f"\n=== Analyzing {file_path.name} ===")
        
        # Load workbook to get sheet names
        workbook = openpyxl.load_workbook(file_path, read_only=True)
        sheet_names = workbook.sheetnames
        print(f"Sheets found: {sheet_names}")
        
        analysis = {
            "filename": file_path.name,
            "sheets": {}
        }
        
        # Analyze each sheet
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                sheet_analysis = {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": list(df.columns),
                    "sample_data": df.head(3).to_dict('records') if not df.empty else []
                }
                
                print(f"\nSheet: {sheet_name}")
                print(f"  - Rows: {sheet_analysis['rows']}")
                print(f"  - Columns: {sheet_analysis['columns']}")
                print(f"  - Column names: {sheet_analysis['column_names']}")
                
                analysis["sheets"][sheet_name] = sheet_analysis
                
            except Exception as e:
                print(f"  Error reading sheet {sheet_name}: {e}")
                analysis["sheets"][sheet_name] = {"error": str(e)}
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing {file_path.name}: {e}")
        return {"filename": file_path.name, "error": str(e)}


def main():
    """Main analysis function"""
    analysis_dir = Path("analysis")
    excel_files = list(analysis_dir.glob("*.xlsx"))
    
    print("INSTAT Files Analysis")
    print("=" * 50)
    
    all_analyses = []
    
    for excel_file in excel_files:
        analysis = analyze_excel_file(excel_file)
        all_analyses.append(analysis)
    
    # Save analysis results
    with open("file_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(all_analyses, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nAnalysis complete. Results saved to file_analysis_results.json")
    print(f"Analyzed {len(excel_files)} Excel files")


if __name__ == "__main__":
    main()
