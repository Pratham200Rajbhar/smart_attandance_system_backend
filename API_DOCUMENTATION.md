# Smart Attendance System - API Documentation

## Overview
This is a comprehensive FastAPI backend for a Smart Attendance System with JWT authentication, face recognition-based attendance marking, and admin management capabilities.

**Base URL:** `http://localhost:8000`

## Tech Stack
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL with SQLAlchemy (async)
- **Authentication:** JWT with bcrypt password hashing
- **Face Recognition:** face_recognition + OpenCV
- **Image Processing:** PIL (Pillow)

---

## 🔐 Authentication Endpoints

### 1. User Registration
**Endpoint:** `POST /api/auth/register`

**Description:** Register a new user (admin, teacher, or student)

**Request Body:**
```json
{
  "username": "john_doe",
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone_number": "1234567890",
  "password": "securepassword123",
  "role": "student",
  "status": "active"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "1234567890",
    "password": "securepassword123",
    "role": "student",
    "status": "active"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": 1
  }
}
```

---

### 2. User Login
**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and get JWT token

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 3. Get User Profile
**Endpoint:** `GET /api/auth/profile`

**Description:** Get current logged-in user's profile information

**Headers:** `Authorization: Bearer <your_jwt_token>`

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/auth/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone_number": "1234567890",
  "role": "student",
  "status": "active",
  "created_at": "2025-11-17T10:30:00Z",
  "updated_at": "2025-11-17T10:30:00Z"
}
```

---

## 🎯 Attendance Endpoints

### 1. Verify Attendance (Face Recognition)
**Endpoint:** `POST /api/attendance/verify`

**Description:** Submit face image for attendance verification

**Content-Type:** `application/x-www-form-urlencoded`

**Form Data:**
- `student_id`: Integer (Student ID)
- `session_id`: Integer (Session ID)
- `face_image`: String (Base64 encoded image)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/attendance/verify" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "student_id=1&session_id=1&face_image=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
```

**Response (Success - Present):**
```json
{
  "status": "success",
  "message": "Attendance marked as present",
  "data": {
    "attendance_id": 1,
    "status": "present",
    "confidence": 0.85,
    "student_name": "John Doe",
    "session_name": "Mathematics - Session 1"
  }
}
```

**Response (Flagged - Low Confidence):**
```json
{
  "status": "success",
  "message": "Attendance marked as flagged",
  "data": {
    "attendance_id": 2,
    "status": "flagged",
    "confidence": 0.45,
    "student_name": "John Doe",
    "session_name": "Mathematics - Session 1"
  }
}
```

---

### 2. Get Student Attendance Records
**Endpoint:** `GET /api/attendance/{student_id}`

**Description:** Retrieve all attendance records for a specific student

**Headers:** `Authorization: Bearer <your_jwt_token>`

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/attendance/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "session_id": 1,
    "status": "present",
    "date": "2025-11-17",
    "time": "10:30:00",
    "final_score": 85.0,
    "face_confidence": 85.0,
    "liveness_confidence": 88.5,
    "background_confidence": 92.0,
    "audio_confidence": 76.8,
    "geofence_validation": true,
    "device_validation": true,
    "verified_by": null,
    "verification_reason": null,
    "is_manually_approved": false,
    "submission_time": "2025-11-17T10:30:15Z",
    "created_at": "2025-11-17T10:30:15Z",
    "updated_at": "2025-11-17T10:30:15Z"
  }
]
```

---

## 👥 Admin Management Endpoints
**Note:** All admin endpoints require `admin` role in JWT token.

### 1. Add New Student
**Endpoint:** `POST /api/admin/students`

**Description:** Create a new student record (Admin only)

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**Request Body:**
```json
{
  "student_id": "STU001",
  "user_id": 2,
  "enrollment_no": "EN2025001",
  "department": "Computer Science",
  "semester": 3,
  "section": "A",
  "status": "active"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "user_id": 2,
    "enrollment_no": "EN2025001",
    "department": "Computer Science",
    "semester": 3,
    "section": "A",
    "status": "active"
  }'
