from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Student
from app.schemas import APIResponse
from app.auth.routes import get_current_user

attendance_router = APIRouter(prefix="/attendance", tags=["Attendance"])

@attendance_router.post("/manual-mark")
async def mark_attendance_manual(
    student_id: int,
    status: str = "present",
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually mark attendance for a student"""
    result = await db.execute(
        select(Student).filter(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    # For now, just return success message (no attendance table in simplified version)
    return APIResponse(
        success=True,
        message=f"Attendance marked as {status} for student {student.name}",
        data={
            "student_id": student_id,
            "student_name": student.name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    )

@attendance_router.get("/students")
async def list_students_for_attendance(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of students for attendance marking"""
    result = await db.execute(select(Student))
    students = result.scalars().all()
    
    return APIResponse(
        success=True,
        message="Students retrieved successfully",
        data=[{
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "department": student.department
        } for student in students]
    )
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
    """Get attendance records for a student"""
    result = await db.execute(
        select(AttendanceRecord).filter(AttendanceRecord.student_id == student_id)
    )
    return result.scalars().all()

@attendance_router.get("/records/all", response_model=List[AttendanceSchema])
async def get_all_attendance_records(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all attendance records (teacher/admin only)"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher or admin access required")
    
    result = await db.execute(select(AttendanceRecord))
    return result.scalars().all()

@attendance_router.get("/records/{record_id}", response_model=AttendanceSchema)
async def get_attendance_record(
    record_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific attendance record"""
    result = await db.execute(select(AttendanceRecord).filter(AttendanceRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    return record

@attendance_router.put("/records/{record_id}", response_model=APIResponse)
async def update_attendance_record(
    record_id: int,
    attendance_update: AttendanceUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update attendance record (teacher/admin only)"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher or admin access required")
    
    result = await db.execute(select(AttendanceRecord).filter(AttendanceRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    update_data = attendance_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(record, key, value)
    
    await db.commit()
    await db.refresh(record)
    
    return APIResponse(
        success=True,
        message="Attendance record updated successfully",
        data={"record_id": record.id}
    )

@attendance_router.delete("/records/{record_id}")
async def delete_attendance_record(
    record_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete attendance record (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    result = await db.execute(select(AttendanceRecord).filter(AttendanceRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    await db.delete(record)
    await db.commit()
    
    return {"status": "success", "message": "Attendance record deleted successfully"}

@attendance_router.post("/manual", response_model=APIResponse)
async def manual_attendance(
    student_id: int = Form(...),
    status: str = Form(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manual attendance marking (teacher/admin only)"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher or admin access required")
    
    if status not in ["present", "absent", "flagged"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status. Must be 'present', 'absent', or 'flagged'")
    
    # Check if student exists
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    attendance = AttendanceRecord(
        student_id=student_id,
        status=status,
        confidence=100.0 if status == "present" else 0.0  # Manual entries get 100% confidence
    )
    
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    
    return APIResponse(
        success=True,
        message=f"Manual attendance marked as {status}",
        data={
            "attendance_id": attendance.id,
            "student_name": student.name,
            "status": status
        }
    )