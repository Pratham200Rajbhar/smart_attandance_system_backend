from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    department: Optional[str] = None

class StudentRead(BaseModel):
    id: int
    student_id: str
    name: str
    email: EmailStr
    department: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    student_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class TeacherRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
