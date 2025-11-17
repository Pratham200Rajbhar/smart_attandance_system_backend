# Smart Attendance System API Documentation

Complete REST API documentation for the Smart Attendance System backend that aligns with frontend requirements.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints (except login/register) require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

## Response Format
All API responses follow this consistent format:
```json
{
  "success": boolean,
  "data": object | array,
  "message": "string",
  "errors": array (optional)
}
```

## Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "field": "field_name",
      "message": "Error message"
    }
  ]
}
```

---

## Authentication Endpoints

### 1. User Login
**Endpoint:** `POST /api/auth/login`
**Description:** Authenticate user and return JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 3600
  },
  "message": "Login successful"
}
```

### 2. User Registration
**Endpoint:** `POST /api/auth/register`
**Description:** Register a new user (admin only)

**Request Body:**
```json
{
  "username": "johndoe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+91-9876543210",
  "password": "password123",
  "role": "student|teacher|admin",
  "status": "active"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "student"
  },
  "message": "User registered successfully"
}
```

### 3. Get User Profile
**Endpoint:** `GET /api/auth/profile`
**Description:** Get current logged-in user profile
**Auth Required:** Yes

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone_number": "+91-9876543210",
    "role": "student",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "message": "Profile retrieved successfully"
}
```

---

## Admin Endpoints

### 4. Admin Dashboard
**Endpoint:** `GET /api/admin/dashboard`
**Description:** Get admin dashboard statistics
**Auth Required:** Yes (Admin only)

**Response:**
```json
{
  "success": true,
  "data": {
    "total_students": 150,
    "total_teachers": 25,
    "total_subjects": 45,
    "total_sessions": 120
  },
  "message": "Dashboard data retrieved successfully"
}
```

### 5. Get All Students
**Endpoint:** `GET /api/admin/students`
**Description:** Get list of all students
**Auth Required:** Yes (Admin only)
**Query Parameters:** `?page=1&limit=10&search=keyword`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "student_id": "STU001",
      "user_id": 5,
      "enrollment_no": "CS2024001",
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone_number": "+91-9876543210",
      "department": "Computer Science",
      "semester": 3,
      "section": "A",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Students retrieved successfully"
}
```

### 6. Add New Student
**Endpoint:** `POST /api/admin/students`
**Description:** Add a new student
**Auth Required:** Yes (Admin only)

**Request Body:**
```json
{
  "user_id": 5,
  "student_id": "STU001",
  "enrollment_no": "CS2024001",
  "department": "Computer Science",
  "semester": 3,
  "section": "A"
}
```

### 7. Delete Student
**Endpoint:** `DELETE /api/admin/students/{student_id}`
**Description:** Delete a student
**Auth Required:** Yes (Admin only)

**Response:**
```json
{
  "success": true,
  "message": "Student deleted successfully"
}
```

### 8. Upload Student Photo
**Endpoint:** `POST /api/admin/students/{student_id}/photo`
**Description:** Upload student photo for face recognition
**Auth Required:** Yes (Admin only)
**Content-Type:** multipart/form-data

**Request Body:** FormData with photo file

