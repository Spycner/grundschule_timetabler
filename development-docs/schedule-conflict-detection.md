# Schedule Conflict Detection

## Overview

The Grundschule Timetabler implements comprehensive conflict detection to ensure valid timetables. The system prevents double-booking at both the application and database levels, providing immediate feedback to users when conflicts would occur.

## Types of Conflicts

### 1. Teacher Conflicts
A teacher cannot be scheduled to teach in two different places at the same time.

**Example:**
- Teacher Maria Müller is already teaching Math to class 1a in room 101 at Monday 8:00
- Attempting to schedule her for German with class 2b at the same time will be rejected

**Detection:**
- Checks if teacher_id already exists for the same timeslot_id and week_type
- Database constraint: `UNIQUE(teacher_id, timeslot_id, week_type)`

### 2. Class Conflicts
A class cannot have two different subjects scheduled at the same time.

**Example:**
- Class 1a is already scheduled for Math at Monday 8:00
- Attempting to schedule them for Sport at the same time will be rejected

**Detection:**
- Checks if class_id already exists for the same timeslot_id and week_type
- Database constraint: `UNIQUE(class_id, timeslot_id, week_type)`

### 3. Room Conflicts
A room cannot be booked for two different classes at the same time.

**Example:**
- The Turnhalle (gym) is booked for class 1a's Sport lesson at Tuesday 9:50
- Attempting to book it for class 2b at the same time will be rejected

**Detection:**
- Checks if room already exists for the same timeslot_id and week_type
- Note: Room is optional, so this only applies when a room is specified

### 4. Break Period Conflicts
No classes can be scheduled during designated break periods.

**Example:**
- Period 3 (9:30-9:50) is marked as "Große Pause" (big break)
- Any attempt to schedule a class during this period will be rejected

**Detection:**
- Checks if the timeslot has `is_break = true`
- Prevents scheduling regardless of teacher, class, or room availability

## Week Type Handling

The system supports alternating week schedules (A/B weeks), common in German schools:

- **ALL**: Entry applies to all weeks
- **A**: Entry only applies to A weeks  
- **B**: Entry only applies to B weeks

### Conflict Rules for Week Types:
- ALL conflicts with ALL, A, and B
- A conflicts with ALL and A
- B conflicts with ALL and B
- A does not conflict with B (allowing alternating schedules)

**Example Use Case:** Religion/Ethics alternation
```json
// Week A: Religion
{
  "class_id": 1,
  "teacher_id": 2,
  "subject_id": 8,  // Religion
  "timeslot_id": 15,
  "room": "Chapel",
  "week_type": "A"
}

// Week B: Ethics (same timeslot, different week)
{
  "class_id": 1,
  "teacher_id": 3,
  "subject_id": 9,  // Ethics
  "timeslot_id": 15,
  "room": "103",
  "week_type": "B"
}
```

## Implementation Layers

### 1. Application Layer (Service)
The `ScheduleService` performs conflict detection before attempting database operations:

```python
def validate_schedule(db: Session, schedule: ScheduleCreate) -> list[ConflictDetail]:
    conflicts = []
    
    # Check break period
    if timeslot.is_break:
        conflicts.append(ConflictDetail(
            type="break_conflict",
            message="Cannot schedule during break"
        ))
    
    # Check teacher conflict
    # Check class conflict  
    # Check room conflict
    
    return conflicts
```

### 2. Database Layer (Constraints)
SQLAlchemy model includes unique constraints as a safety net:

```python
__table_args__ = (
    UniqueConstraint("class_id", "timeslot_id", "week_type"),
    UniqueConstraint("teacher_id", "timeslot_id", "week_type"),
)
```

## API Endpoints for Conflict Management

### Validation Endpoint
`POST /api/v1/schedule/validate`

Check for conflicts before saving:
```bash
curl -X POST http://localhost:8000/api/v1/schedule/validate \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "teacher_id": 1,
    "subject_id": 1,
    "timeslot_id": 1,
    "room": "101",
    "week_type": "ALL"
  }'
```

Response:
```json
{
  "valid": false,
  "conflicts": [
    {
      "type": "teacher_conflict",
      "message": "Teacher is already scheduled for another class at this time",
      "existing_entry_id": 42
    }
  ]
}
```

### Conflict Detection Endpoint
`GET /api/v1/schedule/conflicts`

List all conflicts in the current schedule:
```bash
curl http://localhost:8000/api/v1/schedule/conflicts
```

### Bulk Operations
`POST /api/v1/schedule/bulk`

When creating multiple entries, all are validated first. If any conflict is detected, none are created (atomic operation).

## Error Messages

The API provides clear, actionable error messages:

- **409 Conflict**: Resource conflict detected
  - "Teacher is already scheduled at this time"
  - "Class already has a subject scheduled at this time"
  - "Room is already booked at this time"
  
- **400 Bad Request**: Invalid operation
  - "Cannot schedule during break periods"

## Best Practices

1. **Always validate before saving**: Use the `/validate` endpoint to check for conflicts before attempting to create entries

2. **Handle conflicts gracefully**: Provide users with clear information about what's conflicting and suggest alternatives

3. **Use bulk operations wisely**: When creating multiple related entries, use the bulk endpoint to ensure atomicity

4. **Consider week types**: When scheduling subjects that alternate, ensure proper A/B week assignment

5. **Room allocation**: Only specify rooms when necessary; this reduces potential conflicts

## Testing

The conflict detection system is thoroughly tested with 14 comprehensive tests covering:
- Teacher double-booking prevention
- Class double-booking prevention
- Room double-booking prevention
- Break period enforcement
- A/B week scheduling
- Bulk operation atomicity
- Validation endpoint accuracy

All tests follow TDD principles and ensure 100% coverage of conflict scenarios.

## Future Enhancements

Potential improvements for conflict detection:
- Soft conflicts (warnings vs errors)
- Configurable conflict rules per school
- Automatic conflict resolution suggestions
- Time-based room transitions (buffer time)
- Teacher preference conflicts (preferred vs available times)
- Cross-class activity coordination
