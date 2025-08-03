# User Story: Teacher Assignment

## As a School Principal
I want to assign teachers to classes and subjects
So that all teaching positions are filled according to teacher qualifications and availability

## Acceptance Criteria
1. I can view all available teachers and their qualifications
2. I can see each teacher's availability and constraints
3. I can assign teachers to specific classes and subjects
4. I can see each teacher's total assigned hours
5. The system warns me if a teacher is over/under allocated
6. I can assign multiple teachers to the same class (team teaching)
7. I can designate class teachers (Klassenlehrer)
8. The system prevents double-booking of teachers

## User Flow
1. **View Teacher Pool**
   - See list of all teachers
   - Filter by subject qualification
   - View availability patterns

2. **Assign Class Teachers**
   - Designate primary class teacher for each class
   - These teachers get priority for their class

3. **Assign Subject Teachers**
   - Match teachers to subjects based on qualifications
   - Respect part-time constraints
   - Balance workload across teachers

4. **Review Assignments**
   - See overview of all assignments
   - Check workload distribution
   - Identify gaps or overlaps

5. **Finalize**
   - Confirm all positions are filled
   - Generate teacher schedules
   - Export for communication

## Scenarios

### Scenario 1: Part-Time Teacher
Anna teaches part-time and is only available Monday, Wednesday, and Friday mornings. The system should only allow assignments during these times.

### Scenario 2: Specialist Teacher
Marcus is the only qualified music teacher and must teach music to all 12 classes. The system needs to schedule him efficiently without conflicts.

### Scenario 3: Shared Position
Two teachers share a full-time position, each working 50%. Their schedules must not overlap and together must cover all assigned classes.

## Edge Cases
- Teacher qualified for multiple subjects but has preferences
- Last-minute teacher absence requiring reassignment
- Teacher requests specific time slots for personal reasons
- New teacher joins mid-year with different qualifications

## Constraints to Consider
- Maximum daily teaching hours
- Minimum break time between lessons
- Preparation time requirements
- Part-time contract limitations
- Subject-specific requirements (e.g., Sport teachers need changing time)

## Technical Notes
- Must track teacher qualifications and certifications
- Should support teacher preferences (soft constraints)
- Need audit trail of assignment changes
- Integration with absence management system (future)

## Success Metrics
- All teaching positions filled: 100%
- Teacher satisfaction with assignments: > 80%
- Average workload deviation: < 10%
- Time to complete assignments: < 2 hours
