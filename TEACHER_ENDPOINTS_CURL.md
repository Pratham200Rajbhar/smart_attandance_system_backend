# Teacher Endpoints - cURL Examples

## Overview
This document provides cURL examples for all teacher endpoints in the Smart Attendance System API. All teacher endpoints require JWT authentication with a `teacher` role.

**Base URL:** `http://localhost:8000/api/teacher`

## Prerequisites

### 1. Get Teacher JWT Token
First, you need to login as a teacher to get the JWT token:

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@example.com",
    "password": "teacherpassword"
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

**Important:** Replace `<TEACHER_JWT_TOKEN>` in all examples below with the actual token from the login response.

---

## 📊 Teacher Dashboard

### Get Dashboard Overview
**Endpoint:** `GET /api/teacher/dashboard`

```bash
curl -X GET "http://localhost:8000/api/teacher/dashboard" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "today_sessions": 3,
  "total_students": 45,
  "flagged_attendance": 2,
  "pending_reviews": 2,
  "subject_performance": [
    {
      "subject_name": "Mathematics",
      "total_sessions": 15,
      "attendance_rate": 85.5,
      "flagged_count": 3
    },
    {
      "subject_name": "Physics",
      "total_sessions": 12,
      "attendance_rate": 92.1,
      "flagged_count": 1
    }
  ],
  "quick_stats": {
    "total_sessions_this_week": 12,
    "average_attendance": 88.2,
    "students_present_today": 38
  },
  "weekly_attendance": [85, 90, 78, 92, 88, 85, 89],
  "recent_activity": [],
  "today_sessions_list": [
    {
      "session_id": 1,
      "session_name": "Mathematics - Advanced Calculus",
      "start_time": "2025-11-17T10:00:00",
      "end_time": "2025-11-17T11:30:00",
      "class_room": "Room 101",
      "status": "scheduled",
      "students_registered": 25
    }
  ]
}
```

---

## 📚 Session Management

### 1. Get All Teacher Sessions
**Endpoint:** `GET /api/teacher/sessions`

```bash
curl -X GET "http://localhost:8000/api/teacher/sessions" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "session_name": "Advanced Calculus",
    "subject_name": "Mathematics",
    "start_time": "2025-11-17T10:00:00",
    "end_time": "2025-11-17T11:30:00",
    "class_room": "Room 101",
    "status": "scheduled",
    "students_registered": 25,
    "attendance_count": 23
  },
  {
    "id": 2,
    "session_name": "Linear Algebra",
    "subject_name": "Mathematics",
    "start_time": "2025-11-16T14:00:00",
    "end_time": "2025-11-16T15:30:00",
    "class_room": "Room 102",
    "status": "completed",
    "students_registered": 28,
    "attendance_count": 26
  }
]
```

### 2. Get Session Details
**Endpoint:** `GET /api/teacher/sessions/{session_id}`

```bash
curl -X GET "http://localhost:8000/api/teacher/sessions/1" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "id": 1,
  "session_name": "Advanced Calculus",
  "subject_name": "Mathematics",
  "start_time": "2025-11-17T10:00:00",
  "end_time": "2025-11-17T11:30:00",
  "class_room": "Room 101",
  "status": "active",
  "students_registered": 25,
  "attendance_summary": {
    "present": 20,
    "absent": 3,
    "flagged": 2
  }
}
```

### 3. Get Session Attendance Records
**Endpoint:** `GET /api/teacher/sessions/{session_id}/attendance`

```bash
curl -X GET "http://localhost:8000/api/teacher/sessions/1/attendance" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "student_name": "John Doe",
    "enrollment_no": "EN001",
    "status": "present",
    "confidence": 85.0,
    "timestamp": "2025-11-17T10:30:00",
    "verification_method": "face_recognition"
  },
  {
    "id": 2,
    "student_id": 2,
    "student_name": "Jane Smith",
    "enrollment_no": "EN002",
    "status": "flagged",
    "confidence": 45.0,
    "timestamp": "2025-11-17T10:32:00",
    "verification_method": "face_recognition"
  }
]
```

---

## 📖 Subject Management

### Get Teacher Subjects
**Endpoint:** `GET /api/teacher/subjects`

```bash
curl -X GET "http://localhost:8000/api/teacher/subjects" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "subject_code": "MATH101",
    "subject_name": "Advanced Mathematics",
    "department": "Computer Science",
    "semester": 3,
    "credits": 4,
    "teacher_id": 1,
    "status": "active",
    "created_at": "2025-11-17T10:30:00",
    "updated_at": "2025-11-17T10:30:00",
    "teacher": null
  },
  {
    "id": 2,
    "subject_code": "PHYS101",
    "subject_name": "Physics Fundamentals",
    "department": "Computer Science",
    "semester": 2,
    "credits": 3,
    "teacher_id": 1,
    "status": "active",
    "created_at": "2025-11-17T10:30:00",
    "updated_at": "2025-11-17T10:30:00",
    "teacher": null
  }
]
```

---

## 🚨 Attendance Management

### 1. Get Flagged Attendance Records
**Endpoint:** `GET /api/teacher/attendance/flagged`

```bash
curl -X GET "http://localhost:8000/api/teacher/attendance/flagged" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
[
  {
    "id": 15,
    "student_id": 5,
    "student_name": "John Doe",
    "session_name": "Mathematics - Advanced Calculus",
    "status": "flagged",
    "confidence": 45.0,
    "timestamp": "2025-11-17T10:30:00",
    "reason": "Low confidence score"
  },
  {
    "id": 16,
    "student_id": 8,
    "student_name": "Alice Johnson",
    "session_name": "Physics - Mechanics",
    "status": "flagged",
    "confidence": 38.5,
    "timestamp": "2025-11-17T14:15:00",
    "reason": "Low confidence score"
  }
]
```

