import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================
# 1. ATTENDANCE SESSIONS (Sesi Presensi)
# ==========================================
class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=True) # Null jika absensi harian kelas
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="RESTRICT"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    teaching_schedule_id = Column(UUID(as_uuid=True), ForeignKey("teaching_schedules.id", ondelete="SET NULL"), nullable=True)

    session_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    topic = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    classroom = relationship("Classroom")
    subject = relationship("Subject")
    employee = relationship("Employee")
    academic_year = relationship("AcademicYear")
    semester = relationship("Semester")
    teaching_schedule = relationship("TeachingSchedule")
    records = relationship("AttendanceRecord", back_populates="session", cascade="all, delete-orphan")


# ==========================================
# 2. ATTENDANCE RECORDS (Catatan Kehadiran Siswa)
# ==========================================
class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_session_student_attendance"),
        {'extend_existing': True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("attendance_sessions.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    status = Column(String(20), nullable=False) # present, sick, permit, absent
    remarks = Column(String(255), nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    session = relationship("AttendanceSession", back_populates="records")
    student = relationship("Student")
