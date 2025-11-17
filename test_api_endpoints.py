"""
Comprehensive API Endpoint Testing for Smart Attendance System
Run with: pytest test_api_endpoints.py -v
"""

import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, AsyncSessionLocal, engine
from app.models import Base, User, Student, Teacher, Session, Subject, Attendance
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Test data
TEST_ADMIN_EMAIL = "testadmin@test.com"
TEST_ADMIN_PASSWORD = "admin123"
TEST_TEACHER_EMAIL = "testteacher@test.com"
TEST_TEACHER_PASSWORD = "teacher123"
TEST_STUDENT_EMAIL = "teststudent@test.com"
TEST_STUDENT_PASSWORD = "student123"

# Create a simple test image (base64 encoded)
def create_test_image_base64():
    """Create a simple test image and return as base64"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session"""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
async def test_db():
    """Setup test database"""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
async def admin_token(client, test_db):
    """Create admin user and get token"""
    # Register admin
    response = client.post("/api/auth/register", json={
        "username": "testadmin",
        "full_name": "Test Admin",
        "email": TEST_ADMIN_EMAIL,
        "password": TEST_ADMIN_PASSWORD,
        "role": "admin",
        "phone_number": "+911234567890"
    })
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": TEST_ADMIN_EMAIL,
        "password": TEST_ADMIN_PASSWORD
    })
    
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

@pytest.fixture
async def student_user_and_token(client, test_db):
    """Create student user and get token"""
    # Register student
    response = client.post("/api/auth/register", json={
        "username": "teststudent",
        "full_name": "Test Student",
        "email": TEST_STUDENT_EMAIL,
        "password": TEST_STUDENT_PASSWORD,
        "role": "student",
        "phone_number": "+911234567891"
    })
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": TEST_STUDENT_EMAIL,
        "password": TEST_STUDENT_PASSWORD
    })
    
    token = None
    user_id = None
    if response.status_code == 200:
        token = response.json()["access_token"]
        # Get user ID from profile
        profile_response = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        if profile_response.status_code == 200:
            user_id = profile_response.json()["id"]
    
    return user_id, token

class TestHealthCheck:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["status"] == "running"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client, test_db):
        """Test user registration"""
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "full_name": "New User",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "student",
            "phone_number": "+911234567892"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "user_id" in response.json()["data"]
    
    def test_register_duplicate_email(self, client, test_db):
        """Test duplicate email registration"""
        # Register first time
        client.post("/api/auth/register", json={
            "username": "user1",
            "full_name": "User One",
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "student"
        })
        
        # Try to register again with same email
        response = client.post("/api/auth/register", json={
            "username": "user2",
            "full_name": "User Two",
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "student"
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_login_success(self, client, test_db):
        """Test successful login"""
        # Register first
        client.post("/api/auth/register", json={
            "username": "loginuser",
            "full_name": "Login User",
            "email": "login@test.com",
            "password": "password123",
            "role": "student"
        })
        
        # Login
        response = client.post("/api/auth/login", json={
            "email": "login@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_db):
        """Test login with invalid credentials"""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
    
    def test_get_profile(self, client, test_db, admin_token):
        """Test get user profile"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        response = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        assert "email" in response.json()
        assert response.json()["email"] == TEST_ADMIN_EMAIL
    
    def test_get_profile_unauthorized(self, client):
        """Test get profile without token"""
        response = client.get("/api/auth/profile")
        assert response.status_code == 403

class TestAdminEndpoints:
    """Test admin endpoints"""
    
    def test_add_student(self, client, test_db, admin_token, student_user_and_token):
        """Test adding a student"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        user_id, _ = student_user_and_token
        if not user_id:
            pytest.skip("Student user not created")
        
        response = client.post(
            "/api/admin/students",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "user_id": user_id,
                "student_id": "STU001",
                "enrollment_no": "ENR001",
                "department": "Computer Science",
                "semester": 3,
                "section": "A",
                "status": "active"
            }
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_add_student_unauthorized(self, client, test_db, student_user_and_token):
        """Test adding student without admin token"""
        user_id, token = student_user_and_token
        if not user_id:
            pytest.skip("Student user not created")
        
        response = client.post(
            "/api/admin/students",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": user_id,
                "student_id": "STU002",
                "enrollment_no": "ENR002",
                "department": "Computer Science",
                "semester": 3
            }
        )
        assert response.status_code == 403
    
    def test_list_students(self, client, test_db, admin_token):
        """Test listing students"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        response = client.get(
            "/api/admin/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_add_teacher(self, client, test_db, admin_token):
        """Test adding a teacher"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        # Create teacher user first
        client.post("/api/auth/register", json={
            "username": "teacheruser",
            "full_name": "Teacher User",
            "email": TEST_TEACHER_EMAIL,
            "password": TEST_TEACHER_PASSWORD,
            "role": "teacher"
        })
        
        # Get user ID
        login_response = client.post("/api/auth/login", json={
            "email": TEST_TEACHER_EMAIL,
            "password": TEST_TEACHER_PASSWORD
        })
        teacher_token = login_response.json()["access_token"]
        
        profile_response = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        teacher_user_id = profile_response.json()["id"]
        
        # Add teacher
        response = client.post(
            "/api/admin/teachers",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "user_id": teacher_user_id,
                "teacher_id": "TCH001",
                "department": "Computer Science",
                "designation": "Professor",
                "specialization": "Machine Learning"
            }
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_list_teachers(self, client, test_db, admin_token):
        """Test listing teachers"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        response = client.get(
            "/api/admin/teachers",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestAttendanceEndpoints:
    """Test attendance endpoints"""
    
    def test_verify_attendance_no_face_encoding(self, client, test_db, admin_token, student_user_and_token):
        """Test attendance verification without face encoding"""
        if not admin_token:
            pytest.skip("Admin token not available")
        
        user_id, student_token = student_user_and_token
        if not user_id:
            pytest.skip("Student user not created")
        
        # Add student
        client.post(
            "/api/admin/students",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "user_id": user_id,
                "student_id": "STU003",
                "enrollment_no": "ENR003",
                "department": "Computer Science",
                "semester": 3
            }
        )
        
        # Try to verify attendance
        test_image = create_test_image_base64()
        response = client.post(
            "/api/attendance/verify",
            headers={"Authorization": f"Bearer {student_token}"},
            data={
                "student_id": 1,
                "session_id": 1,
                "face_image": test_image
            }
        )
        # Should fail because face encoding not registered
        assert response.status_code in [400, 404]
    
    def test_get_attendance_records(self, client, test_db, student_user_and_token):
        """Test getting attendance records"""
        user_id, token = student_user_and_token
        if not user_id or not token:
            pytest.skip("Student user not created")
        
        response = client.get(
            "/api/attendance/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        # Should return list (even if empty)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

