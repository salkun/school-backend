from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date, time
from uuid import UUID


# --- 1. Attendance Record Schemas ---
class AttendanceRecordBase(BaseModel):
    student_id: UUID
    status: str = Field(..., example="present") # present, sick, permit, absent
    remarks: Optional[str] = Field(None, example="Surat dokter terlampir")

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordResponse(AttendanceRecordBase):
    id: UUID
    session_id: UUID
    recorded_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 2. Attendance Session Schemas ---
class AttendanceSessionBase(BaseModel):
    classroom_id: UUID
    subject_id: Optional[UUID] = None
    academic_year_id: UUID
    semester_id: UUID
    teaching_schedule_id: Optional[UUID] = None
    session_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    topic: Optional[str] = Field(None, example="Pertemuan 1: Pengenalan Vektor")

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSessionResponse(AttendanceSessionBase):
    id: UUID
    employee_id: Optional[UUID] = None
    created_at: datetime
    records: List[AttendanceRecordResponse] = []
    model_config = ConfigDict(from_attributes=True)

class BatchAttendanceRecordsCreate(BaseModel):
    records: List[AttendanceRecordCreate]

class StudentAttendanceSummary(BaseModel):
    student_id: UUID
    total_sessions: int
    present_count: int
    sick_count: int
    permit_count: int
    absent_count: int
    attendance_rate_percentage: float
