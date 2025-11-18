# API Endpoints Documentation

This document provides all API endpoints with curl examples for frontend developers working with the Simple FastAPI CRUD Backend.

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```bash
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### 1. User Registration
**Endpoint:** `POST /api/auth/register`

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "role": "student"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "email": "john.doe@example.com"
  }
}
```

### 2. User Login
**Endpoint:** `POST /api/auth/login`

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@attendance.com",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get User Profile
**Endpoint:** `GET /api/auth/profile`

```bash
curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Admin User",
  "email": "admin@attendance.com",
  "role": "admin",
  "created_at": "2025-11-17T07:26:05.123456+00:00"
}
```

---

## 👨‍🎓 Student Management Endpoints (Admin Only)

### 4. Get All Students
**Endpoint:** `GET /api/admin/students`

```bash
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "CS001",
    "name": "Aarav Agarwal",
    "email": "aarav.agarwal@student.edu",
    "department": "Computer Science",
    "created_at": "2025-11-17T07:26:05.123456+00:00"
  },
  {
    "id": 2,
    "student_id": "CS002",
    "name": "Diya Mehta",
    "email": "diya.mehta@student.edu",
    "department": "Computer Science",
    "created_at": "2025-11-17T07:26:05.123456+00:00"
  }
]
```

### 5. Get Student by ID
**Endpoint:** `GET /api/admin/students/{student_id}`

```bash
curl -X GET "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "student_id": "CS001",
  "name": "Aarav Agarwal",
  "email": "aarav.agarwal@student.edu",
  "department": "Computer Science",
  "created_at": "2025-11-17T07:26:05.123456+00:00"
}
```

### 6. Add New Student
**Endpoint:** `POST /api/admin/students`

```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "CS999",
    "name": "Raj Patel",
    "email": "raj.patel@student.edu",
    "department": "Computer Science"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Student added successfully",
  "data": {
    "student_id": "CS999"
  }
}
```

### 7. Update Student
**Endpoint:** `PUT /api/admin/students/{student_id}`

```bash
curl -X PUT "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aarav Agarwal Updated",
    "email": "aarav.updated@student.edu",
    "department": "Computer Science & AI"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Student updated successfully",
  "data": {
    "student_id": "CS001"
  }
}
```

### 8. Delete Student
**Endpoint:** `DELETE /api/admin/students/{student_id}`

```bash
curl -X DELETE "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "status": "success",
  "message": "Student deleted successfully"
}
```

---

## 👨‍🏫 Teacher Management Endpoints (Admin Only)

### 9. Get All Teachers
**Endpoint:** `GET /api/admin/teachers`

```bash
curl -X GET "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Priya Sharma",
    "email": "priya.sharma@college.edu",
    "department": "Computer Science",
    "created_at": "2025-11-17T07:26:05.123456+00:00"
  },
  {
    "id": 2,
    "name": "Prof. Vikram Gupta",
    "email": "vikram.gupta@college.edu",
    "department": "Mathematics",
    "created_at": "2025-11-17T07:26:05.123456+00:00"
  }
]
```

### 10. Get Teacher by ID
**Endpoint:** `GET /api/admin/teachers/{teacher_id}`

```bash
curl -X GET "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Dr. Priya Sharma",
  "email": "priya.sharma@college.edu",
  "department": "Computer Science",
  "created_at": "2025-11-17T07:26:05.123456+00:00"
}
```

### 11. Add New Teacher
**Endpoint:** `POST /api/admin/teachers`

```bash
curl -X POST "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Amit Verma",
    "email": "amit.verma@college.edu",
    "department": "Data Science"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Teacher added successfully",
  "data": {
    "teacher_id": 8
  }
}
```

### 12. Update Teacher
**Endpoint:** `PUT /api/admin/teachers/{teacher_id}`

```bash
curl -X PUT "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Priya Sharma Updated",
    "email": "priya.updated@college.edu",
    "department": "Computer Science & AI"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Teacher updated successfully",
  "data": {
    "teacher_id": 1
  }
}
```

