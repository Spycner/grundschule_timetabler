# Grundschule Timetabler API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## API Version
Current version: `v1`

All endpoints are prefixed with `/api/v1/`

## Authentication
Currently no authentication required (development phase)

## Response Format
All responses are in JSON format with appropriate HTTP status codes.

## Endpoints

### Health Check

#### GET /health
Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET /health/ready
Database connectivity check.

**Response:**
```json
{
  "status": "ready",
  "database": "connected"
}
```

---

### Teachers

#### GET /api/v1/teachers
List all teachers with optional pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Müller",
    "email": "maria.mueller@schule.de",
    "abbreviation": "MUE",
    "max_hours_per_week": 28,
    "is_part_time": false,
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

#### GET /api/v1/teachers/{id}
Get a specific teacher by ID.

#### POST /api/v1/teachers
Create a new teacher.

**Request Body:**
```json
{
  "first_name": "Maria",
  "last_name": "Müller",
  "email": "maria.mueller@schule.de",
  "abbreviation": "MUE",
  "max_hours_per_week": 28,
  "is_part_time": false
}
```

#### PUT /api/v1/teachers/{id}
Update a teacher (partial update supported).

#### DELETE /api/v1/teachers/{id}
Delete a teacher.

---

### Teacher Availability

Manage when teachers are available to teach, including part-time schedules, blocked periods, and preferences.

