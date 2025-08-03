# API Documentation

## Overview

The Grundschule Timetabler API is a RESTful API built with FastAPI that provides endpoints for managing school timetabling operations. All endpoints are versioned to ensure backward compatibility and smooth migrations.

## Base URL

```
Development: http://localhost:8000
Production: TBD
```

## API Versioning

### Strategy
We use URL path versioning for clear and explicit version control:
- Current version: `v1`
- Base path: `/api/v1/`
- Example: `http://localhost:8000/api/v1/teachers`

### Version Lifecycle
- **Active**: Currently supported and receiving updates
- **Deprecated**: Supported but not receiving new features (6-month notice)
- **Sunset**: No longer available

### Migration Path
When a new version is released:
1. Both versions run concurrently for 6 months
2. Deprecation warnings added to old version responses
3. Migration guide provided for breaking changes
4. Old version removed after sunset period

## Authentication

Currently, the API does not require authentication (development phase). Future versions will implement:
- JWT-based authentication
- Role-based access control (RBAC)
- API key support for external integrations

## Common Headers

### Request Headers
```http
Content-Type: application/json
Accept: application/json
```

### Response Headers
```http
Content-Type: application/json
X-API-Version: v1
```

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK` - Successful GET, PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource (e.g., email already exists)
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Endpoints

### Health Checks

#### GET /api/v1/health
Basic health check to verify the service is running.

**Response**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T12:00:00Z",
  "service": "Grundschule Timetabler API",
  "version": "0.1.0",
  "environment": "development"
}
```

#### GET /api/v1/health/ready
Readiness check including database connectivity.

**Response**
```json
{
  "status": "ready",
  "timestamp": "2025-08-03T12:00:00Z",
  "service": "Grundschule Timetabler API",
  "version": "0.1.0",
  "environment": "development",
  "database": "connected"
}
```

### Teacher Management

#### GET /api/v1/teachers
List all teachers with optional pagination.

**Query Parameters**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response**
```json
[
  {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Müller",
    "email": "maria.mueller@schule.de",
    "abbreviation": "MUE",
    "max_hours_per_week": 28,
    "is_part_time": false,
    "created_at": "2025-08-03T10:00:00Z",
    "updated_at": "2025-08-03T10:00:00Z"
  }
]
```

#### GET /api/v1/teachers/{id}
Get a specific teacher by ID.

**Path Parameters**
- `id` (int): Teacher ID

**Response**
```json
{
  "id": 1,
  "first_name": "Maria",
  "last_name": "Müller",
  "email": "maria.mueller@schule.de",
  "abbreviation": "MUE",
  "max_hours_per_week": 28,
  "is_part_time": false,
  "created_at": "2025-08-03T10:00:00Z",
  "updated_at": "2025-08-03T10:00:00Z"
}
```

**Error Responses**
- `404 Not Found` - Teacher not found

#### POST /api/v1/teachers
Create a new teacher.

**Request Body**
```json
{
  "first_name": "Maria",
  "last_name": "Müller",
  "email": "maria.mueller@schule.de",
  "abbreviation": "MUE",
  "max_hours_per_week": 28,
  "is_part_time": false
}
```

**Validation Rules**
- `first_name`: Required, 1-100 characters
- `last_name`: Required, 1-100 characters
- `email`: Required, valid email format, unique
- `abbreviation`: Required, 2-3 characters, unique, automatically uppercased
- `max_hours_per_week`: Optional (default: 28), range: 1-40
- `is_part_time`: Optional (default: false)

**Response**
```json
{
  "id": 1,
  "first_name": "Maria",
  "last_name": "Müller",
  "email": "maria.mueller@schule.de",
  "abbreviation": "MUE",
  "max_hours_per_week": 28,
  "is_part_time": false,
  "created_at": "2025-08-03T10:00:00Z",
  "updated_at": "2025-08-03T10:00:00Z"
}
```

**Error Responses**
- `409 Conflict` - Email or abbreviation already exists
- `422 Unprocessable Entity` - Validation error

#### PUT /api/v1/teachers/{id}
Update an existing teacher. All fields are optional.

**Path Parameters**
- `id` (int): Teacher ID

**Request Body**
```json
{
  "max_hours_per_week": 20,
  "is_part_time": true
}
```

