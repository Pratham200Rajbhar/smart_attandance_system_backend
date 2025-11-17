from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Student, Teacher, User
from app.schemas import Student as StudentSchema, StudentCreate, Teacher as TeacherSchema, TeacherCreate
from app.auth.routes import get_admin_user
from app.utils.face_recognition_utils import decode_base64_image, extract_face_encoding, encode_face_to_bytes
from app.core.security import get_password_hash
admin_router = APIRouter(prefix="/admin", tags=["Admin"])
@admin_router.post("/students")
async def add_student(
    student: StudentCreate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(select(User).filter(User.id == student.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    existing_student = await db.execute(
        select(Student).filter(Student.user_id == student.user_id)
    )
    if existing_student.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists for this user")
    enrollment_check = await db.execute(
        select(Student).filter(Student.enrollment_no == student.enrollment_no)
    )
    if enrollment_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enrollment number already exists")
    db_student = Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return {"status": "success", "message": "Student added successfully", "data": {"student_id": db_student.student_id}}
@admin_router.post("/students/{student_id}/photo")
async def upload_student_photo(
    student_id: int,
    photo: str = Form(...),
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    image_array = decode_base64_image(photo)
    from io import BytesIO
    from PIL import Image
    import base64
    if photo.startswith('data:'):
        photo = photo.split(',', 1)[1]
    photo_bytes = base64.b64decode(photo)
    face_encoding = extract_face_encoding(image_array)
    if face_encoding is not None:
        student.face_encoding = encode_face_to_bytes(face_encoding)
    student.photo_path = f"photos/student_{student_id}.jpg"
    await db.commit()
    return {"status": "success", "message": "Photo uploaded successfully"}
@admin_router.get("/students")
async def list_students(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Student, User.full_name)
        .join(User, Student.user_id == User.id)
    )
    students_with_names = result.all()
    return [
        {
            "id": s.id,
            "student_id": s.student_id,
            "user_id": s.user_id,
            "full_name": full_name,
            "enrollment_no": s.enrollment_no,
            "department": s.department,
            "semester": s.semester,
            "section": s.section,
            "photo_path": s.photo_path,
            "status": s.status or "active",
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None
        }
        for s, full_name in students_with_names
    ]
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
    user_result = await db.execute(select(User).filter(User.id == teacher.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    existing_teacher = await db.execute(
        select(Teacher).filter(Teacher.user_id == teacher.user_id)
    )
    if existing_teacher.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher already exists for this user")
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    return {"status": "success", "message": "Teacher added successfully", "data": {"teacher_id": db_teacher.teacher_id}}
@admin_router.get("/teachers")
async def list_teachers(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Teacher, User.full_name)
        .join(User, Teacher.user_id == User.id)
    )
    teachers_with_names = result.all()
    return [
        {
            "id": t.id,
            "teacher_id": t.teacher_id,
            "user_id": t.user_id,
            "full_name": full_name,
            "department": t.department,
            "designation": t.designation,
            "specialization": t.specialization,
            "status": t.status or "active",
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "updated_at": t.updated_at.isoformat() if t.updated_at else None
        }
        for t, full_name in teachers_with_names
    ]
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
