# Grundschule Timetabler - Project Context

## Project Overview
A web-based timetabling application designed specifically for German Grundschule (elementary school) principals and administrators who are responsible for creating and managing class schedules, teacher assignments, and resource allocation.

## Target User
Primary users: Principals and administrative staff at German Grundschule
- Responsible for creating yearly timetables for all classes
- Manages teacher assignments and availability
- Handles room allocation and special requirements
- Needs to resolve scheduling conflicts efficiently
- Works with German educational regulations and constraints

## Tech Stack

### Backend (✅ Implemented)
- **Language**: Python 3.12
- **Package Manager**: uv (modern Python package manager)
- **Framework**: FastAPI (for REST API)
- **Database**: PostgreSQL (for production), SQLite (for development)
- **ORM**: SQLAlchemy 2.0
- **Testing**: pytest with pytest-asyncio
- **Code Quality**: ruff (formatting and linting), ty (type checking from Astral)
- **API Testing**: httpx
- **Migrations**: Alembic

### Frontend (📋 Planned)
- **Language**: TypeScript
- **Framework**: React with Vite (or Next.js - TBD)
- **Styling**: Tailwind CSS
- **State Management**: TBD (Context API, Zustand, or Redux Toolkit)
- **Testing**: Vitest + React Testing Library
- **Code Quality**: ESLint, Prettier

### Infrastructure (Future)
- **IaC**: Terraform
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Hosting**: TBD (AWS, Vercel, or self-hosted)

## Domain Context

### German Education System Specifics
- **Schuljahr**: School year (typically August to July)
- **Stundenplan**: Timetable/schedule
- **Unterrichtsstunden**: Teaching hours (usually 45 minutes)
- **Pausenzeiten**: Break times (important constraints)
- **Fachlehrer**: Subject teachers (may teach specific subjects only)
- **Klassenlehrer**: Class teacher (primary teacher for a class)
- **Vertretung**: Substitute teaching arrangements

### Key Entities
1. **Lehrer** (Teachers)
   - Availability constraints
   - Subject specializations
   - Maximum weekly hours
   - Part-time vs full-time

2. **Klassen** (Classes)
   - Grade levels (1-4 in Grundschule)
   - Class size
   - Special requirements

3. **Fächer** (Subjects)
   - Core subjects: Deutsch, Mathematik, Sachunterricht
   - Special subjects: Sport, Musik, Kunst, Religion/Ethik
   - Weekly hour requirements per grade

4. **Räume** (Rooms)
   - Regular classrooms
   - Special rooms (Sport, Music, Computer)
   - Capacity constraints

5. **Zeitfenster** (Time Slots)
   - Standard lesson times
   - Break schedules
   - Early/late care considerations

## Development Conventions

### Code Style
- Python: Follow PEP 8, use type hints, format with ruff
- TypeScript: Strict mode enabled, explicit types preferred
- Components: Functional components with hooks
- Naming: English for code, German terms in domain models with comments

### Git Workflow
- Main branch: `main`
- Feature branches: `feature/description`
- Commit messages: Conventional commits format
- PR required for main branch

### Testing Strategy (TDD Approach)
- **Test-Driven Development (TDD)**: Write tests first, then implementation
- **Red-Green-Refactor**: Test fails → Make it pass → Improve code
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user workflows
- Minimum 80% code coverage target

### TDD Workflow
1. Write failing test for new feature
2. Write minimal code to pass test
3. Refactor while keeping tests green
4. Repeat for each requirement

#### TDD Example for Teacher Model
```python
# Step 1: Write test first (test_teacher.py)
def test_create_teacher():
    response = client.post("/api/v1/teachers", json={
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria@schule.de"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "maria@schule.de"

# Step 2: Run test (it fails - endpoint doesn't exist)
# Step 3: Implement minimal code to pass
# Step 4: Run test again (it passes)
# Step 5: Refactor if needed, keep test green
```

### Documentation
- Code comments in English
- User-facing documentation in German
- API documentation via OpenAPI/Swagger
- Domain terms documented with translations

## Project Status

