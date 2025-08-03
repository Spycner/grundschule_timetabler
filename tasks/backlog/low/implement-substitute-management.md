# Implement Substitute Management

## Priority
Low

## Created
2025-08-03

## Description
Create a comprehensive substitute teacher management system for handling teacher absences, including automatic substitute suggestions, notification system, and substitute plan generation.

## Acceptance Criteria
- [ ] Create TeacherAbsence model
- [ ] Create SubstituteAssignment model
- [ ] Implement automatic substitute finder
- [ ] Add notification system for substitutes
- [ ] Generate daily substitute plans
- [ ] Track substitute history and preferences
- [ ] Support emergency substitute pool
- [ ] Create substitute availability calendar
- [ ] Add substitute qualification matching
- [ ] Generate substitute statistics and reports

## Technical Details
### Model Structure
```python
class TeacherAbsence:
    id: int
    teacher_id: int (FK)
    start_date: date
    end_date: date
    absence_type: Enum (SICK, TRAINING, PERSONAL, OTHER)
    substitute_required: bool
    notes: str (optional)
    
class SubstituteAssignment:
    id: int
    absence_id: int (FK)
    schedule_id: int (FK)
    substitute_teacher_id: int (FK, optional)
    assignment_type: Enum (TEACHER, CANCELLATION, SELF_STUDY, COMBINED)
    instructions: str (optional)
    confirmed: bool
    
class SubstitutePool:
    teacher_id: int (FK)
    available_from: time
    available_until: time
    weekdays: List[int]
    max_substitutions_per_week: int
```

### Substitute Finding Algorithm
1. Check subject qualification match
2. Check teacher availability (free period)
3. Check substitute pool
4. Check part-time teachers for extra hours
5. Consider combining classes
6. Last resort: supervised self-study

### Assignment Priority
1. Same subject qualified teacher
2. Class's regular teachers (Klassenlehrer)
3. Any qualified teacher
4. Emergency substitute pool
5. Administrative supervision

### API Endpoints
- `POST /api/v1/absences` - Report absence
- `GET /api/v1/absences/current` - Current absences
- `POST /api/v1/substitutes/find` - Find substitutes
- `POST /api/v1/substitutes/assign` - Assign substitute
- `GET /api/v1/substitutes/plan/{date}` - Daily plan
- `POST /api/v1/substitutes/notify` - Send notifications
- `GET /api/v1/substitutes/statistics` - Statistics

### Notification System
- Email notifications to substitutes
- SMS for urgent substitutions
- Dashboard alerts
- Printable substitute plans
- Parent notifications for cancellations

## Dependencies
- Complete Schedule model
- Teacher availability system
- Teacher-subject assignments
- Notification service (email/SMS)

## Substitute Plan Features
### Daily Overview
- List of absences
- Substitute assignments
- Room changes
- Cancelled lessons
- Combined classes
- Special instructions

### Individual Plans
- Per-substitute schedule
- Original teacher's notes
- Class information
- Room locations
- Materials location

### Distribution
- Email to affected teachers
- Print for notice boards
- Parent app updates
- Student information system

## German Specific Requirements
- **Vertretungsplan** - Official substitute plan
- **Aufsichtspflicht** - Supervision duty requirements
- **Freistunde** - Free period utilization
- **Klassenzusammenlegung** - Class combination rules
- **Randstunden** - First/last period cancellation rules

## Notes
- Legal requirements for supervision must be met
- Consider union agreements on substitute duties
- Track substitute hours for compensation
- Emergency contact list maintenance
- Consider data privacy for absence reasons
