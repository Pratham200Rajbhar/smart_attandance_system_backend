from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import base64

from app.database import get_db
from app.models import Student as StudentModel, Teacher as TeacherModel
from app.schemas import Student, StudentCreate, Teacher, TeacherCreate, ResponseModel
from app.auth.routes import get_admin_user
from app.utils.face_recognition_utils import (
    decode_base64_image,
    extract_face_encoding,
    encode_face_to_bytes
)

router = APIRouter(prefix="/admin", tags=["Admin"])

# Student Management
@router.post("/students", response_model=ResponseModel)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Create a new student (Admin only)"""
    
    # Check if student ID already exists
    result = await db.execute(select(StudentModel).filter(StudentModel.student_id == student_data.student_id))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already exists"
        )
    
    # Check if email already exists
    result = await db.execute(select(StudentModel).filter(StudentModel.email == student_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new student
    db_student = StudentModel(
        student_id=student_data.student_id,
        name=student_data.name,
        email=student_data.email
    )
    
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    
    return ResponseModel(
        status="success",
        message="Student created successfully",
        data={
            "id": db_student.id,
            "student_id": db_student.student_id,
            "name": db_student.name,
            "email": db_student.email
        }
    )

@router.post("/students/{student_id}/face", response_model=ResponseModel)
async def upload_student_face(
    student_id: int,
    face_image: str = Form(...),  # Base64 encoded image
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Upload face encoding for a student (Admin only)"""
    
    # Get student
    result = await db.execute(select(StudentModel).filter(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    try:
        # Process face image
        image_array = decode_base64_image(face_image)
        face_encoding = extract_face_encoding(image_array)
        
        # Store face encoding
        student.face_encoding = encode_face_to_bytes(face_encoding)
        
        await db.commit()
        await db.refresh(student)
        
        return ResponseModel(
            status="success",
            message="Student face encoding uploaded successfully",
            data={
                "student_id": student.id,
                "student_name": student.name
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
            detail=f"Error processing face image: {str(e)}"
        )

@router.post("/students/{student_id}/face-upload", response_model=ResponseModel)
async def upload_student_face_file(
    student_id: int,
    face_image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Upload face encoding for a student using file upload (Admin only)"""
    
    # Validate file type
    if not face_image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Get student
    result = await db.execute(select(StudentModel).filter(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    try:
        # Read and convert file to base64
        content = await face_image.read()
        base64_image = base64.b64encode(content).decode('utf-8')
        
        # Process face image
        image_array = decode_base64_image(base64_image)
        face_encoding = extract_face_encoding(image_array)
        
        # Store face encoding
        student.face_encoding = encode_face_to_bytes(face_encoding)
        
        await db.commit()
        await db.refresh(student)
        
        return ResponseModel(
            status="success",
            message="Student face encoding uploaded successfully",
            data={
                "student_id": student.id,
                "student_name": student.name
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
            detail=f"Error processing face image: {str(e)}"
        )

@router.get("/students", response_model=List[Student])
async def get_students(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Get all students (Admin only)"""
    
    result = await db.execute(select(StudentModel).order_by(StudentModel.created_at.desc()))
    students = result.scalars().all()
    return [Student.model_validate(student) for student in students]

@router.delete("/students/{student_id}", response_model=ResponseModel)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Delete a student (Admin only)"""
    
    result = await db.execute(select(StudentModel).filter(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    await db.delete(student)
    await db.commit()
    
    return ResponseModel(
        status="success",
        message="Student deleted successfully",
        data={"deleted_student_id": student_id}
    )

# Teacher Management
@router.post("/teachers", response_model=ResponseModel)
async def create_teacher(
    teacher_data: TeacherCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Create a new teacher (Admin only)"""
    
    # Check if email already exists
    result = await db.execute(select(TeacherModel).filter(TeacherModel.email == teacher_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new teacher
    db_teacher = TeacherModel(
        name=teacher_data.name,
        email=teacher_data.email,
        department=teacher_data.department
    )
    
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    
    return ResponseModel(
        status="success",
        message="Teacher created successfully",
        data={
            "id": db_teacher.id,
            "name": db_teacher.name,
            "email": db_teacher.email,
            "department": db_teacher.department
        }
    )

@router.get("/teachers", response_model=List[Teacher])
async def get_teachers(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Get all teachers (Admin only)"""
    
    result = await db.execute(select(TeacherModel).order_by(TeacherModel.created_at.desc()))
    teachers = result.scalars().all()
    return [Teacher.model_validate(teacher) for teacher in teachers]

@router.delete("/teachers/{teacher_id}", response_model=ResponseModel)
async def delete_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """Delete a teacher (Admin only)"""
    
    result = await db.execute(select(TeacherModel).filter(TeacherModel.id == teacher_id))
    teacher = result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    await db.delete(teacher)
    await db.commit()
    
    return ResponseModel(
        status="success",
        message="Teacher deleted successfully",
        data={"deleted_teacher_id": teacher_id}
    )