# Smart Attendance System - Frontend API Integration Guide

**Base URL:** `http://localhost:8000/api`

**API Version:** 1.0.0

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Error Handling](#error-handling)
5. [Frontend Integration Examples](#frontend-integration-examples)

---

## Quick Start

### 1. Base URL
```
http://localhost:8000/api
```

### 2. Authentication
Most endpoints require a Bearer token. Get it by logging in first.

### 3. Headers
```javascript
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_access_token>"
}
```

---

## Authentication

### Register User

**Endpoint:** `POST /api/auth/register`

**Description:** Register a new user (admin, teacher, or student)

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string",
  "full_name": "string",
  "email": "string (email format)",
  "phone_number": "string (optional)",
  "password": "string",
  "role": "admin | teacher | student",
  "status": "active | inactive | suspended (optional, default: active)"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+911234567890",
    "password": "securepassword123",
    "role": "student",
    "status": "active"
  }'
```

**Response (200):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": 123
  }
}
```

---

### Login

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and get access token

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "string (email format)",
  "password": "string"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@attendance.com",
    "password": "admin123"
  }'
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save the `access_token` for subsequent requests!**

---

### Get User Profile

**Endpoint:** `GET /api/auth/profile`

**Description:** Get current authenticated user's profile

**Authentication:** Required (Bearer token)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200):**
```json
{
  "id": 123,
  "username": "john_doe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+911234567890",
  "role": "student",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## Admin Endpoints

> **Note:** All admin endpoints require admin role authentication.

### Add Student

**Endpoint:** `POST /api/admin/students`

**Description:** Create a new student record (user must exist first)

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "user_id": 123,
  "student_id": "STU001",
  "enrollment_no": "ENR001",
  "department": "Computer Science",
  "semester": 3,
  "section": "A",
  "status": "active"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{
    "user_id": 123,
    "student_id": "STU001",
    "enrollment_no": "ENR001",
    "department": "Computer Science",
    "semester": 3,
    "section": "A",
    "status": "active"
  }'
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Student added successfully",
  "data": {
    "student_id": "STU001"
  }
}
```

---

### List All Students

**Endpoint:** `GET /api/admin/students`

**Description:** Get list of all students

**Authentication:** Required (Admin only)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200):**
```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "user_id": 123,
    "full_name": "John Doe",
    "enrollment_no": "ENR001",
    "department": "Computer Science",
    "semester": 3,
    "section": "A",
    "photo_path": null,
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Upload Student Photo

**Endpoint:** `POST /api/admin/students/{student_id}/photo`

**Description:** Upload student photo for face recognition

**Authentication:** Required (Admin only)

**Content-Type:** `multipart/form-data`

**Request Parameters:**
- `photo` (string, required) - Base64 encoded image or data URL

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/students/1/photo" \
  -H "Authorization: Bearer <admin_token>" \
  -F "photo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Photo uploaded successfully"
}
```

---

### Delete Student

**Endpoint:** `DELETE /api/admin/students/{student_id}`

**Description:** Delete a student record

**Authentication:** Required (Admin only)

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Student deleted successfully"
}
```

---

### Add Teacher

**Endpoint:** `POST /api/admin/teachers`

**Description:** Create a new teacher record (user must exist first)

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "user_id": 125,
  "teacher_id": "TCH001",
  "department": "Computer Science",
  "designation": "Professor",
  "specialization": "Machine Learning"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/teachers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{
    "user_id": 125,
    "teacher_id": "TCH001",
    "department": "Computer Science",
    "designation": "Professor",
    "specialization": "Machine Learning"
  }'
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Teacher added successfully",
  "data": {
    "teacher_id": "TCH001"
  }
}
```

---

### List All Teachers

**Endpoint:** `GET /api/admin/teachers`

**Description:** Get list of all teachers

**Authentication:** Required (Admin only)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200):**
```json
[
  {
    "id": 1,
    "teacher_id": "TCH001",
    "user_id": 125,
    "full_name": "Jane Smith",
    "department": "Computer Science",
    "designation": "Professor",
    "specialization": "Machine Learning",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Delete Teacher

**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`

**Description:** Delete a teacher record

**Authentication:** Required (Admin only)

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Teacher deleted successfully"
}
```

---

## Attendance Endpoints

### Verify Attendance

**Endpoint:** `POST /api/attendance/verify`

**Description:** Mark attendance for a student using face recognition

**Authentication:** Required (Bearer token)

**Content-Type:** `multipart/form-data`

**Request Parameters:**
- `student_id` (integer, required) - Student ID
- `session_id` (integer, required) - Session ID
- `face_image` (string, required) - Base64 encoded image or data URL

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/attendance/verify" \
  -H "Authorization: Bearer <token>" \
  -F "student_id=1" \
  -F "session_id=5" \
  -F "face_image=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Attendance marked as present",
  "data": {
    "attendance_id": 456,
    "status": "present",
    "confidence": 0.85,
    "student_name": "John Doe",
    "session_name": "CS101 - Lecture 1"
  }
}
```

**Status Values:**
- `present` - Attendance marked successfully
- `flagged` - Low confidence, requires manual verification

