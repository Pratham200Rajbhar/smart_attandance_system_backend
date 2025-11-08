from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models import Student, AttendanceRecord
from app.schemas import AttendanceRecord as AttendanceSchema, AttendanceVerify
from app.auth.routes import get_current_user
from app.utils.face_recognition_utils import decode_base64_image, extract_face_encoding, compare_faces, decode_face_from_bytes
from app.core.config import settings

attendance_router = APIRouter(prefix="/attendance", tags=["Attendance"])

@attendance_router.post("/verify")
async def verify_attendance(
    student_id: int = Form(...),
    face_image: str = Form(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get student
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if not student.face_encoding:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student face not registered")
    
    image_array = decode_base64_image(face_image)
    face_encoding = extract_face_encoding(image_array)
    if face_encoding is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face found in image")
    
    stored_encoding = decode_face_from_bytes(student.face_encoding)
    similarity = compare_faces(stored_encoding, face_encoding)
    
    status_value = "present" if similarity >= settings.FACE_RECOGNITION_THRESHOLD else "flagged"
    
    attendance = AttendanceRecord(
        student_id=student_id,
        status=status_value,
        confidence=float(similarity)
    )
    
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    
    return {
        "status": "success",
        "message": f"Attendance marked as {status_value}",
        "data": {
            "attendance_id": attendance.id,
            "status": status_value,
            "confidence": similarity,
            "student_name": student.name
        }
    }

@attendance_router.get("/{student_id}", response_model=List[AttendanceSchema])
async def get_attendance_records(
    student_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify student exists
    student_result = await db.execute(select(Student).filter(Student.id == student_id))
    if not student_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    # Get attendance records
    result = await db.execute(
        select(AttendanceRecord)
        .filter(AttendanceRecord.student_id == student_id)
        .order_by(AttendanceRecord.timestamp.desc())
    )
    records = result.scalars().all()
    return [AttendanceSchema.model_validate(record) for record in records]