### Completed ✅
- Comprehensive project documentation
- Requirements specification (functional and non-functional)
- Task management system setup
- Backend infrastructure with FastAPI
- Development tooling (ruff, ty, pytest)
- VS Code integration
- Health check endpoints
- Test structure
- Pre-commit hooks configuration
- **API versioning structure** (`/api/v1/`)
- **Teacher model** with full CRUD operations (TDD approach)
- **Class model** with full CRUD operations (TDD approach)
- **Subject model** with full CRUD operations (TDD approach)
- **TimeSlot model** with schedule grid management (TDD approach)
- **Schedule model** with comprehensive conflict detection (TDD approach)
- **Teacher Availability model** with AVAILABLE/BLOCKED/PREFERRED states (TDD approach)
- **Teacher-Subject Assignment model** with PRIMARY/SECONDARY/SUBSTITUTE qualifications (TDD approach)
- **Alembic migrations** for database management
- **104 comprehensive tests** total (15 Teacher, 15 Class, 14 Subject, 13 TimeSlot, 14 Schedule, 16 Teacher Availability, 14 Teacher-Subject, 3 Health)
- **Docker & Docker Compose** configuration (with Valkey instead of Redis)
- **GitHub Actions CI/CD** pipeline with comprehensive checks
- **Development data seeders** for teachers, classes, subjects, timeslots, and teacher-subject assignments (40 slots: 5 days × 8 periods)

### Current Phase: MVP Foundation (Simplified Approach)
Focus: Get a working prototype for testing with real users (Hesse pre-school contacts)

#### Phase 1: Basic Entities & CRUD (✅ Completed)
- Simple Teacher model (name, email, max_hours, part_time status) ✅
- Simple Class model (name, grade, size, home_room) ✅
- Simple Subject model (name, code, color for UI) ✅
- Basic TimeSlot model (day, period, times) ✅
- Manual Schedule creation (link entities together) ✅
- Conflict detection (no double bookings) ✅

#### Phase 2: User Testing & Feedback (Next 2 weeks)
- Basic web UI for schedule creation
- Import last year's data
- Export to PDF/Excel
- Test with real school
- Gather feedback on actual constraints

#### Phase 3: Smart Scheduling (After feedback)
- Add discovered constraints from users
- Implement automatic scheduling only for proven needs
- Handle part-time teacher complexities
- Basic substitute marking

### Future Phases (After MVP Success)
- Multi-school support
- Advanced optimization algorithms
- Full substitute management
- User authentication & roles
- GDPR compliance features

## Important Considerations

### Data Privacy (GDPR)
- Personal data handling for teachers and students
- Data retention policies
- Export and deletion capabilities
- Audit logging

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode

### Localization
- German as primary language
- Date/time formats (DD.MM.YYYY)
- Decimal notation (comma vs period)
- Cultural considerations for scheduling

## Development Commands

### Backend
```bash
cd backend
make install          # Install dependencies
make dev             # Run development server
make test            # Run tests
make check           # Run all checks (lint, format, type)
make typecheck       # Run ty type checker
make format          # Format code with ruff
make lint            # Lint code with ruff

# Database migrations:
make migrate-up      # Apply migrations
make migrate-down    # Rollback last migration
make migrate-create name="description"  # Create new migration
make migrate-current # Show current migration
make migrate-history # Show migration history

# Seeder commands:
make seed            # Seed development data
make seed-clear      # Clear and reseed database
make seed-clear-only # Clear all seeded data

# Docker commands:
make docker-build    # Build Docker images
make docker-up       # Start all services
make docker-down     # Stop all services
make docker-logs     # View logs
make docker-shell    # Open shell in backend container
make docker-clean    # Remove containers and volumes

# Or manually:
uv sync              # Install dependencies
uv run uvicorn src.main:app --reload  # Run server
uv run pytest        # Run tests
uv run ruff check .  # Lint
uv run ruff format . # Format
uvx --native-tls ty check  # Type check
uv run alembic upgrade head  # Apply migrations
uv run python src/seeders/run.py  # Run seeders
```

### Frontend (Not yet implemented)
```bash
cd frontend
npm install
npm run dev
npm run build
npm test
```

### Docker
```bash
# Start all services (from root directory)
docker-compose up -d

# Access services:
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Mailhog UI: http://localhost:8025
# PostgreSQL: localhost:5432
# Valkey (Redis): localhost:6379
```

## Key Files and Directories
- `/requirements/` - Detailed project requirements
- `/tasks/` - Task management system (backlog, doing, completed)
- `/backend/` - Python backend application (FastAPI)
  - `/src/seeders/` - Database seeding scripts
  - `/alembic/` - Database migrations
- `/frontend/` - TypeScript frontend application (not yet implemented)
- `/development-docs/` - Development reference documentation (uv, ty)
- `/.vscode/` - VS Code workspace configuration
- `/docker-compose.yml` - Docker services configuration
- `/.github/workflows/` - CI/CD pipelines
- `/DOCKER.md` - Docker setup documentation

## Current Working State

### Backend API
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **API Version**: v1 (URL prefix: `/api/v1`)

