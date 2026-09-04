from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Optional[str] = None
    roles: Optional[List[str]] = []

class TokenData(BaseModel):
    username: Optional[str] = None