# Task Backlog Organization

Tasks have been organized by priority based on the MVP-first approach defined in CLAUDE.md. The goal is to get a working prototype for user testing with real schools (Hesse pre-school contacts) as quickly as possible.

## Directory Structure

### Critical Priority (`/critical/`)
**Must-have for MVP user testing**
- `setup-typescript-frontend.md` - Essential foundation for any UI interaction
- `implement-export-functionality.md` - Schools need PDF/Excel exports to be useful

### High Priority (`/high/`)
**Important for complete MVP**
- `create-timetable-ui.md` - Core user interface for schedule manipulation
- `implement-import-functionality.md` - Schools need to import existing data

### Medium Priority (`/medium/`)
**Valuable enhancements after MVP validation**
- `optimize-scheduling-algorithm.md` - Improve algorithm with soft constraints
- `implement-ai-assistant-ui.md` - Interactive chat for scheduling help
- `implement-websocket-chat-endpoint.md` - Backend for AI assistant

### Low Priority (`/low/`)
**Future features after user feedback**
- `implement-room-requirements.md` - Advanced room management
- `implement-schedule-validation-rules.md` - State-specific regulations
- `implement-schedule-templates.md` - Reusable schedule patterns
- `implement-preference-system.md` - Teacher/admin preferences
- `implement-substitute-management.md` - Substitute teacher handling

## Rationale

### Why This Order?

1. **Frontend Foundation First**: Without a UI (`setup-typescript-frontend.md`), users can't interact with the system.

2. **Export Before Import**: Schools need to trust they can get their data out (`implement-export-functionality.md`) before they'll put significant effort into importing data.

3. **Core UI Next**: The timetable interface (`create-timetable-ui.md`) is essential for schedule manipulation and validation.

4. **Import for Real Data**: Once users can create and export schedules, they'll want to import existing data (`implement-import-functionality.md`).

5. **Algorithm Optimization**: The current algorithm works but can be improved with soft constraints (`optimize-scheduling-algorithm.md`).

6. **AI Features**: Interactive assistance (`implement-ai-assistant-ui.md`, `implement-websocket-chat-endpoint.md`) adds value but isn't essential for core functionality.

7. **Advanced Features**: Room management, validation rules, templates, preferences, and substitute management are valuable but should be driven by real user feedback rather than assumptions.

### MVP Philosophy

Based on the lessons learned from the previous Stundenhexe project:
- Start simple and iterate based on real user needs
- Avoid analysis paralysis with complex features
- Focus on core functionality that solves immediate pain points
- Build incrementally with user feedback at each stage

### Next Steps

1. Complete `setup-typescript-frontend.md` to establish the frontend foundation
2. Implement `implement-export-functionality.md` for PDF/Excel generation
3. Build `create-timetable-ui.md` for schedule manipulation
4. Add `implement-import-functionality.md` for data import
5. Gather user feedback before proceeding to medium/low priority items

## Backend Status

The backend is complete with:
- ✅ All core models (Teacher, Class, Subject, TimeSlot, Schedule, TeacherAvailability, TeacherSubject)
- ✅ Full CRUD APIs for all entities
- ✅ OR-Tools scheduling algorithm with constraint satisfaction
- ✅ 104 comprehensive tests with TDD approach
- ✅ Docker setup and CI/CD pipeline
- ✅ Database migrations with Alembic
- ✅ Development data seeders

The focus now is on creating a usable frontend interface and export functionality to enable real user testing.
