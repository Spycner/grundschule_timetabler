# Database Migrations Guide

## Overview

Database migrations are managed using Alembic, a lightweight database migration tool for SQLAlchemy. This guide covers how to work with migrations in the Grundschule Timetabler project.

## Why Migrations?

Migrations provide:
- **Version Control** for database schema
- **Reproducible** database state across environments
- **Safe Rollbacks** when changes cause issues
- **Team Collaboration** with clear schema change history
- **Production Safety** with tested schema changes

## Initial Setup

### First-Time Setup

If you're setting up the project for the first time:

```bash
cd backend
make install           # Install dependencies
make migrate-up        # Apply all migrations
```

This creates the database with the current schema.

### Existing Database

If you have an existing database without migrations:

```bash
# Backup your data first!
sqlite3 timetabler.db .dump > backup.sql

# Initialize Alembic
make migrate-init

# Create initial migration from existing schema
uv run alembic revision --autogenerate -m "Initial schema"

# Mark database as up-to-date
uv run alembic stamp head
```

## Common Operations

### Check Current Migration

```bash
make migrate-current
# or
uv run alembic current
```

### View Migration History

```bash
make migrate-history
# or
uv run alembic history
```

### Apply All Migrations

```bash
make migrate-up
# or
uv run alembic upgrade head
```

### Rollback One Migration

```bash
make migrate-down
# or
uv run alembic downgrade -1
```

### Rollback to Specific Migration

```bash
uv run alembic downgrade <revision_id>
```

## Creating Migrations

### ⚠️ IMPORTANT: Model Import Requirement

**All SQLAlchemy models MUST be imported in `src/models/__init__.py` for Alembic to detect them during automatic migration generation.**

```python
# src/models/__init__.py
from src.models.teacher import Teacher
from src.models.class_ import Class
from src.models.subject import Subject  # Don't forget new models!

__all__ = ["Teacher", "Class", "Subject"]
```

If you forget this step, Alembic will generate an empty migration with no changes detected!

### Automatic Migration Generation

For most schema changes, Alembic can automatically generate migrations:

```bash
make migrate-create name="add_email_to_users"
# or
uv run alembic revision --autogenerate -m "add_email_to_users"
```

This compares your SQLAlchemy models with the database schema and generates the necessary changes.

### Manual Migration

For complex changes or data migrations:

```bash
uv run alembic revision -m "complex_data_migration"
```

Then edit the generated file in `alembic/versions/`.

## Migration File Structure

A typical migration file:

```python
"""Add Teacher model

Revision ID: 71430f948602
Revises: 
Create Date: 2025-08-03 14:43:35.713154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71430f948602'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table('teachers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        # ... more columns
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers_email'), 'teachers', ['email'], unique=True)


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index(op.f('ix_teachers_email'), table_name='teachers')
    op.drop_table('teachers')
```

## SQLite-Specific Considerations

SQLite has limitations with ALTER TABLE operations. Our configuration handles this with batch operations:

### Configuration (alembic/env.py)

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True,  # Enable batch mode for SQLite
)
```

### Batch Operations Example

When altering columns in SQLite:

```python
def upgrade():
    with op.batch_alter_table('teachers') as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(20)))
        batch_op.create_index('ix_teachers_phone', ['phone'])
```

## Best Practices

### 1. Always Review Generated Migrations

Automatic generation is helpful but not perfect. Always review:
- Check the upgrade and downgrade functions
- Verify indexes are created/dropped correctly
- Ensure data won't be lost

### 2. Test Migrations Locally

Before applying to production:
```bash
# Apply migration
make migrate-up

# Test application
make test

# If issues, rollback
make migrate-down
```

### 3. Backup Before Major Changes

```bash
# SQLite backup
sqlite3 timetabler.db .dump > backup_$(date +%Y%m%d).sql

# PostgreSQL backup
pg_dump database_name > backup_$(date +%Y%m%d).sql
```

### 4. Name Migrations Clearly

Use descriptive names:
- ✅ `add_email_verification_to_users`
- ✅ `create_schedule_conflict_table`
- ❌ `update_db`
- ❌ `fix_stuff`

### 5. Don't Edit Applied Migrations

Once a migration is applied to production, never edit it. Create a new migration instead.

### 6. Handle Data Migrations Carefully

When migrating data:
```python
def upgrade():
    # Create new column
    op.add_column('teachers', sa.Column('full_name', sa.String()))
    
    # Migrate data
    connection = op.get_bind()
    result = connection.execute('SELECT id, first_name, last_name FROM teachers')
    for row in result:
        full_name = f"{row.first_name} {row.last_name}"
        connection.execute(
            f"UPDATE teachers SET full_name = '{full_name}' WHERE id = {row.id}"
        )
