from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_, desc, asc
from typing import List, Optional
from datetime import date, datetime, timedelta
from app.database import get_db
from app.models import (
    Teacher, User, Subject, Session, Student, Attendance, 
    Notification, EnvironmentMetrics
)
from app.schemas import (
    TeacherDashboard, Session as SessionSchema, Subject as SubjectSchema,
    AttendanceRecord, FlaggedAttendance, ManualAttendanceOverride,
    AttendanceReport, Notification as NotificationSchema
)
from app.auth.routes import get_current_user

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])

async def get_current_teacher(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current teacher from JWT token"""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Teacher access required"
        )
    
    result = await db.execute(
        select(Teacher).filter(Teacher.user_id == current_user.id)
    )
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    return teacher

@teacher_router.get("/dashboard", response_model=TeacherDashboard)
async def get_teacher_dashboard(
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get teacher's dashboard with statistics and overview"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    # Today's sessions
    today_sessions_result = await db.execute(
        select(func.count(Session.id))
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                func.date(Session.start_time) == today
            )
        )
    )
    today_sessions = today_sessions_result.scalar() or 0
    
    # Total students across all subjects
    total_students_result = await db.execute(
        select(func.count(Student.id.distinct()))
        .join(Attendance, Student.id == Attendance.student_id)
        .join(Session, Attendance.session_id == Session.id)
        .filter(Session.teacher_id == teacher.id)
    )
    total_students = total_students_result.scalar() or 0
    
    # Flagged attendance count
    flagged_result = await db.execute(
        select(func.count(Attendance.id))
        .join(Session, Attendance.session_id == Session.id)
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                Attendance.status == "flagged",
                Attendance.is_manually_approved == False
            )
        )
    )
    flagged_attendance = flagged_result.scalar() or 0
    
    # Subject performance
    subject_performance_result = await db.execute(
        select(
            Subject.subject_name,
            func.count(Session.id).label("total_sessions"),
            func.avg(
                func.case(
                    (Attendance.status == "present", 100.0),
                    else_=0.0
                )
            ).label("attendance_rate"),
            func.count(
                func.case(
                    (Attendance.status == "flagged", 1),
                    else_=None
                )
            ).label("flagged_count")
        )
        .join(Session, Subject.id == Session.subject_id)
        .join(Attendance, Session.id == Attendance.session_id, isouter=True)
        .filter(Subject.teacher_id == teacher.id)
        .group_by(Subject.id, Subject.subject_name)
    )
    subject_performance = []
    for row in subject_performance_result:
        subject_performance.append({
            "subject_name": row.subject_name,
            "total_sessions": row.total_sessions,
            "attendance_rate": round(float(row.attendance_rate or 0), 1),
            "flagged_count": row.flagged_count
        })
    
    # Weekly attendance for chart
    weekly_attendance = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_attendance_result = await db.execute(
            select(
                func.avg(
                    func.case(
                        (Attendance.status == "present", 100.0),
                        else_=0.0
                    )
                )
            )
            .join(Session, Attendance.session_id == Session.id)
            .filter(
                and_(
                    Session.teacher_id == teacher.id,
                    Attendance.date == day
                )
            )
        )
        day_rate = day_attendance_result.scalar() or 0
        weekly_attendance.append(round(float(day_rate), 0))
    
    # Today's sessions list
    today_sessions_list_result = await db.execute(
        select(Session, Subject.subject_name)
        .join(Subject, Session.subject_id == Subject.id)
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                func.date(Session.start_time) == today
            )
        )
        .order_by(Session.start_time)
    )
    
    today_sessions_list = []
    for session, subject_name in today_sessions_list_result:
        # Count registered students for this session
        students_count_result = await db.execute(
            select(func.count(Attendance.student_id.distinct()))
            .filter(Attendance.session_id == session.id)
        )
        students_registered = students_count_result.scalar() or 0
        
        today_sessions_list.append({
            "session_id": session.id,
            "session_name": f"{subject_name} - {session.session_name}",
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat(),
            "class_room": session.class_room,
            "status": session.status,
            "students_registered": students_registered
        })
    
    return TeacherDashboard(
        today_sessions=today_sessions,
        total_students=total_students,
        flagged_attendance=flagged_attendance,
        pending_reviews=flagged_attendance,  # Same as flagged for now
        subject_performance=subject_performance,
        quick_stats={
            "total_sessions_this_week": len(today_sessions_list),
            "average_attendance": sum(weekly_attendance) / 7 if weekly_attendance else 0,
            "students_present_today": 0  # Placeholder
        },
        weekly_attendance=weekly_attendance,
        recent_activity=[],  # Placeholder for now
        today_sessions_list=today_sessions_list
    )

@teacher_router.get("/sessions")
async def get_teacher_sessions(
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get all sessions for the current teacher"""
    result = await db.execute(
        select(Session, Subject.subject_name)
        .join(Subject, Session.subject_id == Subject.id)
        .filter(Session.teacher_id == teacher.id)
        .order_by(desc(Session.start_time))
    )
    
    sessions = []
    for session, subject_name in result:
        # Count registered students
        students_result = await db.execute(
            select(func.count(Attendance.student_id.distinct()))
            .filter(Attendance.session_id == session.id)
        )
        students_registered = students_result.scalar() or 0
        
        # Count attendance
        attendance_result = await db.execute(
            select(func.count(Attendance.id))
            .filter(
                and_(
                    Attendance.session_id == session.id,
                    Attendance.status == "present"
                )
            )
        )
        attendance_count = attendance_result.scalar() or 0
        
        sessions.append({
            "id": session.id,
            "session_name": session.session_name,
            "subject_name": subject_name,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat(),
            "class_room": session.class_room,
            "status": session.status,
            "students_registered": students_registered,
            "attendance_count": attendance_count
        })
    
    return sessions

@teacher_router.get("/subjects", response_model=List[SubjectSchema])
async def get_teacher_subjects(
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get all subjects assigned to the current teacher"""
    result = await db.execute(
        select(Subject)
        .filter(Subject.teacher_id == teacher.id)
        .order_by(Subject.subject_name)
    )
    
    subjects = result.scalars().all()
    return [SubjectSchema.model_validate(subject) for subject in subjects]

@teacher_router.get("/sessions/{session_id}")
async def get_session_details(
    session_id: int,
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific session"""
    result = await db.execute(
        select(Session, Subject.subject_name)
        .join(Subject, Session.subject_id == Subject.id)
        .filter(
            and_(
                Session.id == session_id,
                Session.teacher_id == teacher.id
            )
        )
    )
    
    session_data = result.first()
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session, subject_name = session_data
    
    # Get attendance summary
    summary_result = await db.execute(
        select(
            Attendance.status,
            func.count(Attendance.id).label("count")
        )
        .filter(Attendance.session_id == session_id)
        .group_by(Attendance.status)
    )
    
    attendance_summary = {"present": 0, "absent": 0, "flagged": 0}
    for row in summary_result:
        if row.status in attendance_summary:
            attendance_summary[row.status] = row.count
    
    # Count total registered students
    total_result = await db.execute(
        select(func.count(Attendance.student_id.distinct()))
        .filter(Attendance.session_id == session_id)
    )
    students_registered = total_result.scalar() or 0
    
    return {
        "id": session.id,
        "session_name": session.session_name,
        "subject_name": subject_name,
        "start_time": session.start_time.isoformat(),
        "end_time": session.end_time.isoformat(),
        "class_room": session.class_room,
        "status": session.status,
        "students_registered": students_registered,
        "attendance_summary": attendance_summary
    }

@teacher_router.get("/sessions/{session_id}/attendance")
async def get_session_attendance(
    session_id: int,
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance records for a specific session"""
    # Verify session belongs to teacher
    session_check = await db.execute(
        select(Session).filter(
            and_(
                Session.id == session_id,
                Session.teacher_id == teacher.id
            )
        )
    )
    
    if not session_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    result = await db.execute(
        select(Attendance, Student.enrollment_no, User.full_name)
        .join(Student, Attendance.student_id == Student.id)
        .join(User, Student.user_id == User.id)
        .filter(Attendance.session_id == session_id)
        .order_by(User.full_name)
    )
    
    attendance_records = []
    for attendance, enrollment_no, full_name in result:
        attendance_records.append({
            "id": attendance.id,
            "student_id": attendance.student_id,
            "student_name": full_name,
            "enrollment_no": enrollment_no,
            "status": attendance.status,
            "confidence": float(attendance.face_confidence or 0),
            "timestamp": attendance.submission_time.isoformat(),
            "verification_method": "face_recognition"
        })
    
    return attendance_records

@teacher_router.get("/attendance/flagged")
async def get_flagged_attendance(
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get all flagged attendance records for teacher's sessions"""
    result = await db.execute(
        select(
            Attendance, 
            Student.id.label("student_id"),
            User.full_name,
            Session.session_name,
            Subject.subject_name
        )
        .join(Student, Attendance.student_id == Student.id)
        .join(User, Student.user_id == User.id)
        .join(Session, Attendance.session_id == Session.id)
        .join(Subject, Session.subject_id == Subject.id)
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                Attendance.status == "flagged",
                Attendance.is_manually_approved == False
            )
        )
        .order_by(desc(Attendance.submission_time))
    )
    
    flagged_records = []
    for attendance, student_id, full_name, session_name, subject_name in result:
        flagged_records.append({
            "id": attendance.id,
            "student_id": student_id,
            "student_name": full_name,
            "session_name": f"{subject_name} - {session_name}",
            "status": attendance.status,
            "confidence": float(attendance.face_confidence or 0),
            "timestamp": attendance.submission_time.isoformat(),
            "reason": "Low confidence score" if attendance.face_confidence and attendance.face_confidence < 60 else "Manual review required"
        })
    
    return flagged_records

@teacher_router.post("/attendance/manual")
async def create_manual_attendance(
    request: dict,
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Create manual attendance record"""
    student_id = request.get("student_id")
    session_id = request.get("session_id")
    attendance_status = request.get("status", "present")
    reason = request.get("reason", "Manual entry by teacher")
    
    # Verify session belongs to teacher
    session_check = await db.execute(
        select(Session).filter(
            and_(
                Session.id == session_id,
                Session.teacher_id == teacher.id
            )
        )
    )
    
    if not session_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify attendance for this session"
        )
    
    # Check if attendance already exists
    existing_attendance = await db.execute(
        select(Attendance).filter(
            and_(
                Attendance.student_id == student_id,
                Attendance.session_id == session_id
            )
        )
    )
    
    existing = existing_attendance.scalar_one_or_none()
    
    today = date.today()
    now = datetime.now().time()
    
    if existing:
        # Update existing record
        existing.status = attendance_status
        existing.verification_reason = reason
        existing.is_manually_approved = True
        existing.verified_by = teacher.user_id
        await db.commit()
        attendance_id = existing.id
    else:
        # Create new record
        new_attendance = Attendance(
            student_id=student_id,
            session_id=session_id,
            status=attendance_status,
            date=today,
            time=now,
            final_score=100.0 if attendance_status == "present" else 0.0,
            verification_reason=reason,
            is_manually_approved=True,
            verified_by=teacher.user_id
        )
        db.add(new_attendance)
        await db.commit()
        await db.refresh(new_attendance)
        attendance_id = new_attendance.id
    
    return {
        "status": "success",
        "message": f"Manual attendance recorded as {attendance_status}",
        "data": {"attendance_id": attendance_id}
    }

@teacher_router.put("/attendance/{attendance_id}/review")
async def review_flagged_attendance(
    attendance_id: int,
    request: dict,
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Approve or reject flagged attendance"""
    decision = request.get("decision")  # "approved" or "rejected"
    reason = request.get("reason", "")
    
    # Get attendance record and verify it belongs to teacher's session
    result = await db.execute(
        select(Attendance, Session)
        .join(Session, Attendance.session_id == Session.id)
        .filter(
            and_(
                Attendance.id == attendance_id,
                Session.teacher_id == teacher.id,
                Attendance.status == "flagged"
            )
        )
    )
    
    attendance_data = result.first()
    if not attendance_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flagged attendance record not found"
        )
    
    attendance, session = attendance_data
    
    # Update attendance based on decision
    if decision == "approved":
        attendance.status = "present"
        attendance.is_manually_approved = True
    elif decision == "rejected":
        attendance.status = "absent"
        attendance.is_manually_approved = True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision must be 'approved' or 'rejected'"
        )
    
    attendance.verified_by = teacher.user_id
    attendance.verification_reason = reason
    
    await db.commit()
    
    return {
        "status": "success",
        "message": f"Attendance {decision} successfully",
        "data": {
            "attendance_id": attendance_id,
            "new_status": attendance.status
        }
    }

