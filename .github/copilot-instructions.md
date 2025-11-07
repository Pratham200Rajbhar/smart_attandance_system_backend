You are an expert FastAPI backend developer. 
Create a minimal, production-ready backend API for a Smart Attendance System prototype.

✅ PROJECT GOAL:
Build a FastAPI backend that supports:
1. Authentication (login, JWT)
2. Attendance marking using face recognition (OpenCV + face_recognition library)
3. PostgreSQL database integration
4. Only face-matching logic — NO liveness, NO geofencing, NO audio validation.

⚙️ TECH STACK:
- FastAPI (Python 3.10+)
- PostgreSQL (via SQLAlchemy + async engine)
- JWT authentication (using PyJWT)
- Face recognition via `face_recognition` library (based on dlib)
- Pydantic for request/response schemas
- bcrypt for password hashing
- Dockerfile + requirements.txt for deployment

📂 PROJECT STRUCTURE:
```

backend/
├── app/
│    ├── main.py
│    ├── auth/
│    │    ├── routes.py
│    │    ├── models.py
│    │    ├── schemas.py
│    │    └── service.py
│    ├── attendance/
│    │    ├── routes.py
│    │    ├── models.py
│    │    ├── schemas.py
│    │    └── service.py
│    ├── database.py
│    ├── core/
│    │    ├── security.py
│    │    └── config.py
│    └── utils/
│         └── face_recognition_util.py
└── requirements.txt

````

🧩 FEATURES TO IMPLEMENT:

### 1. Authentication APIs
**Endpoints:**
- `POST /auth/register` → Create new user (for testing)
- `POST /auth/login` → Authenticate user and return JWT
- `GET /auth/profile` → Return current user from JWT

**Logic:**
- Use bcrypt to hash passwords
- Store users in PostgreSQL (`users` table)
- Roles optional but include a `role` column
- Token expires in 24h

---

### 2. Attendance APIs
**Endpoints:**
- `POST /attendance/verify`
    - Accepts `user_id` and a `face_image` (base64 string)
    - Decode image, extract face embedding
    - Compare with stored embedding in DB (`students.face_encoding`)
    - If similarity ≥ 0.6 → mark `PRESENT`
    - Save record to `attendance_records`
- `GET /attendance/{user_id}`
    - Return recent attendance records for that user

**Logic:**
- Use `face_recognition` library for encoding & comparison
- Store embeddings as binary in PostgreSQL
- Create a helper file `face_recognition_util.py` for encoding/matching
- Attendance record schema:
  ```sql
  id SERIAL PRIMARY KEY
  student_id INT REFERENCES students(id)
  timestamp TIMESTAMP DEFAULT NOW()
  status VARCHAR(10)
  confidence FLOAT
````

---

### 3. Database Models

Use SQLAlchemy ORM models for:

* `User` → id, name, email, password_hash, role
* `Student` → id, student_id, name, email, face_encoding
* `AttendanceRecord` → id, student_id, timestamp, status, confidence

Use Alembic migrations (optional) or SQLAlchemy `create_all()` for prototype.

---

### 4. Example `.env` Configuration

```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/smart_attendance
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
```

---

### 5. Sample Workflow

1. Register or seed a student record with stored face embedding.
2. Login → get JWT token.
3. Call `/attendance/verify` with base64 image.
4. If match successful → attendance recorded in DB.
5. Fetch history via `/attendance/{user_id}`.

---

### 6. Requirements File

Include:

```
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
```

---

### 7. Extra Instructions

* Make sure `/attendance/verify` can handle both base64 and multipart file.
* Use `face_recognition.compare_faces()` and `face_recognition.face_distance()`.
* Return JSON responses with `status`, `confidence`, and `message`.
* Add CORS middleware for mobile app connection.
* Keep all code clean, modular, and ready for expansion later.

---

💬 OUTPUT EXPECTATION:
Generate full working code files (FastAPI app, routes, models, schemas, utilities, and example data seeding).
Include minimal Dockerfile and README with setup commands:

```
docker build -t smart-attendance-backend .
docker run -p 8000:8000 smart-attendance-backend
```

```# Smart Attendance System Backend