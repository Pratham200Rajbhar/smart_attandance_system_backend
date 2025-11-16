# Smart Attendance System API Documentation

**Base URL**: `http://localhost:8000`  
**API Prefix**: `/api`

---

## Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
2. [Attendance Endpoints](#attendance-endpoints)
3. [Admin Endpoints](#admin-endpoints)
4. [System Endpoints](#system-endpoints)

---

## Authentication Endpoints

### Register User

Register a new user in the system.

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "role": "student"
}
```

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securePassword123",
    "role": "student"
  }'
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": 123
  }
}
```

**Error Responses**:
- `400 Bad Request`: Email already registered or invalid role
- `422 Unprocessable Entity`: Invalid input format

---

### Login

Authenticate user and receive JWT token.

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `401 Unauthorized`: Incorrect email or password

**Usage**: Store the `access_token` and use it in subsequent requests:
```bash
Authorization: Bearer <access_token>
```

---

### Get User Profile

Get current authenticated user's profile information.

**Endpoint**: `GET /api/auth/profile`

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "created_at": "2024-01-01T10:00:00.000Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User not found

---

## Attendance Endpoints

### Verify Attendance

Mark attendance using face recognition technology.

**Endpoint**: `POST /api/attendance/verify`

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Form Data**:
- `student_id` (integer, required): ID of the student marking attendance
- `face_image` (string, required): Base64 encoded image (JPEG/PNG)

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/attendance/verify" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -F "student_id=123" \
  -F "face_image=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
```

**Response - Success** (200 OK):
```json
{
  "status": "success",
  "message": "Attendance marked as present",
  "data": {
    "attendance_id": 456,
    "status": "present",
    "confidence": 0.87,
    "student_name": "John Doe"
  }
}
```

**Response - Low Confidence** (200 OK):
```json
{
  "status": "success",
  "message": "Attendance marked as flagged",
  "data": {
    "attendance_id": 457,
    "status": "flagged",
    "confidence": 0.45,
    "student_name": "John Doe"
  }
}
```

**Attendance Status Logic**:
- `present`: Face confidence ≥ 0.6 (60% match)
- `flagged`: Face confidence < 0.6 (requires manual verification)

**Error Responses**:
- `400 Bad Request`: No face detected in image or student face not registered
- `404 Not Found`: Student not found
- `401 Unauthorized`: Invalid token

---

### Get Attendance Records

Retrieve attendance history for a specific student.

**Endpoint**: `GET /api/attendance/{student_id}`

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/api/attendance/123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
[
  {
    "id": 456,
    "student_id": 123,
    "status": "present",
    "confidence": 0.87,
    "timestamp": "2024-01-01T10:00:00.000Z"
  },
  {
    "id": 455,
    "student_id": 123,
    "status": "flagged",
    "confidence": 0.45,
    "timestamp": "2024-01-01T09:00:00.000Z"
  }
]
```

**Error Responses**:
- `404 Not Found`: Student not found
- `401 Unauthorized`: Invalid token

---

## Admin Endpoints

> **Note**: All admin endpoints require admin role authentication

### Student Management

#### Add Student

Add a new student to the system.

**Endpoint**: `POST /api/admin/students`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "STU001",
  "name": "Jane Smith",
  "email": "jane@university.edu"
}
```

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "Jane Smith",
    "email": "jane@university.edu"
  }'
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Student added successfully",
  "data": {
    "student_id": 124
  }
}
```

**Error Responses**:
- `400 Bad Request`: Email already exists
- `403 Forbidden`: Admin access required

---

#### Upload Student Face

Upload face image for a student to enable face recognition.

**Endpoint**: `POST /api/admin/students/{student_id}/face`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
Content-Type: multipart/form-data
```

**Form Data**:
- `face_image` (string, required): Base64 encoded clear face image

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/admin/students/124/face" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -F "face_image=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Face uploaded successfully"
}
```

**Error Responses**:
- `400 Bad Request`: No face found in image
- `404 Not Found`: Student not found
- `403 Forbidden`: Admin access required

---

#### List All Students

Retrieve list of all students.

**Endpoint**: `GET /api/admin/students`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
```

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
[
  {
    "id": 124,
    "student_id": "STU001",
    "name": "Jane Smith",
    "email": "jane@university.edu",
    "created_at": "2024-01-01T10:00:00.000Z"
  },
  {
    "id": 125,
    "student_id": "STU002",
    "name": "Bob Johnson",
    "email": "bob@university.edu",
    "created_at": "2024-01-01T11:00:00.000Z"
  }
]
```

**Error Responses**:
- `403 Forbidden`: Admin access required

---

#### Delete Student

Remove a student from the system.

**Endpoint**: `DELETE /api/admin/students/{student_id}`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
```

**CURL Example**:
```bash
curl -X DELETE "http://localhost:8000/api/admin/students/124" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Student deleted successfully"
}
```

**Note**: This will also delete all associated attendance records due to cascade delete.

**Error Responses**:
- `404 Not Found`: Student not found
- `403 Forbidden`: Admin access required

---

### Teacher Management

#### Add Teacher

Add a new teacher to the system.

**Endpoint**: `POST /api/admin/teachers`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Dr. Sarah Wilson",
  "email": "sarah@university.edu",
  "department": "Computer Science",
  "password": "teacher123"
}
```

