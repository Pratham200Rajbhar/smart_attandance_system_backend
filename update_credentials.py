#!/usr/bin/env python3
"""
Update Database Script - Add specific admin and teacher credentials
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

async def update_credentials():
    """Update database with specific admin and teacher credentials"""
    
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
        
        # Hash the new passwords
        admin_password = pwd_context.hash("admin123")
        teacher_password = pwd_context.hash("password123")
        
        # Check if admin exists and update or insert
        existing_admin = await conn.fetchval(
            "SELECT id FROM users WHERE email = $1", 
            "admin@attendance.com"
        )
        
        if existing_admin:
            # Update existing admin
            await conn.execute("""
                UPDATE users 
                SET name = $1, password_hash = $2 
                WHERE email = $3
            """, "Admin User", admin_password, "admin@attendance.com")
            print("🔄 Updated existing admin user")
        else:
            # Insert new admin
            await conn.execute("""
                INSERT INTO users (name, email, password_hash, role) 
                VALUES ($1, $2, $3, $4)
            """, "Admin User", "admin@attendance.com", admin_password, "admin")
            print("➕ Created new admin user")
        
        # Check if teacher exists and update or insert
        existing_teacher_user = await conn.fetchval(
            "SELECT id FROM users WHERE email = $1", 
            "teacher@example.com"
        )
        
        if existing_teacher_user:
            # Update existing teacher user
            await conn.execute("""
                UPDATE users 
                SET name = $1, password_hash = $2 
                WHERE email = $3
            """, "Teacher User", teacher_password, "teacher@example.com")
            print("🔄 Updated existing teacher user")
        else:
            # Insert new teacher user
            await conn.execute("""
                INSERT INTO users (name, email, password_hash, role) 
                VALUES ($1, $2, $3, $4)
            """, "Teacher User", "teacher@example.com", teacher_password, "teacher")
            print("➕ Created new teacher user")
        
        # Check if teacher profile exists in teachers table
        existing_teacher = await conn.fetchval(
            "SELECT id FROM teachers WHERE email = $1", 
            "teacher@example.com"
        )
        
        if existing_teacher:
            # Update existing teacher profile
            await conn.execute("""
                UPDATE teachers 
                SET name = $1, department = $2 
                WHERE email = $3
            """, "Teacher User", "General", "teacher@example.com")
            print("🔄 Updated existing teacher profile")
        else:
            # Insert new teacher profile
            await conn.execute("""
                INSERT INTO teachers (name, email, department) 
                VALUES ($1, $2, $3)
            """, "Teacher User", "teacher@example.com", "General")
            print("➕ Created new teacher profile")
        
        await conn.close()
        
        print("\n✅ Credentials updated successfully!")
        print("\n🔐 Login Credentials:")
        print("   • Admin: admin@attendance.com / admin123")
        print("   • Teacher: teacher@example.com / password123")
        
    except Exception as e:
        print(f"❌ Error updating credentials: {e}")
        raise

async def main():
    """Main function to update credentials"""
    print("🚀 Updating login credentials...")
    await update_credentials()

if __name__ == "__main__":
    asyncio.run(main())