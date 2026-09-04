from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID


# ==========================================================
# 1. STUDENT IDENTITY SCHEMAS
# ==========================================================
class StudentIdentityCreate(BaseModel):
    family_card_number: Optional[str] = Field(None, max_length=16)
    gender: str = Field(..., max_length=10)
    religion: str = Field(..., max_length=30)
    place_of_birth: str = Field(..., max_length=50)
    date_of_birth: date


class StudentIdentityResponse(StudentIdentityCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# 2. STUDENT ADDRESS SCHEMAS
# ==========================================================
class StudentAddressCreate(BaseModel):
    street_address: str
    rt: str = Field(..., max_length=5)
    rw: str = Field(..., max_length=5)
    village: str = Field(..., max_length=50)
    district: str = Field(..., max_length=50)
    postal_code: Optional[str] = Field(None, max_length=10)
    residence_type: Optional[str] = Field(None, max_length=50)
    transportation_mode: Optional[str] = None


class StudentAddressResponse(StudentAddressCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# ==========================================================
# 3. STUDENT CONTACT SCHEMAS
# ==========================================================
class StudentContactCreate(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=20)
    mobile_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)


class StudentContactResponse(StudentContactCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# ==========================================================
# 4. PARENT / ORANG TUA SCHEMAS
# ==========================================================
class ParentBase(BaseModel):
    nik: Optional[str] = Field(None, max_length=16)
    full_name: str = Field(..., max_length=100)
    place_of_birth: Optional[str] = Field(None, max_length=50)
    birth_year: Optional[str] = Field(None, max_length=4)
    education_code: Optional[str] = None
    occupation_code: Optional[str] = None
    income_code: Optional[str] = None
    special_need_code: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)


class ParentCreate(ParentBase):
    pass


class ParentResponse(ParentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StudentParentInput(ParentCreate):
    relationship_type: int = Field(..., ge=1, le=3, description="1: Ayah, 2: Ibu, 3: Wali")


class StudentParentDetailResponse(BaseModel):
    relationship_type: int
    parent: ParentResponse
    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# 5. STUDENT MAIN SCHEMAS (BERSIH & TERPISAH)
# ==========================================================
class StudentCreate(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    school_id: Optional[UUID] = None
    nik: str = Field(..., min_length=16, max_length=16)
    nisn: str = Field(..., min_length=5, max_length=20)
    full_name: str = Field(..., max_length=100)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class StudentUpdate(BaseModel):
    user_id: Optional[UUID] = None
    school_id: Optional[UUID] = None
    nik: Optional[str] = Field(None, min_length=16, max_length=16)
    nisn: Optional[str] = Field(None, min_length=5, max_length=20)
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class StudentResponse(BaseModel):
    id: UUID
    user_id: UUID
    school_id: Optional[UUID] = None
    nik: str
    nisn: str
    full_name: str
    first_name: str
    last_name: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# Dipakai saat GET /api/students/{student_id} untuk menampilkan relasi lengkap
class StudentDetailResponse(StudentResponse):
    identity: Optional[StudentIdentityResponse] = None
    address: Optional[StudentAddressResponse] = None
    contact: Optional[StudentContactResponse] = None
    student_parents: List[StudentParentDetailResponse] = []
    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# 6. STUDENT ENROLLMENT (Riwayat Kelas)
# ==========================================================
class StudentEnrollmentCreate(BaseModel):
    student_id: UUID
    classroom_id: UUID
    academic_year_id: UUID
    semester_id: UUID
    status: str = Field("Active", max_length=50)

class StudentEnrollmentResponse(StudentEnrollmentCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
