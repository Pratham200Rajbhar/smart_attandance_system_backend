# Smart Attendance System Backend

A clean, minimal FastAPI backend for face recognition-based attendance system.

## Features

- **Authentication**: JWT-based login/register/profile
- **Face Recognition**: Mark attendance using face matching
- **Admin Management**: Add/list/delete students & teachers
- **PostgreSQL Database**: Async SQLAlchemy ORM

## Quick Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Environment Variables**
```bash
cp .env.simple .env
# Edit .env with your database URL and secret key
```

3. **Run Application**
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/profile` - Get current user profile

### Admin (requires admin role)
- `POST /api/admin/students` - Add student
- `POST /api/admin/students/{id}/face` - Upload student face
- `GET /api/admin/students` - List students
- `DELETE /api/admin/students/{id}` - Delete student
- `POST /api/admin/teachers` - Add teacher
- `GET /api/admin/teachers` - List teachers
- `DELETE /api/admin/teachers/{id}` - Delete teacher

### Attendance
- `POST /api/attendance/verify` - Mark attendance using face recognition
- `GET /api/attendance/{student_id}` - Get attendance records

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    face_encoding BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Teachers table
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Attendance records table
CREATE TABLE attendance_records (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) NOT NULL,
    confidence FLOAT DEFAULT 0.0
);
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database with async support
- **SQLAlchemy** - Async ORM
- **JWT** - Token-based authentication
- **bcrypt** - Password hashing
- **face_recognition** - Face detection and encoding
- **OpenCV** - Image processing

The codebase is now clean, minimal, and production-ready!