---

### Get Attendance Records

**Endpoint:** `GET /api/attendance/{student_id}`

**Description:** Get all attendance records for a specific student

**Authentication:** Required (Bearer token)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/attendance/1" \
  -H "Authorization: Bearer <token>"
```

**Response (200):**
```json
[
  {
    "id": 456,
    "student_id": 1,
    "session_id": 5,
    "status": "present",
    "date": "2024-01-15",
    "time": "10:30:00",
    "face_confidence": 85.5,
    "liveness_confidence": 90.2,
    "background_confidence": 78.5,
    "audio_confidence": 82.3,
    "geofence_validation": true,
    "device_validation": true,
    "final_score": 84.13,
    "is_manually_approved": false,
    "submission_time": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Error Handling

### Standard Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Common Error Examples

**401 Unauthorized:**
```json
{
  "detail": "Invalid token"
}
```

**403 Forbidden:**
```json
{
  "detail": "Admin access required"
}
```

**404 Not Found:**
```json
{
  "detail": "Student not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "Email already registered"
}
```

---

## Frontend Integration Examples

### JavaScript/TypeScript Example

```javascript
// API Client Setup
const API_BASE_URL = 'http://localhost:8000/api';

class AttendanceAPI {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // Authentication
  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.token = data.access_token;
    localStorage.setItem('token', data.access_token);
    return data;
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getProfile() {
    return this.request('/auth/profile');
  }

  // Attendance
  async verifyAttendance(studentId, sessionId, faceImage) {
    const formData = new FormData();
    formData.append('student_id', studentId);
    formData.append('session_id', sessionId);
    formData.append('face_image', faceImage);

    return this.request('/attendance/verify', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });
  }

  async getAttendanceRecords(studentId) {
    return this.request(`/attendance/${studentId}`);
  }

  // Admin - Students
  async addStudent(studentData) {
    return this.request('/admin/students', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  async listStudents() {
    return this.request('/admin/students');
  }

  async uploadStudentPhoto(studentId, photo) {
    const formData = new FormData();
    formData.append('photo', photo);

    return this.request(`/admin/students/${studentId}/photo`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });
  }

  async deleteStudent(studentId) {
    return this.request(`/admin/students/${studentId}`, {
      method: 'DELETE',
    });
  }

  // Admin - Teachers
  async addTeacher(teacherData) {
    return this.request('/admin/teachers', {
      method: 'POST',
      body: JSON.stringify(teacherData),
    });
  }

  async listTeachers() {
    return this.request('/admin/teachers');
  }

  async deleteTeacher(teacherId) {
    return this.request(`/admin/teachers/${teacherId}`, {
      method: 'DELETE',
    });
  }
}

// Usage
const api = new AttendanceAPI();

// Login
await api.login('admin@attendance.com', 'admin123');

// Get profile
const profile = await api.getProfile();

// List students
const students = await api.listStudents();

// Verify attendance
const result = await api.verifyAttendance(1, 5, base64Image);
```

### React Example

```jsx
import { useState, useEffect } from 'react';

function AttendanceApp() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [students, setStudents] = useState([]);

  useEffect(() => {
    if (token) {
      fetchStudents();
    }
  }, [token]);

  const login = async (email, password) => {
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    setToken(data.access_token);
    localStorage.setItem('token', data.access_token);
  };

  const fetchStudents = async () => {
    const response = await fetch('http://localhost:8000/api/admin/students', {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    setStudents(data);
  };

  const verifyAttendance = async (studentId, sessionId, faceImage) => {
    const formData = new FormData();
    formData.append('student_id', studentId);
    formData.append('session_id', sessionId);
    formData.append('face_image', faceImage);

    const response = await fetch('http://localhost:8000/api/attendance/verify', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });
    return await response.json();
  };

  return (
    <div>
      {/* Your UI components */}
    </div>
  );
}
```

---

## Important Notes

### Token Management
- Tokens expire after 1440 minutes (24 hours)
- Store tokens securely (localStorage, sessionStorage, or secure cookies)
- Include token in `Authorization: Bearer <token>` header for protected endpoints

### Image Handling
- Face images should be base64 encoded or data URLs
- Supported formats: JPEG, PNG
- Recommended size: 640x480 or higher
- Format: `data:image/png;base64,<base64_string>` or just the base64 string

### Date Formats
- Dates: `YYYY-MM-DD` (e.g., "2024-01-15")
- Times: `HH:MM:SS` (e.g., "10:30:00")
- Datetimes: ISO 8601 format (e.g., "2024-01-15T10:30:00Z")

### CORS
The API supports CORS for:
- `http://localhost:3000`
- `http://localhost:8080`

### Content-Type
- Use `application/json` for JSON requests
- Use `multipart/form-data` for file uploads (photo, face_image)

---

## Testing with cURL

### Quick Test Script

```bash
#!/bin/bash

# Login and get token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@attendance.com","password":"admin123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# Get profile
curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer $TOKEN"

# List students
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Support

For issues or questions, please contact the backend development team.

**Last Updated:** November 2024

