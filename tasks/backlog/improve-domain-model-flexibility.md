# Improve Domain Model Flexibility

## Issue
Current domain model has rigid constraints that limit flexibility:

1. **Redundant `is_part_time` field**: Boolean flag is redundant when we already have `max_hours_per_week`
   - Creates potential data inconsistency (is_part_time=false but max_hours=15)
   - German employment law defines part-time functionally, not as binary flag
   - Part-time status can be derived from hours < full-time standard

2. **Hard-coded grade limits (1-4)**: Prevents expansion and flexibility
   - What if school adds Kindergarten (grade 0) or extends to grade 5/6?
   - International expansion might need different grade ranges
   - Multi-grade classes (1-2, 3-4) are common in some schools

3. **Hard-coded period limits (1-8)**: Doesn't fit all school schedules
   - Typical Grundschule: Usually 6 periods max (8:00-13:15)
   - Extended day schools: Might need 8+ periods
   - After-school programs: Need periods 9, 10, etc.
   - Break periods still count toward limit

## Tasks

### 1. Remove Redundant `is_part_time` Field
- [ ] Remove `is_part_time` boolean from Teacher model (`backend/src/models/teacher.py`)
- [ ] Update teacher schemas (`backend/src/schemas/teacher.py`)
- [ ] Update API routes and validations
- [ ] Add computed property/method to determine part-time status from `max_hours_per_week`
- [ ] Create Alembic migration to drop the column
- [ ] Update all tests to remove is_part_time usage
- [ ] Update seeders to remove is_part_time

### 2. Make Grade Ranges Configurable (Future Enhancement)
- [ ] Keep current 1-4 validation for MVP (German Grundschule requirement)
- [ ] Add school configuration system for future flexibility
- [ ] Document the constraint as "German Grundschule specific" for future expansion
- [ ] Plan architecture for multi-school support with different grade ranges

### 3. Make Period Limits Configurable
- [ ] Replace hard-coded period limit (1-8) with configurable school settings
- [ ] Add School/Configuration entity to store per-school limits
- [ ] Update all validations in schemas to use configurable limits
- [ ] Update TimerSlot model and constraints
- [ ] Update TeacherAvailability validations
- [ ] Keep default of 8 periods for backward compatibility
- [ ] Update timeslot generation service
- [ ] Update tests to handle configurable limits

### 4. Improve Break Period Handling
- [ ] Evaluate whether breaks should count toward period limits
- [ ] Consider if break periods need separate numbering/handling
- [ ] Update timeslot generation to handle breaks more flexibly
- [ ] Document break period design decisions

## Acceptance Criteria

### For `is_part_time` Removal:
- [ ] Teacher model no longer has `is_part_time` field
- [ ] Part-time status can be determined programmatically
- [ ] All existing functionality works without the boolean
- [ ] Database migration completes successfully
- [ ] All tests pass

### For Period Limit Flexibility:
- [ ] Period limits are no longer hard-coded to 8
- [ ] System can handle schools with different period counts
- [ ] Default behavior remains the same (8 periods)
- [ ] Configuration system allows per-school customization
- [ ] Break periods are handled appropriately

## Priority
**Medium** - Improves system flexibility but doesn't block MVP functionality

## Estimated Effort
- Remove `is_part_time`: **2-3 hours**
- Period limit configuration: **4-6 hours**
- Break period improvements: **2-3 hours**
- Testing and validation: **2-3 hours**

**Total: 10-15 hours**

## Notes
- Keep grade limits as-is for MVP (German Grundschule focus)
- Period limit changes should be backward compatible
- Consider this work as foundation for multi-school support
- Document all design decisions for future reference

## Related Files
- `backend/src/models/teacher.py`
- `backend/src/models/timeslot.py` 
- `backend/src/models/teacher_availability.py`
- `backend/src/schemas/teacher.py`
- `backend/src/schemas/timeslot.py`
- `backend/src/schemas/teacher_availability.py`
- `backend/src/services/timeslot.py`
- All test files in `backend/tests/`
