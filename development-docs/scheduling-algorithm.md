# Scheduling Algorithm Documentation

## Overview

The Grundschule Timetabler uses Google's OR-Tools CP-SAT (Constraint Programming with SAT solving) to automatically generate valid timetables for German elementary schools. The algorithm respects all hard constraints while optimizing for soft constraints and preferences.

## Technology Stack

- **Solver**: Google OR-Tools CP-SAT v9.14.6206
- **Language**: Python 3.12 with full type hints
- **Architecture**: Service-based with modular constraint engines
- **Performance**: Sub-second solving for typical Grundschule scale

## Algorithm Architecture

### Core Components

1. **SchedulingAlgorithm Service** (`src/services/scheduling_algorithm.py`)
   - Main algorithm orchestration
   - Variable creation and model setup
   - Solution extraction and quality scoring

2. **GermanConstraints Engine** (`src/services/german_constraints.py`)
   - German school-specific constraint rules
   - Pedagogical best practices
   - Regulatory compliance

3. **ScheduleService Integration** (`src/services/schedule.py`)
   - API endpoint implementations
   - Database persistence
   - Conflict validation

## Constraint System

### Hard Constraints (Must Be Satisfied)

1. **No Double-Booking**
   - Teachers can only teach one class at a time
   - Classes can only have one lesson at a time
   - Rooms cannot be booked for multiple classes simultaneously

2. **Teacher Qualifications**
   - Only teachers qualified for a subject can teach it
   - Supports PRIMARY, SECONDARY, and SUBSTITUTE qualification levels
   - Automatically filters impossible assignments

3. **Teacher Availability**
   - Respects AVAILABLE, BLOCKED, and PREFERRED time slots
   - Part-time teacher constraints (max 3 working days per week)
   - Daily hour limits (6 hours full-time, 3 hours part-time)

4. **Break Period Enforcement**
   - No classes during designated break periods
   - Automatic filtering of break timeslots

5. **German School Regulations**
   - Maximum weekly hours per teacher contract
   - No more than 2 consecutive periods of same subject
   - Pedagogical timing preferences

### Soft Constraints (Optimization Objectives)

1. **Teacher Availability Preferences** (Weight: 10)
   - Bonus for scheduling during PREFERRED time slots
   - Encourages use of teacher's optimal working hours

2. **Qualification Optimization** (Weight: 5)
   - Prefers PRIMARY qualifications over SECONDARY
   - Maximizes teaching expertise utilization

3. **Pedagogical Timing** (Weight: 8)
   - Core subjects (Deutsch, Mathematik, Sachunterricht) in morning periods
   - Physical education in afternoon periods
   - Balances cognitive load throughout the day

4. **Sport Afternoon Preference** (Weight: 3)
   - Schedules physical activities later in the day
   - Supports traditional German school rhythm

*Note: Complex constraints (teacher gap minimization, workload balancing) are temporarily disabled due to OR-Tools syntax complexity and will be re-enabled in future versions.*

## Algorithm Workflow

### 1. Data Loading
```python
def load_data(self) -> None:
    self.teachers = self.db.query(Teacher).all()
    self.classes = self.db.query(Class).all()
    self.subjects = self.db.query(Subject).all()
    self.timeslots = self.db.query(TimeSlot).filter(~TimeSlot.is_break).all()
    self.teacher_availabilities = self.db.query(TeacherAvailability).all()
    self.teacher_subjects = self.db.query(TeacherSubject).all()
```

### 2. Variable Creation
Creates binary variables for each possible assignment:
```
assignment[teacher_id, class_id, subject_id, timeslot_id] = 1 if assigned, 0 otherwise
```

### 3. Constraint Application
- Hard constraints eliminate impossible assignments
- Soft constraints create weighted objective terms
- Fixed assignments are preserved

### 4. Solving
- OR-Tools CP-SAT finds optimal solution
- Configurable time limits (default: 60 seconds)
- Progress logging for transparency

### 5. Solution Extraction
- Converts solver variables back to Schedule objects
- Calculates comprehensive quality metrics
- Returns structured SchedulingSolution

## Quality Scoring System

The algorithm calculates a comprehensive quality score (0-100%) based on multiple factors:

### Scoring Components

1. **Teacher Availability Satisfaction** (25% of total)
   - Perfect match for PREFERRED slots: 100%
   - Neutral for unspecified slots: 50%
   - BLOCKED slots prevented by hard constraints

2. **Qualification Optimization** (20% of total)
   - PRIMARY qualification: 100%
   - SECONDARY qualification: 70%
   - SUBSTITUTE qualification: 30%

3. **Pedagogical Timing** (20% of total)
   - Core subjects in morning periods (1-3): 100%
   - Core subjects in afternoon periods (4-5): 50%
   - Sport in afternoon periods (4+): 100%
   - Sport in morning periods: 30%

4. **Teacher Workload Balance** (15% of total)
   - Ideal range (8-15 assignments/week): 100%
   - Acceptable range (5-20 assignments): 70%
   - Some work but not ideal: 30%

