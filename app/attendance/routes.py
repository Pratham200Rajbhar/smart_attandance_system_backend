from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import base64
from datetime import datetime

from app.database import get_db
from app.models import Student as StudentModel, AttendanceRecord as AttendanceModel
from app.schemas import AttendanceRecord, AttendanceVerify, ResponseModel
from app.auth.routes import get_current_user
from app.utils.face_recognition_utils import (
    decode_base64_image, 
    extract_face_encoding, 
    compare_faces, 
    decode_face_from_bytes
)
from app.core.config import settings

router = APIRouter(prefix="/attendance", tags=["Attendance"])

async def get_student_by_id(db: AsyncSession, student_id: int):
    """Get student by ID"""
    result = await db.execute(select(StudentModel).filter(StudentModel.id == student_id))
    return result.scalar_one_or_none()

@router.post("/verify", response_model=ResponseModel)
async def verify_attendance(
    student_id: int = Form(...),
    face_image: str = Form(...),  # Base64 encoded image
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Verify student attendance using face recognition"""
    
    # Get student record
    student = await get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    if not student.face_encoding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student face encoding not found. Please register student face first."
        )
    
    try:
        # Decode and process the uploaded image
        image_array = decode_base64_image(face_image)
        current_encoding = extract_face_encoding(image_array)
        
        # Get stored face encoding
        stored_encoding = decode_face_from_bytes(student.face_encoding)
        
        # Compare faces
        is_match, confidence = compare_faces(
            stored_encoding, 
            current_encoding, 
            settings.FACE_RECOGNITION_THRESHOLD
        )
        
        # Determine attendance status
        attendance_status = "present" if is_match else "flagged"
        
        # Create attendance record
        attendance_record = AttendanceModel(
            student_id=student_id,
            status=attendance_status,
            confidence=confidence,
            timestamp=datetime.utcnow()
        )
        
        db.add(attendance_record)
        await db.commit()
        await db.refresh(attendance_record)
        
        return ResponseModel(
            status="success",
            message=f"Attendance marked as {attendance_status}",
            data={
                "student_id": student_id,
                "student_name": student.name,
                "status": attendance_status,
                "confidence": round(confidence, 2),
                "timestamp": attendance_record.timestamp.isoformat()
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing attendance: {str(e)}"
        )

@router.post("/verify-upload", response_model=ResponseModel)
async def verify_attendance_upload(
    student_id: int = Form(...),
    face_image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Verify student attendance using uploaded image file"""
    
    # Validate file type
    if not face_image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Check file size
    content = await face_image.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large"
        )
    
    # Convert to base64 and use the existing verify endpoint logic
    base64_image = base64.b64encode(content).decode('utf-8')
    
    # Get student record
    student = await get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    if not student.face_encoding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student face encoding not found. Please register student face first."
        )
    
    try:
        # Decode and process the uploaded image
        image_array = decode_base64_image(base64_image)
        current_encoding = extract_face_encoding(image_array)
        
        # Get stored face encoding
        stored_encoding = decode_face_from_bytes(student.face_encoding)
        
        # Compare faces
        is_match, confidence = compare_faces(
            stored_encoding, 
            current_encoding, 
            settings.FACE_RECOGNITION_THRESHOLD
        )
        
        # Determine attendance status
        attendance_status = "present" if is_match else "flagged"
        
        # Create attendance record
        attendance_record = AttendanceModel(
            student_id=student_id,
            status=attendance_status,
            confidence=confidence,
            timestamp=datetime.utcnow()
        )
        
        db.add(attendance_record)
        await db.commit()
        await db.refresh(attendance_record)
        
        return ResponseModel(
            status="success",
            message=f"Attendance marked as {attendance_status}",
            data={
                "student_id": student_id,
                "student_name": student.name,
                "status": attendance_status,
                "confidence": round(confidence, 2),
                "timestamp": attendance_record.timestamp.isoformat()
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing attendance: {str(e)}"
        )

@router.get("/{student_id}", response_model=List[AttendanceRecord])
async def get_student_attendance(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get attendance records for a specific student"""
    
    # Verify student exists
    student = await get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Get attendance records
    result = await db.execute(
        select(AttendanceModel)
        .filter(AttendanceModel.student_id == student_id)
        .order_by(AttendanceModel.timestamp.desc())
    )
    
    attendance_records = result.scalars().all()
    return [AttendanceRecord.model_validate(record) for record in attendance_records]