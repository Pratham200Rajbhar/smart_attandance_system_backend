Build a simple FastAPI backend with basic CRUD operations and authentication.

Goal:
Implement only essential features:
1. Authentication (JWT login/register/profile)
2. Basic admin management (add/list/update/delete students & teachers)
3. PostgreSQL database schema for core modules
4. Simple manual attendance marking (no face recognition)

Tech Stack:
- FastAPI (Python 3.10+)
- PostgreSQL + SQLAlchemy (async)
- JWT (python-jose)
- bcrypt for password hashing
- python-multipart for form data
- Pydantic for schemas
- CORS middleware enabled

------------------------------------------------------------
📂 Project Structure:
backend/
 ├── app/
 │    ├── main.py
 │    ├── auth/
 │    ├── admin/
 │    ├── attendance/
 │    ├── core/
 │    ├── database.py
 │    ├── models.py
 │    ├── schemas.py
 │    └── utils/
 └── requirements.txt

------------------------------------------------------------
🔐 AUTH MODULE:
Endpoints:
- POST /auth/register → Create user (admin, teacher, student)
- POST /auth/login → Verify credentials, return JWT
- GET /auth/profile → Current logged-in user (from JWT)

Logic:
- bcrypt for password hashing
- JWT tokens valid for 24 hours
- Only admin role can access admin routes
- Table: users(id, name, email, password_hash, role, created_at)

------------------------------------------------------------
🏫 ADMIN MODULE (BASIC CRUD):
Restricted to role="admin" (JWT required)

Student Management:
- POST /admin/students → Add new student
- GET /admin/students → List all students
- GET /admin/students/{id} → Get specific student
- PUT /admin/students/{id} → Update student
- DELETE /admin/students/{id} → Delete student

Teacher Management:
- POST /admin/teachers → Add new teacher
- GET /admin/teachers → List all teachers
- GET /admin/teachers/{id} → Get specific teacher
- PUT /admin/teachers/{id} → Update teacher
- DELETE /admin/teachers/{id} → Delete teacher

Dashboard:
- GET /admin/dashboard/stats → Basic statistics

------------------------------------------------------------
📝 ATTENDANCE MODULE (SIMPLE):
Endpoints:
- POST /attendance/manual-mark → Manually mark student attendance
- GET /attendance/students → Get list of students for attendance

------------------------------------------------------------
🗄 DATABASE SCHEMA (PostgreSQL):

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

------------------------------------------------------------
💡 Implementation Notes:
- Use async SQLAlchemy ORM with `Base.metadata.create_all(engine)`
- Use `python-dotenv` for DB credentials & JWT secret
- Add CORS middleware for frontend integration
- Return clean JSON responses with `success`, `message`, and `data`
- Include routers in main.py:
  ```python
  from app.auth.routes import auth_router
  from app.admin.routes import admin_router
  from app.attendance.routes import attendance_router

  app.include_router(auth_router, prefix="/api")
  app.include_router(admin_router, prefix="/api")
  app.include_router(attendance_router, prefix="/api")
  ```

---

📦 requirements.txt:
fastapi
uvicorn[standard]
sqlalchemy
asyncpg
bcrypt
python-jose[cryptography]
pydantic
pydantic-settings
python-multipart
python-dotenv
passlib
email-validator
psycopg2-binary

---

Expected Output:
A simple, working FastAPI backend with:
✅ JWT-based login/register
✅ Basic CRUD operations for students & teachers
✅ Simple manual attendance marking
✅ PostgreSQL tables ready
✅ Clean, modular code structure
✅ Admin dashboard with basic stats
✅ Tested endpoints via Postman or cURL

Keep it simple, focused on core CRUD functionality, and ready for future enhancements.