### API Versioning Strategy
- **URL Path Versioning**: `/api/v1/...` for all endpoints
- **Version in Accept Header**: Optional support for `Accept: application/vnd.grundschule.v1+json`
- **Deprecation Policy**: 6-month notice before removing old versions
- **Breaking Changes**: New major version only when absolutely necessary

### Available Endpoints
- `GET /` - Welcome message (unversioned)
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/ready` - Database connectivity check

**Teachers:**
- `GET /api/v1/teachers` - List all teachers
- `GET /api/v1/teachers/{id}` - Get specific teacher
- `POST /api/v1/teachers` - Create new teacher
- `PUT /api/v1/teachers/{id}` - Update teacher
- `DELETE /api/v1/teachers/{id}` - Delete teacher

**Teacher Availability:**
- `GET /api/v1/teachers/{id}/availability` - Get teacher's availability
- `POST /api/v1/teachers/{id}/availability` - Create availability entry
- `PUT /api/v1/teachers/{id}/availability/{id}` - Update availability
- `DELETE /api/v1/teachers/{id}/availability/{id}` - Delete availability
- `POST /api/v1/teachers/availability/bulk` - Bulk import availability
- `GET /api/v1/teachers/{id}/availability/overview` - Get availability overview
- `GET /api/v1/teachers/{id}/availability/validate` - Validate constraints
- `GET /api/v1/teachers/availability/overview` - All teachers overview

**Teacher-Subject Assignments:**
- `GET /api/v1/teachers/{id}/subjects` - Get teacher's subject qualifications
- `POST /api/v1/teachers/{id}/subjects` - Assign subject to teacher
- `PUT /api/v1/teachers/{id}/subjects/{id}` - Update assignment
- `DELETE /api/v1/teachers/{id}/subjects/{id}` - Delete assignment
- `GET /api/v1/teachers/{id}/workload` - Get teacher workload calculation
- `GET /api/v1/subjects/{id}/teachers` - Get qualified teachers for subject
- `GET /api/v1/subjects/{id}/teachers/by-grade/{grade}` - Get teachers by grade
- `GET /api/v1/teacher-subjects/matrix` - Get qualification matrix overview

**Classes:**
- `GET /api/v1/classes` - List all classes
- `GET /api/v1/classes/{id}` - Get specific class
- `POST /api/v1/classes` - Create new class
- `PUT /api/v1/classes/{id}` - Update class
- `DELETE /api/v1/classes/{id}` - Delete class

**Subjects:**
- `GET /api/v1/subjects` - List all subjects
- `GET /api/v1/subjects/{id}` - Get specific subject
- `POST /api/v1/subjects` - Create new subject
- `PUT /api/v1/subjects/{id}` - Update subject
- `DELETE /api/v1/subjects/{id}` - Delete subject

**TimeSlots:**
- `GET /api/v1/timeslots` - List all timeslots (ordered by day, period)
- `GET /api/v1/timeslots/{id}` - Get specific timeslot
- `POST /api/v1/timeslots` - Create new timeslot
- `PUT /api/v1/timeslots/{id}` - Update timeslot
- `DELETE /api/v1/timeslots/{id}` - Delete timeslot
- `POST /api/v1/timeslots/generate-default` - Generate standard weekly schedule

**Schedule:**
- `GET /api/v1/schedule` - List all schedules with filters
- `GET /api/v1/schedule/{id}` - Get specific schedule entry
- `POST /api/v1/schedule` - Create new schedule entry (checks qualifications & availability)
- `PUT /api/v1/schedule/{id}` - Update schedule entry
- `DELETE /api/v1/schedule/{id}` - Delete schedule entry
- `GET /api/v1/schedule/class/{id}` - Get schedule by class
- `GET /api/v1/schedule/teacher/{id}` - Get schedule by teacher
- `GET /api/v1/schedule/room/{room}` - Get schedule by room
- `POST /api/v1/schedule/validate` - Validate for conflicts (including qualifications & availability)
- `GET /api/v1/schedule/conflicts` - List all conflicts
- `POST /api/v1/schedule/bulk` - Create multiple entries

### Database Management
- **Alembic Migrations**: Database schema is now managed via migrations
- **Current Migration**: `20cbb13b9d21_add_teacher_subject_model`
- **Apply Migrations**: Run `make migrate-up` before starting the server
- **Create Migrations**: Use `make migrate-create name="description"` for schema changes
- **Important**: All models must be imported in `src/models/__init__.py` for Alembic to detect them

### Immediate Next Steps (MVP Focus)
1. ~~Create simple Teacher model with basic CRUD (TDD)~~ ✅
2. ~~Create simple Class model with basic CRUD (TDD)~~ ✅
3. ~~Create simple Subject model with basic CRUD (TDD)~~ ✅
4. ~~Create TimeSlot model for schedule grid (TDD)~~ ✅
5. ~~Create Schedule model to link entities (TDD)~~ ✅
6. ~~Add conflict detection for double bookings~~ ✅

### Backend Features Roadmap
The following backend features are planned to complete the MVP:

#### High Priority
- ✅ **Teacher Availability Model** - Track when teachers can teach (part-time, blocked periods)
- ✅ **Teacher-Subject Assignment** - Manage qualifications and teaching assignments
- **Basic Scheduling Algorithm** - Automatic timetable generation with constraint solving

#### Medium Priority  
- **Room Requirements** - Room features, capacity, and subject requirements
- **Import Functionality** - Load data from Excel/CSV files
- **Export Functionality** - Generate PDFs, Excel, and iCal exports
- **Schedule Templates** - Save and reuse successful timetable patterns
- **Validation Rules** - Ensure compliance with educational regulations

#### Low Priority
- **Preference System** - Handle scheduling preferences as soft constraints
- **Substitute Management** - Handle teacher absences and find substitutes

See `/tasks/backlog/` for detailed task specifications.

### Session Continuity
Tasks are defined in `/tasks/backlog/` directory. In a new session, you can:
- Check task details: `implement-teacher-model.md`, `implement-class-model.md`, etc.
- Follow TDD approach: Write tests first, then implementation
- Each task is self-contained with clear acceptance criteria
- Complete one model at a time, ensuring tests pass before moving on

## Questions to Address
1. How many schools will this initially support?
2. What are the specific German state regulations to consider?
3. Integration with existing school management systems?
4. Offline capability requirements?
5. Mobile device support needs?

## Resources
- [German School System Overview](https://www.kmk.org)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [uv Documentation](https://github.com/astral-sh/uv)
- [ruff Documentation](https://github.com/astral-sh/ruff)
- [ty Documentation](https://github.com/astral-sh/ty)
- [React + TypeScript Best Practices](https://react-typescript-cheatsheet.netlify.app)

## Project Contact
- **Author**: Pascal Kraus
- **Email**: pascal98kraus@gmail.com
- **Repository**: https://github.com/Spycner/grundschule_timetabler

## Advanced Concepts Reference (From Research)

### From Previous Stundenhexe Project
Keeping these concepts for future reference when the MVP proves successful:

#### Scheduling Algorithm
- **OR-Tools Integration**: Google's constraint programming solver for optimization
- **Constraint Weight System**: 1-10 scale for soft constraints
  - Teacher preferences: 8
  - Pedagogical considerations: 7
  - Administrative preferences: 5
- **Performance Targets**: 
  - Schedule generation < 5 minutes
  - School setup < 30 minutes
  - 100% hard constraints satisfied
  - 80% soft constraints satisfied

#### Advanced Domain Models
- **CurriculumRequirement**: Grade-specific subject requirements with mandatory/optional flags
- **GradeCurriculum**: Yearly curriculum management per grade
- **TeacherAvailability**: Detailed availability windows beyond simple part-time
- **SubjectRequirement**: Links subjects with qualified teachers
- **RoomFeatures**: Detailed room capabilities (projector, lab equipment, etc.)

#### Complex Constraints Discovered
- **Teacher gap minimization** between classes
- **Subject variety distribution** throughout the day
- **Buffer time** for room transitions
- **Pedagogical timing** (difficult subjects in morning)
- **Even workload distribution** across week
- **Special support coordination** (Förderunterricht)
- **AG (Arbeitsgemeinschaft)** afternoon activities
- **Ganztag** full-day vs half-day considerations

#### German School Specifics to Consider
- **Vertretungsplan**: Sophisticated substitute management system
- **Förderunterricht**: Support lessons requiring coordination
- **Elternzeit/Teilzeit**: Complex part-time arrangements
- **State-specific regulations**: Hesse vs other states
- **School calendar integration**: Different holiday schedules
- **Approval workflows**: Multi-party sign-offs

#### Technical Considerations for Scale
- **Docker deployment** for containerization
- **Grade-based partitioning** for large datasets
- **Caching strategies** for constraint validation
- **Multi-school architecture** 
- **Offline capability** for poor connectivity
- **Historical data** retention for analysis

#### Integration Points
- Import from existing systems (Excel, other tools)
- Export to various formats (PDF, Excel, iCal)
- Parent communication systems
- State reporting requirements
- Existing school management systems

### Why These Were Postponed
We learned from the Stundenhexe experience that starting with all these features leads to:
- Analysis paralysis
- Over-engineering before understanding real needs
- Abandoned projects due to complexity
- Missing actual user pain points

Instead, we're building incrementally based on real user feedback from Hesse pre-school contacts.
