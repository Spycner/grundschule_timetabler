# Implement Teacher Availability Model

## Priority
High

## Created
2025-08-03

## Completed
2025-08-03

## Description
Create a comprehensive teacher availability system that tracks when teachers are available to teach, including part-time schedules, blocked periods, and preferences.

## Acceptance Criteria
- [x] Create TeacherAvailability model with SQLAlchemy
- [x] Support different availability types (available, blocked, preferred)
- [x] Handle part-time teacher schedules
- [x] Create CRUD endpoints for availability management
- [x] Add validation to prevent scheduling outside availability
- [x] Support recurring weekly patterns
- [x] Allow exceptions for specific dates (via effective_from/until)
- [x] Integrate with Schedule validation
- [x] Add bulk import for availability data
- [x] Create availability overview endpoints

## Technical Details
### Model Structure
```python
class TeacherAvailability:
    teacher_id: int (FK)
    weekday: int (0-4 for Monday-Friday)
    period: int (1-8)
    availability_type: Enum (AVAILABLE, BLOCKED, PREFERRED)
    effective_from: date
    effective_until: date (optional)
    reason: str (optional)
```

### API Endpoints
- `GET /api/v1/teachers/{id}/availability` - Get teacher's availability
- `POST /api/v1/teachers/{id}/availability` - Set availability
- `PUT /api/v1/teachers/{id}/availability/{availability_id}` - Update
- `DELETE /api/v1/teachers/{id}/availability/{availability_id}` - Remove
- `POST /api/v1/teachers/availability/bulk` - Bulk import

### Validation Rules
- Part-time teachers: Enforce max hours per week
- Blocked periods: Prevent any scheduling
- Preferred periods: Used by optimization algorithm
- Check availability before creating schedules

## Dependencies
- Teacher model must be complete
- TimeSlot model must be complete
- Schedule model must be complete

## Notes
- Consider German part-time regulations (Teilzeit)
- Support for Elternzeit (parental leave) periods
- Integration with substitute system for temporary unavailability
- May need to handle cross-school availability for shared teachers

## Implementation Summary

### Completed Features
1. **TeacherAvailability Model** - SQLAlchemy model with three availability types
2. **Database Migration** - Alembic migration `214fec70abb4_add_teacher_availability_model`
3. **Complete CRUD API** - 8 endpoints for managing availability
4. **Schedule Integration** - Prevents scheduling during BLOCKED periods
5. **Bulk Operations** - Efficient bulk import for multiple entries
6. **Validation System** - Part-time hour limits, date ranges, unique constraints
7. **Overview Endpoints** - Summary views for individual and all teachers
8. **16 Comprehensive Tests** - Full test coverage using TDD approach

### Technical Implementation
- **Weekday Convention**: 0-4 (Monday-Friday) for availability, converted from TimeSlot's 1-5
- **Availability Types**: AVAILABLE, BLOCKED, PREFERRED enum
- **Date Ranges**: effective_from/effective_until for temporal availability
- **Unique Constraint**: One entry per teacher/weekday/period/effective_from
- **Integration**: Schedule validation automatically checks teacher availability

### API Endpoints Created
1. `GET /api/v1/teachers/{id}/availability` - Get teacher's availability
2. `POST /api/v1/teachers/{id}/availability` - Create availability entry
3. `PUT /api/v1/teachers/{id}/availability/{id}` - Update availability
4. `DELETE /api/v1/teachers/{id}/availability/{id}` - Delete availability
5. `POST /api/v1/teachers/availability/bulk` - Bulk import
6. `GET /api/v1/teachers/{id}/availability/overview` - Overview for teacher
7. `GET /api/v1/teachers/{id}/availability/validate` - Validate constraints
8. `GET /api/v1/teachers/availability/overview` - All teachers overview

### Test Results
- 16 new tests added
- Total test count increased from 74 to 90
- All tests passing
- Schedule integration tested and working
