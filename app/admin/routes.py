from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models import Student, Teacher
from app.schemas import Student as StudentSchema, StudentCreate, Teacher as TeacherSchema, TeacherCreate
from app.auth.routes import get_admin_user
from app.utils.face_recognition_utils import decode_base64_image, extract_face_encoding, encode_face_to_bytes

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/students")
async def add_student(
    student: StudentCreate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.email == student.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    
    return {"status": "success", "message": "Student added successfully", "data": {"student_id": db_student.id}}

@admin_router.post("/students/{student_id}/face")
async def upload_student_face(
    student_id: int,
    face_image: str = Form(...),
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    image_array = decode_base64_image(face_image)
    face_encoding = extract_face_encoding(image_array)
    if face_encoding is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face found in image")
    
    student.face_encoding = encode_face_to_bytes(face_encoding)
    await db.commit()
    
    return {"status": "success", "message": "Face uploaded successfully"}

@admin_router.get("/students", response_model=List[StudentSchema])
async def list_students(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return [StudentSchema.model_validate(student) for student in students]

@admin_router.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    await db.delete(student)
    await db.commit()
    
    return {"status": "success", "message": "Student deleted successfully"}

@admin_router.post("/teachers")
async def add_teacher(
    teacher: TeacherCreate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher).filter(Teacher.email == teacher.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    
    return {"status": "success", "message": "Teacher added successfully", "data": {"teacher_id": db_teacher.id}}

@admin_router.get("/teachers", response_model=List[TeacherSchema])
async def list_teachers(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher))
    teachers = result.scalars().all()
    return [TeacherSchema.model_validate(teacher) for teacher in teachers]

@admin_router.delete("/teachers/{teacher_id}")
async def delete_teacher(
    teacher_id: int,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    
    await db.delete(teacher)
    await db.commit()
    
    return {"status": "success", "message": "Teacher deleted successfully"}