@teacher_router.get("/reports/attendance")
async def get_attendance_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    teacher: Teacher = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Generate attendance report for teacher's sessions"""
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Summary statistics
    summary_result = await db.execute(
        select(
            func.count(Session.id.distinct()).label("total_sessions"),
            func.avg(
                func.case(
                    (Attendance.status == "present", 100.0),
                    else_=0.0
                )
            ).label("average_attendance"),
            func.count(
                func.case(
                    (Attendance.status == "present", 1),
                    else_=None
                )
            ).label("total_present"),
            func.count(
                func.case(
                    (Attendance.status == "flagged", 1),
                    else_=None
                )
            ).label("total_flagged")
        )
        .join(Attendance, Session.id == Attendance.session_id, isouter=True)
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        )
    )
    
    summary = summary_result.first()
    
    # Detailed records by date
    detailed_result = await db.execute(
        select(
            Attendance.date,
            Session.session_name,
            Subject.subject_name,
            func.count(Attendance.id.distinct()).label("total_students"),
            func.count(
                func.case(
                    (Attendance.status == "present", 1),
                    else_=None
                )
            ).label("present"),
            func.count(
                func.case(
                    (Attendance.status == "absent", 1),
                    else_=None
                )
            ).label("absent"),
            func.count(
                func.case(
                    (Attendance.status == "flagged", 1),
                    else_=None
                )
            ).label("flagged")
        )
        .join(Session, Attendance.session_id == Session.id)
        .join(Subject, Session.subject_id == Subject.id)
        .filter(
            and_(
                Session.teacher_id == teacher.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        )
        .group_by(Attendance.date, Session.session_name, Subject.subject_name)
        .order_by(desc(Attendance.date))
    )
    
    detailed_records = []
    for row in detailed_result:
        attendance_percentage = (row.present / row.total_students * 100) if row.total_students > 0 else 0
        detailed_records.append({
            "date": row.date.isoformat(),
            "session_name": f"{row.subject_name} - {row.session_name}",
            "total_students": row.total_students,
            "present": row.present,
            "absent": row.absent,
            "flagged": row.flagged,
            "attendance_percentage": round(attendance_percentage, 1)
        })
    
    return {
        "summary": {
            "total_sessions": summary.total_sessions or 0,
            "average_attendance": round(float(summary.average_attendance or 0), 1),
            "total_present": summary.total_present or 0,
            "total_flagged": summary.total_flagged or 0,
            "date_range": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        },
        "detailed_records": detailed_records
    }