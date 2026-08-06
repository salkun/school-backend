from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID

# --- Student Identity Schemas ---
class StudentIdentityCreate(BaseModel):
    gender: str
    religion: str
    family_card_number: str
    place_of_birth: str
    date_of_birth: date
    birth_certificate_number: Optional[str] = None
    nationality: Optional[str] = "IDN"

class StudentIdentityResponse(StudentIdentityCreate):
    id: UUID
    student_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Student Address Schemas ---
class StudentAddressCreate(BaseModel):
    street_address: str
    rt: str
    rw: str
    hamlet: Optional[str] = None
    village: str
    district: str
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    residence_type: int
    transportation_mode: int

class StudentAddressResponse(StudentAddressCreate):
    id: UUID
    student_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Student Schemas ---
class StudentCreate(BaseModel):
    user_id: UUID
    nik: str
    nisn: str
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    identity: StudentIdentityCreate
    address: StudentAddressCreate

class StudentResponse(BaseModel):
    id: UUID
    user_id: UUID
    nik: str
    nisn: str
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema dengan relasi lengkap (untuk detail siswa)
class StudentDetailResponse(StudentResponse):
    identity: Optional[StudentIdentityResponse] = None
    address: Optional[StudentAddressResponse] = None

    model_config = ConfigDict(from_attributes=True)