```

**Response:**
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

### 2. Upload Student Photo
**Endpoint:** `POST /api/admin/students/{student_id}/photo`

**Description:** Upload and process student photo for face recognition

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**Content-Type:** `application/x-www-form-urlencoded`

**Form Data:**
- `photo`: String (Base64 encoded image)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/students/1/photo" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "photo=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
```

**Response:**
```json
{
  "status": "success",
  "message": "Photo uploaded successfully"
}
```

---

### 3. List All Students
**Endpoint:** `GET /api/admin/students`

**Description:** Get list of all students with their details

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "user_id": 2,
    "full_name": "John Doe",
    "enrollment_no": "EN2025001",
    "department": "Computer Science",
    "semester": 3,
    "section": "A",
    "photo_path": "photos/student_1.jpg",
    "status": "active",
    "created_at": "2025-11-17T10:30:00Z",
    "updated_at": "2025-11-17T10:30:00Z"
  }
]
```

---

### 4. Delete Student
**Endpoint:** `DELETE /api/admin/students/{student_id}`

**Description:** Remove a student from the system

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/students/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "status": "success",
  "message": "Student deleted successfully"
}
```

---

### 5. Add New Teacher
**Endpoint:** `POST /api/admin/teachers`

**Description:** Create a new teacher record (Admin only)

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**Request Body:**
```json
{
  "teacher_id": "TCH001",
  "user_id": 3,
  "department": "Computer Science",
  "designation": "Assistant Professor",
  "specialization": "Machine Learning",
  "status": "active"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_id": "TCH001",
    "user_id": 3,
    "department": "Computer Science",
    "designation": "Assistant Professor",
    "specialization": "Machine Learning",
    "status": "active"
  }'
```

**Response:**
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

### 6. List All Teachers
**Endpoint:** `GET /api/admin/teachers`

**Description:** Get list of all teachers with their details

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/admin/teachers" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
[
  {
    "id": 1,
    "teacher_id": "TCH001",
    "user_id": 3,
    "full_name": "Dr. Jane Smith",
    "department": "Computer Science",
    "designation": "Assistant Professor",
    "specialization": "Machine Learning",
    "status": "active",
    "created_at": "2025-11-17T10:30:00Z",
    "updated_at": "2025-11-17T10:30:00Z"
  }
]
```

---

### 7. Delete Teacher
**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`

**Description:** Remove a teacher from the system

