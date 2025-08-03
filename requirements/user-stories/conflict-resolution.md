# User Story: Conflict Resolution

## As a School Principal
I want to identify and resolve scheduling conflicts
So that the timetable is feasible and all constraints are satisfied

## Acceptance Criteria
1. The system automatically detects all types of conflicts
2. Conflicts are clearly highlighted and explained
3. I receive suggestions for resolving each conflict
4. I can manually override automatic suggestions
5. I can prioritize which conflicts to resolve first
6. The system prevents creating new conflicts while resolving existing ones
7. I can see a conflict history/log

## Types of Conflicts

### Hard Conflicts (Must Resolve)
1. **Teacher Double-Booking**: Same teacher scheduled in two places
2. **Room Double-Booking**: Same room assigned to multiple classes
3. **Missing Required Hours**: Subject doesn't meet minimum weekly hours
4. **Exceeding Maximum Hours**: Subject exceeds maximum weekly hours
5. **Break Violations**: Lessons scheduled during mandatory breaks

### Soft Conflicts (Warnings)
1. **Uneven Distribution**: Subject hours poorly distributed through week
2. **Teacher Preference Violation**: Assignment conflicts with stated preferences
3. **Pedagogical Issues**: E.g., Sport directly after lunch
4. **Workload Imbalance**: Uneven teaching load distribution

## User Flow
1. **Detection Phase**
   - System scans timetable for conflicts
   - Conflicts are categorized and prioritized
   - Visual indicators show conflict locations

2. **Review Phase**
   - Click on conflict for detailed explanation
   - See all affected parties (teachers, classes, rooms)
   - Understand the constraint being violated

3. **Resolution Phase**
   - System suggests possible solutions
   - Preview impact of each solution
   - Apply solution or manually adjust

4. **Verification Phase**
   - Confirm conflict is resolved
   - Check no new conflicts created
   - Document resolution if needed

## Scenarios

### Scenario 1: New Teacher Constraint
A teacher suddenly becomes unavailable on Tuesdays. The system must identify all affected lessons and suggest alternative slots.

### Scenario 2: Room Maintenance
The sports hall is unavailable for renovation for 3 weeks. All Sport lessons need to be rescheduled or relocated.

### Scenario 3: Cascading Conflicts
Resolving one conflict (moving a Math lesson) creates a new conflict (teacher now double-booked). The system should warn before applying changes.

## Resolution Strategies
1. **Swap**: Exchange time slots between two lessons
2. **Move**: Relocate lesson to a free slot
3. **Split**: Divide a double period into two singles
4. **Reassign**: Change the teacher assignment
5. **Relocate**: Change the room assignment

## Technical Notes
- Conflict detection should run in real-time during editing
- Should support "what-if" analysis before committing changes
- Need to maintain constraint priority levels
- Must provide clear explanation in German

## Success Metrics
- Automatic conflict detection rate: 100%
- Average resolution time per conflict: < 2 minutes
- Successful auto-resolution rate: > 70%
- New conflicts created during resolution: < 5%
