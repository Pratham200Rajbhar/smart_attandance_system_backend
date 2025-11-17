from datetime import datetime, date, time
from typing import Optional, List, Union, Any
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str
    status: Optional[str] = "active"
class UserCreate(UserBase):
    password: str
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[str] = None
class UserProfile(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int = 3600
class StudentBase(BaseModel):
    student_id: str
    enrollment_no: str
    department: str
    semester: int = Field(ge=1, le=8)
    section: Optional[str] = None
    status: Optional[str] = "active"
class StudentCreate(StudentBase):
    user_id: int
class StudentUpdate(BaseModel):
    department: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    section: Optional[str] = None
    status: Optional[str] = None
class Student(StudentBase):
    id: int
    user_id: int
    photo_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user: Optional[User] = None
    class Config:
        from_attributes = True
class StudentWithUser(BaseModel):
    id: int
    student_id: str
    user_id: int
    enrollment_no: str
    full_name: str
    email: str
    phone_number: Optional[str] = None
    department: str
    semester: int
    section: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class TeacherBase(BaseModel):
    teacher_id: str
    department: str
    designation: Optional[str] = None
    specialization: Optional[str] = None
    status: Optional[str] = "active"
class TeacherCreate(TeacherBase):
    user_id: int
class TeacherUpdate(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None
    specialization: Optional[str] = None
    status: Optional[str] = None
class Teacher(TeacherBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[User] = None
    class Config:
        from_attributes = True
class TeacherWithUser(BaseModel):
    id: int
    teacher_id: str
    user_id: int
    full_name: str
    email: str
    phone_number: Optional[str] = None
    department: str
    designation: Optional[str] = None
    specialization: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class SubjectBase(BaseModel):
    subject_code: str
    subject_name: str
    department: str
    semester: int = Field(ge=1, le=8)
    credits: int = 3
    status: Optional[str] = "active"
class SubjectCreate(SubjectBase):
    teacher_id: Optional[int] = None
class SubjectUpdate(BaseModel):
    subject_name: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    credits: Optional[int] = None
    teacher_id: Optional[int] = None
    status: Optional[str] = None
class Subject(SubjectBase):
    id: int
    teacher_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    teacher: Optional[Teacher] = None
    class Config:
        from_attributes = True
class SessionBase(BaseModel):
    session_name: str
    class_room: Optional[str] = None
    start_time: datetime
    end_time: datetime
    status: Optional[str] = "scheduled"
    attendance_enabled: Optional[bool] = True
    max_students: Optional[int] = None
    description: Optional[str] = None
class SessionCreate(SessionBase):
    subject_id: int
    teacher_id: int
    geofence_id: Optional[int] = None
class SessionUpdate(BaseModel):
    session_name: Optional[str] = None
    class_room: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    geofence_id: Optional[int] = None
    status: Optional[str] = None
    attendance_enabled: Optional[bool] = None
    max_students: Optional[int] = None
    description: Optional[str] = None
class Session(SessionBase):
    id: int
    subject_id: int
    teacher_id: int
    geofence_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    subject: Optional[Subject] = None
    teacher: Optional[Teacher] = None
    class Config:
        from_attributes = True
class GeofenceBase(BaseModel):
    zone_name: str
    description: Optional[str] = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius: float = Field(gt=0)
    status: Optional[str] = "active"
class GeofenceCreate(GeofenceBase):
    created_by: Optional[int] = None
class GeofenceUpdate(BaseModel):
    zone_name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None
class Geofence(GeofenceBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class AttendanceBase(BaseModel):
    status: str
    date: date
    time: time
    final_score: Optional[float] = 0.0
    face_confidence: Optional[float] = None
    liveness_confidence: Optional[float] = None
    background_confidence: Optional[float] = None
    audio_confidence: Optional[float] = None
    geofence_validation: bool = False
    device_validation: bool = False
    verification_reason: Optional[str] = None
    is_manually_approved: bool = False
class AttendanceCreate(AttendanceBase):
    student_id: int
    session_id: int
class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    final_score: Optional[float] = None
    face_confidence: Optional[float] = None
    liveness_confidence: Optional[float] = None
    background_confidence: Optional[float] = None
    audio_confidence: Optional[float] = None
    geofence_validation: Optional[bool] = None
    device_validation: Optional[bool] = None
    verified_by: Optional[int] = None
    verification_reason: Optional[str] = None
    is_manually_approved: Optional[bool] = None
class Attendance(AttendanceBase):
    id: int
    student_id: int
    session_id: int
    verified_by: Optional[int] = None
    submission_time: datetime
    created_at: datetime
    updated_at: datetime
    student: Optional[Student] = None
    session: Optional[Session] = None
    class Config:
        from_attributes = True
class AttendanceVerify(BaseModel):
    student_id: int
    session_id: int
    face_image: str
class AttendanceResponse(BaseModel):
    attendance_id: int
    status: str
    confidence_score: float
    face_recognition_score: Optional[float] = None
    liveness_detection_score: Optional[float] = None
    background_validation_score: Optional[float] = None
    geofence_validation: bool
    timestamp: datetime
    message: str
class AttendanceRecord(BaseModel):
    attendance_id: int
    student_id: int
    student_name: str
    student_email: str
    session_id: int
    session_name: str
    subject_name: str
    status: str
    date: date
    time: time
    final_score: float
    face_confidence: Optional[float]
    liveness_confidence: Optional[float]
    background_confidence: Optional[float]
    geofence_validation: bool
    verified_by: Optional[int]
    verification_reason: Optional[str]
    is_manually_approved: bool
    created_at: datetime
class FlaggedAttendance(BaseModel):
    id: int
    attendance_id: int
    student_id: int
    student_name: str
    student_email: str
    status: str
    confidence: float
    timestamp: datetime
    submission_time: datetime
    face_recognition_score: Optional[float]
    liveness_detection_score: Optional[float]
    background_validation_score: Optional[float]
    geofence_validation: bool
    session_name: str
    subject_name: str
    is_manually_approved: bool
class ManualAttendanceOverride(BaseModel):
    attendance_record_id: int
    decision: str
    reason: str
    teacher_id: int
class EnvironmentMetricsBase(BaseModel):
    background_image_path: Optional[str] = None
    audio_clip_path: Optional[str] = None
    device_info: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    browser_fingerprint: Optional[str] = None
    location_data: Optional[dict] = None
class EnvironmentMetricsCreate(EnvironmentMetricsBase):
    attendance_id: int
class EnvironmentMetrics(EnvironmentMetricsBase):
    id: int
    attendance_id: int
    created_at: datetime
    class Config:
        from_attributes = True
class SystemConfigurationBase(BaseModel):
    config_key: str
    config_value: dict
    description: Optional[str] = None
# compatibility alias: some modules expect `SystemConfigBase`
# keep the longer name but provide the short name used below
SystemConfigBase = SystemConfigurationBase
class SystemConfigCreate(SystemConfigBase):
    pass
class SystemConfigUpdate(BaseModel):
    config_value: Optional[dict] = None
    description: Optional[str] = None
class SystemConfig(SystemConfigBase):
    id: int
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class ConfigurationSettings(BaseModel):
    ai_thresholds: dict
    attendance_settings: dict
    notification_settings: dict
    security_settings: dict
class NotificationBase(BaseModel):
    title: str
    message: str
    type: Optional[str] = "info"
    status: Optional[str] = "unread"
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[int] = None
    scheduled_for: Optional[datetime] = None
class NotificationCreate(NotificationBase):
    user_id: int
class NotificationUpdate(BaseModel):
    status: Optional[str] = None
class Notification(NotificationBase):
    id: int
    user_id: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    class Config:
        from_attributes = True
class AuditLogBase(BaseModel):
    action: str
    resource: str
    resource_id: Optional[int] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None
    user_name: Optional[str] = None
class AuditLog(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    timestamp: datetime
    class Config:
        from_attributes = True
class AdminDashboard(BaseModel):
    total_students: int
    total_teachers: int
    total_subjects: int
    total_sessions: int
class TeacherDashboard(BaseModel):
    today_sessions: int
    total_students: int
    flagged_attendance: int
    pending_reviews: int
    subject_performance: List[dict]
    quick_stats: dict
    weekly_attendance: List[int]
    recent_activity: List[dict]
    today_sessions_list: List[dict]
class AttendanceReport(BaseModel):
    summary: dict
    detailed_records: List[dict]
    date_wise_summary: List[dict]
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str
    errors: Optional[List[dict]] = None
class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: List[dict]