### 13. Delete Teacher
**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`

```bash
curl -X DELETE "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "status": "success",
  "message": "Teacher deleted successfully"
}
```

---

## 📊 Dashboard Endpoints (Admin Only)

### 14. Get Dashboard Statistics
**Endpoint:** `GET /api/admin/dashboard/stats`

```bash
curl -X GET "http://localhost:8000/api/admin/dashboard/stats" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "total_users": 28,
  "total_students": 20,
  "total_teachers": 7
}
```

---

## 📝 Attendance Endpoints

### 15. Mark Attendance Manually
**Endpoint:** `POST /api/attendance/manual-mark`

```bash
curl -X POST "http://localhost:8000/api/attendance/manual-mark" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "status": "present"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance marked as present for student Aarav Agarwal",
  "data": {
    "student_id": 1,
    "student_name": "Aarav Agarwal",
    "status": "present",
    "timestamp": "2025-11-17T12:30:45.123456"
  }
}
```

### 16. Get Students for Attendance
**Endpoint:** `GET /api/attendance/students`

```bash
curl -X GET "http://localhost:8000/api/attendance/students" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "message": "Students retrieved successfully",
  "data": [
    {
      "id": 1,
      "student_id": "CS001",
      "name": "Aarav Agarwal",
      "department": "Computer Science"
    },
    {
      "id": 2,
      "student_id": "CS002",
      "name": "Diya Mehta",
      "department": "Computer Science"
    }
  ]
}
```

---

## 🏥 Health Check Endpoints

### 17. Root Endpoint
**Endpoint:** `GET /`

```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Simple CRUD API",
  "status": "running",
  "version": "1.0.0"
}
```

### 18. Health Check
**Endpoint:** `GET /health`

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🔑 Sample Login Credentials

Use these credentials for testing:

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@attendance.com | admin123 |
| **Teacher** | teacher@example.com | password123 |
| **Student** | aarav.agarwal@student.edu | student123 |

---

## 📝 Complete Workflow Example

Here's a complete workflow for frontend developers:

### 1. Login as Admin
```bash
# Get JWT token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@attendance.com",
    "password": "admin123"
  }'

# Save the returned access_token for subsequent requests
export JWT_TOKEN="your_received_token_here"
```

### 2. Get Dashboard Stats
```bash
curl -X GET "http://localhost:8000/api/admin/dashboard/stats" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### 3. List All Students
```bash
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### 4. Add New Student
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "CS100",
    "name": "New Student",
    "email": "new.student@student.edu",
    "department": "Computer Science"
  }'
```

### 5. Mark Attendance
```bash
curl -X POST "http://localhost:8000/api/attendance/manual-mark" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "status": "present"
  }'
```

---

## 🚫 Error Responses

### Authentication Required (401)
```json
{
  "detail": "Not authenticated"
}
```

### Invalid Token (401)
```json
{
  "detail": "Invalid token"
}
```

### Access Denied (403)
```json
{
  "detail": "Access denied. Admin role required."
}
```

### Not Found (404)
```json
{
  "detail": "Student not found"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Duplicate Entry (400)
```json
{
  "detail": "Student ID already exists"
}
```

---

## 🔧 Environment Variables

Make sure your backend has these environment variables set:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/smart_attendance
SECRET_KEY=your-super-secret-jwt-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 📚 Additional Notes

1. **Rate Limiting**: Currently not implemented, but can be added for production
2. **Pagination**: Not implemented in this basic version
3. **File Uploads**: Not supported in this simplified version
4. **Email Notifications**: Not implemented
5. **Password Reset**: Not implemented in this basic version

For frontend frameworks like React, Vue, or Angular, you can create HTTP service classes that wrap these curl commands into reusable functions.

---

## 🛠️ Frontend Integration Tips

### JavaScript/TypeScript Example
```javascript
// API Service Class Example
class ApiService {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('jwt_token');
  }

  async login(email, password) {
    const response = await fetch(`${this.baseURL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    if (data.access_token) {
      this.token = data.access_token;
      localStorage.setItem('jwt_token', this.token);
    }
    return data;
  }

  async getStudents() {
    const response = await fetch(`${this.baseURL}/api/admin/students`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return response.json();
  }
}
```

This documentation should provide everything a frontend developer needs to integrate with your backend API!