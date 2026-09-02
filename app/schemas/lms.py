from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


# --- 1. Material Schemas ---
class MaterialBase(BaseModel):
    subject_id: UUID
    title: str = Field(..., example="Pengenalan Aljabar Linier")
    content: Optional[str] = Field(None, example="Catatan dan rangkuman materi...")
    file_path: Optional[str] = Field(None, example="/uploads/materials/aljabar.pdf")
    video_url: Optional[str] = Field(None, example="https://www.youtube.com/watch?v=example")
    classroom_id: Optional[UUID] = None
    academic_year_id: Optional[UUID] = None
    semester_id: Optional[UUID] = None
    is_active: bool = True

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    video_url: Optional[str] = None
    classroom_id: Optional[UUID] = None
    academic_year_id: Optional[UUID] = None
    semester_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class MaterialResponse(MaterialBase):
    id: UUID
    employee_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 2. Material Progress Schemas ---
class MaterialProgressResponse(BaseModel):
    id: UUID
    student_id: UUID
    material_id: UUID
    completed_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 3. Assignment Schemas ---
class AssignmentBase(BaseModel):
    subject_id: UUID
    classroom_id: UUID
    academic_year_id: Optional[UUID] = None
    semester_id: Optional[UUID] = None
    title: str = Field(..., example="Tugas Mandiri 1: Persamaan Kuadrat")
    description: str = Field(..., example="Kerjakan soal 1-5 di buku paket hal 42.")
    type: str = Field("file", example="file") # essay, file, quiz, coding, project
    file_path: Optional[str] = Field(None, example="/uploads/assignments/soal_1.pdf")
    deadline: datetime
    max_score: Decimal = Field(Decimal("100.00"), example=100.00)
    is_active: bool = True

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    file_path: Optional[str] = None
    deadline: Optional[datetime] = None
    max_score: Optional[Decimal] = None
    is_active: Optional[bool] = None

class AssignmentResponse(AssignmentBase):
    id: UUID
    employee_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 4. Grade Schemas ---
class GradeCreate(BaseModel):
    score: Decimal = Field(..., example=85.50)
    feedback: Optional[str] = Field(None, example="Penyelesaian soal no 4 perlu ditinjau kembali.")

class GradeResponse(GradeCreate):
    id: UUID
    submission_id: UUID
    graded_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- 5. Submission Schemas ---
class SubmissionCreate(BaseModel):
    assignment_id: UUID
    content: Optional[str] = Field(None, example="Link Github / Jawaban esai...")
    file_path: Optional[str] = Field(None, example="/uploads/submissions/jawaban_1.pdf")
    status: str = Field("submitted", example="submitted")

class SubmissionHistoryResponse(BaseModel):
    id: UUID
    submission_id: UUID
    status: str
    content: Optional[str]
    file_path: Optional[str]
    comment: Optional[str]
    changed_by: Optional[UUID]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SubmissionResponse(BaseModel):
    id: UUID
    assignment_id: UUID
    student_id: UUID
    content: Optional[str] = None
    file_path: Optional[str] = None
    status: str
    submitted_at: datetime
    created_at: datetime
    updated_at: datetime
    grade: Optional[GradeResponse] = None
    model_config = ConfigDict(from_attributes=True)


# --- 6. Portfolio Schemas ---
class PortfolioCreate(BaseModel):
    title: str = Field(..., example="Aplikasi Web E-Commerce Sederhana")
    description: str = Field(..., example="Karya tugas akhir semester 1 menggunakan React.")
    file_path: Optional[str] = Field(None, example="/uploads/portfolios/demo.png")
    submission_id: Optional[UUID] = None
    status: str = Field("draft", example="draft")

class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    submission_id: Optional[UUID] = None
    status: Optional[str] = None

class PortfolioResponse(PortfolioCreate):
    id: UUID
    student_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
