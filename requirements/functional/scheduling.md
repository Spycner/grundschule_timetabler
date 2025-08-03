# Functional Requirements: Scheduling

## Core Scheduling Features

### 1. Time Slot Management
- **Define Schedule Template**
  - Set start and end time for school day
  - Define lesson duration (typically 45 minutes)
  - Configure break times and durations
  - Support for different schedules per day

- **Special Schedules**
  - Short days (e.g., before holidays)
  - Event days with modified timing
  - Temporary schedule changes

### 2. Subject Scheduling
- **Required Hours Configuration**
  - Set weekly hours per subject per grade
  - Define minimum and maximum constraints
  - Support for bi-weekly schedules

- **Subject Rules**
  - Which subjects can be double periods
  - Which subjects cannot be first/last period
  - Prerequisites (e.g., Sport not after lunch)

### 3. Class Management
- **Class Definition**
  - Create classes with grade level
  - Set class size
  - Assign home room
  - Define class-specific constraints

- **Class Groups**
  - Support for split classes (e.g., Religion/Ethics)
  - Combined classes for certain subjects
  - Flexible grouping options

### 4. Automatic Scheduling Algorithm
- **Constraint Satisfaction**
  - Respect all hard constraints
  - Optimize soft constraints
  - Provide multiple solution options

- **Optimization Goals**
  - Minimize gaps in teacher schedules
  - Distribute subjects evenly through week
  - Minimize room changes for classes
  - Balance teacher workloads

### 5. Manual Scheduling
- **Drag and Drop Interface**
  - Move lessons between time slots
  - Visual feedback for conflicts
  - Undo/redo capability

- **Bulk Operations**
  - Copy weekly schedule to multiple weeks
  - Swap entire days
  - Clear and reset sections

## Scheduling Constraints

### Hard Constraints (Must Satisfy)
1. No teacher double-booking
2. No room double-booking
3. No class double-booking
4. Respect teacher availability
5. Meet minimum subject hours
6. Not exceed maximum subject hours
7. Respect break times

### Soft Constraints (Optimize)
1. Teacher preferences
2. Pedagogical recommendations
3. Even distribution of subjects
4. Minimize teacher movement
5. Minimize class movement
6. Preferred time slots for subjects

## Schedule Types

### 1. Master Schedule
- Template for the entire school year
- Base schedule that gets copied

### 2. Weekly Schedule
- Actual schedule for specific week
- Can deviate from master for special events

### 3. Daily Schedule
- View and edit single day
- Quick adjustments for substitutes

### 4. Teacher Schedule
- Individual teacher's weekly view
- Shows all assigned classes and rooms

### 5. Class Schedule
- Individual class weekly view
- Shows all subjects, teachers, and rooms

## Schedule Operations

### Creation
- New schedule from scratch
- Copy from previous year
- Copy from template
- Import from external source

### Modification
- Edit individual lessons
- Bulk updates
- Period swaps
- Day swaps

### Validation
- Check completeness
- Verify constraints
- Identify conflicts
- Suggest improvements

### Publishing
- Lock schedule for editing
- Publish to stakeholders
- Version control
- Change notifications

## Advanced Features

### 1. What-If Analysis
- Try different scenarios
- Compare multiple versions
- Impact analysis of changes

### 2. Optimization Runs
- Improve existing schedule
- Multiple optimization criteria
- Partial optimization (keep some fixed)

### 3. Schedule Templates
- Save common patterns
- Reusable configurations
- School-specific templates

### 4. Multi-Week Planning
- A/B week schedules
- Rotating schedules
- Term planning

## Integration Points
- Import teacher data
- Import room data
- Export to calendars
- Export to PDF/Excel
- API for external systems