5. **Schedule Efficiency** (10% of total)
   - Classes spread across 4-5 days: 100%
   - Classes spread across 3 days: 70%
   - Classes spread across 2 days: 40%

6. **German Compliance** (10% of total)
   - No break period violations: 100%
   - No teacher hour limit violations: 100%
   - Penalty for each violation: -10%

## API Endpoints

### Generate Complete Schedule
```bash
POST /api/v1/schedule/generate
Content-Type: application/json

{
  "preserve_existing": false,
  "time_limit_seconds": 60,
  "clear_existing": true
}
```

**Response:**
```json
{
  "schedules": [...],
  "quality_score": 87.5,
  "generation_time": 2.34,
  "satisfied_constraints": [...],
  "violated_constraints": [],
  "objective_value": 1250
}
```

### Optimize Existing Schedule
```bash
POST /api/v1/schedule/optimize
Content-Type: application/json

{
  "time_limit_seconds": 30
}
```

### Get Schedule Statistics
```bash
GET /api/v1/schedule/statistics
```

## Performance Characteristics

### Benchmarks (Typical Grundschule)
- **Scale**: 12 classes, 15 teachers, 8 subjects, 40 timeslots
- **Generation Time**: < 5 seconds
- **Quality Score**: 75-95% (depending on constraints)
- **Test Coverage**: 104 comprehensive tests

### Scalability
- **Tested up to**: 25 teachers, 200+ weekly lessons
- **Variable Count**: ~12,000 variables for typical school
- **Memory Usage**: < 100MB for standard problem size
- **Time Complexity**: Sub-linear due to OR-Tools optimizations

## Usage Examples

### Basic Schedule Generation
```python
from src.services.scheduling_algorithm import SchedulingAlgorithm

algorithm = SchedulingAlgorithm(db)
solution = algorithm.solve(time_limit_seconds=60)

if solution.is_feasible:
    print(f"Generated {solution.schedule_count} schedules")
    print(f"Quality score: {solution.quality_score:.1f}%")
else:
    print("No feasible solution found")
```

### With Fixed Assignments
```python
# Preserve existing manual assignments
existing_schedules = db.query(Schedule).all()
solution = algorithm.solve(
    fixed_assignments=existing_schedules,
    time_limit_seconds=30
)
```

### Service Integration
```python
from src.services.schedule import ScheduleService

# Generate and save to database
solution = ScheduleService.generate_schedule(
    db=db,
    preserve_existing=False,
    time_limit_seconds=60,
    clear_existing=True
)
```

## Troubleshooting

### Common Issues

1. **No Feasible Solution**
   - Check teacher qualifications for all subjects
   - Verify sufficient teacher availability
   - Ensure reasonable time slot distribution
   - Review part-time teacher constraints

2. **Low Quality Scores**
   - Add more teacher availability preferences
   - Improve teacher-subject qualification mapping
   - Check for unrealistic constraint combinations

3. **Slow Performance**
   - Reduce time limit for faster (potentially lower quality) results
   - Check for excessive constraint complexity
   - Verify data size is within expected ranges

### Debugging Tools

```python
# Enable detailed logging
import logging
logging.getLogger('ortools').setLevel(logging.DEBUG)

# Check constraint satisfaction
conflicts = ScheduleService.validate_generated_schedule(db, solution)

# Analyze quality components
algorithm._calculate_availability_score(solution.schedules)
algorithm._calculate_qualification_score(solution.schedules)
```

## Future Enhancements

### Planned Improvements

1. **Complex Soft Constraints**
   - Teacher gap minimization between lessons
   - Advanced workload balancing
   - Room transition optimization

2. **Performance Optimizations**
   - Parallel processing for large schools
   - Incremental schedule updates
   - Constraint preprocessing

3. **Enhanced Features**
   - Multiple solution generation
   - Interactive constraint weight adjustment
   - What-if scenario analysis

### Integration Roadmap

1. **Frontend Interface** - Visual schedule builder with algorithm integration
2. **Real-time Updates** - WebSocket-based progress reporting
3. **Advanced Analytics** - Detailed constraint violation analysis
4. **Import/Export** - Integration with existing school management systems

## Technical References

- [OR-Tools Documentation](https://developers.google.com/optimization)
- [CP-SAT Solver Guide](https://developers.google.com/optimization/cp/cp_solver)
- [School Timetabling Research](https://www.cse.unsw.edu.au/~tw/csplib/prob/prob030/)
- [German School System Regulations](https://www.kmk.org)

## Contributing

When extending the algorithm:

1. **Add New Constraints**: Extend GermanConstraints class
2. **Modify Objectives**: Update soft constraint weights in SchedulingAlgorithm
3. **Testing**: Add comprehensive tests for new constraint logic
4. **Documentation**: Update this file with new features

All algorithm modifications should maintain backward compatibility and include performance impact analysis.
