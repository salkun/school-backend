from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# 1. Schema for Create / Update Request
class SchoolIdentityCreate(BaseModel):
    name: str = Field(..., max_length=100, example="SMK Negeri 1 Purwakarta")
    npsn: str = Field(..., max_length=10, example="20211111")
    address: str = Field(..., example="Jl. Veteran No. 10, Purwakarta")

# 2. Schema for Response
class SchoolIdentityResponse(SchoolIdentityCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)