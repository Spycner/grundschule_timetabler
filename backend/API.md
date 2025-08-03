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
- Prevents teacher conflicts (same teacher in two places)
- Prevents class conflicts (same class with two subjects)
- Prevents room conflicts (same room booked twice)
- Prevents scheduling during break periods
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
- `teacher_conflict`: Teacher already scheduled
- `class_conflict`: Class already has a subject
- `room_conflict`: Room already booked
- `break_conflict`: Attempting to schedule during break

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
- Sample schedule entries for class 1a (including A/B week examples)

### Testing
Run the test suite:
```bash
make test
```

Currently 74 tests covering all models and endpoints.
