# Grundschule Timetabler Backend

Backend API for the Grundschule Timetabler application - a scheduling system for German elementary schools.

## Tech Stack

- **Python 3.12** - Programming language
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **PostgreSQL/SQLite** - Database
- **uv** - Package manager
- **Ruff** - Linter and formatter
- **ty** - Type checker (from Astral)

## Project Structure

```
backend/
├── src/
│   ├── api/              # API endpoints
│   │   └── v1/           # Version 1 API
│   │       └── routes/   # Route definitions
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic validation schemas
│   ├── services/         # Business logic
│   ├── seeders/          # Database seeders for development
│   ├── config.py         # Configuration
│   └── main.py           # Application entry point
├── tests/                # Test files
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── Makefile              # Common commands
├── pyproject.toml        # Project configuration
├── ruff.toml             # Ruff configuration
├── pytest.ini            # Pytest configuration
├── alembic.ini           # Alembic configuration
├── Dockerfile            # Docker container definition
└── .dockerignore         # Docker ignore patterns
```

## Setup

### Prerequisites

- Python 3.12+
- uv package manager

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
make install
# or
uv sync
```

3. Apply database migrations:
```bash
make migrate-up
# or
uv run alembic upgrade head
```

4. Copy environment variables (if needed):
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Install pre-commit hooks (for development):
```bash
make pre-commit-install
```

## Docker Setup

For Docker-based development, see the [Docker documentation](../DOCKER.md) in the root directory.

Quick start with Docker:
```bash
# From root directory
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python src/seeders/run.py
```

## Development

### Run Development Server

```bash
make dev
# or
uv run uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run Tests

```bash
make test
# or with coverage
make test-cov
```

### Code Quality

Pre-commit hooks are configured to automatically check code quality before commits. They include:
- Python linting and formatting (ruff)
- Type checking (ty)
- File cleanup (trailing whitespace, end of file)
- Config file validation (YAML, TOML, JSON)
- Security checks (no secrets, merge conflicts)
- Commit message validation (conventional commits)

Run hooks manually:
```bash
make pre-commit-run
```

Individual quality checks:
```bash
make format     # Format code
make lint       # Run linter
make typecheck  # Type checking
make check      # Run all checks
make fix        # Fix issues and format
```

To bypass hooks in emergency (not recommended):
```bash
git commit --no-verify -m "Emergency fix"
```

## Database

### Migrations

The database schema is managed by Alembic. Always use migrations to modify the database structure.

Create a new migration:
```bash
make migrate-create name="add_new_table"
# or
uv run alembic revision --autogenerate -m "add_new_table"
```

Apply migrations:
```bash
make migrate-up
# or
uv run alembic upgrade head
```

Rollback one migration:
```bash
make migrate-down
# or
uv run alembic downgrade -1
```

View migration history:
```bash
make migrate-history
# or
uv run alembic history
```

Check current migration:
```bash
make migrate-current
# or
uv run alembic current
```

Reset database (development only):
```bash
make migrate-reset
```

### Seeding Development Data

For development, you can seed the database with sample data:

```bash
# Seed with sample teachers and classes
make seed

# Clear existing data and reseed
make seed-clear

# Only clear seeded data (no reseeding)
make seed-clear-only

# Or manually:
uv run python src/seeders/run.py
uv run python src/seeders/run.py --clear  # Clear and reseed
uv run python src/seeders/run.py --clear-only  # Clear only
```

The seeder creates:
- 8 sample teachers (mix of full-time and part-time)
- 8 sample classes (grades 1-4, two classes per grade)

## API Endpoints

All endpoints are versioned under `/api/v1/`

### Health Check

- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/ready` - Readiness check with database

### Teacher Management

- `GET /api/v1/teachers` - List all teachers
  - Query params: `skip` (offset), `limit` (max results)
- `GET /api/v1/teachers/{id}` - Get specific teacher
- `POST /api/v1/teachers` - Create new teacher
  - Body: `{first_name, last_name, email, abbreviation, max_hours_per_week, is_part_time}`
- `PUT /api/v1/teachers/{id}` - Update teacher
  - Body: Any fields to update
- `DELETE /api/v1/teachers/{id}` - Delete teacher

### Class Management

- `GET /api/v1/classes` - List all classes
  - Query params: `skip` (offset), `limit` (max results)
- `GET /api/v1/classes/{id}` - Get specific class
- `POST /api/v1/classes` - Create new class
  - Body: `{name, grade, size, home_room}`
- `PUT /api/v1/classes/{id}` - Update class
  - Body: Any fields to update
- `DELETE /api/v1/classes/{id}` - Delete class

### Coming Soon

- Subject management
- Timetable generation
- Conflict resolution

## Environment Variables

Key variables:
- `DATABASE_URL` - Database connection string (default: `sqlite:///./timetabler.db`)
- `SECRET_KEY` - Application secret key
- `FRONTEND_URL` - Frontend URL for CORS
- `ENVIRONMENT` - development/testing/production

## Common Commands

See all available commands:
```bash
make help
```

Key commands:
- `make dev` - Run development server
- `make test` - Run tests
- `make format` - Format code
- `make lint` - Run linter
- `make typecheck` - Type checking
- `make migrate-up` - Apply migrations
- `make db-shell` - Open database shell

## Testing

Tests are written using pytest following TDD principles.

Run all tests:
```bash
make test
```

Run specific test file:
```bash
uv run pytest tests/test_teacher.py
```

Run with coverage:
```bash
make test-cov
```

## Development Workflow

1. **Write tests first** (TDD approach)
2. **Implement feature** to make tests pass
3. **Run quality checks**: `make check`
4. **Create migration** if database changes: `make migrate-create name="description"`
5. **Apply migration**: `make migrate-up`
6. **Commit changes** (pre-commit hooks will run automatically)

## Contributing

1. Create a feature branch
2. Follow TDD - write tests first
3. Make your changes
4. Run tests and linting
5. Create migrations if needed
6. Submit a pull request

## License

TBD
