# Docker Setup Guide

## Prerequisites

- Docker Desktop or Docker Engine installed
- Docker Compose V2 (included with Docker Desktop)
- Make (optional, for using Makefile commands)

## Quick Start

### 1. Copy Environment Variables
```bash
cp .env.docker .env
```

### 2. Start All Services
```bash
# Using docker-compose directly
docker-compose up -d

# Or using Make (from backend directory)
cd backend && make docker-up
```

### 3. Run Database Migrations
```bash
# From backend directory
cd backend && make migrate-up

# Or using docker-compose
docker-compose exec backend alembic upgrade head
```

### 4. Seed Development Data (Optional)
```bash
# From backend directory
cd backend && make seed

# Or using docker-compose
docker-compose exec backend python src/seeders/run.py
```

## Available Services

| Service | Port | Description |
|---------|------|-------------|
| Backend API | 8000 | FastAPI application (http://localhost:8000) |
| PostgreSQL | 5432 | Database server |
| Valkey | 6379 | Redis-compatible cache server |
| Mailhog | 8025 | Email testing UI (http://localhost:8025) |

## Docker Commands

### Using Make (from backend directory)

```bash
make docker-build     # Build Docker images
make docker-up        # Start all services
make docker-down      # Stop all services
make docker-logs      # View logs
make docker-shell     # Open shell in backend container
make docker-db-shell  # Open PostgreSQL shell
make docker-clean     # Remove containers and volumes
make docker-restart   # Restart all services
```

### Using docker-compose directly

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Execute commands in container
docker-compose exec backend /bin/bash
docker-compose exec db psql -U postgres -d grundschule_timetabler

# Remove everything including volumes
docker-compose down -v
```

## Development Workflow

1. **Start services**: `docker-compose up -d`
2. **Check logs**: `docker-compose logs -f backend`
3. **Access API**: http://localhost:8000
4. **View API docs**: http://localhost:8000/docs
5. **Check emails**: http://localhost:8025

## Database Management

### Connect to PostgreSQL
```bash
# Using docker-compose
docker-compose exec db psql -U postgres -d grundschule_timetabler

# Using psql directly
psql -h localhost -p 5432 -U postgres -d grundschule_timetabler
```

### Run Migrations
```bash
# Apply migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

## Troubleshooting

### Port Already in Use
If you get port conflicts, either:
1. Stop the conflicting service
2. Or change ports in `docker-compose.yml`

### Database Connection Issues
1. Ensure PostgreSQL service is healthy:
   ```bash
   docker-compose ps
   ```
2. Check database logs:
   ```bash
   docker-compose logs db
   ```

### Permission Issues
The Docker setup runs as non-root user (uid 1000). If you have permission issues:
1. Check file ownership
2. Adjust the user ID in Dockerfile if needed

### Rebuilding After Changes
```bash
# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build backend
```

## Production Deployment

A production configuration is available in `docker-compose.prod.yml`:

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Use with environment file
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
```

Production includes:
- Nginx reverse proxy
- SSL/TLS with Certbot
- Optimized builds
- Health checks
- Restart policies

## VS Code Integration

If using VS Code with Remote Containers:
1. Install "Dev Containers" extension
2. Open command palette: `Ctrl/Cmd + Shift + P`
3. Select "Dev Containers: Reopen in Container"
4. Choose the backend service

## Notes on Valkey

We use Valkey instead of Redis due to licensing concerns:
- Valkey is a community fork of Redis 7.2.4
- Fully compatible with Redis APIs
- BSD licensed (truly open source)
- Supported by Linux Foundation

No code changes are needed - Valkey is a drop-in replacement for Redis.
