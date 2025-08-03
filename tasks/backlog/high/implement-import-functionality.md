# Implement Import Functionality

## Priority
High

## Created
2025-08-03

## Description
Create import functionality to load data from common formats used by schools, including Excel files, CSV, and other timetabling software exports.

## Acceptance Criteria
- [ ] Support Excel file import (.xlsx, .xls)
- [ ] Support CSV import with configurable delimiter
- [ ] Create import templates for download
- [ ] Validate imported data before saving
- [ ] Handle encoding issues (UTF-8, ISO-8859-1)
- [ ] Support incremental imports
- [ ] Create import mapping configuration
- [ ] Add duplicate detection and merging
- [ ] Provide detailed import reports
- [ ] Support rollback on import errors

## Technical Details
### Supported Import Types
```python
class ImportType(Enum):
    TEACHERS = "teachers"
    CLASSES = "classes"
    SUBJECTS = "subjects"
    ROOMS = "rooms"
    SCHEDULES = "schedules"
    FULL_TIMETABLE = "full_timetable"
```

### Import Process
1. Upload file
2. Parse and validate structure
3. Map columns to fields
4. Validate data constraints
5. Preview changes
6. Confirm and import
7. Generate report

### File Format Examples
#### Teachers CSV
```csv
Nachname;Vorname;Email;Kürzel;Stunden;Teilzeit
Müller;Maria;maria.mueller@schule.de;MM;28;false
Schmidt;Thomas;thomas.schmidt@schule.de;TS;14;true
```

#### Schedule Excel Format
| Klasse | Tag | Stunde | Fach | Lehrer | Raum |
|--------|-----|--------|------|--------|------|
| 1a | Montag | 1 | Deutsch | MM | 101 |
| 1a | Montag | 2 | Deutsch | MM | 101 |

### API Endpoints
- `POST /api/v1/import/upload` - Upload file for import
- `POST /api/v1/import/preview` - Preview import changes
- `POST /api/v1/import/confirm` - Execute import
- `GET /api/v1/import/templates/{type}` - Download template
- `GET /api/v1/import/jobs/{job_id}` - Check import status

### Validation Rules
- Check required fields
- Validate email formats
- Check foreign key references
- Detect scheduling conflicts
- Validate time formats
- Check data types

## Dependencies
- All core models must be complete
- File upload handling
- Background job processing for large imports

## Import Sources
- Previous year's timetable
- Excel exports from other systems
- Untis export format
- DaVinci export format
- Custom school formats

## Error Handling
- Row-level error reporting
- Partial import options
- Duplicate handling strategies
- Missing reference handling
- Encoding detection

## Notes
- German Excel files often use semicolon delimiter
- Support German date formats (DD.MM.YYYY)
- Handle umlauts correctly (ä, ö, ü, ß)
- Consider GDPR compliance for personal data
- May need background processing for large files
