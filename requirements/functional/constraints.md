# Functional Requirements: Constraints

## Overview
The constraint system is the core of the timetabling application. It ensures that all schedules are valid, practical, and meet educational requirements.

## Constraint Categories

### 1. Legal/Regulatory Constraints
Mandated by German education law and state regulations.

- **Minimum Teaching Hours**
  - Each subject must meet state-mandated minimum hours
  - Core subjects (Deutsch, Mathematik) have strict requirements
  - Varies by grade level

- **Maximum Daily Hours**
  - Grade 1-2: Maximum 4-5 hours per day
  - Grade 3-4: Maximum 5-6 hours per day
  - Includes break time calculations

- **Break Requirements**
  - Minimum break durations by law
  - Breakfast break (Frühstückspause): 15-20 minutes
  - Main break (Große Pause): 20-30 minutes
  - Frequency of breaks based on lesson count

### 2. Teacher Constraints

#### Availability Constraints
- **Working Hours**
  - Part-time percentages (50%, 75%, etc.)
  - Specific days/times unavailable
  - Maximum daily teaching hours
  - Minimum break between lessons

- **Qualifications**
  - Subjects teacher is qualified to teach
  - Grade levels teacher can teach
  - Special certifications required

#### Workload Constraints
- **Weekly Hours**
  - Contracted hours per week
  - Overtime limitations
  - Preparation time requirements
  - Administrative duties time

- **Daily Limits**
  - Maximum consecutive teaching hours
  - Required break after X hours
  - Maximum number of different classes per day

### 3. Room Constraints

#### Capacity Constraints
- **Room Size**
  - Maximum students per room
  - Special equipment requirements
  - Accessibility requirements

#### Availability Constraints
- **Room Types**
  - Regular classrooms
  - Special purpose rooms (Sport, Music, Art, Computer)
  - Shared facilities

- **Room Scheduling**
  - Exclusive use times
  - Shared use coordination
  - Maintenance windows
  - External bookings (e.g., community use)

### 4. Class Constraints

#### Structural Constraints
- **Class Composition**
  - Fixed class groups
  - Split groups for certain subjects
  - Combined classes possibilities

#### Scheduling Constraints
- **Daily Patterns**
  - Start and end times
  - Core hours (when all students must be present)
  - Maximum gaps in schedule

### 5. Subject Constraints

#### Distribution Constraints
- **Weekly Distribution**
  - Subjects spread across week
  - Not all math on same day
  - Balance of subjects per day

#### Pedagogical Constraints
- **Optimal Timing**
  - Core subjects in morning when possible
  - Sport not immediately after eating
  - Art/Music better with double periods

#### Sequencing Constraints
- **Order Requirements**
  - Certain subjects better early/late
  - Avoiding difficult subjects back-to-back
  - Preparation requirements between subjects

## Constraint Configuration

### Priority Levels
1. **Mandatory (Hard Constraints)**
   - Must be satisfied
   - Schedule invalid if violated
   - Examples: Legal requirements, double-booking

2. **Strong Preference**
   - Should be satisfied if possible
   - Requires justification to violate
   - Examples: Teacher preferences, pedagogical recommendations

3. **Weak Preference**
   - Nice to have
   - Can be violated if necessary
   - Examples: Room preferences, optimal timing

### Constraint Rules Engine

#### Rule Definition
```
CONSTRAINT teacher_availability
  TYPE: HARD
  APPLIES_TO: Teacher
  CONDITION: Teacher.available(day, timeslot) = true
  MESSAGE: "Lehrer nicht verfügbar"
```

#### Rule Sets
- Default rule set (applies to all)
- School-specific rules
- Grade-specific rules
- Subject-specific rules

### Conflict Detection

#### Real-Time Validation
- Check constraints during editing
- Immediate visual feedback
- Prevent invalid operations

#### Batch Validation
- Full schedule validation
- Generate conflict report
- Prioritized conflict list

#### Conflict Information
- Type of constraint violated
- Affected entities (teacher, class, room)
- Severity level
- Suggested resolutions

## Special Constraint Scenarios

### 1. Team Teaching
- Multiple teachers for one class
- Both must be available
- Room must accommodate arrangement

### 2. Combined Classes
- Multiple classes together
- Room capacity for all students
- Common available time for all classes

### 3. Split Groups
- Class divided for certain subjects
- Parallel scheduling required
- Multiple teachers and rooms needed

### 4. Floating Teachers
- Teachers at multiple schools
- Limited availability windows
- Coordination with external schedules

### 5. Inclusion Support
- Special education support in class
- Additional teacher present
- Coordinated scheduling required

## Constraint Management

### User Interface
- Visual constraint editor
- Constraint templates
- Batch constraint updates
- Constraint import/export

### Reporting
- Constraint satisfaction report
- Violation analysis
- Optimization suggestions
- Historical constraint data

### Flexibility
- Temporary constraint overrides
- Emergency modifications
- Constraint relaxation options
- What-if analysis with different constraints

## Performance Considerations
- Efficient constraint checking
- Incremental validation
- Caching of constraint results
- Parallel constraint evaluation