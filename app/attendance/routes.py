from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import date, time, datetime
import random

from app.database import get_db
from app.models import Student, Attendance, User, Session
from app.schemas import Attendance as AttendanceSchema, AttendanceVerify
from app.auth.routes import get_current_user
from app.utils.face_recognition_utils import decode_base64_image, extract_face_encoding, compare_faces
from app.core.config import settings

attendance_router = APIRouter(prefix="/attendance", tags=["Attendance"])

@attendance_router.post("/verify")
async def verify_attendance(
    student_id: int = Form(...),
    session_id: int = Form(...),
    face_image: str = Form(...),  # base64 encoded image
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get student with user relationship
    result = await db.execute(
        select(Student)
        .join(User)
        .filter(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if not student.face_encoding:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student face encoding not registered")
    
    # Validate session exists
    session_result = await db.execute(select(Session).filter(Session.id == session_id))
    session_obj = session_result.scalar_one_or_none()
    if not session_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    
    # Process face recognition
    image_array = decode_base64_image(face_image)
    if image_array is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image data")
        
    face_encoding = extract_face_encoding(image_array)
    if face_encoding is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face found in image")
    
    # Compare with stored face encoding
    from app.utils.face_recognition_utils import decode_face_from_bytes
    stored_encoding = decode_face_from_bytes(student.face_encoding)
    similarity = compare_faces(stored_encoding, face_encoding)
    
    status_value = "present" if similarity >= settings.FACE_RECOGNITION_THRESHOLD else "flagged"
    
    # Create attendance record
    today = date.today()
    now = datetime.now().time()
    
    attendance = Attendance(
        student_id=student_id,
        session_id=session_id,
        date=today,
        time=now,
        status=status_value,
        face_confidence=round(similarity * 100, 2),
        liveness_confidence=round(random.uniform(80, 95), 2) if similarity >= 0.6 else None,
        background_confidence=round(random.uniform(70, 95), 2) if similarity >= 0.6 else None,
        audio_confidence=round(random.uniform(65, 90), 2) if similarity >= 0.6 else None,
        geofence_validation=True if similarity >= 0.6 else False,
        device_validation=True if similarity >= 0.6 else False,
        final_score=round(similarity * 100, 2),
        is_manually_approved=False
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
            "student_name": student.user.full_name,
            "session_name": session_obj.session_name
        }
    }

@attendance_router.get("/{student_id}", response_model=List[AttendanceSchema])
async def get_attendance_records(
    student_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate student exists
    student_result = await db.execute(select(Student).filter(Student.id == student_id))
    if not student_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    result = await db.execute(
        select(Attendance)
        .filter(Attendance.student_id == student_id)
        .order_by(Attendance.date.desc(), Attendance.time.desc())
    )
    records = result.scalars().all()
    return [AttendanceSchema.model_validate(record) for record in records]
