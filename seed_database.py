import asyncio
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, engine, Base
from app.auth.service import AuthService
from app.auth.schemas import UserCreate
from app.attendance.service import AttendanceService
from app.attendance.schemas import StudentCreate

async def seed_database():
    """Seed the database with initial data."""
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        try:
            # Create admin user
            admin_data = UserCreate(
                name="Admin User",
                email="admin@smartattendance.com",
                password="admin123",
                role="admin"
            )
            
            admin_user = await AuthService.create_user(session, admin_data)
            if admin_user:
                print(f"Created admin user: {admin_user.email}")
            else:
                print("Admin user already exists or failed to create")
            
            # Create test user
            user_data = UserCreate(
                name="Test User",
                email="user@smartattendance.com",
                password="user123",
                role="user"
            )
            
            test_user = await AuthService.create_user(session, user_data)
            if test_user:
                print(f"Created test user: {test_user.email}")
            else:
                print("Test user already exists or failed to create")
            
            # Create sample students
            students_data = [
                StudentCreate(
                    student_id="STU001",
                    name="John Doe",
                    email="john.doe@university.com"
                ),
                StudentCreate(
                    student_id="STU002",
                    name="Jane Smith",
                    email="jane.smith@university.com"
                ),
                StudentCreate(
                    student_id="STU003",
                    name="Mike Johnson",
                    email="mike.johnson@university.com"
                ),
                StudentCreate(
                    student_id="STU004",
                    name="Sarah Wilson",
                    email="sarah.wilson@university.com"
                )
            ]
            
            for student_data in students_data:
                student = await AttendanceService.create_student(session, student_data)
                if student:
                    print(f"Created student: {student.name} ({student.student_id})")
                else:
                    print(f"Student {student_data.student_id} already exists or failed to create")
            
            print("\nDatabase seeding completed!")
            print("\nYou can now:")
            print("1. Login as admin: admin@smartattendance.com / admin123")
            print("2. Login as user: user@smartattendance.com / user123")
            print("3. Register face encodings for students")
            print("4. Test attendance verification")
            
        except Exception as e:
            print(f"Error seeding database: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_database())