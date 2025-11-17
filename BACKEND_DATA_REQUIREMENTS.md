# Backend Data Requirements for Attendance Management System

This document outlines the data requirements for each page/component in the frontend dashboard. It specifies what data the website expects from the backend API.

## Table of Contents
- [Authentication System](#authentication-system)
- [Admin Dashboard](#admin-dashboard)
- [Teacher Dashboard](#teacher-dashboard)
- [Student Management](#student-management)
- [Teacher Management](#teacher-management)
- [Attendance Management](#attendance-management)
- [Subject & Session Management](#subject--session-management)
- [Geofence Management](#geofence-management)
- [System Configuration](#system-configuration)
- [Data Models](#data-models)

---

## Authentication System

### Login Page (`/auth/login`)
**Required Endpoints:**
- `POST /api/auth/login`

**Request Data:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Expected Response:**
```json
{
  "access_token": "string",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### User Profile
**Required Endpoints:**
- `GET /api/auth/profile`

**Expected Response:**
```json
{
  "id": "number",
  "username": "string",
  "email": "string",
  "full_name": "string", 
  "phone_number": "string",
  "role": "admin|teacher|student",
  "status": "active|inactive",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### User Registration
**Required Endpoints:**
- `POST /api/auth/register`

**Request Data:**
```json
{
  "username": "string",
  "full_name": "string",
  "email": "string",
  "phone_number": "string",
  "password": "string",
  "role": "admin|teacher|student",
  "status": "active|inactive"
}
```

---

## Admin Dashboard

### Main Dashboard (`/admin/dashboard`)
**Required Endpoints:**
- `GET /api/admin/students`
- `GET /api/admin/teachers`

**Expected Data Structure:**
```json
{
  "total_students": "number",
  "total_teachers": "number", 
  "total_subjects": "number",
  "total_sessions": "number"
}
```

**Dashboard Statistics Needed:**
- Total number of registered students
- Total number of registered teachers
- Total subjects in system
- Total sessions conducted
- Recent activity logs
- System health metrics

---

## Student Management

### Student List (`/admin/students`)
**Required Endpoints:**
- `GET /api/admin/students`

**Expected Response:**
```json
[
  {
    "id": "number",
    "student_id": "string",
    "user_id": "number",
    "enrollment_no": "string",
    "full_name": "string",
    "email": "string",
    "phone_number": "string",
    "department": "string",
    "semester": "number",
    "section": "string",
    "status": "active|inactive",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### Add Student (`/admin/students/add`)
**Required Endpoints:**
- `POST /api/admin/students`

**Request Data:**
```json
{
  "user_id": "number",
  "enrollment_no": "string",
  "department": "string",
  "semester": "number",
  "section": "string"
}
```

### Student Photo Upload
**Required Endpoints:**
- `POST /api/admin/students/{student_id}/photo`

**Request Data:**
- FormData with photo file or base64 image data

### Delete Student
**Required Endpoints:**
- `DELETE /api/admin/students/{student_id}`

---

## Teacher Management

### Teacher List (`/admin/teachers`)
**Required Endpoints:**
- `GET /api/admin/teachers`

**Expected Response:**
```json
[
  {
    "id": "number",
    "teacher_id": "string",
    "user_id": "number",
    "full_name": "string",
    "email": "string",
    "phone_number": "string",
    "department": "string",
    "designation": "string",
    "specialization": "string",
    "status": "active|inactive",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### Add Teacher (`/admin/teachers/add`)
**Required Endpoints:**
- `POST /api/admin/teachers`

**Request Data:**
```json
{
  "user_id": "number",
  "department": "string",
  "designation": "string",
  "specialization": "string"
}
```

### Delete Teacher
**Required Endpoints:**
- `DELETE /api/admin/teachers/{teacher_id}`

---

## Teacher Dashboard

### Teacher Main Dashboard (`/teacher/dashboard`)
**Required Endpoints:**
- `GET /api/teacher/dashboard` (or constructed from multiple endpoints)

**Expected Data Structure:**
```json
{
  "today_sessions": "number",
  "total_students": "number",
  "flagged_attendance": "number",
  "pending_reviews": "number",
  "subject_performance": [
    {
      "subject_name": "string",
      "attendance_rate": "number",
      "total_students": "number"
    }
  ],
  "quick_stats": {
    "this_week": "string",
    "this_month": "string", 
    "total_classes": "string",
    "avg_students": "string"
  },
  "weekly_attendance": ["number array for 7 days"],
  "recent_activity": [
    {
      "student_name": "string",
      "session_name": "string", 
      "status": "present|absent|flagged",
      "timestamp": "datetime"
    }
  ],
  "today_sessions_list": [
    {
      "id": "number",
      "session_name": "string",
      "subject_name": "string",
      "start_time": "time",
      "end_time": "time",
      "status": "ongoing|completed|upcoming"
    }
  ]
}
```

---

## Attendance Management

### Attendance Verification
**Required Endpoints:**
- `POST /api/attendance/verify`

**Request Data:**
- FormData containing:
  - `student_id`: number
  - `class_id`: number
  - `face_image`: File or base64 data

**Expected Response:**
```json
{
  "attendance_id": "number",
  "status": "present|absent|flagged|suspicious",
  "confidence_score": "number",
  "face_recognition_score": "number",
  "liveness_detection_score": "number",
  "background_validation_score": "number",
  "geofence_validation": "boolean",
  "timestamp": "datetime",
  "message": "string"
}
```

### Student Attendance History
**Required Endpoints:**
- `GET /api/attendance/{student_id}`

**Expected Response:**
```json
[
  {
    "attendance_id": "number",
    "student_id": "number",
    "class_id": "number",
    "session_id": "number",
    "status": "present|absent|flagged|suspicious",
    "date": "date",
    "time": "time",
    "final_score": "number",
    "face_confidence": "number",
    "liveness_confidence": "number",
    "background_confidence": "number",
    "geofence_validation": "boolean",
    "verified_by": "number|null",
    "verification_reason": "string|null",
    "created_at": "datetime"
  }
]
```

### Flagged Attendance Review (`/teacher/flagged-review`)
**Data Sources:**
- Student attendance records with low confidence scores
- Manual review queue
- Suspicious activity detection

**Expected Data:**
```json
[
  {
    "id": "number",
    "attendance_id": "number", 
    "student_id": "number",
    "student_name": "string",
    "student_email": "string",
    "status": "flagged|suspicious",
    "confidence": "number",
    "timestamp": "datetime",
    "submission_time": "datetime",
    "face_recognition_score": "number",
    "liveness_detection_score": "number",
    "background_validation_score": "number",
    "geofence_validation": "boolean",
    "session_name": "string",
    "subject_name": "string",
    "is_manually_approved": "boolean"
  }
]
```

### Manual Attendance Override
**Required Endpoints:**
- `POST /api/attendance/manual-override`

**Request Data:**
```json
{
  "attendance_record_id": "number",
  "decision": "approve|reject",
  "reason": "string",
  "teacher_id": "number"
}
```

---

## Subject & Session Management

### Subjects
**Required Endpoints:**
- `GET /api/subjects`
- `POST /api/subjects`
- `DELETE /api/subjects/{subject_id}`

**Subject Data Model:**
```json
{
  "id": "number",
  "subject_code": "string",
  "subject_name": "string",
  "department": "string",
  "semester": "number",
  "credits": "number",
  "teacher_id": "number",
  "status": "active|inactive",
  "created_at": "datetime"
}
```

### Sessions
**Required Endpoints:**
- `GET /api/sessions`
- `POST /api/sessions`
- `GET /api/sessions/{session_id}`
- `DELETE /api/sessions/{session_id}`

**Session Data Model:**
```json
{
  "id": "number",
  "session_name": "string",
  "subject_id": "number",
  "teacher_id": "number",
  "class_room": "string",
  "start_time": "datetime",
  "end_time": "datetime",
  "geofence_id": "number",
  "status": "scheduled|ongoing|completed|cancelled",
  "attendance_enabled": "boolean",
  "created_at": "datetime"
}
```

---

## Geofence Management

### Geofence Zones (`/admin/geofence`)
**Required Endpoints:**
- `GET /api/geofence/zones`
- `POST /api/geofence/zones`
- `DELETE /api/geofence/zones/{zone_id}`

**Geofence Data Model:**
```json
{
  "id": "number",
  "zone_name": "string",
  "description": "string",
  "latitude": "number",
  "longitude": "number", 
  "radius": "number",
  "status": "active|inactive",
  "created_by": "number",
  "created_at": "datetime"
}
```

---

## System Configuration

### System Settings (`/admin/config`)
**Required Endpoints:**
- `GET /api/admin/config`
- `PUT /api/admin/config`

**Configuration Data:**
```json
{
  "ai_thresholds": {
    "face_recognition": "number",
    "liveness_detection": "number", 
    "background_validation": "number",
    "audio_validation": "number"
  },
  "attendance_settings": {
    "auto_mark_absent": "boolean",
    "absent_threshold_minutes": "number",
    "allow_late_submissions": "boolean",
    "late_submission_penalty": "number"
  },
  "notification_settings": {
    "email_notifications": "boolean",
    "sms_notifications": "boolean",
    "push_notifications": "boolean"
  },
  "security_settings": {
    "max_login_attempts": "number",
    "session_timeout_minutes": "number",
    "require_2fa": "boolean"
  }
}
```

### Audit Logs (`/admin/audit-logs`)
**Required Endpoints:**
- `GET /api/admin/audit-logs`

**Audit Log Data:**
```json
[
  {
    "id": "number",
    "user_id": "number",
    "user_name": "string",
    "action": "string",
    "resource": "string",
    "resource_id": "number",
    "details": "json",
    "ip_address": "string",
    "user_agent": "string",
    "timestamp": "datetime"
  }
]
```

---

## Reports

### Attendance Reports (`/teacher/reports`)
**Required Endpoints:**
- `GET /api/reports/attendance`

**Query Parameters:**
- `start_date`: date
- `end_date`: date  
- `subject_id`: number (optional)
- `student_id`: number (optional)
- `report_type`: "summary|detailed|student|subject"

**Report Data:**
```json
{
  "summary": {
    "total_sessions": "number",
    "total_students": "number", 
    "average_attendance": "number",
    "attendance_trend": "increasing|decreasing|stable"
  },
  "detailed_records": [
    {
      "student_id": "number",
      "student_name": "string",
      "total_sessions": "number",
      "present_sessions": "number",
      "absent_sessions": "number",
      "attendance_percentage": "number"
    }
  ],
  "date_wise_summary": [
    {
      "date": "date",
      "total_present": "number",
      "total_absent": "number",
      "percentage": "number"
    }
  ]
}
```

---

## Data Models

### Core Entity Relationships

**User (Base)**
- id, username, email, full_name, phone_number, role, status, timestamps

**Student (extends User)**
- user_id, enrollment_no, department, semester, section

**Teacher (extends User)**  
- user_id, department, designation, specialization

**Subject**
- id, subject_code, subject_name, department, semester, credits, teacher_id

**Session**
- id, session_name, subject_id, teacher_id, classroom, start_time, end_time, geofence_id

**Attendance**
- id, student_id, session_id, status, confidence_scores, geofence_validation, verification_info

**Geofence**
- id, zone_name, coordinates, radius, status

### Status Enums
- **User Status**: active, inactive, suspended
- **Attendance Status**: present, absent, flagged, suspicious, pending
- **Session Status**: scheduled, ongoing, completed, cancelled
- **Verification Status**: verified, pending, rejected

### Required API Response Formats
All API responses should follow consistent format:
```json
{
  "success": "boolean",
  "data": "object|array",
  "message": "string",
  "errors": "array (if any)"
}
```

### Error Response Format
```json
{
  "success": false,
  "message": "string",
  "errors": [
    {
      "field": "string",
      "message": "string"
    }
  ]
}
```

---

## Additional Notes

1. **Authentication**: All endpoints (except login/register) require Bearer token authentication
2. **Pagination**: List endpoints should support pagination with `page`, `limit` parameters
3. **Filtering**: List endpoints should support filtering by relevant fields
4. **File Uploads**: Photo uploads support both FormData and base64 encoding
5. **Date Formats**: Use ISO 8601 format for all datetime fields
6. **Status Codes**: Follow standard HTTP status codes (200, 201, 400, 401, 403, 404, 500)

This document should be used as a reference for backend API development to ensure compatibility with the frontend dashboard requirements.