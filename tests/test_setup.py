#!/usr/bin/env python3
"""
Test script to validate the Smart Attendance System backend setup
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test core imports
        from app.core.config import settings
        print("✅ Core configuration imported successfully")
        
        from app.core.security import create_access_token, verify_password
        print("✅ Security utilities imported successfully")
        
        from app.database import Base, get_db
        print("✅ Database configuration imported successfully")
        
        from app.models import User, Student, Teacher, AttendanceRecord
        print("✅ Database models imported successfully")
        
        from app.schemas import UserCreate, StudentCreate, TeacherCreate
        print("✅ Pydantic schemas imported successfully")
        
        # Test route imports
        from app.auth.routes import router as auth_router
        print("✅ Auth routes imported successfully")
        
        from app.attendance.routes import router as attendance_router
        print("✅ Attendance routes imported successfully")
        
        from app.admin.routes import router as admin_router
        print("✅ Admin routes imported successfully")
        
        from app.main import app
        print("✅ Main FastAPI app imported successfully")
        
        print("\n🎉 All imports successful! The backend is properly configured.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_face_recognition():
    """Test face recognition dependencies"""
    try:
        print("\nTesting face recognition dependencies...")
        
        import face_recognition
        import cv2
        import numpy as np
        from PIL import Image
        
        print("✅ face_recognition library available")
        print("✅ OpenCV available")
        print("✅ NumPy available")
        print("✅ Pillow available")
        
        # Test face recognition utils
        from app.utils.face_recognition_utils import extract_face_encoding, compare_faces
        print("✅ Face recognition utilities available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Face recognition import error: {e}")
        print("💡 Make sure to install: pip install face-recognition opencv-python")
        return False

async def test_config():
    """Test configuration"""
    try:
        print("\nTesting configuration...")
        
        from app.core.config import settings
        
        print(f"✅ Database URL configured: {settings.DATABASE_URL[:20]}...")
        print(f"✅ JWT configuration: Algorithm={settings.ALGORITHM}")
        print(f"✅ Face recognition threshold: {settings.FACE_RECOGNITION_THRESHOLD}")
        print(f"✅ CORS origins: {settings.BACKEND_CORS_ORIGINS}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Smart Attendance System Backend - Setup Validation\n")
    
    tests = [
        ("Basic Imports", test_imports),
        ("Face Recognition", test_face_recognition),
        ("Configuration", test_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test")
        print('='*50)
        
        result = await test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your backend is ready to run.")
        print("\n🚀 To start the server, run:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📚 API Documentation will be available at:")
        print("   http://localhost:8000/docs")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Create .env file with proper configuration")
        print("   3. Setup PostgreSQL database")

if __name__ == "__main__":
    asyncio.run(main())