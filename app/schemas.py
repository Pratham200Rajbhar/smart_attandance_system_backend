from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class AttendanceRecordBase(BaseModel):
    status: str
    confidence: Optional[float] = 0.0

class AttendanceRecord(AttendanceRecordBase):
    id: int
    student_id: int
    timestamp: datetime
    model_config = {"from_attributes": True}

class AttendanceVerify(BaseModel):
    student_id: int