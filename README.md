# Smart Attendance System Backend

A FastAPI backend for Smart Attendance System with face recognition capabilities.

## Features

- **Authentication**: JWT-based authentication with user registration and login
- **Face Recognition**: OpenCV and face_recognition library for attendance verification
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Tech Stack

- FastAPI (Python 3.10+)
- PostgreSQL (via SQLAlchemy + async engine)
- JWT authentication (using PyJWT)
- Face recognition via `face_recognition` library (based on dlib)
- Pydantic for request/response schemas
- bcrypt for password hashing

## Project Structure

```
backend/
├── app/
│    ├── main.py                    # FastAPI application entry point
│    ├── database.py                # Database configuration
│    ├── auth/
│    │    ├── routes.py            # Authentication endpoints
│    │    ├── models.py            # User database models
│    │    ├── schemas.py           # Pydantic schemas for auth
│    │    └── service.py           # Authentication business logic
│    ├── attendance/
│    │    ├── routes.py            # Attendance endpoints
│    │    ├── models.py            # Student/Attendance database models
│    │    ├── schemas.py           # Pydantic schemas for attendance
│    │    └── service.py           # Attendance business logic
│    ├── core/
│    │    ├── security.py          # JWT and password utilities
│    │    └── config.py            # Application configuration
│    └── utils/
│         └── face_recognition_util.py  # Face recognition utilities
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd new_backend
   ```

2. **Set up PostgreSQL Database**
   - Ensure PostgreSQL is installed and running
   - Create a database named `smart_attendance`
   - Set PostgreSQL user `postgres` password to `apple`
   
   **Quick setup using command line:**
   ```bash
   # Create database
   createdb -h localhost -U postgres smart_attendance
   
   # Test connection
   psql -h localhost -U postgres -d smart_attendance -c "SELECT version();"
   ```

3. **Automated Setup (Windows)**
   ```bash
   # Run the setup script (will install dependencies and seed database)
   setup.bat
   ```

4. **Manual Setup**
   
   **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

   **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Seed the database**
   ```bash
   python seed_database.py
   ```

5. **Run the application**
   ```bash
   cd app
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/profile` - Get current user profile (requires JWT)

### Attendance Management

- `POST /attendance/students` - Create a new student (requires JWT)
- `GET /attendance/students` - Get all students (requires JWT)
- `POST /attendance/students/{student_id}/register-face` - Register face encoding for student
- `POST /attendance/students/{student_id}/register-face-upload` - Register face via file upload
- `POST /attendance/verify` - Verify attendance using face recognition
- `POST /attendance/verify-upload/{student_id}` - Verify attendance via file upload
- `GET /attendance/{student_id}` - Get attendance history for student (requires JWT)

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Admin User",
       "email": "admin@example.com",
       "password": "securepassword123",
       "role": "admin"
     }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "securepassword123"
     }'
```

### 3. Create a Student (with JWT token)

```bash
curl -X POST "http://localhost:8000/attendance/students" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "student_id": "STU001",
       "name": "John Doe",
       "email": "john.doe@example.com"
     }'
```

### 4. Register Student Face (file upload)

```bash
curl -X POST "http://localhost:8000/attendance/students/1/register-face-upload" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -F "file=@student_photo.jpg"
```

### 5. Verify Attendance (file upload)

```bash
curl -X POST "http://localhost:8000/attendance/verify-upload/1" \
     -F "file=@attendance_photo.jpg"
```

## Database Models

### User
- id, name, email, password_hash, role, created_at, updated_at

### Student
- id, student_id, name, email, face_encoding, created_at, updated_at

### AttendanceRecord
- id, student_id, timestamp, status, confidence

## Face Recognition

The system uses the `face_recognition` library which provides:
- Face detection in images
- Face encoding extraction (128-dimensional vector)
- Face comparison with configurable tolerance
- Confidence scoring for matches

**Recognition Process:**
1. Extract face encoding from submitted image
2. Compare with stored student face encoding
3. Calculate similarity confidence (0.0 - 1.0)
4. Mark attendance as PRESENT if confidence ≥ 0.6

## Docker Support

### Build Docker Image

```bash
docker build -t smart-attendance-backend .
```

### Run with Docker

```bash
docker run -p 8000:8000 --env-file .env smart-attendance-backend
```

### Docker Compose (with PostgreSQL)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: smart_attendance
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:password@db:5432/smart_attendance
    volumes:
      - .:/app

volumes:
  postgres_data:
```

## Development

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

## Production Deployment

1. **Security Considerations**
   - Change JWT_SECRET to a strong, random secret
   - Use environment variables for sensitive data
   - Enable HTTPS
   - Configure CORS origins properly
   - Use a reverse proxy (nginx)

2. **Database**
   - Use a managed PostgreSQL service
   - Set up database backups
   - Configure connection pooling

3. **Monitoring**
   - Add logging
   - Set up health checks
   - Monitor performance metrics

## Troubleshooting

### Common Issues

1. **Face recognition library installation**
   - Requires cmake and dlib
   - On Windows: Install Visual Studio Build Tools
   - On macOS: `brew install cmake`
   - On Linux: `apt-get install cmake`

2. **Database connection issues**
   - Verify PostgreSQL is running
   - Check database credentials in .env
   - Ensure database exists

3. **Image processing errors**
   - Ensure images contain clear, front-facing faces
   - Supported formats: JPEG, PNG
   - Recommended: well-lit, high-resolution images

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository or contact the development team.