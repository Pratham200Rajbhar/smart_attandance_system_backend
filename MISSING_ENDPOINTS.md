# Missing API Endpoints - Implementation Guide

## Overview
The frontend expects specific teacher endpoints that are not yet implemented in the backend. Below are the required endpoints for full functionality.

## 🚨 Critical Missing Endpoints

### 1. Teacher Dashboard
```
GET /api/teacher/dashboard
```
**Headers:** `Authorization: Bearer <token>`

**Expected Response:**
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

### 2. Teacher Sessions List
```
GET /api/teacher/sessions
```
**Headers:** `Authorization: Bearer <token>`

**Expected Response:**
```json
[
  {
    "id": 1,
    "session_name": "Mathematics - Advanced",
    "subject_name": "Mathematics",
    "start_time": "2025-11-17T10:00:00Z",
    "end_time": "2025-11-17T11:30:00Z",
    "class_room": "Room 101",
    "status": "scheduled",
    "students_registered": 25,
    "attendance_count": 23
  }
]
```

### 3. Teacher Subjects List
```
GET /api/teacher/subjects
```
**Headers:** `Authorization: Bearer <token>`

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
    "status": "active"
  }
]
```

### 4. Session Details
```
GET /api/teacher/sessions/{session_id}
```
**Headers:** `Authorization: Bearer <token>`

**Expected Response:**
```json
{
  "id": 1,
  "session_name": "Mathematics - Advanced",
  "subject_name": "Mathematics",
  "start_time": "2025-11-17T10:00:00Z",
  "end_time": "2025-11-17T11:30:00Z",
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

### 5. Session Attendance Records
```
GET /api/teacher/sessions/{session_id}/attendance
```
**Headers:** `Authorization: Bearer <token>`

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
    "timestamp": "2025-11-17T10:30:00Z",
    "verification_method": "face_recognition"
  }
]
```

### 6. Flagged Attendance Records
```
GET /api/teacher/attendance/flagged
```
**Headers:** `Authorization: Bearer <token>`

**Expected Response:**
```json
[
  {
    "id": 1,
    "student_id": 5,
    "student_name": "John Doe",
    "session_name": "Mathematics",
    "status": "flagged",
    "confidence": 45.0,
    "timestamp": "2025-11-17T10:30:00Z",
    "reason": "Low confidence score"
  }
]
```

### 7. Manual Attendance Override
```
POST /api/teacher/attendance/manual
```
**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "student_id": 1,
  "session_id": 1,
  "status": "present",
  "reason": "Technical issue with face recognition"
}
```

### 8. Approve/Reject Flagged Attendance
```
PUT /api/teacher/attendance/{attendance_id}/review
```
**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "decision": "approved",
  "reason": "Student was present, lighting issue caused low confidence"
}
```

### 9. Attendance History/Reports
```
GET /api/teacher/reports/attendance?start_date=2025-11-01&end_date=2025-11-17
```
**Headers:** `Authorization: Bearer <token>`

**Expected Response:**
```json
{
  "summary": {
    "total_sessions": 25,
    "average_attendance": 88.5,
    "total_present": 980,
    "total_flagged": 15
  },
  "detailed_records": [
    {
      "date": "2025-11-17",
      "session_name": "Mathematics",
      "total_students": 25,
      "present": 23,
      "absent": 2,
      "flagged": 0
    }
  ]
}
```

## 🔧 Implementation Notes

### Authentication
- All teacher endpoints require JWT token with `role: "teacher"`
- Filter data based on `teacher_id` from JWT payload

### Database Queries
- Join `teacher`, `sessions`, `attendance`, and `student` tables
- Filter by teacher's assigned subjects/sessions
- Calculate aggregated statistics for dashboard

### Priority Order
1. **Teacher Dashboard** - Critical for main interface
2. **Sessions List** - Core functionality
3. **Session Details & Attendance** - Essential for attendance management
4. **Flagged Records & Manual Override** - Important for attendance validation

### Response Format
- Use consistent status codes (200, 400, 401, 403, 404)
- Include proper error messages
- Maintain data structure consistency with existing endpoints

## 📝 Quick Implementation Checklist
- [ ] Create teacher router in FastAPI
- [ ] Implement JWT role validation for teacher endpoints
- [ ] Add database queries with proper joins
- [ ] Test with actual teacher JWT token
- [ ] Verify response format matches frontend expectations