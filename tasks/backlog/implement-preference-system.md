# Implement Preference System

## Priority
Low

## Created
2025-08-03

## Description
Create a comprehensive preference system that allows teachers and administrators to specify scheduling preferences, which the algorithm will try to accommodate as soft constraints.

## Acceptance Criteria
- [ ] Create Preference model for various preference types
- [ ] Support teacher time preferences
- [ ] Support pedagogical preferences
- [ ] Implement preference weight/priority system
- [ ] Create preference collection interface
- [ ] Add preference satisfaction reporting
- [ ] Support preference templates
- [ ] Implement preference conflict detection
- [ ] Create preference override mechanism
- [ ] Generate preference satisfaction metrics

## Technical Details
### Model Structure
```python
class Preference:
    id: int
    preference_type: Enum (see below)
    entity_type: Enum (TEACHER, CLASS, SUBJECT)
    entity_id: int
    preference_data: JSON
    weight: int (1-10, 10 being most important)
    reason: str (optional)
    approved_by: str (optional)
    
class PreferenceType(Enum):
    NO_EARLY_LESSONS = "no_early"
    NO_LATE_LESSONS = "no_late"
    PREFERRED_DAYS = "preferred_days"
    BLOCKED_DAYS = "blocked_days"
    MAX_LESSONS_PER_DAY = "max_per_day"
    PREFERRED_ROOMS = "preferred_rooms"
    CONSECUTIVE_LESSONS = "consecutive"
    NO_GAPS = "no_gaps"
    MORNING_SUBJECT = "morning_only"
    AFTERNOON_SUBJECT = "afternoon_only"
    AFTER_BREAK = "after_break"
    BEFORE_BREAK = "before_break"
```

### Preference Categories
#### Teacher Preferences
- Working time preferences
- Day preferences (e.g., no Fridays)
- Maximum consecutive lessons
- Preferred rooms
- Break supervision preferences

#### Pedagogical Preferences
- Difficult subjects in morning
- Sport after breaks
- Double lessons for certain subjects
- No subject twice on same day
- Even distribution across week

#### Administrative Preferences
- Room utilization optimization
- Minimize supervision gaps
- Cluster grades in areas
- Shared resource scheduling

### API Endpoints
- `GET /api/v1/preferences` - List all preferences
- `POST /api/v1/preferences` - Create preference
- `PUT /api/v1/preferences/{id}` - Update preference
- `DELETE /api/v1/preferences/{id}` - Delete preference
- `GET /api/v1/preferences/satisfaction` - Satisfaction report
- `POST /api/v1/preferences/bulk` - Bulk preference import
- `GET /api/v1/preferences/conflicts` - Detect conflicts

### Preference Processing
1. Collect all preferences
2. Check for conflicts
3. Weight preferences by priority
4. Pass to scheduling algorithm
5. Track satisfaction during solving
6. Report satisfaction metrics

## Dependencies
- Scheduling algorithm must support soft constraints
- Teacher and Class models
- Schedule validation system

## Preference Examples
### Teacher Example
```json
{
  "preference_type": "NO_EARLY_LESSONS",
  "entity_type": "TEACHER",
  "entity_id": 5,
  "preference_data": {
    "days": ["Monday", "Friday"],
    "earliest_period": 2
  },
  "weight": 8,
  "reason": "Long commute on these days"
}
```

### Pedagogical Example
```json
{
  "preference_type": "MORNING_SUBJECT",
  "entity_type": "SUBJECT",
  "entity_id": 1,
  "preference_data": {
    "latest_period": 4,
    "grades": [1, 2]
  },
  "weight": 9,
  "reason": "Mathematics requires concentration"
}
```

## Satisfaction Metrics
- Overall satisfaction percentage
- Per-teacher satisfaction
- Per-preference-type analysis
- Critical preferences missed
- Trade-off analysis

## Notes
- Balance individual vs. collective preferences
- Some preferences may be regulatory requirements
- Consider fairness in preference distribution
- May need approval workflow for certain preferences
- Document why preferences couldn't be satisfied