**CURL Example**:
```bash
curl -X POST "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Sarah Wilson",
    "email": "sarah@university.edu",
    "department": "Computer Science",
    "password": "teacher123"
  }'
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Teacher added successfully",
  "data": {
    "teacher_id": 15
  }
}
```

**Important Notes**:
- **Password is REQUIRED**: The password field is mandatory when creating a teacher
- **Automatic User Creation**: The system automatically creates a User record in the users table with the provided password
- **Immediate Login**: Teachers can login immediately after creation using their email and password
- **Dual Records**: Creating a teacher creates both a `Teacher` record (in teachers table) and a `User` record (in users table)

**Error Responses**:
- `400 Bad Request`: Email already exists in teachers table or users table
- `403 Forbidden`: Admin access required
- `422 Unprocessable Entity`: Missing required password field

---

#### List All Teachers

Retrieve list of all teachers.

**Endpoint**: `GET /api/admin/teachers`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
```

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
[
  {
    "id": 15,
    "name": "Dr. Sarah Wilson",
    "email": "sarah@university.edu",
    "department": "Computer Science",
    "created_at": "2024-01-01T10:00:00.000Z"
  },
  {
    "id": 16,
    "name": "Prof. Michael Brown",
    "email": "michael@university.edu",
    "department": "Mathematics",
    "created_at": "2024-01-01T11:00:00.000Z"
  }
]
```

**Error Responses**:
- `403 Forbidden`: Admin access required

---

#### Delete Teacher

Remove a teacher from the system.

**Endpoint**: `DELETE /api/admin/teachers/{teacher_id}`

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
```

**CURL Example**:
```bash
curl -X DELETE "http://localhost:8000/api/admin/teachers/15" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Teacher deleted successfully"
}
```

**Important Notes**:
- **Cascade Deletion**: Deleting a teacher will also automatically delete the associated User record
- **Login Access**: After deletion, the teacher will no longer be able to login

**Error Responses**:
- `404 Not Found`: Teacher not found
- `403 Forbidden`: Admin access required

---

## System Endpoints

### Health Check

Verify API is running.

**Endpoint**: `GET /`

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/"
```

**Response** (200 OK):
```json
{
  "message": "Smart Attendance System API",
  "status": "running"
}
```

---

### Detailed Health Check

Detailed health check endpoint.

**Endpoint**: `GET /health`

**CURL Example**:
```bash
curl -X GET "http://localhost:8000/health"
```

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

---

## Authentication Flow

### Complete Example Workflow

1. **Register a new user** (optional, if not using admin):
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "student"
  }'
