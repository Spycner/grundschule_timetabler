# Implement Teacher-Subject Assignment

## Priority
High

## Created
2025-08-03

## Description
Create a system to manage which teachers are qualified and assigned to teach specific subjects, including primary and secondary qualifications.

## Acceptance Criteria
- [ ] Create TeacherSubject association model
- [ ] Support qualification levels (primary, secondary, substitute)
- [ ] Add endpoints for managing assignments
- [ ] Validate teacher qualifications in scheduling
- [ ] Support subject-specific constraints (e.g., Sport requires certification)
- [ ] Handle Klassenlehrer (class teacher) assignments
- [ ] Create overview of teaching assignments
- [ ] Add workload calculation per teacher
- [ ] Support team teaching scenarios
- [ ] Generate qualification matrix reports

## Technical Details
### Model Structure
```python
class TeacherSubject:
    teacher_id: int (FK)
    subject_id: int (FK)
    qualification_level: Enum (PRIMARY, SECONDARY, SUBSTITUTE)
    max_hours_per_week: int (optional)
    grades: List[int] (which grades can teach)
    certification_date: date (optional)
    certification_expires: date (optional)
```

### API Endpoints
- `GET /api/v1/teachers/{id}/subjects` - Get teacher's subjects
- `POST /api/v1/teachers/{id}/subjects` - Assign subject
- `DELETE /api/v1/teachers/{id}/subjects/{subject_id}` - Remove assignment
- `GET /api/v1/subjects/{id}/teachers` - Get qualified teachers
- `GET /api/v1/teacher-subjects/matrix` - Qualification overview

### Business Rules
- Primary qualification: Preferred for scheduling
- Secondary qualification: Can teach if needed
- Substitute qualification: Only for emergencies
- Special subjects may require certifications
- Klassenlehrer must be qualified for core subjects

## Dependencies
- Teacher model must be complete
- Subject model must be complete
- Schedule model should integrate qualifications

## Notes
- German system distinguishes between Fachlehrer and Klassenlehrer
- Some subjects require special certifications (e.g., Sport, Religion)
- Consider workload distribution fairness
- May need to track professional development for maintaining qualifications
