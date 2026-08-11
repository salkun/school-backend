from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- 1. Academic Year ---
class AcademicYearCreate(BaseModel):
    start_year: int = Field(..., example=2023)
    end_year: int = Field(..., example=2024)
    is_active: bool = True

class AcademicYearResponse(AcademicYearCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- 2. Semester ---
class SemesterCreate(BaseModel):
    academic_year_id: UUID
    name: str = Field(..., example="Odd") # Odd (Ganjil) / Even (Genap)
    is_active: bool = True

class SemesterResponse(SemesterCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- 3. Building ---
class BuildingCreate(BaseModel):
    name: str = Field(..., example="Gedung Utama A")
    established_year: Optional[int] = Field(None, example=2010)
    area: Optional[float] = Field(None, example=500.5)
    width: Optional[float] = Field(None, example=20.0)
    height: Optional[float] = Field(None, example=15.0)
    is_active: bool = True

class BuildingResponse(BuildingCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- 4. Classroom ---
class ClassroomCreate(BaseModel):
    building_id: UUID
    name: str = Field(..., example="Kelas 10 RPL 1")
    area: Optional[float] = Field(None, example=64.0)
    width: Optional[float] = Field(None, example=8.0)
    height: Optional[float] = Field(None, example=4.0)
    is_active: bool = True

class ClassroomResponse(ClassroomCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- 5. Subject ---
class SubjectCreate(BaseModel):
    name: str = Field(..., example="Matematika Lanjut")
    lesson_hours: int = Field(..., example=4)
    is_active: bool = True

class SubjectResponse(SubjectCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)