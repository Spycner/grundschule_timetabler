# Optimize Scheduling Algorithm

## Priority
Medium

## Created
2025-08-03

## Description
Re-enable and fix the complex soft constraints in the scheduling algorithm that were temporarily disabled due to OR-Tools syntax issues. These constraints improve schedule quality by minimizing teacher gaps and balancing workloads.

## Acceptance Criteria
- [ ] Fix OR-Tools constraint syntax for teacher gap minimization
- [ ] Re-enable workload balance objective with proper boolean logic
- [ ] Add advanced room transition optimization
- [ ] Implement teacher preference weighting system
- [ ] Create configurable constraint weights
- [ ] Add parallel processing for large schools
- [ ] Optimize constraint preprocessing for performance

## Technical Details

### Currently Disabled Constraints

1. **Teacher Gap Minimization** (Weight: 6)
   - Issue: Complex boolean logic with consecutive timeslot variables
   - Error: `TypeError: not supported: model.get_or_make_boolean_index('BoundedLinearExpression')`
   - Solution: Use auxiliary boolean variables for gap detection

2. **Workload Balance Objective** (Weight: 4)
   - Issue: `AddBoolOr` expects boolean variables, not linear expressions
   - Error: OR-Tools constraint syntax incompatibility
   - Solution: Create intermediate boolean variables for workload ranges

### Implementation Strategy

#### Fix Teacher Gap Minimization
```python
# Current broken approach:
self.model.AddBoolOr([total_assignments <= 7, total_assignments >= 16])

# Fixed approach:
low_workload = self.model.NewBoolVar("low_workload")
high_workload = self.model.NewBoolVar("high_workload")
self.model.Add(total_assignments <= 7).OnlyEnforceIf(low_workload)
self.model.Add(total_assignments >= 16).OnlyEnforceIf(high_workload)
```

#### Advanced Soft Constraints to Add

1. **Room Transition Minimization**
   - Reduce class movement between different rooms
   - Consider walking time between room locations
   - Group consecutive lessons in same/nearby rooms

2. **Subject Distribution Balance**
   - Spread subjects evenly across the week
   - Avoid clustering difficult subjects on same day
   - Balance cognitive load distribution

3. **Teacher Preference Integration**
   - Configurable weight system for individual teacher preferences
   - Time-of-day preferences beyond AVAILABLE/BLOCKED
   - Subject-specific teaching preferences

4. **Advanced Pedagogical Constraints**
   - No difficult subjects in last period of day
   - Group preparation time for teachers with consecutive classes
   - Consideration for special needs students

### Performance Optimizations

1. **Constraint Preprocessing**
   - Pre-filter impossible variable combinations
   - Cache constraint evaluation results
   - Reduce search space before solving

2. **Parallel Processing**
   - Multiple solver instances for different constraint weights
   - Parallel evaluation of solution quality metrics
   - Distributed solving for very large schools

3. **Incremental Updates**
   - Support for modifying existing schedules without full regeneration
   - Delta-based constraint evaluation
   - Hot-start capabilities for iterative improvements

## Dependencies
- Current algorithm implementation must be stable
- Understanding of OR-Tools boolean constraint syntax
- Performance testing framework for large datasets

## Research Areas
- OR-Tools advanced constraint patterns
- School timetabling optimization literature
- Multi-objective optimization strategies
- Constraint satisfaction heuristics

## Acceptance Testing
- All 104 existing tests must continue to pass
- Performance should not degrade for standard use cases
- Quality scores should improve by 10-15% with new constraints
- Large school scenarios (25+ teachers) should complete within 30 seconds

## Notes
- This is an enhancement, not a critical bug fix
- Current algorithm works well without these optimizations
- Focus on maintainable code that doesn't complicate the core logic
- Consider feature flags for enabling/disabling advanced constraints

## Future Considerations
- Machine learning-based constraint weight optimization
- User interface for constraint weight adjustment
- Historical data analysis for improving default preferences
- Integration with external room booking systems
