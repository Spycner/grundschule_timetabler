# API Versioning Strategy

## Overview
This document outlines our API versioning approach to ensure backward compatibility and smooth transitions for school systems using our timetabling API.

## Versioning Method
We use **URL path versioning** as our primary method:
- Pattern: `/api/v{version}/resource`
- Example: `/api/v1/teachers`

## Current Version
- **v1**: Initial MVP release (current)

## Versioning Rules

### When to Create a New Version
Create a new major version (v2, v3, etc.) only when:
1. **Breaking Changes**:
   - Removing fields from responses
   - Changing field types (e.g., string to number)
   - Changing required fields in requests
   - Removing endpoints
   - Changing authentication methods

### When NOT to Version
No new version needed for:
1. **Backward Compatible Changes**:
   - Adding new optional fields to requests
   - Adding new fields to responses
   - Adding new endpoints
   - Performance improvements
   - Bug fixes

## Implementation in FastAPI

### Router Configuration
```python
from fastapi import APIRouter

# Version 1 router
v1_router = APIRouter(prefix="/api/v1")

# Register endpoints
v1_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
v1_router.include_router(classes.router, prefix="/classes", tags=["classes"])
```

### Main App Setup
```python
from fastapi import FastAPI

app = FastAPI(title="Grundschule Timetabler API")

# Include versioned routers
app.include_router(v1_router)

# Future: app.include_router(v2_router) when needed
```

## Migration Strategy

### Deprecation Process
1. **Announce**: 6 months notice before deprecating a version
2. **Document**: Clear migration guide for breaking changes
3. **Support**: Maintain old version during transition period
4. **Monitor**: Track usage of deprecated endpoints
5. **Remove**: Only after all schools have migrated

### Version Headers
Support optional version specification via headers:
```
Accept: application/vnd.grundschule.v1+json
```

### Response Headers
Include version information in responses:
```
X-API-Version: v1
X-API-Deprecated: false
```

## Client Recommendations

### For Frontend
```typescript
// Configure API base URL with version
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Use in requests
fetch(`${API_BASE}/teachers`)
```

### For External Integrations
Always use explicit versioning in URLs to avoid breaking changes.

## Version Lifecycle

### v1 (Current - MVP)
- **Status**: Active Development
- **Focus**: Basic CRUD operations
- **Stability**: May have minor changes based on user feedback

### v2 (Future)
- **Planned After**: MVP validation with real schools
- **Potential Changes**:
  - Enhanced constraint system
  - Advanced scheduling algorithms
  - Multi-school support

## Testing Strategy

### Version-Specific Tests
```python
def test_v1_teachers_endpoint():
    response = client.get("/api/v1/teachers")
    assert response.status_code == 200

def test_v2_teachers_endpoint():
    # Future v2 tests
    response = client.get("/api/v2/teachers")
    assert response.status_code == 200
```

### Backward Compatibility Tests
Ensure v1 endpoints continue working when v2 is introduced.

## Documentation

### OpenAPI/Swagger
Each version has its own documentation:
- v1 Docs: `http://localhost:8000/api/v1/docs`
- v2 Docs: `http://localhost:8000/api/v2/docs` (future)

### Changelog
Maintain a detailed CHANGELOG.md for each version with:
- Breaking changes
- New features
- Deprecations
- Migration guides

## Best Practices

1. **Start with v1**: Don't use "v0" or unversioned endpoints in production
2. **Minimize versions**: Avoid creating new versions unnecessarily
3. **Clear communication**: Always announce changes well in advance
4. **Gradual migration**: Support multiple versions during transition
5. **Monitor usage**: Track which versions are being used
6. **Document everything**: Clear API documentation for each version

## Examples

### Good Version Change (v1 → v2)
```python
# v1 Response
{
    "id": 1,
    "name": "Maria Müller",  # Single field
    "email": "maria@school.de"
}

# v2 Response (Breaking change - field split)
{
    "id": 1,
    "first_name": "Maria",  # Split into two fields
    "last_name": "Müller",
    "email": "maria@school.de"
}
```

### Good Non-Breaking Addition (within v1)
```python
# Original v1 Response
{
    "id": 1,
    "name": "1a",
    "grade": 1
}

# Enhanced v1 Response (no version change needed)
{
    "id": 1,
    "name": "1a",
    "grade": 1,
    "size": 22  # New optional field added
}
```

## Conclusion
By following this versioning strategy, we ensure that schools can rely on our API without unexpected disruptions while we continue to improve and expand functionality based on user feedback.