#### GET /api/v1/teachers/{teacher_id}/availability
Get all availability entries for a specific teacher.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Query Parameters:**
- `weekday` (int, optional): Filter by weekday (0=Monday, 4=Friday)
- `period` (int, optional): Filter by period (1-8)
- `active_date` (date, optional): Filter by active date (ISO format: YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "teacher_id": 1,
    "weekday": 0,
    "period": 1,
    "availability_type": "AVAILABLE",
    "effective_from": "2020-01-01",
    "effective_until": null,
    "reason": null,
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  },
  {
    "id": 2,
    "teacher_id": 1,
    "weekday": 2,
    "period": 3,
    "availability_type": "BLOCKED",
    "effective_from": "2020-01-01",
    "effective_until": "2020-06-30",
    "reason": "Staff meeting",
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

#### POST /api/v1/teachers/{teacher_id}/availability
Create a new availability entry for a teacher.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Request Body:**
```json
{
  "weekday": 0,
  "period": 1,
  "availability_type": "BLOCKED",
  "effective_from": "2020-01-01",
  "effective_until": "2020-06-30",
  "reason": "Administrative duties"
}
```

**Availability Types:**
- `AVAILABLE`: Teacher can teach during this period
- `BLOCKED`: Teacher cannot teach (meetings, other duties)
- `PREFERRED`: Teacher prefers to teach (soft constraint for optimization)

**Validation Rules:**
- `weekday`: 0-4 (Monday to Friday)
- `period`: 1-8
- `effective_until` must be after `effective_from` if provided
- Unique constraint: One entry per teacher/weekday/period/effective_from

#### PUT /api/v1/teachers/{teacher_id}/availability/{availability_id}
Update an existing availability entry.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID
- `availability_id` (int): The availability entry ID

**Request Body (all fields optional):**
```json
{
  "availability_type": "PREFERRED",
  "reason": "Updated reason"
}
```

#### DELETE /api/v1/teachers/{teacher_id}/availability/{availability_id}
Delete an availability entry.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID
- `availability_id` (int): The availability entry ID

**Response:** 204 No Content

#### POST /api/v1/teachers/availability/bulk
Create multiple availability entries for a teacher at once.

**Request Body:**
```json
{
  "teacher_id": 1,
  "availabilities": [
    {
      "weekday": 0,
      "period": 1,
      "availability_type": "AVAILABLE",
      "effective_from": "2020-01-01"
    },
    {
      "weekday": 0,
      "period": 2,
      "availability_type": "AVAILABLE",
      "effective_from": "2020-01-01"
    },
    {
      "weekday": 1,
      "period": 1,
      "availability_type": "BLOCKED",
      "effective_from": "2020-01-01",
      "reason": "Part-time schedule"
    }
  ]
}
```

**Response:**
```json
{
  "created_count": 3,
  "entries": [/* array of created availability entries */]
}
```

#### GET /api/v1/teachers/{teacher_id}/availability/overview
Get an overview of a teacher's availability patterns.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Query Parameters:**
- `active_date` (date, optional): Date to check availability for (default: today)

**Response:**
```json
{
  "teacher_id": 1,
  "teacher_name": "Maria Müller",
  "is_part_time": false,
  "max_hours_per_week": 28,
  "available_hours": 20,
  "blocked_hours": 5,
  "preferred_hours": 3,
  "availability_by_day": {
    "0": {"available": 4, "blocked": 1, "preferred": 1},
    "1": {"available": 4, "blocked": 1, "preferred": 0},
    "2": {"available": 4, "blocked": 1, "preferred": 1},
    "3": {"available": 4, "blocked": 1, "preferred": 1},
    "4": {"available": 4, "blocked": 1, "preferred": 0}
  }
}
```

#### GET /api/v1/teachers/{teacher_id}/availability/validate
Validate a teacher's availability against constraints (e.g., part-time limits).

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Query Parameters:**
- `active_date` (date, optional): Date to validate for (default: today)

**Response:**
```json
{
  "teacher_id": 1,
  "max_hours_per_week": 20,
  "available_hours": 20,
  "scheduled_hours": 15,
  "is_valid": true,
  "warnings": [
    "Part-time teacher has 20 available hours but max is 20"
  ],
  "conflicts": []
}
```

#### GET /api/v1/teachers/availability/overview
Get availability overview for all teachers.

**Query Parameters:**
- `active_date` (date, optional): Date to check availability for (default: today)

**Response:**
```json
{
  "teachers": [
    {
      "teacher_id": 1,
      "teacher_name": "Maria Müller",
      "is_part_time": false,
      "max_hours_per_week": 28,
      "available_hours": 20,
      "blocked_hours": 5,
      "preferred_hours": 3,
      "availability_by_day": {/* ... */}
    },
    {
      "teacher_id": 2,
      "teacher_name": "Hans Schmidt",
      "is_part_time": true,
      "max_hours_per_week": 15,
      "available_hours": 15,
      "blocked_hours": 10,
      "preferred_hours": 0,
      "availability_by_day": {/* ... */}
    }
  ],
  "total": 2
}
```

**Use Cases:**
1. **Part-time Teacher Management**: Track when part-time teachers work (e.g., only Monday-Wednesday)
2. **Meeting Schedules**: Block periods for staff meetings, planning time
3. **Optimization Hints**: Mark preferred teaching times for schedule optimization
4. **Temporary Absences**: Use date ranges for known absences (Elternzeit, training)

---

### Teacher-Subject Assignments

Manage which teachers are qualified to teach specific subjects, including qualification levels, grade restrictions, and certifications.

#### GET /api/v1/teachers/{teacher_id}/subjects
Get all subject qualifications for a specific teacher.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Response:**
```json
[
  {
    "id": 1,
    "teacher_id": 1,
    "subject_id": 1,
    "qualification_level": "PRIMARY",
    "grades": [1, 2, 3, 4],
    "max_hours_per_week": 10,
    "certification_date": "2020-09-01",
    "certification_expires": "2025-08-31",
    "certification_document": "Sport Teaching Certificate",
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00",
    "subject": {
      "id": 1,
      "name": "Sport",
      "code": "SP",
      "color": "#10B981"
    }
  }
]
```

#### POST /api/v1/teachers/{teacher_id}/subjects
Assign a subject qualification to a teacher.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Request Body:**
```json
{
  "subject_id": 1,
  "qualification_level": "PRIMARY",
  "grades": [1, 2, 3, 4],
  "max_hours_per_week": 10,
  "certification_date": "2020-09-01",
  "certification_expires": "2025-08-31",
  "certification_document": "Sport Teaching Certificate"
}
```

**Qualification Levels:**
- `PRIMARY`: Teacher's main subject specialization (preferred for scheduling)
- `SECONDARY`: Teacher can teach this subject competently
- `SUBSTITUTE`: Teacher can cover this subject in emergencies only

**Validation Rules:**
- `grades`: Array of integers 1-4 (Grundschule grades)
- `max_hours_per_week`: Optional hours limit for this subject
- `certification_expires`: Must be after `certification_date` if provided
- Unique constraint: One qualification per teacher-subject pair

#### PUT /api/v1/teachers/{teacher_id}/subjects/{subject_id}
Update a teacher-subject qualification.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID
- `subject_id` (int): The subject's ID

**Request Body (all fields optional):**
```json
{
  "qualification_level": "SECONDARY",
  "grades": [3, 4],
  "max_hours_per_week": 8
}
```

#### DELETE /api/v1/teachers/{teacher_id}/subjects/{subject_id}
Remove a subject qualification from a teacher.

**Response:** 204 No Content

#### GET /api/v1/teachers/{teacher_id}/workload
Get teacher's workload calculation across all subject assignments.

**Path Parameters:**
- `teacher_id` (int): The teacher's ID

**Response:**
```json
{
  "teacher_id": 1,
  "total_assigned_hours": 18,
  "max_hours_per_week": 28,
  "available_hours": 10,
  "subjects": [
    {
      "subject_id": 1,
      "subject_name": "Mathematik",
      "qualification_level": "PRIMARY",
      "max_hours_per_week": 10,
      "grades": [1, 2]
    },
    {
      "subject_id": 2,
      "subject_name": "Deutsch",
      "qualification_level": "SECONDARY",
      "max_hours_per_week": 8,
      "grades": [1, 2, 3, 4]
    }
  ]
}
```

#### GET /api/v1/subjects/{subject_id}/teachers
Get all teachers qualified for a specific subject.

**Path Parameters:**
- `subject_id` (int): The subject's ID

**Response:**
```json
[
  {
    "id": 1,
    "teacher_id": 1,
    "subject_id": 1,
    "qualification_level": "PRIMARY",
    "grades": [1, 2, 3, 4],
    "max_hours_per_week": 10,
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00",
    "teacher": {
      "id": 1,
      "first_name": "Maria",
      "last_name": "Müller",
      "abbreviation": "MUE",
      "max_hours_per_week": 28,
      "is_part_time": false
    }
  }
]
```

**Note:** Results are automatically sorted by qualification level (PRIMARY first, then SECONDARY, then SUBSTITUTE).

#### GET /api/v1/subjects/{subject_id}/teachers/by-grade/{grade}
Get teachers qualified for a subject at a specific grade level.

**Path Parameters:**
- `subject_id` (int): The subject's ID
- `grade` (int): The grade level (1-4)

**Response:** Same format as above, filtered by teachers who can teach the specified grade.

#### GET /api/v1/teacher-subjects/matrix
Get the complete teacher-subject qualification matrix for overview and reporting.

**Response:**
```json
{
  "teachers": [
    {
      "id": 1,
      "first_name": "Maria",
      "last_name": "Müller",
      "abbreviation": "MUE"
    }
  ],
  "subjects": [
    {
      "id": 1,
      "name": "Mathematik",
      "code": "MA"
    }
  ],
  "assignments": [
    {
      "id": 1,
      "teacher_id": 1,
      "subject_id": 1,
      "qualification_level": "PRIMARY",
      "grades": [1, 2, 3, 4]
    }
  ],
  "summary": {
    "total_teachers": 8,
    "total_subjects": 9,
    "total_assignments": 25,
    "primary_qualifications": 15,
    "secondary_qualifications": 7,
    "substitute_qualifications": 3
  }
}
```

**Use Cases:**
1. **Qualification Management**: Track which teachers can teach which subjects and at what level
2. **Scheduling Validation**: Ensure only qualified teachers are assigned to subjects
3. **Workload Planning**: Calculate how many hours each teacher is committed to
4. **Certification Tracking**: Monitor expiring certifications (e.g., Sport, First Aid)
5. **German School Compliance**: Support Klassenlehrer vs Fachlehrer distinctions
6. **Grade Restrictions**: Some teachers may only be qualified for specific grades

---

### Classes

#### GET /api/v1/classes
List all classes with optional pagination.

**Response:**
```json
[
  {
    "id": 1,
    "name": "1a",
    "grade": 1,
    "size": 22,
    "home_room": "Raum 101",
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

#### GET /api/v1/classes/{id}
Get a specific class by ID.

#### POST /api/v1/classes
Create a new class.

**Request Body:**
```json
{
  "name": "1a",
  "grade": 1,
  "size": 22,
  "home_room": "Raum 101"
}
```

#### PUT /api/v1/classes/{id}
Update a class (partial update supported).

#### DELETE /api/v1/classes/{id}
Delete a class.

---

### Subjects

#### GET /api/v1/subjects
List all subjects with optional pagination.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Mathematik",
    "code": "MA",
    "color": "#2563EB",
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

#### GET /api/v1/subjects/{id}
Get a specific subject by ID.

#### POST /api/v1/subjects
Create a new subject.

**Request Body:**
```json
{
  "name": "Mathematik",
  "code": "MA",
  "color": "#2563EB"
}
```

#### PUT /api/v1/subjects/{id}
Update a subject (partial update supported).

#### DELETE /api/v1/subjects/{id}
Delete a subject.

---

### TimeSlots

#### GET /api/v1/timeslots
List all timeslots ordered by day and period.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "day": 1,
    "period": 1,
    "start_time": "08:00:00",
    "end_time": "08:45:00",
    "is_break": false,
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

**Notes:**
- Results are automatically ordered by day (1-5) and period
- `day`: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
- `is_break`: Indicates whether this is a break period (e.g., Große Pause, Kleine Pause)

#### GET /api/v1/timeslots/{id}
Get a specific timeslot by ID.

#### POST /api/v1/timeslots
Create a new timeslot.

**Request Body:**
```json
{
  "day": 1,
  "period": 1,
  "start_time": "08:00",
  "end_time": "08:45",
  "is_break": false
}
```

**Validation Rules:**
- `day` must be between 1 and 5 (Monday to Friday)
- `period` must be a positive integer
- `end_time` must be after `start_time`
- Combination of (day, period) must be unique
- Time ranges on the same day cannot overlap

#### PUT /api/v1/timeslots/{id}
Update a timeslot (partial update supported).

**Request Body:**
```json
{
  "start_time": "08:15",
  "end_time": "09:00"
}
```

#### DELETE /api/v1/timeslots/{id}
Delete a timeslot.

#### POST /api/v1/timeslots/generate-default
Generate a default weekly schedule for a German Grundschule.

**Response:**
```json
{
  "message": "Successfully generated 40 timeslots for the weekly schedule",
  "count": 40
}
```

**Generated Schedule:**
- Creates 40 timeslots (5 days × 8 periods)
- Standard German school day: 08:00 - 13:00
- Includes 2 breaks per day:
  - Große Pause: 09:30 - 09:50 (period 3)
  - Kleine Pause: 11:20 - 11:30 (period 6)
- 6 teaching periods per day (45 minutes each)

**Warning:** This endpoint clears all existing timeslots before generating the default schedule.

---

### Schedule

#### GET /api/v1/schedule
List all schedule entries with optional filters.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)
- `week_type` (string, optional): Filter by week type (ALL, A, or B)
- `day` (int, optional): Filter by day (1-5)
- `include_breaks` (bool, optional): Include break periods (default: true)

**Response:**
```json
[
  {
    "id": 1,
    "class": {"id": 1, "name": "1a", "grade": 1},
    "teacher": {"id": 1, "first_name": "Maria", "last_name": "Müller", "abbreviation": "MUE"},
    "subject": {"id": 1, "name": "Mathematik", "code": "MA", "color": "#2563EB"},
    "timeslot": {"id": 1, "day": 1, "period": 1, "start_time": "08:00", "end_time": "08:45", "is_break": false},
    "room": "101",
    "week_type": "ALL",
    "created_at": "2025-08-03T10:00:00",
    "updated_at": "2025-08-03T10:00:00"
  }
]
```

#### GET /api/v1/schedule/{id}
Get a specific schedule entry by ID.

#### POST /api/v1/schedule
Create a new schedule entry.

**Request Body:**
```json
{
  "class_id": 1,
  "teacher_id": 1,
  "subject_id": 1,
  "timeslot_id": 1,
  "room": "101",
  "week_type": "ALL"
}
```

**Validation:**
- Validates teacher qualification for the subject (PRIMARY/SECONDARY/SUBSTITUTE)
- Prevents teacher conflicts (same teacher in two places)
- Prevents class conflicts (same class with two subjects)
- Prevents room conflicts (same room booked twice)
- Prevents scheduling during break periods
- Prevents scheduling when teacher is not available (BLOCKED periods)
- `week_type` must be "ALL", "A", or "B"

#### PUT /api/v1/schedule/{id}
Update a schedule entry (partial update supported).

**Request Body:**
```json
{
  "room": "102",
  "week_type": "A"
}
```

#### DELETE /api/v1/schedule/{id}
Delete a schedule entry.

#### GET /api/v1/schedule/class/{class_id}
Get all schedule entries for a specific class.

**Query Parameters:**
- `week_type` (string, optional): Filter by week type (ALL, A, or B)

**Response:** Array of schedule entries sorted by day and period.

#### GET /api/v1/schedule/teacher/{teacher_id}
Get all schedule entries for a specific teacher.

**Query Parameters:**
- `week_type` (string, optional): Filter by week type (ALL, A, or B)

**Response:** Array of schedule entries sorted by day and period.

#### GET /api/v1/schedule/room/{room}
Get all schedule entries for a specific room.

**Query Parameters:**
- `week_type` (string, optional): Filter by week type (ALL, A, or B)

**Response:** Array of schedule entries sorted by day and period.

#### GET /api/v1/schedule/timeslot/{timeslot_id}
Get all schedule entries at a specific timeslot.

**Query Parameters:**
- `week_type` (string, optional): Filter by week type (ALL, A, or B)

#### POST /api/v1/schedule/validate
Validate a schedule entry for conflicts without saving.

**Request Body:**
```json
{
  "class_id": 1,
  "teacher_id": 1,
  "subject_id": 1,
  "timeslot_id": 1,
  "room": "101",
  "week_type": "ALL"
}
```

**Response:**
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

**Conflict Types:**
- `qualification_conflict`: Teacher is not qualified to teach this subject
- `teacher_conflict`: Teacher already scheduled
- `class_conflict`: Class already has a subject
- `room_conflict`: Room already booked
- `break_conflict`: Attempting to schedule during break
- `availability_conflict`: Teacher is not available during this period

#### GET /api/v1/schedule/conflicts
List all conflicts in the current schedule.

**Response:**
```json
[
  {
    "schedule_id": 1,
    "conflicts": [
      {
        "type": "teacher_conflict",
        "message": "Teacher is already scheduled for another class at this time",
        "existing_entry_id": 2
      }
    ]
  }
]
```

#### POST /api/v1/schedule/bulk
Create multiple schedule entries at once.

**Request Body:**
```json
[
  {
    "class_id": 1,
    "teacher_id": 1,
    "subject_id": 1,
    "timeslot_id": 1,
    "room": "101",
    "week_type": "ALL"
  },
  {
    "class_id": 1,
    "teacher_id": 1,
    "subject_id": 1,
    "timeslot_id": 2,
    "room": "101",
    "week_type": "ALL"
  }
]
```

**Response:** Array of created schedule entries.

**Note:** All entries are validated before any are created. If any conflict is detected, none are created.

### A/B Week Scheduling

The system supports alternating week schedules, common in German schools for subjects like Religion/Ethics:

- **Week Type "ALL"**: Entry applies to all weeks
- **Week Type "A"**: Entry only applies to A weeks
- **Week Type "B"**: Entry only applies to B weeks

**Example:** Religion in week A, Ethics in week B:
```json
[
  {
    "class_id": 1,
    "teacher_id": 2,
    "subject_id": 8,  // Religion
    "timeslot_id": 15,
    "room": "Chapel",
    "week_type": "A"
  },
  {
    "class_id": 1,
    "teacher_id": 3,
    "subject_id": 9,  // Ethics
    "timeslot_id": 15,
    "room": "103",
    "week_type": "B"
  }
]
```

---

## Error Responses

### 400 Bad Request
Invalid request data or validation error.

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "validation error message",
      "type": "validation_error"
    }
  ]
}
```

### 404 Not Found
Resource not found.

```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
Conflict with existing data (e.g., duplicate unique values, overlapping time ranges).

```json
{
  "detail": "Conflict description"
}
```

### 422 Unprocessable Entity
Request validation failed.

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "validation error message",
      "type": "validation_error"
    }
  ]
}
```

### 500 Internal Server Error
Server error occurred.

```json
{
  "detail": "Internal server error"
}
```

---

## Data Validation Rules

### Teacher
- `email`: Must be a valid email address
- `abbreviation`: 2-3 uppercase characters
- `max_hours_per_week`: 1-40 hours

### Class
- `name`: Required, must be unique
- `grade`: 1-4 (Grundschule grades)
- `size`: 1-35 students

### Subject
- `name`: Required, must be unique
- `code`: 2-5 uppercase characters, must be unique
- `color`: Valid hex color code (e.g., #RRGGBB)

### TimeSlot
- `day`: 1-5 (Monday to Friday)
- `period`: Positive integer
- `start_time`: Time format (HH:MM or HH:MM:SS)
- `end_time`: Time format, must be after start_time
- Unique constraint: (day, period) combination
- No overlapping time ranges on the same day

---

## Development Tools

### Interactive API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Seeders
Run seeders to populate development data:
```bash
make seed
```

This creates:
- 8 sample teachers
- 8 sample classes (2 per grade)
- 9 sample subjects
- 40 timeslots (standard weekly schedule)
- 25 teacher-subject assignments with realistic qualifications
- Sample schedule entries for class 1a (including A/B week examples)

### Testing
Run the test suite:
```bash
make test
```

Currently 104 tests covering all models and endpoints.
