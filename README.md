# Grundschule Timetabler

A modern, web-based timetabling application designed specifically for German Grundschule (elementary school) principals and administrators. This tool simplifies the complex task of creating and managing class schedules, teacher assignments, and resource allocation while respecting all necessary constraints and regulations.

## 🎯 Project Goals

- **Simplify schedule creation** for German elementary schools
- **Automate conflict resolution** in timetabling
- **Support part-time teachers** and complex availability patterns
- **Ensure pedagogical best practices** (e.g., difficult subjects in morning slots)
- **Provide intuitive UI** for non-technical users
- **Handle German-specific requirements** like Förderunterricht and AG activities

## 📊 Current Status

### ✅ Completed
- Backend infrastructure with FastAPI
- API versioning structure (`/api/v1/`)
- Teacher model with full CRUD operations
- Class model with full CRUD operations
- Database migrations with Alembic
- Test-Driven Development setup (33 tests passing)
- Pre-commit hooks for code quality
- Development tooling (uv, ruff, ty)

### 🚧 In Progress
- Subject model implementation
- Time slot management
- Basic scheduling logic

### 📋 Planned
- Frontend with React/TypeScript
- Automatic schedule generation
- Conflict detection and resolution
- Multi-school support
- GDPR compliance features

## 🛠 Tech Stack

### Backend
- **Python 3.12** with **FastAPI**
- **SQLAlchemy** ORM with **Alembic** migrations
- **PostgreSQL** (production) / **SQLite** (development)
- **uv** for package management
- **Ruff** for linting/formatting
- **ty** for type checking

### Frontend (Planned)
- **TypeScript** with **React**
- **Tailwind CSS** for styling
- **Vite** for build tooling

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- OR Python 3.12+ with uv package manager
- Git

### Option 1: Using Docker (Recommended)
```bash
# Clone repository
git clone https://github.com/Spycner/grundschule_timetabler.git
cd grundschule_timetabler

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed development data (optional)
docker-compose exec backend python src/seeders/run.py

# Access the application
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Email UI: http://localhost:8025
```

See [DOCKER.md](DOCKER.md) for detailed Docker setup.

### Option 2: Local Development
```bash
# Clone repository
git clone https://github.com/Spycner/grundschule_timetabler.git
cd grundschule_timetabler

# Set up backend
cd backend
make install        # Install dependencies
make migrate-up     # Apply database migrations
make dev           # Start development server

# Access the application
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📚 Documentation

- [Backend Documentation](./backend/README.md) - Detailed backend setup and API reference
- [Requirements Overview](./requirements/overview.md) - Functional and non-functional requirements
- [Task Management](./tasks/README.md) - Current and completed tasks
- [Development Docs](./development-docs/) - Technical references and guides

## 🧪 Development

### Test-Driven Development (TDD)
We follow TDD principles:
1. Write tests first
2. Write minimal code to pass tests
3. Refactor while keeping tests green

Example:
```bash
cd backend
uv run pytest tests/test_teacher.py  # Run teacher tests
make test                              # Run all tests
make test-cov                          # Run with coverage
```

### Code Quality
Pre-commit hooks ensure code quality:
```bash
make pre-commit-install  # Install hooks (one-time)
make check              # Run all checks manually
make format             # Format code
make lint               # Check linting
```

### Database Migrations
```bash
make migrate-create name="add_new_feature"  # Create migration
make migrate-up                              # Apply migrations
make migrate-down                            # Rollback last migration
```

## 🔑 Key Features

### Current
- **Teacher Management**: Create, update, and manage teacher profiles
- **API Versioning**: Future-proof API design with version control
- **Database Migrations**: Safe schema evolution with Alembic
- **Comprehensive Testing**: TDD with pytest

### Planned
- **Automatic Scheduling**: OR-Tools based constraint solver
- **Conflict Detection**: Real-time conflict identification
- **Multi-language Support**: German and English interfaces
- **Export Functions**: PDF, Excel, and calendar exports
- **Substitute Management**: Handle teacher absences efficiently

## 📖 API Examples

### Create a Teacher
```bash
curl -X POST http://localhost:8000/api/v1/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Maria",
    "last_name": "Müller",
    "email": "maria.mueller@schule.de",
    "abbreviation": "MUE",
    "max_hours_per_week": 28,
    "is_part_time": false
  }'
```

### List All Teachers
```bash
curl http://localhost:8000/api/v1/teachers
```

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Follow TDD - write tests first
4. Ensure all tests pass
5. Run code quality checks
6. Submit a pull request

## 📄 License

TBD - This project is currently under development.

## 📞 Contact

- **Author**: Pascal Kraus
- **Email**: pascal98kraus@gmail.com
- **Repository**: https://github.com/Spycner/grundschule_timetabler

## 🙏 Acknowledgments

- Inspired by the challenges faced by German elementary school administrators
- Built with modern Python tooling from Astral (uv, ruff, ty)
- Designed for real-world use in Hesse pre-schools