### 9. Get All Teachers
**Endpoint:** `GET /api/admin/teachers`
**Description:** Get list of all teachers
**Auth Required:** Yes (Admin only)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "teacher_id": "TEA001",
      "user_id": 3,
      "full_name": "Dr. Jane Smith",
      "email": "jane@example.com",
      "phone_number": "+91-9876543210",
      "department": "Computer Science",
      "designation": "Professor",
      "specialization": "Machine Learning",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Teachers retrieved successfully"
}
```

### 10. Add New Teacher
**Endpoint:** `POST /api/admin/teachers`
**Description:** Add a new teacher
**Auth Required:** Yes (Admin only)

**Request Body:**
```json
{
  "user_id": 3,
  "teacher_id": "TEA001",
  "department": "Computer Science",
  "designation": "Professor",
  "specialization": "Machine Learning"
}
```

### 11. Delete Teacher
**Endpoint:** `DELETE /api/admin/teachers/{teacher_id}`
**Description:** Delete a teacher
**Auth Required:** Yes (Admin only)

---

## Teacher Dashboard Endpoints

### 12. Teacher Dashboard
**Endpoint:** `GET /api/teacher/dashboard`
**Description:** Get teacher dashboard data
**Auth Required:** Yes (Teacher only)

**Response:**
```json
{
  "success": true,
  "data": {
    "today_sessions": 3,
    "total_students": 45,
    "flagged_attendance": 2,
    "pending_reviews": 5,
    "subject_performance": [
      {
        "subject_name": "Machine Learning",
        "attendance_rate": 85.5,
        "total_students": 30
      }
    ],
    "quick_stats": {
      "this_week": "25",
      "this_month": "120",
      "total_classes": "450",
      "avg_students": "28"
    },
    "weekly_attendance": [20, 25, 30, 28, 22, 15, 18],
    "recent_activity": [
      {
        "student_name": "John Doe",
        "session_name": "ML Basics",
        "status": "flagged",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ],
    "today_sessions_list": [
      {
        "id": 1,
        "session_name": "ML Basics",
        "subject_name": "Machine Learning",
        "start_time": "09:00",
        "end_time": "10:30",
        "status": "upcoming"
      }
    ]
  },
  "message": "Dashboard data retrieved successfully"
}
```

### 13. Get Flagged Attendance
**Endpoint:** `GET /api/teacher/flagged-attendance`
**Description:** Get attendance records requiring manual review
**Auth Required:** Yes (Teacher only)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "attendance_id": 15,
      "student_id": 5,
      "student_name": "John Doe",
      "student_email": "john@example.com",
      "status": "flagged",
      "confidence": 65.5,
      "timestamp": "2024-01-15T10:30:00Z",
      "submission_time": "2024-01-15T10:32:00Z",
      "face_recognition_score": 70.0,
      "liveness_detection_score": 65.0,
      "background_validation_score": 60.0,
      "geofence_validation": false,
      "session_name": "ML Basics",
      "subject_name": "Machine Learning",
      "is_manually_approved": false
    }
  ],
  "message": "Flagged attendance retrieved successfully"
}
```

---

## Attendance Management Endpoints

### 14. Verify Attendance
**Endpoint:** `POST /api/attendance/verify`
**Description:** Verify student attendance using face recognition
**Auth Required:** Yes
**Content-Type:** multipart/form-data

**Request Body:**
```
student_id: 5
session_id: 10
face_image: base64_encoded_image_data
```

**Response:**
```json
{
  "success": true,
  "data": {
    "attendance_id": 25,
    "status": "present",
    "confidence_score": 87.5,
    "face_recognition_score": 90.0,
    "liveness_detection_score": 85.0,
    "background_validation_score": 88.0,
    "geofence_validation": true,
    "timestamp": "2024-01-15T10:30:00Z",
    "message": "Attendance marked successfully"
  },
  "message": "Attendance verified successfully"
}
```

### 15. Get Student Attendance History
**Endpoint:** `GET /api/attendance/{student_id}`
**Description:** Get attendance history for a specific student
**Auth Required:** Yes
**Query Parameters:** `?start_date=2024-01-01&end_date=2024-01-31`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "attendance_id": 25,
      "student_id": 5,
      "session_id": 10,
      "status": "present",
      "date": "2024-01-15",
      "time": "10:30:00",
      "final_score": 87.5,
      "face_confidence": 90.0,
      "liveness_confidence": 85.0,
      "background_confidence": 88.0,
      "geofence_validation": true,
      "verified_by": null,
      "verification_reason": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Attendance history retrieved successfully"
}
```

### 16. Manual Attendance Override
**Endpoint:** `POST /api/attendance/manual-override`
**Description:** Manually approve or reject flagged attendance
**Auth Required:** Yes (Teacher only)

**Request Body:**
```json
{
  "attendance_record_id": 25,
  "decision": "approve",
  "reason": "Student was late but verified in person",
  "teacher_id": 3
}
```

---

## Subject Management Endpoints

### 17. Get All Subjects
**Endpoint:** `GET /api/subjects`
**Description:** Get list of all subjects
**Auth Required:** Yes

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "subject_code": "CS301",
      "subject_name": "Machine Learning",
      "department": "Computer Science",
      "semester": 6,
      "credits": 4,
      "teacher_id": 3,
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Subjects retrieved successfully"
}
```

### 18. Create Subject
**Endpoint:** `POST /api/subjects`
**Description:** Create a new subject
**Auth Required:** Yes (Admin/Teacher)

**Request Body:**
```json
{
  "subject_code": "CS301",
  "subject_name": "Machine Learning",
  "department": "Computer Science",
  "semester": 6,
  "credits": 4,
  "teacher_id": 3
}
```

### 19. Delete Subject
**Endpoint:** `DELETE /api/subjects/{subject_id}`
**Description:** Delete a subject
**Auth Required:** Yes (Admin only)

---

## Session Management Endpoints

### 20. Get All Sessions
**Endpoint:** `GET /api/sessions`
**Description:** Get list of all sessions
**Auth Required:** Yes
**Query Parameters:** `?teacher_id=3&date=2024-01-15&status=scheduled`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_name": "ML Basics - Introduction",
      "subject_id": 5,
      "teacher_id": 3,
      "class_room": "Room 101",
      "start_time": "2024-01-15T09:00:00Z",
      "end_time": "2024-01-15T10:30:00Z",
      "geofence_id": 1,
      "status": "scheduled",
      "attendance_enabled": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Sessions retrieved successfully"
}
```

### 21. Create Session
**Endpoint:** `POST /api/sessions`
**Description:** Create a new session
**Auth Required:** Yes (Teacher/Admin)

**Request Body:**
```json
{
  "session_name": "ML Basics - Introduction",
  "subject_id": 5,
  "teacher_id": 3,
  "class_room": "Room 101",
  "start_time": "2024-01-15T09:00:00Z",
  "end_time": "2024-01-15T10:30:00Z",
  "geofence_id": 1,
  "description": "Introduction to machine learning concepts"
}
```

### 22. Get Session Details
**Endpoint:** `GET /api/sessions/{session_id}`
**Description:** Get detailed information about a specific session
**Auth Required:** Yes

### 23. Delete Session
**Endpoint:** `DELETE /api/sessions/{session_id}`
**Description:** Delete a session
**Auth Required:** Yes (Teacher/Admin)

---

## Geofence Management Endpoints

### 24. Get Geofence Zones
**Endpoint:** `GET /api/geofence/zones`
**Description:** Get list of all geofence zones
**Auth Required:** Yes (Admin only)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "zone_name": "Main Building",
      "description": "Main academic building",
      "latitude": 28.6139,
      "longitude": 77.2090,
      "radius": 50.0,
      "status": "active",
      "created_by": 1,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Geofence zones retrieved successfully"
}
```

