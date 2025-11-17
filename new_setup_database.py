#!/usr/bin/env python3
"""
Database Setup Script for Smart Attendance System
Creates tables and initial data based on the new schema
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.models import Base, User, SystemConfig, AuditLog
from app.core.security import get_password_hash
from app.core.config import settings
import json
from datetime import datetime

async def create_database():
    """Create database tables"""
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=True
    )
    
    try:
        async with engine.begin() as conn:
            # Drop existing tables (for fresh setup)
            await conn.run_sync(Base.metadata.drop_all)
            print("✓ Dropped existing tables")
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✓ Created new tables")
            
        # Create session for data insertion
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Insert default system configurations
            default_configs = [
                {
                    "config_key": "ai_thresholds",
                    "config_value": {
                        "face_recognition": 85.0,
                        "liveness_detection": 80.0,
                        "background_validation": 75.0,
                        "audio_validation": 70.0
                    },
                    "description": "AI confidence thresholds for attendance validation"
                },
                {
                    "config_key": "attendance_settings",
                    "config_value": {
                        "auto_mark_absent": True,
                        "absent_threshold_minutes": 15,
                        "allow_late_submissions": True,
                        "late_submission_penalty": 5.0
                    },
                    "description": "Attendance system behavior settings"
                },
                {
                    "config_key": "notification_settings",
                    "config_value": {
                        "email_notifications": True,
                        "sms_notifications": False,
                        "push_notifications": True
                    },
                    "description": "Notification delivery preferences"
                },
                {
                    "config_key": "security_settings",
                    "config_value": {
                        "max_login_attempts": 5,
                        "session_timeout_minutes": 1440,
                        "require_2fa": False
                    },
                    "description": "Security and authentication settings"
                }
            ]
            
            for config_data in default_configs:
                config = SystemConfig(**config_data)
                session.add(config)
            
            # Create default admin user
            admin_user = User(
                username="admin",
                full_name="System Administrator",
                email="admin@smartattendance.com",
                password_hash=get_password_hash("admin123"),
                role="admin",
                status="active"
            )
            session.add(admin_user)
            
            await session.commit()
            print("✓ Inserted default configurations and admin user")
            
            # Log the setup
            audit_log = AuditLog(
                user_id=None,
                user_name="System",
                action="database_setup",
                resource="system",
                details={"message": "Database setup completed", "timestamp": datetime.utcnow().isoformat()},
                ip_address="127.0.0.1"
            )
            session.add(audit_log)
            await session.commit()
            
        await engine.dispose()
        print("✓ Database setup completed successfully!")
        print("\nDefault Admin Credentials:")
        print("Email: admin@smartattendance.com")
        print("Password: admin123")
        print("\n⚠️  Please change the admin password after first login!")
        
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        raise

async def check_database_connection():
    """Check if database connection is working"""
    try:
        engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        )
        
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
        
        await engine.dispose()
        print("✓ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your DATABASE_URL in .env file")
        return False

async def main():
    print("🚀 Starting Smart Attendance System Database Setup...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Check connection first
    if not await check_database_connection():
        sys.exit(1)
    
    # Create database schema
    await create_database()
    
    print("\n🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("2. Login with admin credentials")
    print("3. Add teachers and students through the admin interface")

if __name__ == "__main__":
    asyncio.run(main())