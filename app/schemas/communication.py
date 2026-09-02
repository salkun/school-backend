from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID


# --- 1. Announcement Schemas ---
class AnnouncementBase(BaseModel):
    title: str = Field(..., example="Libur Hari Raya Idul Fitri")
    content: str = Field(..., example="Diberitahukan kepada seluruh siswa dan guru...")
    priority: str = Field("normal", example="normal") # low, normal, high, urgent
    target_role: str = Field("all", example="all") # all, teacher, student, parent
    school_id: Optional[UUID] = None
    classroom_id: Optional[UUID] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    target_role: Optional[str] = None
    school_id: Optional[UUID] = None
    classroom_id: Optional[UUID] = None

class AnnouncementResponse(AnnouncementBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 2. Media File Schemas ---
class MediaFileResponse(BaseModel):
    id: UUID
    uploaded_by: Optional[UUID] = None
    original_name: str
    stored_path: str
    mime_type: str
    file_size: int
    category: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 3. Activity Log Schemas ---
class ActivityLogResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    activity: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Any] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 4. System Setting Schemas ---
class SystemSettingCreate(BaseModel):
    key: str = Field(..., example="active_academic_year")
    value: str = Field(..., example="2024/2025")

class SystemSettingResponse(SystemSettingCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 5. Profile & Dashboard Schemas ---
class ProfileUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

class DashboardStatsResponse(BaseModel):
    total_students: int
    total_teachers: int
    total_classrooms: int
    total_subjects: int
    total_assignments: int
    total_materials: int
    total_announcements: int
