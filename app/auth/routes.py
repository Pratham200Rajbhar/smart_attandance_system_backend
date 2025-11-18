from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserProfile, Token, UserLogin, UserUpdate
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

async def get_teacher_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher access required")
    return current_user
@auth_router.post("/register")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user_data.role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
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
    return {"status": "success", "message": "User registered successfully", "data": {"user_id": db_user.id}}
@auth_router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")
@auth_router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserProfile.model_validate(current_user)

@auth_router.put("/profile", response_model=UserProfile)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    update_data = user_update.dict(exclude_unset=True)
    
    # Check for email conflicts if updating email
    if "email" in update_data and update_data["email"] != current_user.email:
        existing_email = await get_user_by_email(db, update_data["email"])
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserProfile.model_validate(current_user)

# Admin-only user management endpoints
@auth_router.get("/users", response_model=List[UserProfile])
async def list_users(
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Admin only: List all users"""
    result = await db.execute(select(User))
    return [UserProfile.model_validate(user) for user in result.scalars().all()]

@auth_router.post("/teacher-login", response_model=Token)
async def teacher_login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Teacher-specific login endpoint"""
    user = await get_user_by_email(db, email=user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher access required")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")

@auth_router.post("/admin-login", response_model=Token)
async def admin_login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Admin-specific login endpoint"""
    user = await get_user_by_email(db, email=user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")

@auth_router.get("/users/{user_id}", response_model=UserProfile)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Admin only: Get specific user"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserProfile.model_validate(user)

@auth_router.put("/users/{user_id}", response_model=UserProfile)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Admin only: Update any user"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Check for email conflicts if updating email
    if "email" in update_data and update_data["email"] != user.email:
        existing_email = await get_user_by_email(db, update_data["email"])
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    
    return UserProfile.model_validate(user)

@auth_router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Admin only: Delete user"""
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")
    
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return {"status": "success", "message": "User deleted successfully"}
