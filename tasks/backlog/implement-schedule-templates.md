# Implement Schedule Templates

## Priority
Medium

## Created
2025-08-03

## Description
Create a template system that allows schools to save and reuse successful timetable patterns, standard weekly structures, and typical lesson distributions.

## Acceptance Criteria
- [ ] Create ScheduleTemplate model
- [ ] Support saving current schedule as template
- [ ] Allow template categorization
- [ ] Implement template application with mapping
- [ ] Support partial template application
- [ ] Create template library management
- [ ] Add template sharing between schools
- [ ] Support template versioning
- [ ] Create template preview functionality
- [ ] Add template validation before application

## Technical Details
### Model Structure
```python
class ScheduleTemplate:
    id: int
    name: str
    description: str
    category: Enum (WEEKLY, DAILY, SUBJECT_BLOCK, FULL_TIMETABLE)
    grade_level: int (optional)
    template_data: JSON
    created_by: str
    school_type: str
    is_public: bool
    usage_count: int
    rating: float
    
class TemplateApplication:
    template_id: int (FK)
    mapping: JSON (old_id -> new_id mappings)
    applied_to: str (school/grade/class)
    applied_at: datetime
```

### Template Types
#### Weekly Template
- Standard week structure
- Break patterns
- Subject distribution

#### Subject Block Template
- Double lessons for specific subjects
- Lab sessions
- Project blocks

#### Grade-Specific Template
- Age-appropriate scheduling
- Grade 1: shorter attention spans
- Grade 4: exam preparation

### API Endpoints
- `GET /api/v1/templates` - List available templates
- `POST /api/v1/templates` - Create new template
- `GET /api/v1/templates/{id}` - Get template details
- `POST /api/v1/templates/{id}/apply` - Apply template
- `POST /api/v1/templates/{id}/preview` - Preview application
- `GET /api/v1/templates/library` - Public template library
- `POST /api/v1/schedule/save-as-template` - Save current as template

### Template Application Process
1. Select template
2. Map template entities to current entities
   - Map teachers by subject qualification
   - Map rooms by type/features
   - Map classes by grade
3. Preview conflicts and adjustments
4. Apply with conflict resolution
5. Manual fine-tuning

## Dependencies
- Complete Schedule model
- All entity models (Teacher, Class, Subject, Room)
- Import/Export functionality for template sharing

## Template Library
### Default Templates
- "Grundschule Standard NRW" - North Rhine-Westphalia standard
- "Ganztag Modell" - Full-day school model
- "Flexible Eingangsstufe" - Flexible entry stage
- "Sport Schwerpunkt" - Sports focus school
- "Musik Schwerpunkt" - Music focus school

### Community Templates
- User-submitted templates
- Rating and review system
- Usage statistics
- Comments and tips

## Mapping Rules
- Intelligent subject matching
- Teacher qualification matching
- Room requirement matching
- Time slot alignment
- Partial application for specific days/grades

## Notes
- Consider state-specific requirements
- Templates should be adaptable to school size
- Support for special educational concepts
- Version control for template updates
- Consider intellectual property for shared templates
