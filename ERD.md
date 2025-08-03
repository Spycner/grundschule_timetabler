# Entity Relationship Diagram (ERD)
## Grundschule Timetabler Domain Model

## Entity Relationship Diagram

### Core Entities

**TEACHER**
- `id` (Primary Key)
- `first_name`, `last_name`
- `email` (Unique), `abbreviation` (Unique)
- `max_hours_per_week` (default: 28)
- `is_part_time` (boolean)

**CLASS** 
- `id` (Primary Key)
- `name` (Unique), `grade` (1-4)
- `size`, `home_room`

**SUBJECT**
- `id` (Primary Key) 
- `name` (Unique), `code` (Unique)
- `color` (hex format for UI)

**TIMESLOT**
- `id` (Primary Key)
- `day` (1-5: Mon-Fri), `period` (1-8)
- `start_time`, `end_time`, `is_break`

### Central Scheduling Entity

**SCHEDULE** *(Links all core entities)*
- `id` (Primary Key)
- `class_id` → CLASS.id
- `teacher_id` → TEACHER.id  
- `subject_id` → SUBJECT.id
- `timeslot_id` → TIMESLOT.id
- `room` (optional)
- `week_type` (ALL/A/B for alternating weeks)

### Constraint & Qualification Entities

**TEACHER_AVAILABILITY** *(When teachers can teach)*
- `id` (Primary Key)
- `teacher_id` → TEACHER.id
- `weekday` (0-4), `period` (1-8)
- `availability_type` (AVAILABLE/BLOCKED/PREFERRED)
- `effective_from`, `effective_until`

**TEACHER_SUBJECT** *(Teacher qualifications)*
- `id` (Primary Key)
- `teacher_id` → TEACHER.id
- `subject_id` → SUBJECT.id
- `qualification_level` (PRIMARY/SECONDARY/SUBSTITUTE)  
- `grades` (JSON array: [1,2,3,4])
- `certification_date`, `certification_expires`

### Relationships

```
TEACHER ──┬── 1:N ── SCHEDULE
          ├── 1:N ── TEACHER_AVAILABILITY  
          └── 1:N ── TEACHER_SUBJECT

CLASS ────── 1:N ── SCHEDULE

SUBJECT ──┬── 1:N ── SCHEDULE
          └── 1:N ── TEACHER_SUBJECT

TIMESLOT ─── 1:N ── SCHEDULE
```

## Constraints and Business Rules

### Database Constraints

#### TIMESLOT Constraints
- **Unique Constraint**: `(day, period)` - One timeslot per day/period combination
- **Check Constraints**: 
  - `day >= 1 AND day <= 5` (Monday to Friday)
  - `period >= 1 AND period <= 8` (up to 8 periods per day)

#### SCHEDULE Constraints
- **Unique Constraint**: `(class_id, timeslot_id, week_type)` - Prevents double-booking of classes
- **Unique Constraint**: `(teacher_id, timeslot_id, week_type)` - Prevents double-booking of teachers
- **Week Types**: `ALL` (every week), `A` (A-week), `B` (B-week) for alternating schedules

#### TEACHER_AVAILABILITY Constraints
- **Unique Constraint**: `(teacher_id, weekday, period, effective_from)` - One availability entry per time slot
- **Check Constraints**:
  - `weekday >= 0 AND weekday <= 4` (Monday=0 to Friday=4)
  - `period >= 1 AND period <= 8`
- **Date Validation**: `effective_until >= effective_from` (if set)

#### TEACHER_SUBJECT Constraints
- **Unique Constraint**: `(teacher_id, subject_id)` - One qualification record per teacher-subject pair
- **Grades Validation**: Array of integers 1-4 (Grundschule grades)
- **Hours Validation**: `max_hours_per_week BETWEEN 1 AND 30`
- **Certification Validation**: `certification_expires >= certification_date` (if both set)

### Enumerations

#### AvailabilityType
- `AVAILABLE` - Teacher is available to teach (default)
- `BLOCKED` - Teacher cannot teach (meetings, other duties)
- `PREFERRED` - Teacher prefers to teach (soft constraint for optimization)

#### QualificationLevel
- `PRIMARY` - Hauptfach: Full qualification, preferred for scheduling
- `SECONDARY` - Nebenfach: Can teach if needed
- `SUBSTITUTE` - Vertretung: Emergency/substitute only

### Business Logic Constraints

#### Teacher Constraints
- **Max Hours**: Teachers have `max_hours_per_week` limit (default 28)
- **Part-time**: `is_part_time` flag affects scheduling constraints
- **Abbreviation**: 3-character unique identifier for UI display

#### Class Constraints
- **Grades**: Limited to 1-4 (Grundschule)
- **Home Room**: Optional default room assignment

#### Subject Constraints
- **Color Coding**: Hex color format for UI visualization
- **Subject Codes**: 4-character unique codes (e.g., "MATH", "DEUT")

#### Scheduling Constraints
- **Room Conflicts**: Not enforced at DB level (rooms are strings, can be shared)
- **Teacher Qualifications**: Schedule validates teacher can teach subject
- **Teacher Availability**: Schedule respects availability windows
- **Time Conflicts**: Hard constraints prevent double-booking

### Relationship Cardinalities

- **Teacher : Schedule** = 1:N (One teacher teaches many lessons)
- **Class : Schedule** = 1:N (One class has many lessons)  
- **Subject : Schedule** = 1:N (One subject taught in many lessons)
- **TimeSlot : Schedule** = 1:N (One timeslot can have many lessons across classes)
- **Teacher : TeacherAvailability** = 1:N (One teacher has many availability entries)
- **Teacher : TeacherSubject** = 1:N (One teacher qualified for many subjects)
- **Subject : TeacherSubject** = 1:N (One subject taught by many teachers)

### Indexes for Performance

#### Primary Indexes
- All primary keys (`id` columns)
- Unique constraints automatically create indexes

#### Secondary Indexes
- `teachers.email` - User lookup
- `teachers.abbreviation` - UI display
- `classes.name` - Class lookup
- `subjects.code` - Subject lookup  
- `schedule.class_id, teacher_id, subject_id, timeslot_id, room` - Query optimization
- `teacher_availability.teacher_id, weekday, period, effective_from` - Availability checks
- `teacher_subject.teacher_id, subject_id` - Qualification lookups

## German Education Domain Context

### Time Structure
- **Schulwoche**: School week (Monday-Friday, 5 days)
- **Unterrichtsstunden**: Lesson periods (typically 8 per day max)
- **Pausenzeiten**: Break periods marked with `is_break=true`

### Teacher Types
- **Vollzeit**: Full-time teachers (`is_part_time=false`, max 28 hours)
- **Teilzeit**: Part-time teachers (`is_part_time=true`, reduced hours)
- **Fachlehrer**: Subject specialists (qualified for specific subjects)
- **Klassenlehrer**: Class teachers (primary responsibility for one class)

### Subject Categories
- **Kernfächer**: Core subjects (Deutsch, Mathematik, Sachunterricht)
- **Nebenfächer**: Secondary subjects (Sport, Musik, Kunst)
- **Wahlpflichtfächer**: Elective subjects (Religion, Ethik)

### Scheduling Patterns
- **Wochenplan**: Weekly schedule pattern
- **A/B-Wochen**: Alternating week schedules (week_type field)
- **Vertretungsplan**: Substitute schedule management (via availability system)
