Build a full FastAPI backend for a Smart Attendance System prototype.

Goal:
Implement only working core features:
1. Authentication (JWT login/register/profile)
2. Attendance marking using face recognition
3. Basic admin management (add/list/delete students & teachers)
4. PostgreSQL database schema for all modules

Tech Stack:
- FastAPI (Python 3.10+)
- PostgreSQL + SQLAlchemy (async)
- JWT (python-jose)
- bcrypt for password hashing
- face_recognition + OpenCV for face matching
- python-multipart for image uploads
- Pydantic for schemas
- CORS middleware enabled
- Docker-ready

------------------------------------------------------------
📂 Project Structure:
backend/
 ├── app/
 │    ├── main.py
 │    ├── auth/
 │    ├── attendance/
 │    ├── admin/
 │    ├── core/
 │    ├── database.py
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
🤖 ATTENDANCE MODULE (FACE RECOGNITION):
Endpoints:
- POST /attendance/verify
    → Accepts user_id + face_image (base64 or multipart)
    → Convert to embedding using face_recognition
    → Compare with stored student embedding
    → If similarity ≥ 0.6 → mark PRESENT
    → Else FLAGGED
- GET /attendance/{user_id}
    → Return attendance records

Tables:
- students(id, student_id, name, email, face_encoding, created_at)
- attendance_records(id, student_id, timestamp, status, confidence)

------------------------------------------------------------
🧩 ADMIN MODULE (BASIC CRUD):
Restricted to role="admin" (JWT required)

Endpoints:
- POST /admin/students → Add new student
- GET /admin/students → List students
- DELETE /admin/students/{id} → Delete student
- POST /admin/teachers → Add new teacher
- GET /admin/teachers → List teachers
- DELETE /admin/teachers/{id} → Delete teacher

Models:
- Teacher(id, name, email, department, created_at)
- Student(id, student_id, name, email, face_encoding, created_at)

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
    face_encoding BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE attendance_records (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'flagged', 'absent')),
    confidence FLOAT DEFAULT 0.0
);

------------------------------------------------------------
💡 Implementation Notes:
- Use async SQLAlchemy ORM with `Base.metadata.create_all(engine)`
- Store face encodings as binary (numpy array → .tobytes())
- Decode embeddings using np.frombuffer() when comparing
- Use `face_recognition.face_distance()` for similarity
- Use `python-dotenv` for DB credentials & JWT secret
- Add CORS middleware for frontend/mobile integration
- Return clean JSON responses with `message`, `status`, and `data`
- Include all routers in main.py
  ```python
  from app.auth.routes import router as auth_router
  from app.attendance.routes import router as attendance_router
  from app.admin.routes import router as admin_router

  app.include_router(auth_router)
  app.include_router(attendance_router)
  app.include_router(admin_router)
````

---

📦 requirements.txt:
fastapi
uvicorn
sqlalchemy
asyncpg
bcrypt
python-jose[cryptography]
pydantic
face_recognition
opencv-python
python-multipart
python-dotenv

---

Expected Output:
A fully working FastAPI backend prototype with:
✅ JWT-based login/register
✅ Face recognition attendance marking
✅ Admin CRUD for students & teachers
✅ PostgreSQL tables ready
✅ Modular, extendable code structure
✅ Tested endpoints via Postman or cURL

Keep it clean, modular, and ready for future features like subjects, sessions, and analytics.
```