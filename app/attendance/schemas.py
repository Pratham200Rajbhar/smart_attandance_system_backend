from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    student_id: str
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentWithEncoding(StudentResponse):
    has_face_encoding: bool

class AttendanceVerifyRequest(BaseModel):
    student_id: int
    face_image: str  # Base64 encoded image

class AttendanceVerifyResponse(BaseModel):
    status: str
    confidence: float
    message: str
    timestamp: datetime

class AttendanceRecordResponse(BaseModel):
    id: int
    student_id: int
    timestamp: datetime
    status: str
    confidence: Optional[float]
    
    class Config:
        from_attributes = True

class AttendanceHistoryResponse(BaseModel):
    student: StudentResponse
    records: List[AttendanceRecordResponse]