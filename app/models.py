from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Float, Boolean, Date, Time, Text, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, INET
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(15), nullable=True)
    role = Column(String(20), nullable=False)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'teacher', 'student')", name="check_role"),
        CheckConstraint("status IN ('active', 'inactive', 'suspended')", name="check_status"),
    )
    
    # Relationships
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    verified_attendance = relationship("Attendance", foreign_keys="[Attendance.verified_by]", back_populates="verified_by_user")

class Student(Base):
    __tablename__ = "student"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)  # enrollment number
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    enrollment_no = Column(String(50), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String(10), nullable=True)
    face_encoding = Column(LargeBinary, nullable=True)  # binary face encoding data
    photo_path = Column(Text, nullable=True)  # path to student photo
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("semester >= 1 AND semester <= 8", name="check_semester"),
        CheckConstraint("status IN ('active', 'inactive')", name="check_student_status"),
    )
    
    # Relationships
    user = relationship("User", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")

class Teacher(Base):
    __tablename__ = "teacher"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    designation = Column(String(50), nullable=True)
    specialization = Column(String(100), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive')", name="check_teacher_status"),
    )
    
    # Relationships
    user = relationship("User", back_populates="teacher")
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="teacher", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String(20), unique=True, nullable=False, index=True)
    subject_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    credits = Column(Integer, default=3, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("semester >= 1 AND semester <= 8", name="check_subject_semester"),
        CheckConstraint("status IN ('active', 'inactive')", name="check_subject_status"),
    )
    
    # Relationships
    teacher = relationship("Teacher", back_populates="subjects")
    sessions = relationship("Session", back_populates="subject", cascade="all, delete-orphan")

class Geofence(Base):
    __tablename__ = "geofence"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    radius = Column(Numeric(10, 2), nullable=False)  # in meters
    status = Column(String(20), default="active", nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("radius > 0", name="check_radius"),
        CheckConstraint("status IN ('active', 'inactive')", name="check_geofence_status"),
    )
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    sessions = relationship("Session", back_populates="geofence")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id", ondelete="CASCADE"), nullable=False, index=True)
    class_room = Column(String(50), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    geofence_id = Column(Integer, ForeignKey("geofence.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(20), default="scheduled", nullable=False)
    attendance_enabled = Column(Boolean, default=True)
    max_students = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('scheduled', 'ongoing', 'completed', 'cancelled')", name="check_session_status"),
        CheckConstraint("end_time > start_time", name="check_time_order"),
    )
    
    # Relationships
    subject = relationship("Subject", back_populates="sessions")
    teacher = relationship("Teacher", back_populates="sessions")
    geofence = relationship("Geofence", back_populates="sessions")
    attendance_records = relationship("Attendance", back_populates="session", cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    # AI Confidence Scores (0-100)
    final_score = Column(Numeric(5, 2), default=0.0, nullable=False)
    face_confidence = Column(Numeric(5, 2), nullable=True)
    liveness_confidence = Column(Numeric(5, 2), nullable=True)
    background_confidence = Column(Numeric(5, 2), nullable=True)
    audio_confidence = Column(Numeric(5, 2), nullable=True)
    # Validations
    geofence_validation = Column(Boolean, default=False, nullable=False)
    device_validation = Column(Boolean, default=False, nullable=False)
    # Manual Review Fields
    verified_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verification_reason = Column(Text, nullable=True)
    is_manually_approved = Column(Boolean, default=False, nullable=False)
    # Timestamps
    submission_time = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('present', 'absent', 'flagged', 'suspicious', 'pending')", name="check_attendance_status"),
        CheckConstraint("face_confidence IS NULL OR (face_confidence >= 0 AND face_confidence <= 100)", name="check_face_confidence"),
        CheckConstraint("liveness_confidence IS NULL OR (liveness_confidence >= 0 AND liveness_confidence <= 100)", name="check_liveness_confidence"),
        CheckConstraint("background_confidence IS NULL OR (background_confidence >= 0 AND background_confidence <= 100)", name="check_bg_confidence"),
        CheckConstraint("audio_confidence IS NULL OR (audio_confidence >= 0 AND audio_confidence <= 100)", name="check_audio_confidence"),
        CheckConstraint("final_score >= 0 AND final_score <= 100", name="check_final_score"),
    )
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    session = relationship("Session", back_populates="attendance_records")
    verified_by_user = relationship("User", foreign_keys=[verified_by], back_populates="verified_attendance")
    environment_metrics = relationship("EnvironmentMetrics", back_populates="attendance", cascade="all, delete-orphan", uselist=False)

class EnvironmentMetrics(Base):
    __tablename__ = "environment_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    background_image_path = Column(Text, nullable=True)
    audio_clip_path = Column(Text, nullable=True)
    device_info = Column(JSONB, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    browser_fingerprint = Column(Text, nullable=True)
    location_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    attendance = relationship("Attendance", back_populates="environment_metrics")

class SystemConfig(Base):
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(JSONB, nullable=False)
    description = Column(Text, nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    updated_by_user = relationship("User", foreign_keys=[updated_by])

class Notification(Base):
    __tablename__ = "notification"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="info", nullable=False)
    status = Column(String(20), default="unread", nullable=False)
    related_entity_type = Column(String(50), nullable=True)
    related_entity_id = Column(Integer, nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("type IN ('info', 'success', 'warning', 'error')", name="check_notification_type"),
        CheckConstraint("status IN ('unread', 'read', 'archived')", name="check_notification_status"),
    )
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_name = Column(String(100), nullable=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer, nullable=True)
    details = Column(JSONB, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