```

2. **Login to get token**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

3. **Use token in subsequent requests**:
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error description"
}
```

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input or missing required fields |
| 401 | Unauthorized | Invalid or missing authentication token |
| 403 | Forbidden | Insufficient permissions (non-admin accessing admin routes) |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error in request data |
| 500 | Internal Server Error | Server error |

---

## Face Image Format

### Base64 Encoding

The API accepts base64 encoded images in two formats:

1. **Data URL format** (recommended):
```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA...
```

2. **Raw base64 string**:
```
/9j/4AAQSkZJRgABAQEA...
```

### Image Requirements

- **Format**: JPEG, PNG, or BMP
- **Resolution**: Recommended 640x480 or higher
- **Content**: Clear, front-facing photo with good lighting
- **Faces**: Only one face per image

### JavaScript Example (Frontend)

```javascript
// Capture image from camera
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
context.drawImage(video, 0, 0, canvas.width, canvas.height);
const base64Image = canvas.toDataURL('image/jpeg');

// Send to API
const formData = new FormData();
formData.append('student_id', studentId);
formData.append('face_image', base64Image);

fetch('/api/attendance/verify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

---

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key (change in production)
- `BACKEND_CORS_ORIGINS`: Allowed origins for CORS
- `FACE_RECOGNITION_THRESHOLD`: Face matching threshold (default: 0.6)

### Default Settings

- **JWT Expiry**: 24 hours (1440 minutes)
- **Face Recognition Threshold**: 0.6 (60% similarity)
- **CORS Origins**: `localhost:3000, localhost:8080`

---

## Default Admin Credentials

After initial setup, you can login with the default admin account:

- **Email**: `admin@smartattendance.com`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change this password immediately after first login in production!

---

## Testing

### Automated Test Suite

A comprehensive test script is available to test all endpoints:

```bash
python test_all_endpoints.py
```

The test suite covers:
- ✅ System endpoints (health checks)
- ✅ Authentication endpoints (register, login, profile)
- ✅ Student management (CRUD operations)
- ✅ Teacher management (CRUD operations with automatic login)
- ✅ Attendance endpoints
- ✅ Error handling (unauthorized access, invalid credentials, etc.)

**Test Results**: The script provides detailed output showing which tests passed/failed with a success rate percentage.

### Manual Testing

You can also test endpoints manually using:
- **Swagger UI**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative documentation view)
- **CURL**: Use the examples provided in this documentation
- **Postman**: Import the API collection from Swagger UI

---

## Interactive API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Quick Reference

### Authentication Headers
```bash
-H "Authorization: Bearer <your_jwt_token>"
```

### Content Types
- JSON: `-H "Content-Type: application/json"`
- Form Data: `-F "key=value"` (for multipart/form-data)

### Base URL
```
http://localhost:8000
```

---

## Important Implementation Notes

### Teacher Creation Flow

When creating a teacher via `/api/admin/teachers`:

1. **Required Fields**: `name`, `email`, `password` (required), `department` (optional)
2. **Dual Record Creation**: 
   - Creates a `Teacher` record in the `teachers` table
   - Automatically creates a `User` record in the `users` table with:
     - Same name and email
     - Hashed password
     - Role set to "teacher"
3. **Immediate Login**: The teacher can login immediately using `/api/auth/login` with their email and password
4. **Deletion**: Deleting a teacher also deletes the associated User record

### Student vs User

- **Students**: Created via `/api/admin/students` - stored in `students` table (no password, no login)
- **Users**: Created via `/api/auth/register` or automatically for teachers - stored in `users` table (has password, can login)
- **Teachers**: Created via `/api/admin/teachers` - stored in both `teachers` and `users` tables (can login)

### Face Recognition Workflow

1. **Register Student**: Admin creates student via `/api/admin/students`
2. **Upload Face**: Admin uploads student's face image via `/api/admin/students/{id}/face`
3. **Mark Attendance**: Teacher/Student uses `/api/attendance/verify` with face image
4. **View Records**: Get attendance history via `/api/attendance/{student_id}`

---

**Last Updated**: November 2024  
**API Version**: 1.0.0  
**Test Coverage**: 94.1% (17 endpoints tested)

