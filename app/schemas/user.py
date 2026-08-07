from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "student"
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: Optional[str] = None  # <--- UBAH JADI OPTIONAL AGAR TIDAK ERROR JIKA KOSONG / NULL
    role: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)