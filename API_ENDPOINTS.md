# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### 1. Register User
**Endpoint:** `POST /api/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "student"
}
```

**Roles:** `admin`, `teacher`, `student` (default: `student`)

**Response:**
```json
{
  "message": "User registered successfully"
}
```

**cURL Example:**
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

---

### 2. Login User
**Endpoint:** `POST /api/auth/login`

Authenticate user and get JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

---

### 3. Get User Profile
**Endpoint:** `GET /api/auth/profile`

Get current user's profile information.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student"
}
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <your_token>" \
  "http://localhost:8000/api/auth/profile"
```

---

## 👨‍💼 Admin Endpoints (Admin Only)

### Students Management

#### 1. Add Student
**Endpoint:** `POST /api/admin/students`

Add a new student to the system.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "student_id": "STU001",
  "name": "Alice Smith",
  "email": "alice@student.edu",
  "department": "Computer Science"
}
```

**Response:**
```json
{
  "message": "Student added successfully",
  "id": 25
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "Alice Smith",
    "email": "alice@student.edu",
    "department": "Computer Science"
  }'
```

---

#### 2. List All Students
**Endpoint:** `GET /api/admin/students`

Get list of all students.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "name": "Alice Smith",
    "email": "alice@student.edu",
    "department": "Computer Science",
    "created_at": "2025-11-19T10:00:00Z"
  }
]
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/students"
```

---

#### 3. Get Student by ID
**Endpoint:** `GET /api/admin/students/{student_id}`

Get details of a specific student.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "name": "Alice Smith",
  "email": "alice@student.edu",
  "department": "Computer Science",
  "created_at": "2025-11-19T10:00:00Z"
}
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/students/1"
```

---

#### 4. Update Student
**Endpoint:** `PUT /api/admin/students/{student_id}`

Update student information.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice.johnson@student.edu",
  "department": "Data Science"
}
```

**Response:**
```json
{
  "message": "Student updated successfully"
}
```

**cURL Example:**
```bash
curl -X PUT "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "department": "Data Science"
  }'
```

---

#### 5. Delete Student
**Endpoint:** `DELETE /api/admin/students/{student_id}`

Delete a student from the system.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
{
  "message": "Student deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer <admin_token>"
```

---

### Teachers Management

#### 1. Add Teacher
**Endpoint:** `POST /api/admin/teachers`

Add a new teacher to the system.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "Dr. Jane Smith",
  "email": "jane@college.edu",
  "department": "Computer Science"
}
```

**Response:**
```json
{
  "message": "Teacher added successfully",
  "id": 10
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Jane Smith",
    "email": "jane@college.edu",
    "department": "Computer Science"
  }'
```

---

#### 2. List All Teachers
**Endpoint:** `GET /api/admin/teachers`

Get list of all teachers.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Jane Smith",
    "email": "jane@college.edu",
    "department": "Computer Science",
    "created_at": "2025-11-19T10:00:00Z"
  }
]
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/teachers"
```

---

#### 3. Get Teacher by ID
**Endpoint:** `GET /api/admin/teachers/{teacher_id}`

Get details of a specific teacher.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
{
  "id": 1,
  "name": "Dr. Jane Smith",
  "email": "jane@college.edu",
  "department": "Computer Science",
  "created_at": "2025-11-19T10:00:00Z"
}
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/teachers/1"
```

---

#### 4. Update Teacher
**Endpoint:** `PUT /api/admin/teachers/{teacher_id}`

Update teacher information.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "Prof. Jane Smith",
  "department": "Data Science"
}
```

**Response:**
```json
{
  "message": "Teacher updated successfully"
}
```

**cURL Example:**
```bash
curl -X PUT "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prof. Jane Smith",
    "department": "Data Science"
  }'
```

---

#### 5. Delete Teacher
**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`

Delete a teacher from the system.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
{
  "message": "Teacher deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer <admin_token>"
```

---

### Dashboard & Statistics

#### Get Admin Stats
**Endpoint:** `GET /api/admin/stats`

Get dashboard statistics for admin panel.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
{
  "users": 31,
  "students": 24,
  "teachers": 8
}
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/stats"
```

---

## 📋 Attendance Endpoints (Admin Only)

#### 1. Get Students for Attendance
**Endpoint:** `GET /api/admin/attendance/students`

Get simplified list of students for attendance marking.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "name": "Alice Smith"
  },
  {
    "id": 2,
    "student_id": "STU002",
    "name": "Bob Johnson"
  }
]
```

**cURL Example:**
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/attendance/students"
```

---

#### 2. Mark Attendance
**Endpoint:** `POST /api/admin/attendance/mark`

Mark attendance for a student.

**Headers:** `Authorization: Bearer <admin_token>`

**Query Parameters:**
- `student_id` (required): Student ID
- `status` (optional): Attendance status (default: "present")

**Response:**
```json
{
  "message": "Attendance marked for student 1 as present"
}
```

**cURL Examples:**
```bash
# Mark as present (default)
curl -X POST "http://localhost:8000/api/admin/attendance/mark?student_id=1" \
  -H "Authorization: Bearer <admin_token>"

# Mark as absent
curl -X POST "http://localhost:8000/api/admin/attendance/mark?student_id=1&status=absent" \
  -H "Authorization: Bearer <admin_token>"
```

---

## 🌐 General Endpoints

#### Root Endpoint
**Endpoint:** `GET /`

API health check and basic information.

**Response:**
```json
{
  "message": "Simple CRUD API",
  "status": "running"
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/"
```

---

## 📚 Interactive Documentation

### Swagger UI
Access interactive API documentation at:
```
http://localhost:8000/docs
```

### ReDoc
Alternative documentation interface:
```
http://localhost:8000/redoc
```

---

## ❌ Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "Student not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Email already exists"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```

---

## 🔑 Getting Started

1. **Register an admin user:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "admin123",
    "role": "admin"
  }'
```

2. **Login and get token:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

3. **Use the token in subsequent requests:**
```bash
export TOKEN="your_jwt_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/admin/stats"
```

---

## 📝 Notes

- All timestamps are in UTC format
- JWT tokens expire after 24 hours (1440 minutes)
- Email addresses must be unique across the system
- Student IDs must be unique
- All protected endpoints require valid JWT authentication
- Admin role is required for all admin/* endpoints