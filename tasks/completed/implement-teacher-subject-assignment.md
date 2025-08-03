# Implement Teacher-Subject Assignment

## Priority
High

## Created
2025-08-03

## Completed
2025-08-03

## Description
Create a system to manage which teachers are qualified and assigned to teach specific subjects, including primary and secondary qualifications.

## Acceptance Criteria
- [x] Create TeacherSubject association model
- [x] Support qualification levels (primary, secondary, substitute)
- [x] Add endpoints for managing assignments
- [x] Validate teacher qualifications in scheduling
- [x] Support subject-specific constraints (e.g., Sport requires certification)
- [x] Handle Klassenlehrer (class teacher) assignments
- [x] Create overview of teaching assignments
- [x] Add workload calculation per teacher
- [ ] Support team teaching scenarios (deferred - beyond current scope)
- [x] Generate qualification matrix reports

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

## Implementation Summary

### Completed Features
1. **TeacherSubject Model** - Association model with PRIMARY/SECONDARY/SUBSTITUTE qualification levels
2. **Database Migration** - Alembic migration `20cbb13b9d21_add_teacher_subject_model`
3. **Complete CRUD API** - 8 endpoints for managing teacher-subject assignments
4. **Schedule Integration** - Validates teacher qualifications before allowing schedule creation
5. **Qualification Matrix** - Overview endpoint for viewing all teacher-subject relationships
6. **Workload Calculation** - Track assigned hours per teacher across all subjects
7. **Grade Restrictions** - Teachers can be qualified for specific grades (1-4)
8. **Certification Tracking** - Optional certification dates, expiry, and documents
9. **German School Support** - Handles Klassenlehrer vs Fachlehrer distinctions
10. **Development Seeders** - 25 realistic teacher-subject assignments
11. **14 Comprehensive Tests** - Full test coverage using TDD approach

### Technical Implementation
- **Qualification Levels**: PRIMARY (preferred), SECONDARY (capable), SUBSTITUTE (emergency only)
- **Grade Filtering**: Array of integers [1,2,3,4] for Grundschule grades
- **Certification Support**: Optional dates, expiry tracking, document references
- **Workload Management**: Max hours per week per subject with availability calculation
- **Priority Scoring**: Automatic priority ordering for schedule optimization
- **Unique Constraints**: One qualification per teacher-subject pair
- **Integration**: Schedule validation automatically checks teacher qualifications first

### API Endpoints Created
1. `GET /api/v1/teachers/{id}/subjects` - Get teacher's subject qualifications
2. `POST /api/v1/teachers/{id}/subjects` - Assign subject to teacher
3. `PUT /api/v1/teachers/{id}/subjects/{subject_id}` - Update assignment
4. `DELETE /api/v1/teachers/{id}/subjects/{subject_id}` - Delete assignment
5. `GET /api/v1/teachers/{id}/workload` - Get teacher workload calculation
6. `GET /api/v1/subjects/{id}/teachers` - Get qualified teachers for subject
7. `GET /api/v1/subjects/{id}/teachers/by-grade/{grade}` - Get teachers by grade
8. `GET /api/v1/teacher-subjects/matrix` - Get qualification matrix overview

### Business Logic Implementation
- **Qualification Validation**: Schedule creation now validates teacher qualifications before other conflicts
- **Certification Validity**: Checks certification expiry dates for time-sensitive qualifications
- **Grade Compatibility**: Validates that teachers can teach specific grade levels
- **Workload Tracking**: Calculates total assigned hours vs available hours per teacher
- **Priority Ordering**: Orders qualified teachers by qualification level for optimization

### Test Results
- 14 new tests added (bringing total from 90 to 104)
- All existing schedule tests updated to work with qualification validation
- 1 teacher availability test updated for qualification integration
- Complete test coverage for all CRUD operations and business logic
- All 104 tests passing with qualification validation integrated

### Comparison to Other Completed Tasks

**Similar Complexity to Schedule Model:**
- Both are association models connecting multiple entities
- Both required extensive conflict detection and validation
- Both needed comprehensive test coverage for all edge cases
- Both have complex business rules and German school system requirements

**More Complex than Basic Models (Teacher/Class/Subject):**
- Required integration with existing Schedule model validation
- Needed sophisticated business logic for qualification levels
- Required workload calculation and certification tracking
- More API endpoints (8 vs 5 for basic models)

**More Comprehensive than Teacher Availability:**
- Includes qualification matrix and workload calculations
- Has more complex relationships (teacher-subject pairs vs individual availability)
- Required updating existing functionality (schedule validation)
- More extensive seeder data with realistic German school assignments

### German School System Compliance
- **Klassenlehrer Support**: Primary qualifications for core subjects (Deutsch, Mathematik, Sachunterricht)
- **Fachlehrer Support**: Secondary/substitute qualifications for specialized subjects
- **Certification Requirements**: Tracks certifications for subjects like Sport, Religion, First Aid
- **Grade Restrictions**: Some teachers only qualified for specific grade levels
- **Workload Distribution**: Ensures fair distribution of teaching hours across subjects

### Impact on System Architecture
- **Enhanced Schedule Validation**: Qualification check is now the first validation step
- **Data Integrity**: Prevents unqualified teachers from being assigned to subjects
- **Reporting Capabilities**: Qualification matrix enables administrative oversight
- **Future Optimization**: Priority scoring enables intelligent teacher selection
- **Compliance Tracking**: Certification dates support regulatory compliance

This implementation successfully bridges the gap between basic entity management and intelligent scheduling, providing the foundation for automated timetable generation while ensuring compliance with German elementary school requirements.
