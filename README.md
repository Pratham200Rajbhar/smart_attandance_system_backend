# Simple FastAPI Backend

Minimal FastAPI backend with CRUD operations and JWT authentication.

## Structure
```
app/
├── main.py              # FastAPI app
├── security.py          # JWT & password functions + settings
├── database.py          # Database connection
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── auth/
│   └── routes.py       # Auth endpoints
└── admin/
    └── routes.py       # Admin & attendance endpoints
```

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment
Create `.env`:
```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
```

## Endpoints
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/profile
- GET/POST/PUT/DELETE /api/admin/students
- GET/POST/PUT/DELETE /api/admin/teachers
- GET /api/admin/stats
- GET /api/admin/attendance/students
- POST /api/admin/attendance/mark