# Implement Schedule Validation Rules

## Priority
Medium

## Created
2025-08-03

## Description
Create a comprehensive validation rule system that ensures schedules meet all educational, legal, and pedagogical requirements specific to German elementary schools.

## Acceptance Criteria
- [ ] Create ValidationRule model with configurable rules
- [ ] Implement rule engine for checking compliance
- [ ] Support state-specific regulations
- [ ] Add curriculum requirement validation
- [ ] Create custom rule builder
- [ ] Generate validation reports
- [ ] Support rule overrides with justification
- [ ] Add rule templates for different states
- [ ] Implement warning vs error severity levels
- [ ] Create rule testing framework

## Technical Details
### Model Structure
```python
class ValidationRule:
    id: int
    name: str
    category: Enum (LEGAL, PEDAGOGICAL, ADMINISTRATIVE, CUSTOM)
    severity: Enum (ERROR, WARNING, INFO)
    rule_type: Enum (see below)
    parameters: JSON
    applicable_to: List[str] (grades, subjects, etc.)
    state_specific: str (optional, e.g., "HE", "NRW")
    active: bool
    
class RuleType(Enum):
    MAX_HOURS_PER_DAY = "max_daily_hours"
    MIN_HOURS_PER_DAY = "min_daily_hours"
    MAX_CONSECUTIVE_HOURS = "max_consecutive"
    REQUIRED_WEEKLY_HOURS = "required_hours"
    BREAK_REQUIREMENTS = "break_rules"
    SUBJECT_DISTRIBUTION = "distribution"
    TEACHER_WORKLOAD = "workload"
    CURRICULUM_COMPLIANCE = "curriculum"
```

### Core Validation Rules
#### Legal Requirements
- Maximum 6 lessons per day (grades 1-2)
- Maximum 8 lessons per day (grades 3-4)
- Minimum 5-minute break between lessons
- 20-minute break after 2 lessons
- Maximum teaching hours per teacher per week

#### Pedagogical Rules
- Core subjects in morning (Deutsch, Mathematik)
- Sport not directly after eating
- Maximum 2 consecutive hours same subject
- Art/Music distributed across week
- Religion/Ethics at appropriate times

#### Curriculum Requirements
- Minimum weekly hours per subject per grade
- Required subjects must be scheduled
- Förderunterricht allocation
- AG (activity group) time slots

### API Endpoints
- `GET /api/v1/validation/rules` - List all rules
- `POST /api/v1/validation/rules` - Create custom rule
- `POST /api/v1/validation/check` - Validate schedule
- `GET /api/v1/validation/report/{schedule_id}` - Validation report
- `POST /api/v1/validation/override` - Override with reason
- `GET /api/v1/validation/templates/{state}` - State templates

### Validation Process
```python
def validate_schedule(schedule: Schedule) -> ValidationReport:
    results = []
    for rule in active_rules:
        if rule.applies_to(schedule):
            result = rule.check(schedule)
            results.append(result)
    return ValidationReport(results)
```

### Validation Report Structure
```json
{
  "valid": false,
  "errors": [
    {
      "rule": "MAX_HOURS_PER_DAY",
      "message": "Class 1a has 7 lessons on Monday (max: 6)",
      "severity": "ERROR",
      "affected_entities": ["class:1a", "day:Monday"]
    }
  ],
  "warnings": [
    {
      "rule": "SUBJECT_DISTRIBUTION",
      "message": "Mathematics clustered on Mon-Tue",
      "severity": "WARNING"
    }
  ],
  "statistics": {
    "total_rules_checked": 25,
    "passed": 20,
    "failed": 3,
    "warnings": 2
  }
}
```

## Dependencies
- Complete Schedule model
- All entity models
- State-specific regulation database

## State-Specific Rules
### Hessen (HE)
- Stundentafel requirements
- Förderunterricht allocation
- Ganztag regulations

### Nordrhein-Westfalen (NRW)  
- Different hour requirements
- Inclusion support hours
- OGS (Offene Ganztagsschule) rules

### Bayern (BY)
- Intensivierungsstunden
- Flexible Grundschule rules
- Different break patterns

## Custom Rules
Allow schools to create custom rules:
```json
{
  "name": "No Math on Fridays",
  "rule_type": "CUSTOM",
  "parameters": {
    "subject": "Mathematics",
    "blocked_days": ["Friday"]
  },
  "severity": "WARNING",
  "reason": "School policy"
}
```

## Override System
- Require justification for overrides
- Track who approved override
- Generate override report
- Time-limited overrides

## Notes
- Rules should be configurable per school
- Consider transition periods for rule changes
- Support experimental schedules with relaxed rules
- Generate compliance certificates
- Regular updates for regulation changes
