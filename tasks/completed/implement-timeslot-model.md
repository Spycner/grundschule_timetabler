# Implement TimeSlot Model (MVP Version)

## Priority
High

## Created
2025-08-03

## Completed
2025-08-03

## Description
Create a TimeSlot (Zeitfenster) data model and basic CRUD API endpoints. TimeSlots define the weekly schedule grid structure with periods and breaks.

## Acceptance Criteria
- [ ] Create simple TimeSlot SQLAlchemy model
- [ ] Create basic Pydantic schemas
- [ ] Implement basic CRUD endpoints
- [ ] Add day and period ordering
- [ ] Mark break periods
- [ ] Create basic API tests
- [ ] Add validation for time ranges

## Technical Details

### Simplified TimeSlot Model Fields
```python
- id (int, auto-increment)
- day (int, 1=Monday to 5=Friday)
- period (int, 1=first period, 2=second, etc.)
- start_time (time, e.g., 08:00)
- end_time (time, e.g., 08:45)
- is_break (bool, default: False)
- created_at (datetime)
- updated_at (datetime)
```

### Basic API Endpoints (Versioned)
- `GET /api/v1/timeslots` - List all timeslots (ordered by day, period)
- `GET /api/v1/timeslots/{id}` - Get timeslot details
- `POST /api/v1/timeslots` - Create new timeslot
- `PUT /api/v1/timeslots/{id}` - Update timeslot
- `DELETE /api/v1/timeslots/{id}` - Delete timeslot
- `POST /api/v1/timeslots/generate-default` - Generate standard week

### MVP Validation Rules
- day must be between 1 and 5 (Monday to Friday)
- period must be positive integer
- end_time must be after start_time
- Unique constraint on (day, period) combination
- No overlapping time ranges on same day

## Default Schedule Template
Standard German Grundschule schedule:
```python
# Monday-Friday typical structure
Period 1: 08:00 - 08:45
Period 2: 08:45 - 09:30
Break:    09:30 - 09:50 (Große Pause)
Period 3: 09:50 - 10:35
Period 4: 10:35 - 11:20
Break:    11:20 - 11:30 (Kleine Pause)
Period 5: 11:30 - 12:15
Period 6: 12:15 - 13:00
```

## What We're NOT Implementing (Yet)
- Different schedules per grade
- Saturday classes
- Flexible period lengths
- Holiday calendar integration
- Special event scheduling
- Before/after school care times
- Lunch break scheduling

## Sample Test Data
```python
{
    "day": 1,  # Monday
    "period": 1,
    "start_time": "08:00",
    "end_time": "08:45",
    "is_break": false
}

{
    "day": 1,  # Monday
    "period": 3,
    "start_time": "09:30",
    "end_time": "09:50",
    "is_break": true  # Große Pause
}
```

## Helper Endpoint: Generate Default
The `/api/v1/timeslots/generate-default` endpoint should create a standard week:
- 6 periods per day
- 2 breaks per day
- Monday through Friday
- Total: 30 timeslots (5 days × 6 periods)

## Notes
- Keep periods fixed at 45 minutes initially
- Breaks are included in the grid but marked with is_break flag
- No weekend support in MVP
- Times stored as time type, not datetime (no dates)
- Order by day and period for display

## Dependencies
- Backend setup must be complete ✅
- Database configuration ready ✅

## Success Criteria
- Can create, read, update, delete timeslots
- Can generate a default weekly schedule
- Prevents time overlaps on same day
- Validates day and period ranges
- Takes < 10 minutes to implement with default generator
- Schedule grid displays correctly with breaks marked
