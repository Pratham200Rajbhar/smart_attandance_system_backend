#!/usr/bin/env python3
import asyncio
import sys
import argparse
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import text, func

from app.database import engine
from app.models import User, Student, Teacher, AttendanceRecord
from app.core.security import get_password_hash

async def create_tables():
    from app.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully")

async def drop_tables():
    from app.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ Tables dropped successfully")

async def reset_database():
    await drop_tables()
    await create_tables()
    print("✅ Database reset successfully")

async def create_admin(name: str, email: str, password: str):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == email))
        if result.scalar_one_or_none():
            print(f"❌ User with email {email} already exists")
            return
        
        admin_user = User(
            name=name,
            email=email,
            password_hash=get_password_hash(password),
            role="admin"
        )
        
        session.add(admin_user)
        await session.commit()
        print(f"✅ Admin user created: {name} ({email})")

async def list_users():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(User).order_by(User.created_at))
        users = result.scalars().all()
        
        if not users:
            print("No users found")
            return
        
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Role':<10} {'Created':<20}")
        print("-" * 90)
        for user in users:
            print(f"{user.id:<5} {user.name:<25} {user.email:<30} {user.role:<10} {user.created_at.strftime('%Y-%m-%d %H:%M'):<20}")

async def list_students():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(Student).order_by(Student.created_at))
        students = result.scalars().all()
        
        if not students:
            print("No students found")
            return
        
        print(f"{'ID':<5} {'Student ID':<12} {'Name':<25} {'Email':<30} {'Face':<8} {'Created':<20}")
        print("-" * 100)
        for student in students:
            face_status = "✅" if student.face_encoding else "❌"
            print(f"{student.id:<5} {student.student_id:<12} {student.name:<25} {student.email:<30} {face_status:<8} {student.created_at.strftime('%Y-%m-%d %H:%M'):<20}")

async def list_teachers():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(Teacher).order_by(Teacher.created_at))
        teachers = result.scalars().all()
        
        if not teachers:
            print("No teachers found")
            return
        
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Department':<20} {'Created':<20}")
        print("-" * 100)
        for teacher in teachers:
            dept = teacher.department or "N/A"
            print(f"{teacher.id:<5} {teacher.name:<25} {teacher.email:<30} {dept:<20} {teacher.created_at.strftime('%Y-%m-%d %H:%M'):<20}")

async def attendance_stats():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        total_result = await session.execute(select(func.count(AttendanceRecord.id)))
        total_records = total_result.scalar()
        
        status_result = await session.execute(
            select(AttendanceRecord.status, func.count(AttendanceRecord.id))
            .group_by(AttendanceRecord.status)
        )
        status_counts = dict(status_result.fetchall())
        
        week_ago = datetime.now() - timedelta(days=7)
        recent_result = await session.execute(
            select(func.count(AttendanceRecord.id))
            .filter(AttendanceRecord.timestamp >= week_ago)
        )
        recent_records = recent_result.scalar()
        
        unique_students_result = await session.execute(
            select(func.count(func.distinct(AttendanceRecord.student_id)))
        )
        unique_students = unique_students_result.scalar()
        
        print("📊 ATTENDANCE STATISTICS")
        print("=" * 50)
        print(f"Total attendance records: {total_records}")
        print(f"Records in last 7 days: {recent_records}")
        print(f"Unique students with attendance: {unique_students}")
        print("\nStatus breakdown:")
        for status, count in status_counts.items():
            percentage = (count / total_records * 100) if total_records > 0 else 0
            print(f"  {status.upper()}: {count} ({percentage:.1f}%)")

async def database_info():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        tables = [
            ("users", User),
            ("students", Student), 
            ("teachers", Teacher),
            ("attendance_records", AttendanceRecord)
        ]
        
        print("📋 DATABASE INFORMATION")
        print("=" * 50)
        print(f"Database URL: {engine.url}")
        print("\nTable counts:")
        
        for table_name, model in tables:
            result = await session.execute(select(func.count(model.id)))
            count = result.scalar()
            print(f"  {table_name}: {count} records")

async def cleanup_old_attendance(days: int = 365):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    async with async_session() as session:
        count_result = await session.execute(
            select(func.count(AttendanceRecord.id))
            .filter(AttendanceRecord.timestamp < cutoff_date)
        )
        count_to_delete = count_result.scalar()
        
        if count_to_delete == 0:
            print(f"No attendance records older than {days} days found")
            return
        
        print(f"Found {count_to_delete} attendance records older than {days} days")
        confirmation = input("Do you want to delete these records? (y/N): ")
        
        if confirmation.lower() != 'y':
            print("Deletion cancelled")
            return
        
        result = await session.execute(
            text("DELETE FROM attendance_records WHERE timestamp < :cutoff_date"),
            {"cutoff_date": cutoff_date}
        )
        await session.commit()
        
        print(f"✅ Deleted {result.rowcount} old attendance records")

def main():
    parser = argparse.ArgumentParser(description="Database Management Utility")
    parser.add_argument("command", choices=[
        "create-tables", "drop-tables", "reset", 
        "create-admin", "list-users", "list-students", "list-teachers",
        "stats", "info", "cleanup"
    ], help="Command to execute")
    
    parser.add_argument("--name", help="Name for admin user creation")
    parser.add_argument("--email", help="Email for admin user creation") 
    parser.add_argument("--password", help="Password for admin user creation")
    parser.add_argument("--days", type=int, default=365, help="Days for cleanup command")
    
    args = parser.parse_args()
    
    async def run_command():
        try:
            if args.command == "create-tables":
                await create_tables()
            elif args.command == "drop-tables":
                await drop_tables()
            elif args.command == "reset":
                await reset_database()
            elif args.command == "create-admin":
                if not all([args.name, args.email, args.password]):
                    print("❌ --name, --email, and --password are required for create-admin")
                    sys.exit(1)
                await create_admin(args.name, args.email, args.password)
            elif args.command == "list-users":
                await list_users()
            elif args.command == "list-students":
                await list_students()
            elif args.command == "list-teachers":
                await list_teachers()
            elif args.command == "stats":
                await attendance_stats()
            elif args.command == "info":
                await database_info()
            elif args.command == "cleanup":
                await cleanup_old_attendance(args.days)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
        finally:
            await engine.dispose()
    
    asyncio.run(run_command())

if __name__ == "__main__":
    main()