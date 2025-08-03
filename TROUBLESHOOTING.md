# Troubleshooting Guide

This guide documents common issues encountered during development and their solutions.

## Database Issues

### "no such table" Error After Creating New Model

**Problem**: After creating a new SQLAlchemy model and running migrations, the API throws `sqlite3.OperationalError: no such table: <table_name>` errors.

**Cause**: The model wasn't imported in `src/models/__init__.py`, causing Alembic's autogenerate to create an empty migration.

**Solution**:
1. Import your new model in `src/models/__init__.py`:
   ```python
   from src.models.your_model import YourModel
   __all__ = ["YourModel", ...]
   ```

2. If you already created an empty migration:
   ```bash
   # Rollback the empty migration
   uv run alembic downgrade -1
   
   # Delete the empty migration file
   rm alembic/versions/<migration_id>_*.py
   
   # Regenerate the migration
   uv run alembic revision --autogenerate -m "add_your_model"
   
   # Apply the migration
   uv run alembic upgrade head
   ```

3. Restart your development server to pick up the database changes

**Prevention**: Always import new models in `src/models/__init__.py` before generating migrations.

### Database Out of Sync with Models

**Problem**: Tests pass but the API fails with database errors.

**Cause**: The test database and development database are separate files (`test.db` vs `timetabler.db`).

**Solution**:
```bash
# Check current migration status
make migrate-current

# Apply all pending migrations
make migrate-up

# Restart the development server
make dev
```

## Alembic Migration Issues

### Empty Migration Files

**Problem**: Running `alembic revision --autogenerate` creates a migration with empty `upgrade()` and `downgrade()` functions.

**Cause**: Alembic can't detect your model changes because:
1. Models aren't imported in `src/models/__init__.py`
2. The model isn't inheriting from the correct `Base` class
3. There are no actual changes to detect

**Solution**: Ensure all models are properly imported and inherit from `src.models.database.Base`.

### Migration History Issues

**Problem**: Alembic complains about migration conflicts or can't find the head.

**Solution**:
```bash
# View migration history
make migrate-history

# Show current migration
make migrate-current

# Reset to a specific migration (use with caution!)
uv run alembic downgrade <revision_id>

# Start fresh (DESTROYS ALL DATA!)
rm timetabler.db
uv run alembic upgrade head
```

## Test Issues

### Tests Failing After Model Changes

**Problem**: Tests fail after adding new models or fields.

**Solution**:
1. Ensure test fixtures are updated in `tests/conftest.py`
2. The test database uses migrations, so apply them:
   ```bash
   rm test.db  # Remove old test database
   make test   # Tests will create a fresh database
   ```

### Import Errors in Tests

**Problem**: `ModuleNotFoundError` when running tests.

**Solution**: Always run tests from the backend directory using:
```bash
make test
# or
uv run pytest
```

## Development Server Issues

### Server Not Reflecting Code Changes

**Problem**: Changes to code aren't reflected even with `--reload` flag.

**Solution**:
1. Check if the server is actually running with reload:
   ```bash
   make dev  # Should show "Uvicorn running... (reload enabled)"
   ```

2. For model/database changes, restart the server completely:
   ```bash
   # Stop the server (Ctrl+C)
   make migrate-up  # Apply any pending migrations
   make dev         # Start fresh
   ```

### Port Already in Use

**Problem**: `[Errno 48] Address already in use` when starting the server.

**Solution**:
```bash
# Find the process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn src.main:app --reload --port 8001
```

## Code Quality Issues

### Ruff/Type Checking Failures

**Problem**: `make check` fails with linting or type errors.

**Solution**:
```bash
# Auto-fix formatting issues
make format

# Check what can't be auto-fixed
make lint

# For type errors
make typecheck
```

### Pre-commit Hook Failures

**Problem**: Git commits fail due to pre-commit hooks.

**Solution**:
1. Fix the issues identified by the hooks
2. Or temporarily skip hooks (not recommended):
   ```bash
   git commit --no-verify -m "your message"
   ```

## Common Development Workflows

### Adding a New Model (Correct Order)

1. Create test file first (TDD approach)
2. Create the model in `src/models/`
3. **Import the model in `src/models/__init__.py`** ← Don't forget!
4. Create schemas in `src/schemas/`
5. Create service in `src/services/`
6. Create API routes in `src/api/v1/routes/`
7. Register routes in `src/api/v1/router.py`
8. Generate migration: `make migrate-create name="add_modelname"`
9. Apply migration: `make migrate-up`
10. Run tests: `make test`
11. Restart dev server: `make dev`

### Debugging Database Issues

```bash
# Check what tables exist
sqlite3 timetabler.db ".tables"

# Check table schema
sqlite3 timetabler.db ".schema <table_name>"

# Check migration status
make migrate-current

# View all migrations
make migrate-history
```

## Getting Help

If you encounter issues not covered here:

1. Check the development documentation in `/development-docs/`
2. Review similar working models (Teacher, Class) for patterns
3. Check test files for expected behavior
4. Review the CLAUDE.md file for project conventions
