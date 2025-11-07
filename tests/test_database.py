#!/usr/bin/env python3
"""
Database Connection Test for Smart Attendance System
Tests PostgreSQL connection with credentials: postgres:apple@localhost
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_database_connection():
    """Test database connection and basic operations"""
    try:
        print("🔗 Testing database connection...")
        
        from app.database import AsyncSessionLocal, engine
        from app.models import User, Student, Teacher, AttendanceRecord
        from sqlalchemy.future import select
        
        # Test connection
        async with AsyncSessionLocal() as session:
            try:
                # Test basic query
                result = await session.execute(select(User).limit(1))
                user = result.scalar_one_or_none()
                
                print("✅ Database connection successful!")
                
                # Test table access
                users_result = await session.execute(select(User))
                users = users_result.scalars().all()
                print(f"✅ Users table accessible ({len(users)} records)")
                
                students_result = await session.execute(select(Student))
                students = students_result.scalars().all()
                print(f"✅ Students table accessible ({len(students)} records)")
                
                teachers_result = await session.execute(select(Teacher))
                teachers = teachers_result.scalars().all()
                print(f"✅ Teachers table accessible ({len(teachers)} records)")
                
                attendance_result = await session.execute(select(AttendanceRecord))
                attendance = attendance_result.scalars().all()
                print(f"✅ Attendance records table accessible ({len(attendance)} records)")
                
                # Show sample data
                if users:
                    print("\n👥 Sample Users:")
                    for user in users[:3]:
                        print(f"   - {user.name} ({user.email}) - {user.role}")
                
                if students:
                    print("\n🎓 Sample Students:")
                    for student in students[:3]:
                        face_status = "✅ Face registered" if student.face_encoding else "❌ No face"
                        print(f"   - {student.student_id}: {student.name} ({student.email}) - {face_status}")
                
                if teachers:
                    print("\n👨‍🏫 Sample Teachers:")
                    for teacher in teachers[:3]:
                        dept = teacher.department if teacher.department else "No department"
                        print(f"   - {teacher.name} ({teacher.email}) - {dept}")
                
                return True
                
            except Exception as e:
                print(f"❌ Database query error: {e}")
                return False
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Check if PostgreSQL is running and credentials are correct")
        print("💡 Database: smart_attendance, User: postgres, Password: apple")
        return False

async def test_environment_config():
    """Test environment configuration"""
    try:
        print("\n⚙️  Testing environment configuration...")
        
        from app.core.config import settings
        
        print(f"✅ Database URL: {settings.DATABASE_URL}")
        print(f"✅ JWT Secret Key: {'*' * 20}")
        print(f"✅ CORS Origins: {settings.BACKEND_CORS_ORIGINS}")
        print(f"✅ Face Recognition Threshold: {settings.FACE_RECOGNITION_THRESHOLD}")
        
        # Validate database URL format
        if "postgresql://" in settings.DATABASE_URL and "apple" in settings.DATABASE_URL:
            print("✅ Database URL format is correct")
            return True
        else:
            print("❌ Database URL format is incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def test_auth_functionality():
    """Test authentication functionality"""
    try:
        print("\n🔐 Testing authentication functionality...")
        
        from app.core.security import get_password_hash, verify_password, create_access_token, verify_token
        
        # Test password hashing
        test_password = "test123"
        hashed = get_password_hash(test_password)
        
        if verify_password(test_password, hashed):
            print("✅ Password hashing and verification works")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test JWT token creation and verification
        test_data = {"sub": "test@example.com", "role": "student"}
        token = create_access_token(test_data)
        
        if token and isinstance(token, str):
            print("✅ JWT token creation works")
        else:
            print("❌ JWT token creation failed")
            return False
        
        # Test token verification
        payload = verify_token(token)
        if payload and payload.get("sub") == "test@example.com":
            print("✅ JWT token verification works")
            return True
        else:
            print("❌ JWT token verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Smart Attendance System - Database Connection Test")
    print("=" * 60)
    
    tests = [
        ("Environment Configuration", test_environment_config),
        ("Database Connection", test_database_connection),
        ("Authentication System", test_auth_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        print("-" * 40)
        
        result = await test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your database is ready!")
        print("\n🚀 To start the backend server:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📚 Then visit: http://localhost:8000/docs")
        print("\n👤 Default admin login:")
        print("   Email: admin@smartattendance.com")
        print("   Password: admin123")
    else:
        print("\n❌ Some tests failed. Please check the setup:")
        print("   1. Ensure PostgreSQL is running")
        print("   2. Check database credentials (postgres:apple@localhost)")
        print("   3. Run setup_database.ps1 script")
        print("   4. Verify .env file configuration")

if __name__ == "__main__":
    asyncio.run(main())