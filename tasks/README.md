# Task Management System

## Overview
This directory contains all project tasks organized in a simple kanban-style system. Tasks are markdown files that move between directories as they progress.

## Directory Structure
- **backlog/** - Future tasks and ideas not yet started
- **doing/** - Tasks currently being worked on
- **completed/** - Finished tasks kept for reference

## Task File Format
Each task is a markdown file with the following structure:

```markdown
# Task Title

## Priority
[High/Medium/Low]

## Created
YYYY-MM-DD

## Description
Detailed description of what needs to be done.

## Acceptance Criteria
- [ ] Specific measurable outcome 1
- [ ] Specific measurable outcome 2

## Notes
Any additional context, decisions, or progress notes.

## Completed
YYYY-MM-DD (added when task is done)
```

## Workflow

### Creating a New Task
1. Create a new `.md` file in `backlog/`
2. Use descriptive filename: `implement-teacher-crud.md`
3. Fill out the task template
4. Commit to git

### Starting a Task
1. Move file from `backlog/` to `doing/`
2. Update any relevant information
3. Commit the move

### Completing a Task
1. Move file from `doing/` to `completed/`
2. Add completion date
3. Add any final notes or learnings
4. Commit the move

## Best Practices

### Task Sizing
- Tasks should be completable in 1-3 days
- Larger features should be broken into multiple tasks
- Each task should have clear, measurable outcomes

### Naming Conventions
- Use lowercase with hyphens: `add-user-authentication.md`
- Start with verb: `implement-`, `fix-`, `update-`, `research-`
- Be specific but concise

### Priority Guidelines
- **High**: Blocking other work or critical for next release
- **Medium**: Important but not blocking
- **Low**: Nice to have, can be deferred

### Work in Progress Limits
- Maximum 3 tasks in `doing/` at once
- Finish current tasks before starting new ones
- If blocked, document the blocker and move to another task

## Task Categories
Common task prefixes to organize work:

- `feature-` : New functionality
- `bug-` : Bug fixes
- `refactor-` : Code improvements
- `docs-` : Documentation updates
- `research-` : Investigation and planning
- `setup-` : Project configuration
- `test-` : Testing improvements

## Review Process
- Weekly review of `backlog/` to prioritize
- Daily check of `doing/` tasks
- Monthly archive of old `completed/` tasks

## Integration with Git
- Task moves should be individual commits
- Commit message format: `task: move [filename] to [status]`
- Reference task files in related code commits

## Tips
- Keep task descriptions focused and actionable
- Update tasks with progress notes while working
- Link to relevant requirements or documentation
- Include any decisions made during implementation