**Response**
```json
{
  "id": 1,
  "first_name": "Maria",
  "last_name": "Müller",
  "email": "maria.mueller@schule.de",
  "abbreviation": "MUE",
  "max_hours_per_week": 20,
  "is_part_time": true,
  "created_at": "2025-08-03T10:00:00Z",
  "updated_at": "2025-08-03T12:00:00Z"
}
```

**Error Responses**
- `404 Not Found` - Teacher not found
- `409 Conflict` - Email or abbreviation already exists
- `422 Unprocessable Entity` - Validation error

#### DELETE /api/v1/teachers/{id}
Delete a teacher.

**Path Parameters**
- `id` (int): Teacher ID

**Response**
- `204 No Content` - Successfully deleted

**Error Responses**
- `404 Not Found` - Teacher not found

## Pagination

For endpoints that return lists, pagination is implemented using `skip` and `limit` parameters:
- `skip`: Number of records to skip (for offset-based pagination)
- `limit`: Maximum number of records to return

Example:
```
GET /api/v1/teachers?skip=20&limit=10
```
This returns 10 teachers starting from the 21st record.

## Rate Limiting

Currently not implemented. Future versions will include:
- 1000 requests per hour per IP (anonymous)
- 10000 requests per hour per authenticated user
- Headers will include rate limit information

## CORS

Cross-Origin Resource Sharing is configured for:
- Development: `http://localhost:5173`, `http://localhost:3000`
- Production: Will be configured based on frontend deployment

## Examples

### cURL Examples

#### Create a Teacher
```bash
curl -X POST http://localhost:8000/api/v1/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Hans",
    "last_name": "Schmidt",
    "email": "hans.schmidt@schule.de",
    "abbreviation": "SCH",
    "max_hours_per_week": 20,
    "is_part_time": true
  }'
```

#### Update a Teacher
```bash
curl -X PUT http://localhost:8000/api/v1/teachers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "max_hours_per_week": 25
  }'
```

#### Delete a Teacher
```bash
curl -X DELETE http://localhost:8000/api/v1/teachers/1
```

### Python Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Create a teacher
teacher_data = {
    "first_name": "Anna",
    "last_name": "Weber",
    "email": "anna.weber@schule.de",
    "abbreviation": "WEB",
    "max_hours_per_week": 28,
    "is_part_time": False
}

response = requests.post(f"{BASE_URL}/teachers", json=teacher_data)
teacher = response.json()
print(f"Created teacher with ID: {teacher['id']}")

# Get all teachers
response = requests.get(f"{BASE_URL}/teachers")
teachers = response.json()
print(f"Total teachers: {len(teachers)}")
```

### JavaScript/TypeScript Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Create a teacher
async function createTeacher() {
  const teacherData = {
    first_name: 'Klaus',
    last_name: 'Meyer',
    email: 'klaus.meyer@schule.de',
    abbreviation: 'MEY',
    max_hours_per_week: 28,
    is_part_time: false
  };

  const response = await fetch(`${BASE_URL}/teachers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(teacherData),
  });

  const teacher = await response.json();
  console.log('Created teacher:', teacher);
}

// Get all teachers
async function getTeachers() {
  const response = await fetch(`${BASE_URL}/teachers`);
  const teachers = await response.json();
  console.log('Teachers:', teachers);
}
```

## Coming Soon

### Planned Endpoints

#### Class Management
- `GET /api/v1/classes` - List all classes
- `GET /api/v1/classes/{id}` - Get specific class
- `POST /api/v1/classes` - Create new class
- `PUT /api/v1/classes/{id}` - Update class
- `DELETE /api/v1/classes/{id}` - Delete class

#### Subject Management
- `GET /api/v1/subjects` - List all subjects
- `GET /api/v1/subjects/{id}` - Get specific subject
- `POST /api/v1/subjects` - Create new subject
- `PUT /api/v1/subjects/{id}` - Update subject
- `DELETE /api/v1/subjects/{id}` - Delete subject

#### Schedule Management
- `GET /api/v1/schedules` - List all schedules
- `POST /api/v1/schedules/generate` - Generate new schedule
- `GET /api/v1/schedules/{id}/conflicts` - Get schedule conflicts

## Support

For API issues or questions:
- Check the interactive documentation at `/docs`
- Review error messages for specific validation issues
- Contact: pascal98kraus@gmail.com
