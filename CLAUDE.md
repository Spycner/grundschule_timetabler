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

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user workflows
- Minimum 80% code coverage target

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

### Current Phase: Foundation
- Basic domain modeling (Next)
- Simple CRUD operations for core entities
- Database schema design

### Phase 2: Core Scheduling
- Timetable creation algorithm
- Conflict detection
- Manual adjustments

### Phase 3: Advanced Features
- Automatic optimization
- Substitute teacher management
- Report generation

### Phase 4: Production Ready
- Multi-school support
- User authentication
- Data import/export
- GDPR compliance

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

# Or manually:
uv sync              # Install dependencies
uv run uvicorn src.main:app --reload  # Run server
uv run pytest        # Run tests
uv run ruff check .  # Lint
uv run ruff format . # Format
uvx --native-tls ty check  # Type check
```

### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
npm test
```

## Key Files and Directories
- `/requirements/` - Detailed project requirements
- `/tasks/` - Task management system (backlog, doing, completed)
- `/backend/` - Python backend application (FastAPI)
- `/frontend/` - TypeScript frontend application (not yet implemented)
- `/development-docs/` - Development reference documentation (uv, ty)
- `/.vscode/` - VS Code workspace configuration

## Current Working State

### Backend API
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health
- **Readiness**: http://localhost:8000/api/health/ready

### Available Endpoints
- `GET /` - Welcome message
- `GET /api/health` - Basic health check
- `GET /api/health/ready` - Database connectivity check

### Next Steps
1. Implement Teacher model and CRUD operations
2. Implement Class model and CRUD operations
3. Implement Subject model
4. Design Room management
5. Create basic timetable structure

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