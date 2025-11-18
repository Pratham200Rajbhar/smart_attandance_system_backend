from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Student, Teacher, User
from app.schemas import StudentRead, StudentCreate, StudentUpdate, TeacherRead, TeacherCreate, TeacherUpdate, APIResponse
from app.auth.routes import get_admin_user

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

# STUDENT CRUD OPERATIONS
@admin_router.post("/students", response_model=APIResponse)
async def add_student(
    student: StudentCreate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if student_id already exists
    existing_student = await db.execute(
        select(Student).filter(Student.student_id == student.student_id)
    )
    if existing_student.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student ID already exists")
    
    # Check if email already exists
    email_check = await db.execute(
        select(Student).filter(Student.email == student.email)
    )
    if email_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    db_student = Student(
        student_id=student.student_id,
        name=student.name,
        email=student.email,
        department=student.department
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    
    return APIResponse(
        success=True,
        message="Student added successfully",
        data={"student_id": db_student.student_id}
    )

@admin_router.get("/students", response_model=List[StudentRead])
@admin_router.get("/students", response_model=List[StudentRead])
async def list_students(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student))
    return result.scalars().all()

@admin_router.get("/students/{student_id}", response_model=StudentRead)
async def get_student(
    student_id: int,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@admin_router.put("/students/{student_id}", response_model=APIResponse)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    # Check for conflicts if updating unique fields
    update_data = student_update.dict(exclude_unset=True)
    
    if "student_id" in update_data and update_data["student_id"] != student.student_id:
        existing_student_id = await db.execute(
            select(Student).filter(Student.student_id == update_data["student_id"])
        )
        if existing_student_id.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student ID already exists")
    
    if "email" in update_data and update_data["email"] != student.email:
        existing_email = await db.execute(
            select(Student).filter(Student.email == update_data["email"])
        )
        if existing_email.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    for key, value in update_data.items():
        setattr(student, key, value)
    
    await db.commit()
    await db.refresh(student)
    
    return APIResponse(
        success=True,
        message="Student updated successfully",
        data={"student_id": student.student_id}
    )

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

# TEACHER CRUD OPERATIONS
@admin_router.post("/teachers", response_model=APIResponse)
async def add_teacher(
    teacher: TeacherCreate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if email already exists
    email_check = await db.execute(
        select(Teacher).filter(Teacher.email == teacher.email)
    )
    if email_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    db_teacher = Teacher(
        name=teacher.name,
        email=teacher.email,
        department=teacher.department
    )
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    
    return APIResponse(
        success=True,
        message="Teacher added successfully",
        data={"teacher_id": db_teacher.id}
    )

@admin_router.get("/teachers", response_model=List[TeacherRead])
async def list_teachers(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher))
    return result.scalars().all()

@admin_router.get("/teachers/{teacher_id}", response_model=TeacherRead)
async def get_teacher(
    teacher_id: int,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher

@admin_router.put("/teachers/{teacher_id}", response_model=APIResponse)
async def update_teacher(
    teacher_id: int,
    teacher_update: TeacherUpdate,
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    
    # Check for email conflicts if updating email
    update_data = teacher_update.dict(exclude_unset=True)
    
    if "email" in update_data and update_data["email"] != teacher.email:
        existing_email = await db.execute(
            select(Teacher).filter(Teacher.email == update_data["email"])
        )
        if existing_email.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    for key, value in update_data.items():
        setattr(teacher, key, value)
    
    await db.commit()
    await db.refresh(teacher)
    
    return APIResponse(
        success=True,
        message="Teacher updated successfully",
        data={"teacher_id": teacher.id}
    )

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

@admin_router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get basic dashboard statistics"""
    from sqlalchemy import func
    
    # Count total users
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar()
    
    # Count students
    students_result = await db.execute(select(func.count(Student.id)))
    total_students = students_result.scalar()
    
    # Count teachers
    teachers_result = await db.execute(select(func.count(Teacher.id)))
    total_teachers = teachers_result.scalar()
    
    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers
    }