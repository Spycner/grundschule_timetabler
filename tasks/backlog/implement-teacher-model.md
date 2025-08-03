# Implement Teacher Model (MVP Version)

## Priority
High

## Created
2025-08-03

## Updated
2025-08-03 - Simplified for MVP approach

## Description
Create a simple Teacher data model and basic CRUD API endpoints. Focus on minimum viable functionality for schedule creation.

## Acceptance Criteria
- [ ] Create simple Teacher SQLAlchemy model
- [ ] Create basic Pydantic schemas for validation
- [ ] Implement basic CRUD endpoints
- [ ] Add simple part-time flag
- [ ] Create basic API tests
- [ ] Add essential validation (email, max_hours)

## Technical Details

### Simplified Teacher Model Fields
```python
- id (int, auto-increment)
- first_name (str, required)
- last_name (str, required)
- email (str, unique, required)
- abbreviation (str, 2-3 chars, e.g., "MUE")
- max_hours_per_week (int, default: 28)
- is_part_time (bool, default: False)
- created_at (datetime)
- updated_at (datetime)
```

### Basic API Endpoints (Versioned)
- `GET /api/v1/teachers` - List all teachers
- `GET /api/v1/teachers/{id}` - Get teacher details
- `POST /api/v1/teachers` - Create new teacher
- `PUT /api/v1/teachers/{id}` - Update teacher
- `DELETE /api/v1/teachers/{id}` - Delete teacher

### MVP Validation Rules
- Email must be valid format and unique
- first_name and last_name required
- max_hours_per_week between 1 and 40
- abbreviation unique and 2-3 characters

## What We're NOT Implementing (Yet)
- Complex availability windows
- Subject qualifications (any teacher can teach anything for now)
- Detailed contract types
- Preferences and constraints
- Soft delete
- Audit logging
- Bulk import
- Phone numbers
- Employee IDs

## Sample Test Data
```python
{
    "first_name": "Maria",
    "last_name": "Müller",
    "email": "maria.mueller@schule.de",
    "abbreviation": "MUE",
    "max_hours_per_week": 28,
    "is_part_time": False
}
```

## Notes
- Keep it simple - we can add complexity based on user feedback
- Focus on getting something that works for basic scheduling
- GDPR considerations postponed until we have real user data

## Dependencies
- Backend setup must be complete ✅
- Database configuration ready ✅

## Success Criteria
- Can create, read, update, delete teachers
- Prevents duplicate emails
- Takes < 5 minutes to implement basic version
- Test users can understand and use it immediately