**Headers:** `Authorization: Bearer <admin_jwt_token>`

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/api/admin/teachers/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "status": "success",
  "message": "Teacher deleted successfully"
}
```

---

## 👨‍🏫 Teacher Endpoints
**Note:** These endpoints are designed for teachers and require `teacher` role in JWT token.

### 1. Teacher Dashboard
**Description:** Get teacher's dashboard with session stats, attendance overview, and quick metrics

**Response Schema:**
```json
{
  "today_sessions": 3,
  "total_students": 45,
  "flagged_attendance": 2,
  "pending_reviews": 5,
  "subject_performance": [
    {
      "subject_name": "Mathematics",
      "total_sessions": 15,
      "attendance_rate": 85.5,
      "flagged_count": 3
    }
  ],
  "quick_stats": {
    "total_sessions_this_week": 12,
    "average_attendance": 88.2,
    "students_present_today": 38
  },
  "weekly_attendance": [85, 90, 78, 92, 88, 85, 89],
  "recent_activity": [
    {
      "type": "attendance_verified",
      "student_name": "John Doe",
      "session_name": "Math-101",
      "timestamp": "2025-11-17T10:30:00Z"
    }
  ],
  "today_sessions_list": [
    {
      "session_id": 1,
      "session_name": "Mathematics - Advanced",
      "start_time": "2025-11-17T10:00:00Z",
      "end_time": "2025-11-17T11:30:00Z",
      "class_room": "Room 101",
      "status": "scheduled",
      "students_registered": 25
    }
  ]
}
```

### 2. Teacher Sessions Management
**Description:** Manage class sessions including creation, updates, and attendance tracking

**Session Creation Schema:**
```json
{
  "session_name": "Mathematics - Advanced Calculus",
  "subject_id": 1,
  "class_room": "Room 101",
  "start_time": "2025-11-17T10:00:00Z",
  "end_time": "2025-11-17T11:30:00Z",
  "geofence_id": 1,
  "status": "scheduled",
  "attendance_enabled": true,
  "max_students": 30,
  "description": "Advanced calculus session covering derivatives and integrals"
}
```

### 3. Subject Assignment
**Description:** View and manage assigned subjects

**Subject Schema:**
```json
{
  "id": 1,
  "subject_code": "MATH101",
  "subject_name": "Advanced Mathematics",
  "department": "Computer Science", 
  "semester": 3,
  "credits": 4,
  "teacher_id": 1,
  "status": "active",
  "created_at": "2025-11-17T10:30:00Z",
  "updated_at": "2025-11-17T10:30:00Z"
}
```

### 4. Attendance Review & Approval
**Description:** Review flagged attendance records and approve/reject them

**Manual Override Schema:**
```json
{
  "attendance_record_id": 1,
  "decision": "approved",
  "reason": "Student was present but face recognition failed due to lighting",
  "teacher_id": 1
}
```

**Flagged Attendance Response:**
```json
[
  {
    "id": 1,
    "attendance_id": 15,
    "student_id": 5,
    "student_name": "John Doe",
    "student_email": "john.doe@example.com",
    "status": "flagged",
    "confidence": 0.45,
    "timestamp": "2025-11-17T10:30:00Z",
    "submission_time": "2025-11-17T10:30:15Z",
    "face_recognition_score": 45.0,
    "liveness_detection_score": 60.0,
    "background_validation_score": 70.0,
    "geofence_validation": false,
    "session_name": "Mathematics - Session 1",
    "subject_name": "Advanced Mathematics",
    "is_manually_approved": false
  }
]
```

### 5. Attendance Reports
**Description:** Generate detailed attendance reports for teacher's subjects and sessions

**Report Schema:**
```json
{
  "summary": {
    "total_sessions": 25,
    "total_students": 45,
    "average_attendance": 88.5,
    "total_present": 980,
    "total_absent": 125,
    "total_flagged": 15,
    "date_range": {
      "start_date": "2025-10-01",
      "end_date": "2025-11-17"
    }
  },
  "detailed_records": [
    {
      "attendance_id": 1,
      "student_id": 5,
      "student_name": "John Doe",
      "student_email": "john.doe@example.com",
      "session_id": 1,
      "session_name": "Math Advanced",
      "subject_name": "Mathematics",
      "status": "present",
      "date": "2025-11-17",
      "time": "10:30:00",
      "final_score": 85.0,
      "face_confidence": 85.0,
      "geofence_validation": true,
      "is_manually_approved": false,
      "created_at": "2025-11-17T10:30:15Z"
    }
  ],
  "date_wise_summary": [
    {
      "date": "2025-11-17",
      "total_sessions": 3,
      "total_students": 75,
      "present": 65,
      "absent": 8,
      "flagged": 2,
      "attendance_percentage": 86.7
    }
  ]
}
```

### 6. Geofence Management
**Description:** Manage location-based attendance zones

**Geofence Schema:**
```json
{
  "id": 1,
  "zone_name": "Main Classroom Block",
  "description": "Primary teaching area with rooms 101-120",
  "latitude": 12.9715987,
  "longitude": 77.5945627,
  "radius": 50.0,
  "status": "active",
  "created_by": 1,
  "created_at": "2025-11-17T10:30:00Z",
  "updated_at": "2025-11-17T10:30:00Z"
}
```

### 7. Notifications
**Description:** View and manage teacher notifications

**Notification Schema:**
```json
{
  "id": 1,
  "user_id": 3,
  "title": "Flagged Attendance Review",
  "message": "5 attendance records require your review for Mathematics session",
  "type": "warning",
  "status": "unread",
  "related_entity_type": "attendance",
  "related_entity_id": 15,
  "scheduled_for": null,
  "sent_at": "2025-11-17T10:30:00Z",
  "created_at": "2025-11-17T10:30:00Z"
}
```

---

## 🔧 System Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Description:** Check if the API is running

**cURL Example:**
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

### 2. Root Endpoint
**Endpoint:** `GET /`

**Description:** Get basic API information

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Smart Attendance System API",
  "status": "running"
}
```

