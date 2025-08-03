# MVP Domain Models

## Overview
Simplified domain models focused on getting a working prototype quickly. These models prioritize simplicity and testability over completeness.

## Core Entities (Phase 1)

### 1. Teacher (Lehrer)
Basic teacher representation for scheduling.

```python
class Teacher:
    id: int
    first_name: str
    last_name: str
    email: str
    abbreviation: str  # e.g., "MUE" for Müller
    max_hours_per_week: int
    is_part_time: bool
    created_at: datetime
    updated_at: datetime
```

**Key Points:**
- No complex availability modeling yet
- Simple part-time flag instead of percentage
- Abbreviation for display in schedule grid

### 2. Class (Klasse)
Represents a group of students.

```python
class Class:
    id: int
    name: str  # e.g., "1a", "2b"
    grade: int  # 1-4 for Grundschule
    size: int  # number of students
    home_room: str  # e.g., "101", "Turnhalle"
    created_at: datetime
    updated_at: datetime
```

**Key Points:**
- Room is just a string for now (not a separate entity)
- No complex grouping or splitting yet
- Grade stored for future curriculum requirements

### 3. Subject (Fach)
School subjects with basic requirements.

```python
class Subject:
    id: int
    name: str  # e.g., "Mathematik"
    code: str  # e.g., "MA"
    color: str  # for UI display, e.g., "#FF5733"
    created_at: datetime
    updated_at: datetime
```

**Key Points:**
- No grade-specific hours yet (add based on user feedback)
- Color for visual distinction in schedule
- Simple code for grid display

### 4. TimeSlot (Zeitfenster)
Represents a period in the weekly schedule.

```python
class TimeSlot:
    id: int
    day: int  # 1=Monday, 5=Friday
    period: int  # 1=first period, 2=second, etc.
    start_time: time  # e.g., 08:00
    end_time: time  # e.g., 08:45
    is_break: bool  # true for breaks
    created_at: datetime
    updated_at: datetime
```

**Key Points:**
- Fixed 45-minute periods initially
- Breaks marked but schedule continues
- Week-based (no specific dates yet)

### 5. Schedule (Stundenplan)
Links everything together - the actual timetable entries.

```python
class Schedule:
    id: int
    class_id: int  # FK to Class
    teacher_id: int  # FK to Teacher
    subject_id: int  # FK to Subject
    timeslot_id: int  # FK to TimeSlot
    room: str  # Simple string for now
    week_type: str  # "A", "B", or "ALL" for alternating weeks
    created_at: datetime
    updated_at: datetime
    
    # Unique constraint on (class_id, timeslot_id, week_type)
    # Unique constraint on (teacher_id, timeslot_id, week_type)
    # Unique constraint on (room, timeslot_id, week_type) if room is not null
```

**Key Points:**
- This is where actual assignments happen
- Supports A/B week schedules (common in German schools)
- Room as string allows flexibility without room entity
- Unique constraints prevent double-bookings

## Simplified Relationships

```
Teacher --< Schedule >-- Class
            |    |
            v    v
        Subject TimeSlot
```

- A Schedule entry connects one teacher, class, subject, and timeslot
- Multiple schedule entries form the complete timetable
- Constraints enforced at database level prevent conflicts

## What We're NOT Modeling (Yet)

1. **Teacher Qualifications**: Assuming any teacher can teach any subject
2. **Room Types**: Rooms are just strings, no capacity or features
3. **Complex Availability**: No detailed time windows
4. **Curriculum Requirements**: No grade-specific hour requirements
5. **Substitutes**: No special handling, just change the teacher
6. **Student Groups**: No splitting classes for subjects

## Migration Path to Complex Models

When user feedback indicates need:

1. **Room becomes entity** when we need capacity/features
2. **TeacherSubject** link table when qualifications matter
3. **SubjectRequirement** when curriculum hours are needed
4. **Availability** model when simple part-time isn't enough
5. **ClassGroup** when splitting classes is required

## Database Considerations

### Indexes Needed
- `schedule.class_id, schedule.timeslot_id` (conflict detection)
- `schedule.teacher_id, schedule.timeslot_id` (conflict detection)
- `schedule.timeslot_id` (schedule display)
- `timeslot.day, timeslot.period` (ordering)

### Sample Data for Testing
- 10 teachers (2 part-time)
- 8 classes (2 per grade)
- 10 subjects (core + specials)
- 30 timeslots (6 periods × 5 days)
- ~200 schedule entries (partially filled)

## API Endpoints (Basic CRUD)

All endpoints are versioned under `/api/v1` prefix.

### Teachers
- `GET /api/v1/teachers` - List all
- `GET /api/v1/teachers/{id}` - Get one
- `POST /api/v1/teachers` - Create
- `PUT /api/v1/teachers/{id}` - Update
- `DELETE /api/v1/teachers/{id}` - Delete

### Classes
- `GET /api/v1/classes` - List all
- `GET /api/v1/classes/{id}` - Get one
- `POST /api/v1/classes` - Create
- `PUT /api/v1/classes/{id}` - Update
- `DELETE /api/v1/classes/{id}` - Delete

### Subjects
- `GET /api/v1/subjects` - List all
- `GET /api/v1/subjects/{id}` - Get one
- `POST /api/v1/subjects` - Create
- `PUT /api/v1/subjects/{id}` - Update
- `DELETE /api/v1/subjects/{id}` - Delete

### TimeSlots
- `GET /api/v1/timeslots` - List all
- `GET /api/v1/timeslots/{id}` - Get one
- `POST /api/v1/timeslots` - Create
- `PUT /api/v1/timeslots/{id}` - Update
- `DELETE /api/v1/timeslots/{id}` - Delete

### Schedule
- `GET /api/v1/schedule` - Get full schedule
- `GET /api/v1/schedule/class/{class_id}` - Class schedule
- `GET /api/v1/schedule/teacher/{teacher_id}` - Teacher schedule
- `POST /api/v1/schedule` - Create entry
- `PUT /api/v1/schedule/{id}` - Update entry
- `DELETE /api/v1/schedule/{id}` - Delete entry
- `POST /api/v1/schedule/validate` - Check for conflicts

## Success Metrics for MVP

1. Can create a basic weekly schedule
2. Prevents double-booking of teachers
3. Prevents double-booking of classes
4. Can export to PDF/Excel
5. Takes < 30 minutes to input a small school
6. Gets positive feedback from test users
