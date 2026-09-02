from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    role: Optional[str] = "student"
    school_id: Optional[UUID] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: Optional[str] = None  
    role: str
    school_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    school_id: Optional[UUID] = None 
    password: Optional[str] = None