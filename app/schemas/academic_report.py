from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


# --- 1. Report Card Item Schemas ---
class ReportCardItemBase(BaseModel):
    subject_id: UUID
    teacher_id: Optional[UUID] = None
    knowledge_score: Optional[Decimal] = Field(None, example=85.00)
    skill_score: Optional[Decimal] = Field(None, example=88.00)
    final_score: Decimal = Field(..., example=86.50)
    letter_grade: str = Field(..., example="A")
    competency_description: Optional[str] = Field(None, example="Sangat baik dalam memahami konsep aljabar.")

class ReportCardItemCreate(ReportCardItemBase):
    pass

class ReportCardItemResponse(ReportCardItemBase):
    id: UUID
    report_card_id: UUID
    model_config = ConfigDict(from_attributes=True)


# --- 2. Report Card Schemas ---
class ReportCardBase(BaseModel):
    student_id: UUID
    classroom_id: UUID
    academic_year_id: UUID
    semester_id: UUID
    homeroom_teacher_id: Optional[UUID] = None
    sick_count: int = 0
    permitted_count: int = 0
    unexcused_count: int = 0
    homeroom_notes: Optional[str] = Field(None, example="Pertahankan prestasi belajar dan keaktifan di kelas.")
    status: str = Field("draft", example="draft") # draft, locked, published

class ReportCardCreate(ReportCardBase):
    pass

class ReportCardUpdate(BaseModel):
    sick_count: Optional[int] = None
    permitted_count: Optional[int] = None
    unexcused_count: Optional[int] = None
    homeroom_notes: Optional[str] = None
    status: Optional[str] = None
    homeroom_teacher_id: Optional[UUID] = None

class ReportCardResponse(ReportCardBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    items: List[ReportCardItemResponse] = []
    model_config = ConfigDict(from_attributes=True)

class BatchReportCardItemsCreate(BaseModel):
    items: List[ReportCardItemCreate]
