# Smart Attendance System - API Documentation

**Base URL:** `http://localhost:8000/api`

**API Version:** 1.0.0

---

## Table of Contents

1. [Authentication](#authentication)
2. [Attendance Endpoints](#attendance-endpoints)
3. [Admin Endpoints](#admin-endpoints)
4. [Error Handling](#error-handling)
5. [Data Models](#data-models)

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header.

### How to Authenticate

1. Login using `/api/auth/login` to get an access token
2. Include the token in subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

---

## Authentication Endpoints

### 1. Register User

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

**Example Request:**
```json
{
  "username": "john_doe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+911234567890",
  "password": "securepassword123",
  "role": "student",
  "status": "active"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": 123
  }
}
```

**Error Responses:**
- `400 Bad Request` - Email already registered or invalid role
- `422 Unprocessable Entity` - Validation error

---

### 2. Login

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

**Example Request:**
```json
{
  "email": "admin@attendance.com",
  "password": "admin123"
}
```

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password

**Example Usage:**
```javascript
const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'admin@attendance.com',
    password: 'admin123'
  })
});

const data = await response.json();
localStorage.setItem('token', data.access_token);
```

---

### 3. Get User Profile

**Endpoint:** `GET /api/auth/profile`

**Description:** Get current authenticated user's profile

**Authentication:** Required (Bearer token)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "user_id": 123,
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

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

## Attendance Endpoints

### 1. Verify Attendance

**Endpoint:** `POST /api/attendance/verify`

**Description:** Mark attendance for a student using face recognition

**Authentication:** Required (Bearer token)

**Content-Type:** `multipart/form-data`

**Request Parameters (Form Data):**
- `student_id` (integer, required) - Student ID
- `class_id` (integer, required) - Class ID
- `face_image` (string, required) - Base64 encoded image or data URL

**Example Request (JavaScript):**
```javascript
const formData = new FormData();
formData.append('student_id', '1');
formData.append('class_id', '5');
formData.append('face_image', base64ImageString); // or data URL

const response = await fetch('http://localhost:8000/api/attendance/verify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Attendance marked as present",
  "data": {
    "attendance_id": 456,
    "status": "present",
    "confidence": 0.85,
    "student_name": "John Doe"
  }
}

// or for flagged attendance:
{
  "status": "success",
  "message": "Attendance marked as flagged",
  "data": {
    "attendance_id": 457,
    "status": "flagged",
    "confidence": 0.45,
    "student_name": "Jane Smith"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Student photo not registered or no face found in image
- `401 Unauthorized` - Invalid or missing token
- `404 Not Found` - Student or class not found

**Status Values:**
- `present` - Attendance marked successfully
- `flagged` - Low confidence, requires manual verification
- `late` - Student marked as late
- `absent` - Student absent

---

### 2. Get Attendance Records

**Endpoint:** `GET /api/attendance/{student_id}`

**Description:** Get all attendance records for a specific student

**Authentication:** Required (Bearer token)

**URL Parameters:**
- `student_id` (integer, required) - Student ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example Request:**
```javascript
const response = await fetch(`http://localhost:8000/api/attendance/1`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**Success Response (200):**
```json
[
  {
    "attendance_id": 456,
    "student_id": 1,
    "class_id": 5,
    "teacher_id": 10,
    "date": "2024-01-15",
    "time": "10:30:00",
    "status": "present",
    "face_confidence": 85.5,
    "liveness_confidence": 90.2,
    "background_confidence": 78.5,
    "audio_confidence": 82.3,
    "geofence_validation": true,
    "final_score": 84.13,
    "remarks": null,
    "verified_by": null
  },
  {
    "attendance_id": 455,
    "student_id": 1,
    "class_id": 3,
    "teacher_id": 8,
    "date": "2024-01-14",
    "time": "14:20:00",
    "status": "late",
    "face_confidence": 88.0,
    "liveness_confidence": 92.5,
    "background_confidence": 80.0,
    "audio_confidence": 85.0,
    "geofence_validation": true,
    "final_score": 86.38,
    "remarks": "Arrived 10 minutes late",
    "verified_by": 118
  }
]
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `404 Not Found` - Student not found

---

## Admin Endpoints

All admin endpoints require admin role authentication.

### 1. Add Student

**Endpoint:** `POST /api/admin/students`

**Description:** Create a new student record (user must exist first)

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "user_id": 123,
  "enrollment_no": "CS2023001",
  "department": "Computer Science",
  "semester": 3,
  "section": "A"
}
```

**Example Request:**
```json
{
  "user_id": 123,
  "enrollment_no": "CS2023001",
  "department": "Computer Science",
  "semester": 3,
  "section": "A"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Student added successfully",
  "data": {
    "student_id": 45
  }
}
```

**Error Responses:**
- `400 Bad Request` - Student already exists or enrollment number already exists
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required
- `404 Not Found` - User not found

---

### 2. Upload Student Photo

**Endpoint:** `POST /api/admin/students/{student_id}/photo`

**Description:** Upload student photo for face recognition

**Authentication:** Required (Admin only)

**Content-Type:** `multipart/form-data`

**URL Parameters:**
- `student_id` (integer, required) - Student ID

**Request Parameters (Form Data):**
- `photo` (string, required) - Base64 encoded image or data URL

**Example Request:**
```javascript
const formData = new FormData();
formData.append('photo', base64ImageString);

const response = await fetch(`http://localhost:8000/api/admin/students/1/photo`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Photo uploaded successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required
- `404 Not Found` - Student not found

---

### 3. List All Students

**Endpoint:** `GET /api/admin/students`

**Description:** Get list of all students

**Authentication:** Required (Admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
[
  {
    "student_id": 1,
    "user_id": 123,
    "enrollment_no": "CS2023001",
    "department": "Computer Science",
    "semester": 3,
    "section": "A",
    "photo": null
  },
  {
    "student_id": 2,
    "user_id": 124,
    "enrollment_no": "EC2023002",
    "department": "Electronics",
    "semester": 2,
    "section": "B",
    "photo": null
  }
]
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required

---

### 4. Delete Student

**Endpoint:** `DELETE /api/admin/students/{student_id}`

**Description:** Delete a student record (cascades to user)

**Authentication:** Required (Admin only)

**URL Parameters:**
- `student_id` (integer, required) - Student ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Student deleted successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required
- `404 Not Found` - Student not found

---

### 5. Add Teacher

**Endpoint:** `POST /api/admin/teachers`

**Description:** Create a new teacher record (user must exist first)

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "user_id": 125,
  "department": "Computer Science",
  "designation": "Assistant Professor",
  "specialization": "Machine Learning"
}
```

**Example Request:**
```json
{
  "user_id": 125,
  "department": "Computer Science",
  "designation": "Assistant Professor",
  "specialization": "Machine Learning"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Teacher added successfully",
  "data": {
    "teacher_id": 15
  }
}
```

**Error Responses:**
- `400 Bad Request` - Teacher already exists for this user
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required
- `404 Not Found` - User not found

---

### 6. List All Teachers

**Endpoint:** `GET /api/admin/teachers`

**Description:** Get list of all teachers

**Authentication:** Required (Admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
[
  {
    "teacher_id": 1,
    "user_id": 125,
    "department": "Computer Science",
    "designation": "Assistant Professor",
    "specialization": "Machine Learning"
  },
  {
    "teacher_id": 2,
    "user_id": 126,
    "department": "Electronics",
    "designation": "Professor",
    "specialization": "Digital Circuits"
  }
]
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required

---

### 7. Delete Teacher

**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`

**Description:** Delete a teacher record (cascades to user)

**Authentication:** Required (Admin only)

**URL Parameters:**
- `teacher_id` (integer, required) - Teacher ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Teacher deleted successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Admin access required
- `404 Not Found` - Teacher not found

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

### Common Error Messages

**Authentication Errors:**
```json
{
  "detail": "Invalid token"
}
```

```json
{
  "detail": "Incorrect email or password"
}
```

```json
{
  "detail": "Admin access required"
}
```

**Validation Errors:**
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

**Not Found Errors:**
```json
{
  "detail": "Student not found"
}
```

---

## Data Models

### User Model

```typescript
interface User {
  user_id: number;
  username: string;
  full_name: string;
  email: string;
  phone_number: string | null;
  role: "admin" | "teacher" | "student";
  status: "active" | "inactive" | "suspended";
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
}
```

### Student Model

```typescript
interface Student {
  student_id: number;
  user_id: number;
  enrollment_no: string;
  department: string;
  semester: number; // 1-8
  section: string | null;
  photo: string | null; // Base64 encoded or null
}
```

### Teacher Model

```typescript
interface Teacher {
  teacher_id: number;
  user_id: number;
  department: string;
  designation: string | null;
  specialization: string | null;
}
```

### Attendance Model

```typescript
interface Attendance {
  attendance_id: number;
  student_id: number;
  class_id: number;
  teacher_id: number;
  date: string; // YYYY-MM-DD format
  time: string; // HH:MM:SS format
  status: "present" | "absent" | "late" | "flagged";
  face_confidence: number | null; // 0-100
  liveness_confidence: number | null; // 0-100
  background_confidence: number | null; // 0-100
  audio_confidence: number | null; // 0-100
  geofence_validation: boolean;
  final_score: number | null; // 0-100
  remarks: string | null;
  verified_by: number | null; // user_id of verifier
}
```

---

## Example Frontend Integration

### React/JavaScript Example

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
  async verifyAttendance(studentId, classId, faceImage) {
    const formData = new FormData();
    formData.append('student_id', studentId);
    formData.append('class_id', classId);
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

  // Admin
  async addStudent(studentData) {
    return this.request('/admin/students', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
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

  async listStudents() {
    return this.request('/admin/students');
  }

  async deleteStudent(studentId) {
    return this.request(`/admin/students/${studentId}`, {
      method: 'DELETE',
    });
  }

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

// Verify attendance
const result = await api.verifyAttendance(1, 5, base64Image);
```

---

## Testing Credentials

### Admin Account
- **Email:** `admin@attendance.com`
- **Password:** `admin123`

### Teacher Account
- **Email:** `teacher@example.com`
- **Password:** `password123`

---

## API Documentation (Swagger UI)

Interactive API documentation is available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Notes for Frontend Developers

1. **Token Storage:** Store the access token securely (localStorage, sessionStorage, or secure cookies)

2. **Token Expiration:** Tokens expire after 1440 minutes (24 hours). Implement token refresh logic if needed.

3. **Image Handling:** 
   - Face images should be base64 encoded or data URLs
   - Supported formats: JPEG, PNG
   - Recommended size: 640x480 or higher

4. **Date Formats:**
   - Dates: `YYYY-MM-DD` (e.g., "2024-01-15")
   - Times: `HH:MM:SS` (e.g., "10:30:00")
   - Datetimes: ISO 8601 format (e.g., "2024-01-15T10:30:00Z")

5. **Error Handling:** Always check response status and handle errors gracefully

6. **CORS:** The API supports CORS for `http://localhost:3000` and `http://localhost:8080` by default

7. **Content-Type:**
   - Use `application/json` for JSON requests
   - Use `multipart/form-data` for file uploads

---

## Support

For issues or questions, please contact the backend development team.

**Last Updated:** January 2024

