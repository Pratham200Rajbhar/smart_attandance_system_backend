from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    face_encoding = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    attendance_records = relationship("AttendanceRecord", back_populates="student")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    
    student = relationship("Student", back_populates="attendance_records")