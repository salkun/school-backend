from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# --- 1. Schema Input Biodata Orang Tua + Tipe Relasi ---
class ParentCreateWithRelation(BaseModel):
    # Kolom relasi ke siswa
    relationship_type: int = Field(..., description="1=Ayah, 2=Ibu, 3=Wali")
    
    # Kolom biodata parent
    nik: Optional[str] = Field(None, max_length=16)
    full_name: str = Field(..., max_length=100)
    place_of_birth: Optional[str] = Field(None, max_length=50)
    birth_year: Optional[str] = Field(None, max_length=4)
    education_code: Optional[str] = Field(None, max_length=2)
    occupation_code: Optional[str] = Field(None, max_length=2)
    income_code: Optional[str] = Field(None, max_length=2)
    special_need_code: Optional[str] = Field(None, max_length=2)
    address: Optional[str] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)


# --- 2. Schema Murni Parent (Untuk Response) ---
class ParentResponse(BaseModel):
    id: UUID
    nik: Optional[str] = None
    full_name: str
    place_of_birth: Optional[str] = None
    birth_year: Optional[str] = None
    education_code: Optional[str] = None
    occupation_code: Optional[str] = None
    income_code: Optional[str] = None
    special_need_code: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- 3. Schema Relasi Lengkap (Parent + Tipe Relasi) ---
class StudentParentRelationResponse(BaseModel):
    id: UUID
    student_id: UUID
    parent_id: UUID
    relationship_type: int
    created_at: datetime
    
    # Menampilkan detail orang tua di dalam relasi
    parent: ParentResponse

    model_config = ConfigDict(from_attributes=True)