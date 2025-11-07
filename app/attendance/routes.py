from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..auth.routes import get_current_user
from ..auth.models import User
from .schemas import (
    StudentCreate, 
    StudentResponse, 
    StudentWithEncoding,
    AttendanceVerifyRequest, 
    AttendanceVerifyResponse,
    AttendanceHistoryResponse
)
from .service import AttendanceService
import base64
from typing import List

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/students", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new student (requires authentication)."""
    # Check if student already exists
    existing_student = await AttendanceService.get_student_by_student_id(db, student_data.student_id)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already exists"
        )
    
    # Create new student
    student = await AttendanceService.create_student(db, student_data)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create student"
        )
    
    return student

@router.get("/students", response_model=List[StudentWithEncoding])
async def get_all_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all students (requires authentication)."""
    students = await AttendanceService.get_all_students(db)
    
    # Add has_face_encoding field
    students_with_encoding = []
    for student in students:
        student_dict = {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "created_at": student.created_at,
            "has_face_encoding": student.face_encoding is not None
        }
        students_with_encoding.append(student_dict)
    
    return students_with_encoding

@router.post("/students/{student_id}/register-face")
async def register_student_face(
    student_id: int,
    face_image: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Register face encoding for a student."""
    success = await AttendanceService.update_student_face_encoding(db, student_id, face_image)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register face. Make sure the image contains a clear face."
        )
    
    return {"message": "Face registered successfully"}

@router.post("/students/{student_id}/register-face-upload")
async def register_student_face_upload(
    student_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Register face encoding for a student using file upload."""
    # Read file content
    contents = await file.read()
    
    # Convert to base64
    face_image_base64 = base64.b64encode(contents).decode('utf-8')
    
    success = await AttendanceService.update_student_face_encoding(db, student_id, face_image_base64)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register face. Make sure the image contains a clear face."
        )
    
    return {"message": "Face registered successfully"}

@router.post("/verify", response_model=AttendanceVerifyResponse)
async def verify_attendance(
    verify_data: AttendanceVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    """Verify student attendance using face recognition."""
    result = await AttendanceService.verify_attendance(db, verify_data)
    return result

@router.post("/verify-upload/{student_id}")
async def verify_attendance_upload(
    student_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Verify student attendance using file upload."""
    # Read file content
    contents = await file.read()
    
    # Convert to base64
    face_image_base64 = base64.b64encode(contents).decode('utf-8')
    
    # Create verify request
    verify_data = AttendanceVerifyRequest(
        student_id=student_id,
        face_image=face_image_base64
    )
    
    result = await AttendanceService.verify_attendance(db, verify_data)
    return result

@router.get("/{student_id}", response_model=AttendanceHistoryResponse)
async def get_student_attendance(
    student_id: int,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance history for a student (requires authentication)."""
    result = await AttendanceService.get_student_attendance_history(db, student_id, limit)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return result