---

## 🗄️ Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Students Table
```sql
CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    enrollment_no VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INTEGER CHECK (semester >= 1 AND semester <= 8),
    section VARCHAR(10),
    face_encoding BYTEA,
    photo_path TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Teachers Table
```sql
CREATE TABLE teacher (
    id SERIAL PRIMARY KEY,
    teacher_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    department VARCHAR(100) NOT NULL,
    designation VARCHAR(50),
    specialization VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Attendance Table
```sql
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES student(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,
    status VARCHAR(20) CHECK (status IN ('present', 'absent', 'flagged', 'suspicious', 'pending')),
    date DATE NOT NULL,
    time TIME NOT NULL,
    final_score NUMERIC(5,2) DEFAULT 0.0,
    face_confidence NUMERIC(5,2),
    liveness_confidence NUMERIC(5,2),
    background_confidence NUMERIC(5,2),
    audio_confidence NUMERIC(5,2),
    geofence_validation BOOLEAN DEFAULT FALSE,
    device_validation BOOLEAN DEFAULT FALSE,
    verified_by INTEGER REFERENCES users(id),
    verification_reason TEXT,
    is_manually_approved BOOLEAN DEFAULT FALSE,
    submission_time TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚨 Error Handling

### Common HTTP Status Codes

- **200 OK:** Successful request
- **400 Bad Request:** Invalid request data
- **401 Unauthorized:** Missing or invalid JWT token
- **403 Forbidden:** Insufficient permissions (non-admin accessing admin routes)
- **404 Not Found:** Resource not found
- **422 Unprocessable Entity:** Validation error

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 🔐 Authentication Flow

### 1. Register User
1. Call `POST /api/auth/register`
2. Get success response with user_id

### 2. Login
1. Call `POST /api/auth/login` with email/password
2. Receive JWT token in response
3. Include token in all subsequent requests

### 3. Access Protected Routes
1. Add `Authorization: Bearer <token>` header to requests
2. Token expires in 24 hours (1440 minutes)

---

## 🎯 Face Recognition Flow

### 1. Register Student Face
1. Admin uploads student photo via `POST /api/admin/students/{id}/photo`
2. System extracts face encoding and stores in database

### 2. Attendance Verification
1. Student submits face image via `POST /api/attendance/verify`
2. System compares with stored encoding
3. If similarity ≥ 0.6 (threshold): Mark as "present"
4. If similarity < 0.6: Mark as "flagged" for manual review

---

## 🔧 Configuration

### Environment Variables
```env
DATABASE_URL=postgresql://username:password@localhost/database_name
SECRET_KEY=your-secret-jwt-key-here
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
FACE_RECOGNITION_THRESHOLD=0.6
```

### Default Settings
- **JWT Expiry:** 24 hours
- **Face Recognition Threshold:** 0.6 (60% similarity)
- **CORS:** Enabled for localhost:3000 and localhost:8080
- **Password Hashing:** bcrypt

---

## 📝 Testing Examples

### Complete Workflow Test

1. **Register Admin User**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "full_name": "Admin User", "email": "admin@test.com", "password": "admin123", "role": "admin"}'
```

2. **Login as Admin**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}'
```

3. **Create Student User**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "full_name": "John Student", "email": "student@test.com", "password": "student123", "role": "student"}'
```

4. **Add Student Record**
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"student_id": "STU001", "user_id": 2, "enrollment_no": "EN001", "department": "CS", "semester": 1}'
```

5. **Upload Student Photo**
```bash
curl -X POST "http://localhost:8000/api/admin/students/1/photo" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "photo=<base64_encoded_image>"
```

---

## 📚 Additional Information

### Face Recognition Details
- Uses `face_recognition` library with dlib backend
- Supports common image formats (JPEG, PNG, etc.)
- Extracts 128-dimensional face encodings
- Stores encodings as binary data in PostgreSQL

### Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control (RBAC)
- CORS protection enabled

### Future Enhancements
- Session management for classes
- Geofencing for location-based attendance
- Real-time notifications
- Attendance analytics and reporting
- Mobile app integration
- Video-based attendance verification