### 25. Create Geofence Zone
**Endpoint:** `POST /api/geofence/zones`
**Description:** Create a new geofence zone
**Auth Required:** Yes (Admin only)

**Request Body:**
```json
{
  "zone_name": "Library Building",
  "description": "University library",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "radius": 30.0
}
```

### 26. Delete Geofence Zone
**Endpoint:** `DELETE /api/geofence/zones/{zone_id}`
**Description:** Delete a geofence zone
**Auth Required:** Yes (Admin only)

---

## System Configuration Endpoints

### 27. Get System Configuration
**Endpoint:** `GET /api/admin/config`
**Description:** Get system configuration settings
**Auth Required:** Yes (Admin only)

**Response:**
```json
{
  "success": true,
  "data": {
    "ai_thresholds": {
      "face_recognition": 85.0,
      "liveness_detection": 80.0,
      "background_validation": 75.0,
      "audio_validation": 70.0
    },
    "attendance_settings": {
      "auto_mark_absent": true,
      "absent_threshold_minutes": 15,
      "allow_late_submissions": true,
      "late_submission_penalty": 5.0
    },
    "notification_settings": {
      "email_notifications": true,
      "sms_notifications": false,
      "push_notifications": true
    },
    "security_settings": {
      "max_login_attempts": 5,
      "session_timeout_minutes": 1440,
      "require_2fa": false
    }
  },
  "message": "Configuration retrieved successfully"
}
```

### 28. Update System Configuration
**Endpoint:** `PUT /api/admin/config`
**Description:** Update system configuration settings
**Auth Required:** Yes (Admin only)

**Request Body:**
```json
{
  "ai_thresholds": {
    "face_recognition": 90.0,
    "liveness_detection": 85.0
  }
}
```

### 29. Get Audit Logs
**Endpoint:** `GET /api/admin/audit-logs`
**Description:** Get system audit logs
**Auth Required:** Yes (Admin only)
**Query Parameters:** `?page=1&limit=50&start_date=2024-01-01&end_date=2024-01-31`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "admin",
      "action": "student_created",
      "resource": "student",
      "resource_id": 5,
      "details": {"student_id": "STU001", "name": "John Doe"},
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Audit logs retrieved successfully"
}
```

---

## Reporting Endpoints

### 30. Get Attendance Reports
**Endpoint:** `GET /api/reports/attendance`
**Description:** Generate attendance reports
**Auth Required:** Yes (Teacher/Admin)
**Query Parameters:** `?start_date=2024-01-01&end_date=2024-01-31&subject_id=5&student_id=10&report_type=summary`

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_sessions": 20,
      "total_students": 30,
      "average_attendance": 85.5,
      "attendance_trend": "increasing"
    },
    "detailed_records": [
      {
        "student_id": 5,
        "student_name": "John Doe",
        "total_sessions": 20,
        "present_sessions": 18,
        "absent_sessions": 2,
        "attendance_percentage": 90.0
      }
    ],
    "date_wise_summary": [
      {
        "date": "2024-01-15",
        "total_present": 25,
        "total_absent": 5,
        "percentage": 83.33
      }
    ]
  },
  "message": "Report generated successfully"
}
```

---

## Notification Endpoints

### 31. Get User Notifications
**Endpoint:** `GET /api/notifications`
**Description:** Get notifications for current user
**Auth Required:** Yes
**Query Parameters:** `?status=unread&page=1&limit=20`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Attendance Flagged",
      "message": "Your attendance for ML class has been flagged for review",
      "type": "warning",
      "status": "unread",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "message": "Notifications retrieved successfully"
}
```

### 32. Mark Notification as Read
**Endpoint:** `PUT /api/notifications/{notification_id}/read`
**Description:** Mark a notification as read
**Auth Required:** Yes

---

## HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

---

## Pagination

List endpoints support pagination:
```
GET /api/admin/students?page=1&limit=10
```

## Search and Filtering

Most list endpoints support search and filtering:
```
GET /api/admin/students?search=john&department=CS&semester=3
```

## Error Handling

All errors return appropriate HTTP status codes with detailed error messages in the response body.