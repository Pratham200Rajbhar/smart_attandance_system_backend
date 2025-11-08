# Smart Attendance System - FastAPI Backend

A comprehensive FastAPI backend for Smart Attendance System with face recognition capabilities.

## Features

✅ **Authentication Module**
- JWT-based user authentication
- User registration with role-based access (admin, teacher, student)
- Protected routes with role validation

✅ **Face Recognition Attendance**
- Face encoding storage and comparison
- Real-time attendance marking
- Confidence-based verification
- Support for both base64 and file upload

✅ **Admin Management**
- Student CRUD operations
- Teacher CRUD operations
- Face encoding registration for students
- Admin-only protected endpoints

✅ **Database Integration**
- PostgreSQL with async SQLAlchemy
- Comprehensive data models
- Automated database setup

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Async ORM
- **JWT** - Secure token-based authentication
- **bcrypt** - Password hashing
- **face_recognition** - Face detection and recognition
- **OpenCV** - Image processing

## Quick Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd smart_attendance_system_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
Edit the `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://postgres:password@localhost/smart_attendance
SECRET_KEY=your-secret-key-here-change-in-production
```

5. **Setup PostgreSQL database**
```bash
# Create database (if not exists)
createdb smart_attendance

# Run the automated setup
python quick_setup.py
```

6. **Start the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Default Admin User

After running `quick_setup.py`, you can login with:
- **Email**: `admin@smartattendance.com`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change this password immediately after first login!

## Database Management

Use the database manager for maintenance:

```bash
# List all users
python db_manager.py list-users

# List students
python db_manager.py list-students

# Show database info
python db_manager.py info

# Create new admin user
python db_manager.py create-admin --name "New Admin" --email "new@admin.com" --password "secure123"
```
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Attendance
- `POST /api/attendance/verify` - Verify attendance with base64 image
- `POST /api/attendance/verify-upload` - Verify attendance with file upload
- `GET /api/attendance/{student_id}` - Get student attendance records

### Admin (Admin only)
- `POST /api/admin/students` - Create student
- `GET /api/admin/students` - List all students
- `DELETE /api/admin/students/{id}` - Delete student
- `POST /api/admin/students/{id}/face` - Upload student face (base64)
- `POST /api/admin/students/{id}/face-upload` - Upload student face (file)
- `POST /api/admin/teachers` - Create teacher
- `GET /api/admin/teachers` - List all teachers
- `DELETE /api/admin/teachers/{id}` - Delete teacher

## Usage Examples

### 1. Login with Default Admin
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@smartattendance.com",
    "password": "admin123"
  }'
```

### 2. Create Student (Admin only)
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@student.edu"
  }'
```

### 4. Upload Student Face
```bash
# Using file upload
curl -X POST "http://localhost:8000/api/admin/students/1/face-upload" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "face_image=@student_photo.jpg"
```

### 5. Verify Attendance
```bash
# Using file upload
curl -X POST "http://localhost:8000/api/attendance/verify-upload" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "student_id=1" \
  -F "face_image=@attendance_photo.jpg"
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    face_encoding BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Teachers Table
```sql
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Attendance Records Table
```sql
CREATE TABLE attendance_records (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'flagged', 'absent')),
    confidence FLOAT DEFAULT 0.0
);
```

## Configuration

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (change in production)
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins
- `FACE_RECOGNITION_THRESHOLD` - Face matching threshold (default: 0.6)
- `MAX_FILE_SIZE` - Maximum file upload size (default: 10MB)

### Face Recognition Settings

- **Threshold**: 0.6 (configurable)
- **Encoding**: 128-dimensional face embeddings
- **Storage**: Binary format in PostgreSQL
- **Supported formats**: JPG, PNG, BMP

## Testing

### Manual Testing with Postman

1. Import the API collection from `/docs`
2. Set environment variables:
   - `base_url`: http://localhost:8000
   - `token`: JWT token from login

### Health Check
```bash
curl http://localhost:8000/health
```

## Production Deployment

### Security Considerations

1. **Change default SECRET_KEY**
2. **Use strong database passwords**
3. **Enable HTTPS**
4. **Configure proper CORS origins**
5. **Set up rate limiting**
6. **Enable database SSL**

### Performance Optimization

1. **Database indexing** (already configured)
2. **Connection pooling**
3. **Image compression for uploads**
4. **Caching for face encodings**

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the [API documentation](http://localhost:8000/docs)
2. Review the logs for error details
3. Open an issue on GitHub

---

**Note**: This is a prototype implementation. For production use, implement additional security measures, error handling, and monitoring.