from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class EmployeeContactCreate(BaseModel):
    employee_id: UUID
    contact_name: str = Field(..., max_length=100)
    relation: str = Field(..., max_length=50, example="Spouse")
    phone_number: str = Field(..., max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_emergency_contact: bool = True

class EmployeeContactUpdate(BaseModel):
    contact_name: Optional[str] = None
    relation: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_emergency_contact: Optional[bool] = None

class EmployeeContactResponse(EmployeeContactCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)