```

## Common Scenarios

### Adding a New Model

1. Create the SQLAlchemy model in `src/models/`
2. **CRITICAL: Import it in `src/models/__init__.py`** ← This step is essential!
3. Generate migration:
```bash
make migrate-create name="add_schedule_model"
```
4. Review the generated migration file to ensure it's not empty
5. Apply the migration: `make migrate-up`

### Adding a Column

1. Add field to SQLAlchemy model
2. Generate migration:
```bash
make migrate-create name="add_phone_to_teacher"
```

### Renaming a Column

SQLite doesn't support column rename directly:

```python
def upgrade():
    with op.batch_alter_table('teachers') as batch_op:
        batch_op.alter_column('old_name', new_column_name='new_name')
```

### Adding an Index

```python
def upgrade():
    op.create_index('ix_teachers_email_lastname', 'teachers', ['email', 'last_name'])

def downgrade():
    op.drop_index('ix_teachers_email_lastname', table_name='teachers')
```

### Adding a Constraint

```python
def upgrade():
    with op.batch_alter_table('teachers') as batch_op:
        batch_op.create_check_constraint(
            'ck_teachers_max_hours',
            'max_hours_per_week >= 1 AND max_hours_per_week <= 40'
        )
```

## Troubleshooting

### Empty Migration Files (No Changes Detected)

**Problem**: `alembic revision --autogenerate` creates empty `upgrade()` and `downgrade()` functions.

**Most Common Cause**: The model isn't imported in `src/models/__init__.py`.

**Solution**:
1. Import your model in `src/models/__init__.py`
2. If you already generated an empty migration:
   ```bash
   uv run alembic downgrade -1  # Rollback
   rm alembic/versions/<empty_migration>.py  # Delete it
   ```
3. Regenerate the migration:
   ```bash
   make migrate-create name="your_model_name"
   ```

### "Target database is not up to date"

The database is behind the latest migration:
```bash
make migrate-up
```

### "Can't locate revision"

Migration files are out of sync:
```bash
# Check current state
make migrate-current

# Check history
make migrate-history

# If needed, stamp to specific revision
uv run alembic stamp <revision_id>
```

### "Multiple head revisions"

Merge conflicts in migrations:
```bash
# Show current heads
uv run alembic heads

# Merge heads
uv run alembic merge -m "merge_heads"
```

### SQLite "table already exists"

Database and migrations are out of sync:
```bash
# Option 1: Reset database (development only!)
make migrate-reset

# Option 2: Manually sync
uv run alembic stamp head  # Mark as current without running
```

## Production Deployment

### Pre-deployment Checklist

1. ✅ Test migrations on staging environment
2. ✅ Backup production database
3. ✅ Review migration SQL: `uv run alembic upgrade --sql`
4. ✅ Have rollback plan ready
5. ✅ Schedule maintenance window if needed

### Deployment Process

```bash
# 1. Backup
pg_dump production_db > backup_pre_migration.sql

# 2. Apply migrations
uv run alembic upgrade head

# 3. Verify
uv run alembic current

# 4. Test application
make test

# 5. If issues, rollback
uv run alembic downgrade -1
```

## Migration Strategy for Different Environments

### Development
- Reset database freely: `make migrate-reset`
- Experiment with migrations
- Use SQLite for simplicity

### Testing/CI
- Fresh database for each test run
- Apply all migrations from scratch
- Verify migration chain integrity

### Staging
- Mirror production setup
- Test migrations before production
- Use same database type as production

### Production
- Never use `migrate-reset`
- Always backup before migrations
- Use transactions where possible
- Have rollback plan

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLite ALTER TABLE Limitations](https://www.sqlite.org/lang_altertable.html)

## Quick Command Reference

```bash
# Status
make migrate-current      # Show current migration
make migrate-history      # Show all migrations

# Apply/Rollback
make migrate-up          # Apply all pending
make migrate-down        # Rollback one

# Create
make migrate-create name="description"  # New migration

# Reset (dev only)
make migrate-reset       # Drop and recreate

# Manual
uv run alembic upgrade head              # Latest
uv run alembic downgrade -1              # Back one
uv run alembic upgrade <revision>        # Specific
uv run alembic stamp head                # Mark current
```
