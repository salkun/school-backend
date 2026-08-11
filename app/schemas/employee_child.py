from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class EmployeeChildCreate(BaseModel):
    employee_id: UUID
    child_name: str = Field(..., max_length=100)
    child_status: str = Field(..., max_length=50, example="Biological")
    gender: str = Field(..., max_length=20, example="Male")
    place_of_birth: str = Field(..., max_length=50)
    date_of_birth: date
    
    education_level: Optional[str] = Field(None, max_length=50, example="SD")
    nisn: Optional[str] = Field(None, max_length=20)
    enrollment_year: Optional[str] = Field(None, max_length=4, example="2024")

class EmployeeChildUpdate(BaseModel):
    child_name: Optional[str] = None
    child_status: Optional[str] = None
    gender: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_birth: Optional[date] = None
    education_level: Optional[str] = None
    nisn: Optional[str] = None
    enrollment_year: Optional[str] = None

class EmployeeChildResponse(EmployeeChildCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)