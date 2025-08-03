# Implement Schedule Model (MVP Version)

## Priority
High

## Created
2025-08-03

## Description
Create the Schedule (Stundenplan) model that links Teachers, Classes, Subjects, and TimeSlots together. This is the core model that represents actual timetable entries.

## Acceptance Criteria
- [ ] Create Schedule SQLAlchemy model with foreign keys
- [ ] Create Pydantic schemas for requests/responses
- [ ] Implement CRUD endpoints with conflict detection
- [ ] Add unique constraints to prevent double-booking
- [ ] Create schedule viewing endpoints (by class, teacher)
- [ ] Implement conflict validation endpoint
- [ ] Create comprehensive API tests
- [ ] Add bulk operations support

## Technical Details

### Schedule Model Fields
```python
- id (int, auto-increment)
- class_id (int, FK to Class, required)
- teacher_id (int, FK to Teacher, required)
- subject_id (int, FK to Subject, required)
- timeslot_id (int, FK to TimeSlot, required)
- room (str, optional, e.g., "101", "Turnhalle")
- week_type (str, "ALL", "A", or "B" for alternating weeks)
- created_at (datetime)
- updated_at (datetime)
```

### Database Constraints
```sql
-- Prevent double-booking
UNIQUE(class_id, timeslot_id, week_type)
UNIQUE(teacher_id, timeslot_id, week_type)
UNIQUE(room, timeslot_id, week_type) WHERE room IS NOT NULL
```

### API Endpoints (Versioned)
- `GET /api/v1/schedule` - Get full schedule (with filters)
- `GET /api/v1/schedule/{id}` - Get single entry
- `POST /api/v1/schedule` - Create schedule entry
- `PUT /api/v1/schedule/{id}` - Update entry
- `DELETE /api/v1/schedule/{id}` - Delete entry
- `POST /api/v1/schedule/bulk` - Create multiple entries
- `DELETE /api/v1/schedule/bulk` - Delete multiple entries

### View Endpoints
- `GET /api/v1/schedule/class/{class_id}` - Get class timetable
- `GET /api/v1/schedule/teacher/{teacher_id}` - Get teacher timetable
- `GET /api/v1/schedule/room/{room}` - Get room usage
- `GET /api/v1/schedule/timeslot/{timeslot_id}` - What's happening at this time

### Validation Endpoints
- `POST /api/v1/schedule/validate` - Check for conflicts before saving
- `GET /api/v1/schedule/conflicts` - List all conflicts in current schedule
- `POST /api/v1/schedule/check-swap` - Check if two slots can be swapped

## Conflict Detection Rules
The system should detect and prevent:
1. **Teacher conflicts**: Same teacher in two places
2. **Class conflicts**: Same class with two subjects
3. **Room conflicts**: Same room booked twice
4. **Break conflicts**: No scheduling during breaks

## Response Format
```python
# Single schedule entry response
{
    "id": 1,
    "class": {"id": 1, "name": "1a"},
    "teacher": {"id": 1, "name": "Maria Müller", "abbreviation": "MUE"},
    "subject": {"id": 1, "name": "Mathematik", "code": "MA", "color": "#2563EB"},
    "timeslot": {"id": 1, "day": 1, "period": 1, "start_time": "08:00", "end_time": "08:45"},
    "room": "101",
    "week_type": "ALL"
}

# Conflict response
{
    "valid": false,
    "conflicts": [
        {
            "type": "teacher_conflict",
            "message": "Teacher 'Maria Müller' already scheduled for class 2b at this time",
            "existing_entry_id": 42
        }
    ]
}
```

## What We're NOT Implementing (Yet)
- Automatic schedule generation
- Optimization algorithms
- Substitute teacher handling
- Multi-week planning beyond A/B
- Resource scheduling (equipment, materials)
- Student group management
- Cross-class activities

## Sample Test Data
```python
# Create a math lesson for class 1a
{
    "class_id": 1,
    "teacher_id": 1,
    "subject_id": 1,  # Mathematics
    "timeslot_id": 1,  # Monday, Period 1
    "room": "101",
    "week_type": "ALL"
}

# Create alternating Religion/Ethics
{
    "class_id": 1,
    "teacher_id": 2,
    "subject_id": 8,  # Religion
    "timeslot_id": 15,  # Wednesday, Period 3
    "room": "Chapel",
    "week_type": "A"  # Only in A weeks
}
```

## Bulk Operations
Support creating/updating multiple entries at once:
```python
POST /api/v1/schedule/bulk
[
    {"class_id": 1, "teacher_id": 1, "subject_id": 1, "timeslot_id": 1},
    {"class_id": 1, "teacher_id": 1, "subject_id": 1, "timeslot_id": 2},
    {"class_id": 1, "teacher_id": 1, "subject_id": 1, "timeslot_id": 3}
]
```

## Query Parameters
Support filtering on GET endpoints:
- `?week_type=ALL` - Filter by week type
- `?day=1` - Filter by day
- `?include_breaks=false` - Exclude break periods

## Notes
- This is the most complex model - connects everything
- Database constraints ensure data integrity
- Conflict detection is critical for usability
- Room is optional string (not all lessons need specific rooms)
- Support A/B week scheduling (common in German schools)

## Dependencies
- Teacher model must be implemented
- Class model must be implemented
- Subject model must be implemented
- TimeSlot model must be implemented

## Success Criteria
- Can create schedule entries without conflicts
- Prevents all types of double-booking
- Can view schedules by class/teacher
- Conflict detection works reliably
- Bulk operations improve data entry speed
- Takes < 30 minutes to implement with conflict detection
- Test users can create a basic weekly schedule
