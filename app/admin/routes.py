from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Student, Teacher, User
from app.schemas import StudentRead, StudentCreate, StudentUpdate, TeacherRead, TeacherCreate, TeacherUpdate
from app.auth.routes import get_admin_user

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

# Students
@admin_router.post("/students")
async def add_student(student: StudentCreate, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    # Check for duplicates
    result = await db.execute(select(Student).filter(
        (Student.student_id == student.student_id) | (Student.email == student.email)
    ))
    if result.scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Student ID or email already exists")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return {"message": "Student added successfully", "id": db_student.id}

@admin_router.get("/students")
async def list_students(_=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()

@admin_router.get("/students/{student_id}")
async def get_student(student_id: int, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    return student

@admin_router.put("/students/{student_id}")
async def update_student(
    student_id: int, 
    student_update: StudentUpdate, 
    _=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    
    update_data = student_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    await db.commit()
    return {"message": "Student updated successfully"}

@admin_router.delete("/students/{student_id}")
async def delete_student(student_id: int, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    
    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted successfully"}

# Teachers
@admin_router.post("/teachers")
async def add_teacher(teacher: TeacherCreate, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Teacher).filter(Teacher.email == teacher.email))
    if result.scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already exists")
    
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    return {"message": "Teacher added successfully", "id": db_teacher.id}

@admin_router.get("/teachers")
async def list_teachers(_=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Teacher))
    return result.scalars().all()

@admin_router.get("/teachers/{teacher_id}")
async def get_teacher(teacher_id: int, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Teacher not found")
    return teacher

@admin_router.put("/teachers/{teacher_id}")
async def update_teacher(
    teacher_id: int, 
    teacher_update: TeacherUpdate, 
    _=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Teacher not found")
    
    update_data = teacher_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)
    
    await db.commit()
    return {"message": "Teacher updated successfully"}

@admin_router.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int, _=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Teacher not found")
    
    await db.delete(teacher)
    await db.commit()
    return {"message": "Teacher deleted successfully"}

@admin_router.get("/stats")
async def get_stats(_=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    users_count = await db.scalar(select(func.count(User.id)))
    students_count = await db.scalar(select(func.count(Student.id)))
    teachers_count = await db.scalar(select(func.count(Teacher.id)))
    
    return {
        "users": users_count,
        "students": students_count,
        "teachers": teachers_count
    }

# Attendance
@admin_router.get("/attendance/students")
async def get_students_attendance(_=Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return [{"id": s.id, "student_id": s.student_id, "name": s.name} for s in students]

@admin_router.post("/attendance/mark")
async def mark_attendance(student_id: int, status: str = "present", _=Depends(get_admin_user)):
    return {"message": f"Attendance marked for student {student_id} as {status}"}