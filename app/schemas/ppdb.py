from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal


# ==========================================
# 1. AKUN CALON SISWA (PPDB ACCOUNT)
# ==========================================
class PPDBAccountRegister(BaseModel):
    nik: str = Field(..., min_length=16, max_length=16, example="3201012345670001")
    full_name: str = Field(..., max_length=100, example="Ahmad Fauzi Rahman")
    email: EmailStr = Field(..., example="ahmad.fauzi@gmail.com")
    password: str = Field(..., min_length=6, example="Pendaftar123!")


class PPDBAccountResponse(BaseModel):
    id: UUID
    nik: str
    full_name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PPDBLoginRequest(BaseModel):
    # Bisa login menggunakan NIK atau Email
    nik: Optional[str] = Field(None, example="3201012345670001")
    email: Optional[EmailStr] = Field(None, example="ahmad.fauzi@gmail.com")
    password: str = Field(..., example="Pendaftar123!")


class PPDBTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    account_id: UUID
    nik: str
    full_name: str
    email: str


# ==========================================
# 2. SUB-SCHEMA FORMULIR PENDAFTARAN BERSARANG
# (STRUKTUR IDENTIK 100% DENGAN MODUL SIAKAD)
# ==========================================
class PPDBIdentityInput(BaseModel):
    family_card_number: Optional[str] = Field(None, max_length=20, example="3201010000000001")
    gender: str = Field(..., max_length=20, example="Laki-laki")
    religion: str = Field(..., max_length=50, example="Islam")
    place_of_birth: str = Field(..., max_length=50, example="Jakarta")
    date_of_birth: date = Field(..., example="2008-05-14")
    birth_order: Optional[int] = Field(None, ge=1, description="Anak keberapa", example=2)
    siblings_count: Optional[int] = Field(None, ge=0, description="Jumlah saudara", example=3)


class PPDBAddressInput(BaseModel):
    street_address: str = Field(..., example="Jl. Merdeka No. 45")
    rt: str = Field(..., max_length=5, example="002")
    rw: str = Field(..., max_length=5, example="005")
    village: str = Field(..., max_length=100, example="Sukamaju")
    district: str = Field(..., max_length=100, example="Cilodong")
    postal_code: Optional[str] = Field(None, max_length=10, example="16415")
    residence_type: Optional[str] = Field(None, max_length=50, example="Bersama Orang Tua")
    transportation_mode: Optional[str] = Field(None, max_length=100, example="Sepeda Motor")


class PPDBContactInput(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=20, example="021-77889900")
    mobile_number: Optional[str] = Field(None, max_length=20, example="081234567890")
    whatsapp_number: Optional[str] = Field(None, max_length=20, example="081234567890")
    email: Optional[str] = Field(None, max_length=100, example="ahmad.fauzi@student.sch.id")


class PPDBParentDataInput(BaseModel):
    nik: Optional[str] = Field(None, max_length=16, example="3201011122330001")
    full_name: str = Field(..., max_length=100, example="Bambang Sudarsono")
    place_of_birth: Optional[str] = Field(None, max_length=50, example="Semarang")
    birth_year: Optional[str] = Field(None, max_length=4, example="1978")
    education_code: Optional[str] = Field(None, max_length=10, example="05")
    occupation_code: Optional[str] = Field(None, max_length=10, example="02")
    income_code: Optional[str] = Field(None, max_length=10, example="03")
    special_need_code: Optional[str] = Field(None, max_length=10, example="00")
    address: Optional[str] = Field(None, example="Jl. Merdeka No. 45")
    phone_number: Optional[str] = Field(None, max_length=20, example="081311223344")
    whatsapp_number: Optional[str] = Field(None, max_length=20, example="081311223344")
    email: Optional[str] = Field(None, max_length=100, example="bambang.sudarsono@example.com")


class PPDBParentRelationInput(BaseModel):
    relationship_type: int = Field(..., ge=1, le=3, description="1=Ayah, 2=Ibu, 3=Wali", example=1)
    parent: PPDBParentDataInput


# Schema Formulir Utama (Format Utuh Sesuai Spesifikasi)
class PPDBRegistrationFormInput(BaseModel):
    nik: str = Field(..., min_length=16, max_length=16, example="3201012345670001")
    nisn: str = Field(..., min_length=5, max_length=20, example="0051234567")
    full_name: str = Field(..., max_length=100, example="Ahmad Fauzi Rahman")
    first_name: Optional[str] = Field(None, max_length=50, example="Ahmad")
    last_name: Optional[str] = Field(None, max_length=50, example="Fauzi Rahman")
    
    # Data Asal Sekolah & Peminatan Jurusan
    school_origin: Optional[str] = Field(None, max_length=150, example="SMP Negeri 1 Jakarta")
    school_origin_address: Optional[str] = Field(None, max_length=500, example="Jl. Pendidikan No. 45")
    major: Optional[str] = Field(None, max_length=50, example="reguler")
    
    identity: Optional[PPDBIdentityInput] = None
    address: Optional[PPDBAddressInput] = None
    contact: Optional[PPDBContactInput] = None
    student_parents: List[PPDBParentRelationInput] = []


# ==========================================
# 3. RESPONS REGISTRASI & VERIFIKASI ADMIN
# ==========================================
class PPDBRegistrationResponse(BaseModel):
    id: UUID
    account_id: UUID
    payment_status: str
    payment_amount: Decimal
    payment_proof_path: Optional[str] = None
    payment_verified_at: Optional[datetime] = None
    payment_verified_by: Optional[UUID] = None
    registration_status: str
    form_data: Optional[Dict[str, Any]] = None
    student_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    account: Optional[PPDBAccountResponse] = None

    model_config = ConfigDict(from_attributes=True)


class PPDBPaymentVerifyRequest(BaseModel):
    payment_status: str = Field("paid", example="paid")  # "paid" / "rejected"
    payment_amount: Optional[Decimal] = Field(None, example=250000.00)


class PPDBAcceptResponse(BaseModel):
    message: str
    registration_id: UUID
    student_id: UUID
    user_id: UUID
    username: str
    full_name: str
    role: str
    migrated_at: datetime


class PPDBAdminUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    nik: Optional[str] = None
    email: Optional[EmailStr] = None
    payment_status: Optional[str] = None
    payment_amount: Optional[Decimal] = None
    registration_status: Optional[str] = None
    form_data: Optional[Dict[str, Any]] = None
