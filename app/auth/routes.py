from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, User as UserSchema, Token
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

@auth_router.post("/register")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if user_data.role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password_hash=hashed_password,
        role=user_data.role,
        status=user_data.status or "active"
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

@auth_router.get("/profile", response_model=UserSchema)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserSchema.model_validate(current_user)