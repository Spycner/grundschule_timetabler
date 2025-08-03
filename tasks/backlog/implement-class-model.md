# Implement Class Model

## Priority
High

## Created
2025-08-03

## Description
Create the Class (Klasse) data model and API endpoints for managing class information, including grade level, size, and assigned teachers.

## Acceptance Criteria
- [ ] Create Class SQLAlchemy model
- [ ] Create Pydantic schemas
- [ ] Implement CRUD endpoints
- [ ] Add class teacher relationship
- [ ] Add room assignment
- [ ] Support class groups/splits
- [ ] Create API tests
- [ ] Add validation for class size
- [ ] Implement grade level logic

## Technical Details
### Class Model Fields
- id (UUID)
- name (e.g., "1a", "2b", "3c")
- grade_level (1-4)
- academic_year
- student_count
- class_teacher_id (foreign key)
- home_room_id (foreign key)
- special_requirements (JSON)
- created_at
- updated_at

### API Endpoints
- GET /api/classes - List all classes
- GET /api/classes/{id} - Get class details
- POST /api/classes - Create new class
- PUT /api/classes/{id} - Update class
- DELETE /api/classes/{id} - Delete class
- GET /api/classes/{id}/schedule - Get class schedule
- GET /api/classes/by-grade/{grade} - Get classes by grade

## Notes
- Support splitting classes for subjects like Religion/Ethics
- Consider combined classes for special subjects
- Track historical data for previous years
- Validate grade level constraints

## Dependencies
- Teacher model should be implemented
- Room model needed for home room assignment