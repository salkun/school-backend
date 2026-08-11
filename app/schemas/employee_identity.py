from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class EmployeeIdentityCreate(BaseModel):
    employee_id: UUID
    street_address: str = Field(..., max_length=255)
    rt: Optional[str] = Field(None, max_length=5)
    rw: Optional[str] = Field(None, max_length=5)
    hamlet: Optional[str] = Field(None, max_length=100)
    village: str = Field(..., max_length=100)
    district: str = Field(..., max_length=100)
    postal_code: Optional[str] = Field(None, max_length=10)
    
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    
    family_card_number: Optional[str] = Field(None, max_length=20)
    religion: str = Field(..., max_length=50)
    citizenship: str = Field("WNI", max_length=50)
    
    marital_status: str = Field(..., max_length=50)
    spouse_name: Optional[str] = Field(None, max_length=100)
    
    tax_number: Optional[str] = Field(None, max_length=30)
    tax_holder_name: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=50)
    bank_account_number: Optional[str] = Field(None, max_length=50)
    
class EmployeeIdentityUpdate(BaseModel):
    street_address: Optional[str] = None
    rt: Optional[str] = None
    rw: Optional[str] = None
    hamlet: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    family_card_number: Optional[str] = None
    religion: Optional[str] = None
    citizenship: Optional[str] = None
    marital_status: Optional[str] = None
    spouse_name: Optional[str] = None
    tax_number: Optional[str] = None
    tax_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None

class EmployeeIdentityResponse(EmployeeIdentityCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)