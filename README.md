# Simple FastAPI CRUD Backend

A simplified FastAPI backend with basic CRUD operations and JWT authentication.

## Features

✅ JWT-based authentication (login/register/profile)  
✅ Admin panel for managing students and teachers  
✅ Basic CRUD operations (Create, Read, Update, Delete)  
✅ PostgreSQL database with async SQLAlchemy  
✅ Simple manual attendance marking  
✅ Clean, modular code structure  
✅ Sample data with Indian names  

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Async ORM
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing
- **Pydantic** - Data validation

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

## Quick Setup

### 1. Clone and Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup

Create PostgreSQL database:
```sql
CREATE DATABASE smart_attendance;
```

### 3. Environment Configuration

Copy environment file:
```bash
cp .env.example .env
```

Update `.env` with your database credentials:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/smart_attendance
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

### 4. Initialize Database

Run the database setup script:
```bash
python setup_database.py
```

Or manually run the SQL script:
```bash
psql -U postgres -d smart_attendance -f database_setup.sql
```

### 5. Start the Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Default Login Credentials

After running the database setup script:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@attendance.com | admin123 |
| Teacher | teacher@example.com | password123 |
| Student | aarav.agarwal@student.edu | student123 |

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get current user profile

### Admin Operations (Admin Only)
- `GET /api/admin/dashboard/stats` - Dashboard statistics
- `POST /api/admin/students` - Add new student
- `GET /api/admin/students` - List all students
- `GET /api/admin/students/{id}` - Get student by ID
- `PUT /api/admin/students/{id}` - Update student
- `DELETE /api/admin/students/{id}` - Delete student
- `POST /api/admin/teachers` - Add new teacher
- `GET /api/admin/teachers` - List all teachers
- `GET /api/admin/teachers/{id}` - Get teacher by ID
- `PUT /api/admin/teachers/{id}` - Update teacher
- `DELETE /api/admin/teachers/{id}` - Delete teacher

### Attendance (Basic)
- `POST /api/attendance/manual-mark` - Mark attendance manually
- `GET /api/attendance/students` - Get students for attendance

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Teachers Table
```sql
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Sample API Usage

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@college.edu", "password": "admin123"}'
```

### Get Students (with JWT token)
```bash
curl -X GET "http://localhost:8000/api/admin/students" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Add Student
```bash
curl -X POST "http://localhost:8000/api/admin/students" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "CS006",
       "name": "Raj Patel",
       "email": "raj.patel@student.edu",
       "department": "Computer Science"
     }'
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── auth/
│   │   └── routes.py        # Authentication routes
│   ├── admin/
│   │   └── routes.py        # Admin CRUD routes
│   ├── attendance/
│   │   └── routes.py        # Attendance routes
│   ├── core/
│   │   ├── config.py        # App configuration
│   │   └── security.py      # Security utilities
│   └── utils/
│       └── face_recognition_utils.py  # Placeholder for future features
├── database_setup.sql       # Manual SQL setup script
├── setup_database.py        # Automated Python setup script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## Development

### Running with Auto-reload
```bash
python -m uvicorn app.main:app --reload
```

### Database Reset
To reset the database with fresh sample data:
```bash
python setup_database.py
```

## Production Deployment

1. Update `.env` with production database credentials
2. Change `SECRET_KEY` to a strong, unique value
3. Set `ENVIRONMENT=production`
4. Configure proper CORS origins in `BACKEND_CORS_ORIGINS`
5. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Future Enhancements

This simplified backend can be extended with:
- Face recognition for attendance
- Class scheduling system
- Detailed attendance reporting
- Email notifications
- File upload capabilities
- Advanced analytics dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.