# Implement Teacher Availability Model

## Priority
High

## Created
2025-08-03

## Description
Create a comprehensive teacher availability system that tracks when teachers are available to teach, including part-time schedules, blocked periods, and preferences.

## Acceptance Criteria
- [ ] Create TeacherAvailability model with SQLAlchemy
- [ ] Support different availability types (available, blocked, preferred)
- [ ] Handle part-time teacher schedules
- [ ] Create CRUD endpoints for availability management
- [ ] Add validation to prevent scheduling outside availability
- [ ] Support recurring weekly patterns
- [ ] Allow exceptions for specific dates
- [ ] Integrate with Schedule validation
- [ ] Add bulk import for availability data
- [ ] Create availability overview endpoints

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
