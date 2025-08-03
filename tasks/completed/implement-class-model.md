# Implement Class Model (MVP Version)

## Priority
High

## Created
2025-08-03

## Updated
2025-08-03 - Simplified for MVP approach

## Completed
2025-08-03 - Successfully implemented with TDD approach

## Description
Create a simple Class (Klasse) data model and basic CRUD API endpoints. Focus on minimum viable functionality for schedule creation.

## Acceptance Criteria
- [ ] Create simple Class SQLAlchemy model
- [ ] Create basic Pydantic schemas
- [ ] Implement basic CRUD endpoints
- [ ] Add grade level (1-4)
- [ ] Add home room as simple string
- [ ] Create basic API tests
- [ ] Add validation for class size

## Technical Details

### Simplified Class Model Fields
```python
- id (int, auto-increment)
- name (str, e.g., "1a", "2b", "3c")
- grade (int, 1-4 for Grundschule)
- size (int, number of students)
- home_room (str, e.g., "101", "Turnhalle")
- created_at (datetime)
- updated_at (datetime)
```

### Basic API Endpoints (Versioned)
- `GET /api/v1/classes` - List all classes
- `GET /api/v1/classes/{id}` - Get class details
- `POST /api/v1/classes` - Create new class
- `PUT /api/v1/classes/{id}` - Update class
- `DELETE /api/v1/classes/{id}` - Delete class

### MVP Validation Rules
- name must be unique (e.g., can't have two "1a" classes)
- grade must be between 1 and 4
- size must be between 1 and 35 (typical class size)
- home_room is optional but recommended

## What We're NOT Implementing (Yet)
- Class teacher assignment (separate concern)
- Room as separate entity (just string for now)
- Class groups/splits for Religion/Ethics
- Combined classes
- Academic year tracking
- Special requirements field
- Historical data
- Grade-specific filtering endpoint

## Sample Test Data
```python
{
    "name": "1a",
    "grade": 1,
    "size": 22,
    "home_room": "101"
}
```

## Notes
- Keep it simple - a class is just a group of students
- Room is a string to avoid creating Room entity yet
- No teacher assignment in the class itself (handled in Schedule)
- Focus on what's needed for basic scheduling

## Dependencies
- Backend setup must be complete ✅
- Database configuration ready ✅
- Teacher model NOT required (independent entities)

## Success Criteria
- Can create, read, update, delete classes
- Prevents duplicate class names
- Validates grade levels
- Takes < 5 minutes to implement basic version
- Test users can immediately create their school's classes
