from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.attendance import AttendanceSession, AttendanceRecord
from app.schemas.attendance import (
    AttendanceSessionCreate, AttendanceSessionResponse,
    AttendanceRecordCreate, AttendanceRecordResponse,
    BatchAttendanceRecordsCreate, StudentAttendanceSummary
)
from app.dependencies import get_current_user, require_admin, require_staff, require_all

router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance & Presensi"]
)

# ==========================================
# 1. ATTENDANCE SESSIONS
# ==========================================
@router.post("/sessions/", response_model=AttendanceSessionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_staff)])
def create_attendance_session(data: AttendanceSessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    employee_id = current_user.employee.id if current_user.employee else None
    new_session = AttendanceSession(
        **data.model_dump(),
        employee_id=employee_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/sessions/classroom/{classroom_id}", response_model=List[AttendanceSessionResponse], dependencies=[Depends(require_all)])
def get_classroom_attendance_sessions(classroom_id: UUID, db: Session = Depends(get_db)):
    return db.query(AttendanceSession).filter(AttendanceSession.classroom_id == classroom_id).order_by(AttendanceSession.session_date.desc()).all()

@router.get("/sessions/{session_id}", response_model=AttendanceSessionResponse, dependencies=[Depends(require_all)])
def get_attendance_session_detail(session_id: UUID, db: Session = Depends(get_db)):
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    return session

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_staff)])
def delete_attendance_session(session_id: UUID, db: Session = Depends(get_db)):
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    db.delete(session)
    db.commit()
    return None


# ==========================================
# 2. ATTENDANCE RECORDS (BATCH SAVE & REKAP)
# ==========================================
@router.post("/sessions/{session_id}/records", response_model=List[AttendanceRecordResponse], dependencies=[Depends(require_staff)])
def batch_save_attendance_records(session_id: UUID, payload: BatchAttendanceRecordsCreate, db: Session = Depends(get_db)):
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Attendance session not found")

    saved_records = []
    for rec in payload.records:
        record = db.query(AttendanceRecord).filter(
            AttendanceRecord.session_id == session_id,
            AttendanceRecord.student_id == rec.student_id
        ).first()

        if record:
            record.status = rec.status
            record.remarks = rec.remarks
        else:
            record = AttendanceRecord(
                session_id=session_id,
                student_id=rec.student_id,
                status=rec.status,
                remarks=rec.remarks
            )
            db.add(record)
        saved_records.append(record)

    db.commit()
    for r in saved_records:
        db.refresh(r)
    return saved_records

@router.get("/summary/student/{student_id}", response_model=StudentAttendanceSummary, dependencies=[Depends(require_all)])
def get_student_attendance_summary(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    records = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student_id).all()
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    sick = sum(1 for r in records if r.status == "sick")
    permit = sum(1 for r in records if r.status == "permit")
    absent = sum(1 for r in records if r.status == "absent")
    percentage = (present / total * 100.0) if total > 0 else 0.0

    return StudentAttendanceSummary(
        student_id=student_id,
        total_sessions=total,
        present_count=present,
        sick_count=sick,
        permit_count=permit,
        absent_count=absent,
        attendance_rate_percentage=round(percentage, 2)
    )
