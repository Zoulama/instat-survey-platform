# Integrated Metadata Fixes During Upload and Parsing

## Overview
The functionality from `scripts/fix_empty_existing_conditions.py` and `scripts/fix_full_paths.py` has been integrated directly into the upload and parsing process. This ensures that all metadata issues are automatically fixed when surveys and templates are created from uploaded Excel files.

## Integration Points

### 1. Excel Parser Integration (`src/utils/instat_excel_parser.py`)

#### New Method: `_validate_and_fix_metadata()`
- **Purpose**: Automatically fix metadata issues during parsing
- **Location**: Lines 672-774 in `instat_excel_parser.py`
- **Triggered**: Automatically called at the end of `parse_file()` method

#### Fixes Applied:
1. **Empty existingConditions**: 
   - Replaces empty or missing `existingConditions` with "Réponse conditionnelle basée sur une question précédente"

2. **Incorrect Full Paths**:
   - Rebuilds `entryFullPath` for all elements using proper hierarchy
   - Removes truncation indicators (`...`)
   - Ensures consistent path structure
   - Smart text truncation at word/sentence boundaries

#### Coverage:
- ✅ Sections
- ✅ Subsections  
- ✅ Questions
- ✅ Response Options
- ✅ All metadata fields

### 2. File Upload API Integration (`src/api/v1/file_upload.py`)

#### Both Upload Endpoints Enhanced:
- `/upload-excel-and-create-survey` (line 149)
- `/upload-excel-and-create-survey-with-template` (line 351)

#### Additional Features:
1. **Automatic JSON Structure Saving**:
   - Processed structures with fixes are saved to `generated/` directory
   - Files saved as `{filename}_structure.json`
   - Contains all applied fixes and proper metadata

2. **Process Flow**:
   ```
   Upload Excel → Parse with INSTATExcelParser → 
   Apply Metadata Fixes → Create Survey/Template → 
   Save Fixed Structure to JSON
   ```

### 3. Metadata Updater Enhancement (`scripts/update_survey_metadata.py`)

#### New Method: `_fix_full_path()`
- **Purpose**: Fix truncated paths in existing JSON files
- **Location**: Lines 342-372

#### Enhanced Methods:
- `_generate_existing_conditions()`: Always returns French conditional text
- Section/Subsection/Question metadata updaters: Now fix paths automatically

## Benefits

### ✅ Automatic Processing
- No need to run separate fix scripts after upload
- Metadata issues resolved at source during parsing
- Consistent data quality across all surveys

### ✅ Performance
- Single-pass processing during upload
- No additional file processing steps needed
- Reduced manual intervention

### ✅ Reliability
- All surveys/templates have consistent metadata
- No empty `existingConditions` fields
- Properly formatted `entryFullPath` values

### ✅ Backward Compatibility
- Existing fix scripts still work for historical data
- Can be used for batch processing existing files
- Same fixing logic applied in both contexts

## Usage

### For New Files
Simply upload Excel files through the API endpoints:
- `POST /v1/api/files/upload-excel-and-create-survey`
- `POST /v1/api/files/upload-excel-and-create-survey-with-template`

The fixes are automatically applied during processing.

### For Existing Files
Use the standalone scripts for batch processing:
```bash
python3 scripts/fix_empty_existing_conditions.py
python3 scripts/fix_full_paths.py
python3 scripts/update_survey_metadata.py
```

## Default Values Applied

### existingConditions
- **Default**: "Réponse conditionnelle basée sur une question précédente"
- **Applied When**: Field is empty, missing, or null
- **Scope**: All metadata objects (sections, questions, options, etc.)

### entryFullPath  
- **Format**: `"/Section/Subsection/Question/Option"`
- **Smart Truncation**: 60 characters for questions, 80 for other elements
- **Break Points**: Sentence endings (. ? !) → Word boundaries → Character limit
- **Applied When**: Path contains `...` or during initial creation

## Testing

The integration has been tested with existing survey structures:
- ✅ 3 JSON files processed successfully
- ✅ All empty `existingConditions` fixed
- ✅ Truncated paths rebuilt properly
- ✅ Upload process maintains performance

## Next Steps

1. **Monitor**: Check upload logs for any parsing issues
2. **Validate**: Verify new uploads have correct metadata
3. **Cleanup**: Consider archiving old fix scripts once confident in integration
4. **Document**: Update API documentation to mention automatic metadata fixing
