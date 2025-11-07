from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# User schemas
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

# Student schemas
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

# Teacher schemas
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

# Attendance schemas
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

# Response schemas
class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None