# uv Package Manager Reference

## Overview
uv is an extremely fast Python package manager written in Rust by Astral. It's a drop-in replacement for pip, pip-tools, pipx, poetry, pyenv, and virtualenv.

## Installation
uv is pre-installed on this system and available globally.

## Common Commands

### Project Management
```bash
# Initialize a new project
uv init [project-name]

# Initialize in current directory
uv init

# Add a dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Lock dependencies (creates/updates uv.lock)
uv lock

# Sync environment with lock file
uv sync

# Update dependencies
uv lock --upgrade
```

### Virtual Environment Management
```bash
# Create a virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Pin Python version for project
uv python pin 3.11

# Install Python versions
uv python install 3.11 3.12
```

### Running Code
```bash
# Run a script with project dependencies
uv run python script.py

# Run a module
uv run -m module_name

# Run with additional inline dependencies
uv run --with package-name python script.py
```

### Tool Management
```bash
# Run tool without installing (like npx)
uvx tool-name

# Install tool globally
uv tool install tool-name

# Update installed tool
uv tool upgrade tool-name

# List installed tools
uv tool list
```

### Pip Compatibility Mode
```bash
# Compile requirements
uv pip compile requirements.in -o requirements.txt

# Install from requirements
uv pip install -r requirements.txt

# Sync exact requirements
uv pip sync requirements.txt
```

## Project Configuration (pyproject.toml)

### Basic Structure
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]
```

## Workspace Configuration (Monorepo)

### Root pyproject.toml
```toml
[tool.uv.workspace]
members = ["backend", "shared"]
```

### Member pyproject.toml
```toml
[project]
name = "backend"
version = "0.1.0"
dependencies = [
    "shared",  # Reference to workspace member
]

[tool.uv.sources]
shared = { workspace = true }
```

## Environment Variables
```bash
# Set Python version
UV_PYTHON=3.11

# Set virtual environment location
UV_PROJECT_ENVIRONMENT=.venv

# Use system Python
UV_SYSTEM_PYTHON=1

# Offline mode
UV_OFFLINE=1
```

## VS Code Integration

### Settings for Subdirectory Project
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true
}
```

## Common Workflows

### Starting a New Project
```bash
cd backend
uv init
uv add fastapi uvicorn sqlalchemy
uv add --dev pytest ruff
uv run python -m main
```

### Installing from Existing Project
```bash
cd backend
uv sync  # Creates venv and installs from uv.lock
```

### Updating Dependencies
```bash
uv lock --upgrade  # Update all
uv lock --upgrade-package fastapi  # Update specific
uv sync  # Apply updates
```

### Running Tests
```bash
uv run pytest
uv run --with pytest-cov pytest --cov
```

### Formatting and Linting
```bash
uv run ruff check .
uv run ruff format .
```

### Type Checking with ty
```bash
# Run ty type checker (from Astral)
uvx --native-tls ty check

# Check specific files
uvx --native-tls ty check src/main.py

# Note: ty is in alpha, use --native-tls flag for certificate issues
```

## Performance Tips
- uv uses a global cache, so packages are shared across projects
- Lock files ensure reproducible installations
- Use `uv sync` instead of `uv install` for faster syncing
- The `.venv` is created automatically when needed

## Troubleshooting

### Clear Cache
```bash
uv cache clean
```

### Reinstall All Dependencies
```bash
rm -rf .venv
uv sync
```

### Check Python Version
```bash
uv python list  # Available versions
uv python pin 3.11  # Pin for project
```

### Verbose Output
```bash
uv -v sync  # Verbose mode
uv -vv sync  # Very verbose
```

## Migration from pip/poetry

### From requirements.txt
```bash
uv pip install -r requirements.txt
uv add $(cat requirements.txt | grep -v '^#' | cut -d= -f1)
```

### From poetry
```bash
# Export from poetry first
poetry export -f requirements.txt -o requirements.txt
uv pip install -r requirements.txt
```

## Best Practices
1. Always commit `uv.lock` for reproducible builds
2. Use `uv sync` in CI/CD pipelines
3. Pin Python version with `uv python pin`
4. Use workspace for monorepo projects
5. Leverage global cache for faster installs
6. Use `--dev` flag for development dependencies
7. Run tools with `uvx` to avoid global installs
