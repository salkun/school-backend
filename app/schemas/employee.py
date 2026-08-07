from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID

# 1. Schema untuk input (POST / Create)
class EmployeeCreate(BaseModel):
    user_id: Optional[UUID] = None
    school_id: Optional[UUID] = None
    
    full_name: str = Field(..., max_length=100)
    nik: str = Field(..., max_length=16)
    gender: str = Field(..., max_length=20)
    place_of_birth: str = Field(..., max_length=50)
    date_of_birth: date
    mother_maiden_name: str = Field(..., max_length=100)
    
    nip: Optional[str] = None
    niy: Optional[str] = None
    nuptk: Optional[str] = None
    
    employment_status: str = Field(..., example="GTY")
    ptk_type: str = Field(..., example="Guru Mapel")
    appointment_decree: Optional[str] = None
    appointment_start_date: Optional[date] = None
    appointing_institution: Optional[str] = None
    
    cpns_decree: Optional[str] = None
    pns_start_date: Optional[date] = None
    rank_class: Optional[str] = None
    salary_source: Optional[str] = None
    employee_card_number: Optional[str] = None
    
    is_active: bool = True

# 2. Schema untuk update (PUT / Update - Semua opsional)
class EmployeeUpdate(BaseModel):
    user_id: Optional[UUID] = None
    school_id: Optional[UUID] = None
    full_name: Optional[str] = None
    nik: Optional[str] = None
    gender: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_birth: Optional[date] = None
    mother_maiden_name: Optional[str] = None
    nip: Optional[str] = None
    niy: Optional[str] = None
    nuptk: Optional[str] = None
    employment_status: Optional[str] = None
    ptk_type: Optional[str] = None
    appointment_decree: Optional[str] = None
    appointment_start_date: Optional[date] = None
    appointing_institution: Optional[str] = None
    cpns_decree: Optional[str] = None
    pns_start_date: Optional[date] = None
    rank_class: Optional[str] = None
    salary_source: Optional[str] = None
    employee_card_number: Optional[str] = None
    is_active: Optional[bool] = None

# 3. Schema untuk response (GET / Output)
class EmployeeResponse(EmployeeCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)