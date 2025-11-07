from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.security import get_password_hash, verify_password, create_access_token
from .models import User
from .schemas import UserCreate, UserLogin
from typing import Optional

class AuthService:
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> Optional[User]:
        try:
            hashed_password = get_password_hash(user_data.password)
            
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=hashed_password,
                role=user_data.role
            )
            
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            
            return db_user
            
        except IntegrityError:
            await db.rollback()
            return None
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if user and verify_password(login_data.password, user.password_hash):
            return user
        
        return None
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    def create_token(user: User) -> str:
        return create_access_token(data={"sub": user.email, "user_id": user.id})