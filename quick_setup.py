#!/usr/bin/env python3
"""
Quick Database Setup Script
A simpler alternative for setting up the database
"""

import asyncio
from app.database import Base, engine
from app.models import *  # Import all models
from app.core.security import get_password_hash
import sys

async def quick_setup():
    """Quick database setup - creates tables and admin user"""
    try:
        print("🚀 Quick Database Setup Starting...")
        
        # Create all tables
        async with engine.begin() as conn:
            print("📋 Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")
        
        # Create admin user
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.future import select
        from app.models import User
        
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Check if admin exists
            result = await session.execute(
                select(User).filter(User.email == "admin@smartattendance.com")
            )
            
            if not result.scalar_one_or_none():
                admin_user = User(
                    name="System Administrator",
                    email="admin@smartattendance.com",
                    password_hash=get_password_hash("admin123"),
                    role="admin"
                )
                session.add(admin_user)
                await session.commit()
                print("✅ Admin user created")
                print("   📧 Email: admin@smartattendance.com")
                print("   🔑 Password: admin123")
            else:
                print("✅ Admin user already exists")
        
        print("\n🎉 Setup completed successfully!")
        print("💡 Run: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(quick_setup())