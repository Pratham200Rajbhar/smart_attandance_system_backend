#!/usr/bin/env python3
"""
Database Setup Script for Simple CRUD Backend
This script creates tables and populates them with sample Indian names
"""

import asyncio
import asyncpg
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database connection settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:apple@localhost/smart_attendance")

async def create_database_schema():
    """Create database tables with proper schema"""
    
    # Extract connection details
    connection_parts = DATABASE_URL.replace("postgresql://", "").split("/")
    db_name = connection_parts[-1]
    user_host_port = connection_parts[0].split("@")
    user_pass = user_host_port[0].split(":")
    host_port = user_host_port[1].split(":")
    
    user = user_pass[0]
    password = user_pass[1]
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 5432
    
    print(f"Connecting to PostgreSQL database: {db_name} on {host}:{port}")
    
    try:
        # Connect to database
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=db_name,
            host=host,
            port=port
        )
        
        print("✅ Connected to database successfully!")
        
        # Drop existing tables
        await conn.execute("DROP TABLE IF EXISTS students CASCADE;")
        await conn.execute("DROP TABLE IF EXISTS teachers CASCADE;")
        await conn.execute("DROP TABLE IF EXISTS users CASCADE;")
        print("🗑️  Dropped existing tables")
        
        # Create Users table
        await conn.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Create Students table
        await conn.execute("""
            CREATE TABLE students (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Create Teachers table
        await conn.execute("""
            CREATE TABLE teachers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        print("📊 Created database tables successfully!")
        
        # Create indexes
        indexes = [
            "CREATE INDEX idx_users_email ON users(email);",
            "CREATE INDEX idx_users_role ON users(role);",
            "CREATE INDEX idx_students_student_id ON students(student_id);",
            "CREATE INDEX idx_students_email ON students(email);",
            "CREATE INDEX idx_students_department ON students(department);",
            "CREATE INDEX idx_teachers_email ON teachers(email);",
            "CREATE INDEX idx_teachers_department ON teachers(department);"
        ]
        
        for index in indexes:
            await conn.execute(index)
        
        print("📈 Created database indexes successfully!")
        
        # Insert sample data
        await populate_sample_data(conn)
        
        await conn.close()
        print("✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        raise

async def populate_sample_data(conn):
    """Populate database with sample Indian names"""
    
    # Hash passwords
    admin_password = pwd_context.hash("admin123")
    teacher_password = pwd_context.hash("teacher123")
    student_password = pwd_context.hash("student123")
    
    # Insert admin user
    await conn.execute("""
        INSERT INTO users (name, email, password_hash, role) VALUES 
        ($1, $2, $3, $4)
    """, "Rajesh Kumar", "admin@college.edu", admin_password, "admin")
    
    # Insert teachers
    teachers_data = [
        ("Dr. Priya Sharma", "priya.sharma@college.edu", "Computer Science"),
        ("Prof. Vikram Gupta", "vikram.gupta@college.edu", "Mathematics"),
        ("Dr. Kavita Patel", "kavita.patel@college.edu", "Physics"),
        ("Prof. Arjun Singh", "arjun.singh@college.edu", "Chemistry"),
        ("Dr. Meera Reddy", "meera.reddy@college.edu", "Electronics"),
        ("Prof. Suresh Nair", "suresh.nair@college.edu", "Mechanical Engineering"),
        ("Dr. Deepika Jain", "deepika.jain@college.edu", "Electrical Engineering")
    ]
    
    for name, email, department in teachers_data:
        await conn.execute("""
            INSERT INTO teachers (name, email, department) VALUES ($1, $2, $3)
        """, name, email, department)
        
        await conn.execute("""
            INSERT INTO users (name, email, password_hash, role) VALUES ($1, $2, $3, $4)
        """, name, email, teacher_password, "teacher")
    
    # Insert students
    students_data = [
        ("CS001", "Aarav Agarwal", "aarav.agarwal@student.edu", "Computer Science"),
        ("CS002", "Diya Mehta", "diya.mehta@student.edu", "Computer Science"),
        ("CS003", "Ishaan Joshi", "ishaan.joshi@student.edu", "Computer Science"),
        ("CS004", "Aditi Sharma", "aditi.sharma@student.edu", "Computer Science"),
        ("CS005", "Karan Malhotra", "karan.malhotra@student.edu", "Computer Science"),
        ("MT001", "Ananya Iyer", "ananya.iyer@student.edu", "Mathematics"),
        ("MT002", "Rohan Kapoor", "rohan.kapoor@student.edu", "Mathematics"),
        ("MT003", "Shreya Desai", "shreya.desai@student.edu", "Mathematics"),
        ("PH001", "Sanya Nair", "sanya.nair@student.edu", "Physics"),
        ("PH002", "Vihaan Shah", "vihaan.shah@student.edu", "Physics"),
        ("PH003", "Riya Bhatt", "riya.bhatt@student.edu", "Physics"),
        ("CH001", "Kiara Bansal", "kiara.bansal@student.edu", "Chemistry"),
        ("CH002", "Aryan Verma", "aryan.verma@student.edu", "Chemistry"),
        ("EC001", "Myra Ghosh", "myra.ghosh@student.edu", "Electronics"),
        ("EC002", "Nikhil Rao", "nikhil.rao@student.edu", "Electronics"),
        ("ME001", "Sahil Kumar", "sahil.kumar@student.edu", "Mechanical Engineering"),
        ("ME002", "Tanvi Singh", "tanvi.singh@student.edu", "Mechanical Engineering"),
        ("EE001", "Dev Patel", "dev.patel@student.edu", "Electrical Engineering"),
        ("EE002", "Aisha Khan", "aisha.khan@student.edu", "Electrical Engineering"),
        ("EE003", "Yash Gupta", "yash.gupta@student.edu", "Electrical Engineering")
    ]
    
    for student_id, name, email, department in students_data:
        await conn.execute("""
            INSERT INTO students (student_id, name, email, department) VALUES ($1, $2, $3, $4)
        """, student_id, name, email, department)
        
        await conn.execute("""
            INSERT INTO users (name, email, password_hash, role) VALUES ($1, $2, $3, $4)
        """, name, email, student_password, "student")
    
    print("👥 Populated sample data successfully!")
    
    # Display counts
    user_count = await conn.fetchval("SELECT COUNT(*) FROM users")
    teacher_count = await conn.fetchval("SELECT COUNT(*) FROM teachers")
    student_count = await conn.fetchval("SELECT COUNT(*) FROM students")
    
    print(f"📊 Database Statistics:")
    print(f"   • Users: {user_count}")
    print(f"   • Teachers: {teacher_count}")
    print(f"   • Students: {student_count}")
    
    print(f"\n🔐 Default Login Credentials:")
    print(f"   • Admin: admin@college.edu / admin123")
    print(f"   • Teachers: [teacher_email] / teacher123")
    print(f"   • Students: [student_email] / student123")

async def main():
    """Main function to set up the database"""
    print("🚀 Starting database setup...")
    await create_database_schema()

if __name__ == "__main__":
    asyncio.run(main())