### 2. Create Manual Attendance
**Endpoint:** `POST /api/teacher/attendance/manual`

```bash
curl -X POST "http://localhost:8000/api/teacher/attendance/manual" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "session_id": 1,
    "status": "present",
    "reason": "Technical issue with face recognition, student was verified manually"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Manual attendance recorded as present",
  "data": {
    "attendance_id": 25
  }
}
```

### 3. Review/Approve Flagged Attendance
**Endpoint:** `PUT /api/teacher/attendance/{attendance_id}/review`

#### Approve Attendance:
```bash
curl -X PUT "http://localhost:8000/api/teacher/attendance/15/review" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approved",
    "reason": "Student was present, lighting conditions caused low confidence score"
  }'
```

#### Reject Attendance:
```bash
curl -X PUT "http://localhost:8000/api/teacher/attendance/16/review" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "rejected", 
    "reason": "Student was not actually present in class"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Attendance approved successfully",
  "data": {
    "attendance_id": 15,
    "new_status": "present"
  }
}
```

---

## 📊 Reports

### Get Attendance Report
**Endpoint:** `GET /api/teacher/reports/attendance`

#### Get Report for Last 30 Days (Default):
```bash
curl -X GET "http://localhost:8000/api/teacher/reports/attendance" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

#### Get Report for Specific Date Range:
```bash
curl -X GET "http://localhost:8000/api/teacher/reports/attendance?start_date=2025-11-01&end_date=2025-11-17" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

#### Get Report for This Week:
```bash
curl -X GET "http://localhost:8000/api/teacher/reports/attendance?start_date=2025-11-11&end_date=2025-11-17" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "summary": {
    "total_sessions": 25,
    "average_attendance": 88.5,
    "total_present": 980,
    "total_flagged": 15,
    "date_range": {
      "start_date": "2025-11-01",
      "end_date": "2025-11-17"
    }
  },
  "detailed_records": [
    {
      "date": "2025-11-17",
      "session_name": "Mathematics - Advanced Calculus",
      "total_students": 25,
      "present": 23,
      "absent": 2,
      "flagged": 0,
      "attendance_percentage": 92.0
    },
    {
      "date": "2025-11-16",
      "session_name": "Physics - Mechanics",
      "total_students": 28,
      "present": 24,
      "absent": 2,
      "flagged": 2,
      "attendance_percentage": 85.7
    }
  ]
}
```

---

## 🔄 Complete Workflow Example

### 1. Teacher Daily Workflow

#### Step 1: Check Dashboard
```bash
curl -X GET "http://localhost:8000/api/teacher/dashboard" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

#### Step 2: View Today's Sessions
```bash
curl -X GET "http://localhost:8000/api/teacher/sessions" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

#### Step 3: Check Session Attendance (Session ID: 1)
```bash
curl -X GET "http://localhost:8000/api/teacher/sessions/1/attendance" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

#### Step 4: Review Flagged Attendance
```bash
curl -X GET "http://localhost:8000/api/teacher/attendance/flagged" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

#### Step 5: Approve Flagged Record
```bash
curl -X PUT "http://localhost:8000/api/teacher/attendance/15/review" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approved",
    "reason": "Verified student presence manually"
  }'
```

### 2. Manual Attendance Entry Workflow

#### Step 1: Create Manual Entry for Absent Student
```bash
curl -X POST "http://localhost:8000/api/teacher/attendance/manual" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 10,
    "session_id": 1,
    "status": "present",
    "reason": "Student arrived late, face recognition system was offline"
  }'
```

#### Step 2: Verify the Entry
```bash
curl -X GET "http://localhost:8000/api/teacher/sessions/1/attendance" \
  -H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

---

## 🚨 Error Responses

### Common Error Codes:

#### 401 Unauthorized (Invalid/Missing Token):
```json
{
  "detail": "Invalid token"
}
```

#### 403 Forbidden (Not a Teacher):
```json
{
  "detail": "Teacher access required"
}
```

#### 404 Not Found (Session/Record Not Found):
```json
{
  "detail": "Session not found"
}
```

#### 400 Bad Request (Invalid Data):
```json
{
  "detail": "Decision must be 'approved' or 'rejected'"
}
```

---

## 🔧 Testing Tips

### 1. Authentication Headers
Always include the `Authorization` header with a valid teacher JWT token:
```bash
-H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
```

### 2. Content Type
For POST/PUT requests, include the content type header:
```bash
-H "Content-Type: application/json"
```

### 3. JSON Data
Ensure JSON data is properly formatted and quoted:
```bash
-d '{"key": "value", "number": 123}'
```

### 4. URL Encoding
For query parameters with special characters, ensure proper encoding:
```bash
"?start_date=2025-11-01&end_date=2025-11-17"
```

### 5. Response Validation
Check HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

---

## 📝 Quick Reference

### All Teacher Endpoints:
1. `GET /api/teacher/dashboard` - Dashboard overview
2. `GET /api/teacher/sessions` - All sessions
3. `GET /api/teacher/subjects` - Assigned subjects
4. `GET /api/teacher/sessions/{id}` - Session details
5. `GET /api/teacher/sessions/{id}/attendance` - Session attendance
6. `GET /api/teacher/attendance/flagged` - Flagged records
7. `POST /api/teacher/attendance/manual` - Manual attendance
8. `PUT /api/teacher/attendance/{id}/review` - Review attendance
9. `GET /api/teacher/reports/attendance` - Attendance reports

### Required Headers:
```bash
-H "Authorization: Bearer <TEACHER_JWT_TOKEN>"
-H "Content-Type: application/json"  # For POST/PUT requests
```