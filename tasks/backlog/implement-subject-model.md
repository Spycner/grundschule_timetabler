# Implement Subject Model (MVP Version)

## Priority
High

## Created
2025-08-03

## Description
Create a simple Subject (Fach) data model and basic CRUD API endpoints. Focus on minimum viable functionality for schedule creation.

## Acceptance Criteria
- [ ] Create simple Subject SQLAlchemy model
- [ ] Create basic Pydantic schemas
- [ ] Implement basic CRUD endpoints
- [ ] Add subject code for display
- [ ] Add color for UI visualization
- [ ] Create basic API tests
- [ ] Add validation for uniqueness

## Technical Details

### Simplified Subject Model Fields
```python
- id (int, auto-increment)
- name (str, e.g., "Mathematik", "Deutsch")
- code (str, 2-4 chars, e.g., "MA", "DE", "SPO")
- color (str, hex color, e.g., "#FF5733")
- created_at (datetime)
- updated_at (datetime)
```

### Basic API Endpoints (Versioned)
- `GET /api/v1/subjects` - List all subjects
- `GET /api/v1/subjects/{id}` - Get subject details
- `POST /api/v1/subjects` - Create new subject
- `PUT /api/v1/subjects/{id}` - Update subject
- `DELETE /api/v1/subjects/{id}` - Delete subject

### MVP Validation Rules
- name must be unique
- code must be unique and 2-4 characters
- color must be valid hex color format (#RRGGBB)

## What We're NOT Implementing (Yet)
- Grade-specific weekly hours requirements
- Teacher qualifications for subjects
- Room requirements (e.g., Sport needs gym)
- Difficulty levels for scheduling
- Subject categories or grouping
- Special equipment requirements

## Sample Test Data
```python
{
    "name": "Mathematik",
    "code": "MA",
    "color": "#2563EB"  # Blue
}

{
    "name": "Deutsch", 
    "code": "DE",
    "color": "#DC2626"  # Red
}

{
    "name": "Sport",
    "code": "SPO", 
    "color": "#16A34A"  # Green
}
```

## Common German Grundschule Subjects
For reference when creating test data:
- **Deutsch** (DE) - German
- **Mathematik** (MA) - Mathematics  
- **Sachunterricht** (SU) - General Studies
- **Englisch** (EN) - English (grades 3-4)
- **Sport** (SPO) - Physical Education
- **Musik** (MU) - Music
- **Kunst** (KU) - Art
- **Religion** (REL) - Religion
- **Ethik** (ETH) - Ethics (alternative to Religion)

## Notes
- Keep it simple - just name, code, and color for visual distinction
- No complex requirements or constraints yet
- Any teacher can teach any subject in MVP
- Colors help users quickly identify subjects in schedule grid

## Dependencies
- Backend setup must be complete ✅
- Database configuration ready ✅

## Success Criteria
- Can create, read, update, delete subjects
- Prevents duplicate names and codes
- Validates color format
- Takes < 5 minutes to implement basic version
- Test users can create their school's subject list immediately
