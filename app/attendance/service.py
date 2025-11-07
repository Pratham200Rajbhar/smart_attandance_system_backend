from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from .models import Student, AttendanceRecord
from .schemas import StudentCreate, AttendanceVerifyRequest
from utils.face_recognition_util import (
    encode_face_from_base64, 
    compare_faces, 
    encoding_to_bytes, 
    bytes_to_encoding
)
from typing import Optional, List
from datetime import datetime
import numpy as np

class AttendanceService:
    
    @staticmethod
    async def create_student(db: AsyncSession, student_data: StudentCreate) -> Optional[Student]:
        try:
            db_student = Student(
                student_id=student_data.student_id,
                name=student_data.name,
                email=student_data.email
            )
            
            db.add(db_student)
            await db.commit()
            await db.refresh(db_student)
            
            return db_student
            
        except IntegrityError:
            await db.rollback()
            return None
    
    @staticmethod
    async def get_student_by_id(db: AsyncSession, student_id: int) -> Optional[Student]:
        result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_student_by_student_id(db: AsyncSession, student_id: str) -> Optional[Student]:
        result = await db.execute(
            select(Student).where(Student.student_id == student_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_student_face_encoding(db: AsyncSession, student_id: int, face_image: str) -> bool:
        try:
            encoding = encode_face_from_base64(face_image)
            if encoding is None:
                return False
            
            student = await AttendanceService.get_student_by_id(db, student_id)
            if not student:
                return False
            
            student.face_encoding = encoding_to_bytes(encoding)
            await db.commit()
            
            return True
            
        except Exception as e:
            await db.rollback()
            print(f"Error updating face encoding: {str(e)}")
            return False
    
    @staticmethod
    async def verify_attendance(db: AsyncSession, verify_data: AttendanceVerifyRequest) -> dict:
        try:
            student = await AttendanceService.get_student_by_id(db, verify_data.student_id)
            if not student:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "message": "Student not found",
                    "timestamp": datetime.utcnow()
                }
            
            if not student.face_encoding:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "message": "Student face encoding not found. Please register face first.",
                    "timestamp": datetime.utcnow()
                }
            
            unknown_encoding = encode_face_from_base64(verify_data.face_image)
            if unknown_encoding is None:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "message": "No face detected in the image",
                    "timestamp": datetime.utcnow()
                }
            
            known_encoding = bytes_to_encoding(student.face_encoding)
            is_match, confidence = compare_faces(known_encoding, unknown_encoding, tolerance=0.6)
            
            status = "PRESENT" if is_match else "ABSENT"
            message = f"Face match successful - confidence: {confidence:.2f}" if is_match else f"Face match failed - confidence: {confidence:.2f}"
            
            attendance_record = AttendanceRecord(
                student_id=student.id,
                status=status,
                confidence=confidence
            )
            
            db.add(attendance_record)
            await db.commit()
            await db.refresh(attendance_record)
            
            return {
                "status": status,
                "confidence": confidence,
                "message": message,
                "timestamp": attendance_record.timestamp
            }
            
        except Exception as e:
            await db.rollback()
            print(f"Error verifying attendance: {str(e)}")
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "message": f"Error processing attendance: {str(e)}",
                "timestamp": datetime.utcnow()
            }
    
    @staticmethod
    async def get_student_attendance_history(db: AsyncSession, student_id: int, limit: int = 50) -> dict:
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.attendance_records))
            .where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()
        
        if not student:
            return None
        
        records = sorted(student.attendance_records, key=lambda x: x.timestamp, reverse=True)[:limit]
        
        return {
            "student": student,
            "records": records
        }
    
    @staticmethod
    async def get_all_students(db: AsyncSession) -> List[Student]:
        result = await db.execute(select(Student))
        return result.scalars().all()