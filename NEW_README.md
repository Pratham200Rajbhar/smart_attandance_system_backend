# Smart Attendance System Backend

A comprehensive FastAPI backend for a Smart Attendance System with AI-powered face recognition, geofence validation, and comprehensive attendance management.

## 🚀 Features

### Core Functionality
- **JWT Authentication** - Secure token-based authentication system
- **Role-based Access Control** - Admin, Teacher, and Student roles
- **Face Recognition** - AI-powered attendance verification
- **Geofence Validation** - Location-based attendance confirmation
- **Manual Review System** - Teacher oversight for flagged attendance
- **Comprehensive Reporting** - Detailed analytics and reports

### Technical Features
- **Async FastAPI** - High-performance asynchronous API
- **PostgreSQL Database** - Robust relational database with async support
- **SQLAlchemy ORM** - Modern async ORM with Pydantic integration
- **Comprehensive Logging** - Full audit trail and system monitoring
- **Scalable Architecture** - Modular design for easy expansion

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip package manager

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart_attendance_system_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost/smart_attendance
SECRET_KEY=your-super-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
FACE_RECOGNITION_THRESHOLD=0.6
```

### 5. Database Setup
```bash
# Create PostgreSQL database
createdb smart_attendance

# Run the database setup script
python new_setup_database.py
```

### 6. Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Database Schema

The system uses a comprehensive PostgreSQL schema with the following key tables:

### Core Tables
- **users** - User authentication and profile data
- **student** - Student-specific information and face encodings
- **teacher** - Teacher profiles and specializations
- **subjects** - Academic subjects and course management
- **sessions** - Class sessions and lecture management
- **attendance** - Attendance records with AI confidence scores

### Supporting Tables
- **geofence** - Location-based validation zones
- **system_config** - Flexible system configuration
- **audit_logs** - Complete system activity tracking
- **notification** - User notification management
- **environment_metrics** - Additional validation data

See `DATABASE_SCHEMA_UPDATES.md` for complete schema documentation.

## 🔗 API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration (admin only)
- `GET /api/auth/profile` - Get user profile

### Admin Endpoints
- `GET /api/admin/dashboard` - Admin dashboard statistics
- `GET /api/admin/students` - List all students
- `POST /api/admin/students` - Add new student
- `DELETE /api/admin/students/{id}` - Delete student
- `GET /api/admin/teachers` - List all teachers
- `POST /api/admin/teachers` - Add new teacher
- `DELETE /api/admin/teachers/{id}` - Delete teacher

### Attendance Endpoints
- `POST /api/attendance/verify` - Verify attendance with face recognition
- `GET /api/attendance/{student_id}` - Get attendance history
- `POST /api/attendance/manual-override` - Manual attendance approval

### Dashboard Endpoints
- `GET /api/teacher/dashboard` - Teacher dashboard data
- `GET /api/teacher/flagged-attendance` - Flagged attendance for review

### Management Endpoints
- `GET /api/subjects` - List subjects
- `POST /api/subjects` - Create subject
- `GET /api/sessions` - List sessions
- `POST /api/sessions` - Create session
- `GET /api/geofence/zones` - List geofence zones

See `COMPLETE_API_DOCUMENTATION.md` for detailed API specification.

## 🧪 Testing the API

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Default Admin Credentials
After running the setup script, use these credentials to access admin features:
- **Email**: `admin@smartattendance.com`
- **Password**: `admin123`

⚠️ **Important**: Change the admin password immediately after first login!

### Sample API Calls

#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@smartattendance.com", "password": "admin123"}'
```

#### Get Profile (with auth token)
```bash
curl -X GET "http://localhost:8000/api/auth/profile" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Verify Attendance
```bash
curl -X POST "http://localhost:8000/api/attendance/verify" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -F "student_id=1" \
     -F "session_id=1" \
     -F "face_image=@student_photo.jpg"
```

## 🏗 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database connection and session management
│   ├── models.py               # SQLAlchemy database models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── auth/
│   │   └── routes.py           # Authentication endpoints
│   ├── admin/
│   │   └── routes.py           # Admin management endpoints
│   ├── attendance/
│   │   └── routes.py           # Attendance verification endpoints
│   ├── core/
│   │   ├── config.py           # Application configuration
│   │   └── security.py         # JWT and password utilities
│   └── utils/
│       └── face_recognition_utils.py  # Face recognition utilities
├── database_schema.sql         # Complete PostgreSQL schema
├── new_setup_database.py       # Database initialization script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔐 Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (Admin, Teacher, Student)
- Secure password hashing with bcrypt
- Token expiration and refresh mechanisms

### Data Protection
- Encrypted face encoding storage
- SQL injection prevention through ORM
- Input validation with Pydantic schemas
- CORS protection for web access

### Audit & Monitoring
- Complete audit trail for all user actions
- System configuration change tracking
- Failed authentication attempt logging
- Resource access monitoring

## 🤖 AI Features

### Face Recognition
- Face encoding extraction and storage
- Similarity matching with configurable thresholds
- Liveness detection for anti-spoofing
- Background validation for environment checking

### Intelligent Flagging
- Automatic flagging of low-confidence submissions
- Teacher review workflow for flagged attendance
- Manual approval/rejection system
- Confidence score tracking and analytics

## 📈 Performance Considerations

### Database Optimization
- Strategic indexing for common queries
- Async database operations
- Connection pooling
- Query optimization with SQLAlchemy

### Caching Strategy
- Dashboard data caching
- Configuration settings caching
- Face recognition model caching
- API response caching for static data

### Scalability
- Async FastAPI for high concurrency
- Modular architecture for easy scaling
- Microservice-ready design
- Database connection pooling

## 🚀 Deployment

### Docker Deployment (Recommended)
```bash
# Build the Docker image
docker build -t smart-attendance-backend .

# Run with environment variables
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host/db \
  -e SECRET_KEY=your-secret-key \
  smart-attendance-backend
```

### Production Configuration
```env
DATABASE_URL=postgresql://user:password@prod-db:5432/smart_attendance
SECRET_KEY=your-super-secret-production-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=https://yourdomain.com
FACE_RECOGNITION_THRESHOLD=0.8
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT signing secret | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 1440 (24 hours) |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | localhost |
| `FACE_RECOGNITION_THRESHOLD` | Face matching threshold | 0.6 |

## 🔧 Development

### Code Style
- Follow PEP 8 Python style guide
- Use type hints throughout the codebase
- Implement proper error handling
- Write comprehensive docstrings

### Database Migrations
```bash
# Apply new database schema
python new_setup_database.py

# For production, use proper migration tools
alembic upgrade head
```

### Testing
```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=app

# Integration tests
pytest tests/integration/
```

## 📚 Additional Documentation

- `DATABASE_SCHEMA_UPDATES.md` - Database design and changes
- `COMPLETE_API_DOCUMENTATION.md` - Comprehensive API reference
- `BACKEND_DATA_REQUIREMENTS.md` - Frontend integration requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in this repository
- Review the API documentation at `/docs`
- Open an issue for bug reports or feature requests

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Core authentication system
- ✅ Face recognition attendance
- ✅ Admin management interface
- ✅ Database schema design

### Phase 2 (Planned)
- Advanced analytics and reporting
- Real-time notifications
- Mobile app integration
- Bulk data import/export

### Phase 3 (Future)
- Machine learning improvements
- Multi-camera support
- Integration with LMS systems
- Advanced fraud detection

---

**Built with FastAPI, PostgreSQL, and modern Python async/await patterns for high performance and scalability.**