from fastapi import Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.database import get_db
from app.config import settings
from app.models.user import User, UserRole
from app.schemas.auth import TokenData

# Memberitahu FastAPI bahwa endpoint login ada di /api/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode token JWT menggunakan SECRET_KEY
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    # Ambil user dari database
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user

# ==========================================================
# SATPAM RBAC (ROLE-BASED ACCESS CONTROL)
# ==========================================================
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak. Endpoint ini hanya untuk role: {', '.join(self.allowed_roles)}"
            )
        return current_user


# --- 3 SATPAM INSTAN YANG SIAP PAKAI DI SEMUA ROUTER ---
# 1. Khusus Admin (Untuk Create, Update, Delete data master)
require_admin = RoleChecker([UserRole.ADMIN.value])

# 2. Staff (Admin & Guru -> Untuk melihat data siswa / input nilai)
require_staff = RoleChecker([UserRole.ADMIN.value, UserRole.TEACHER.value])

# 3. Semua Pengguna Login (Admin, Guru, dan Siswa)
require_all = RoleChecker([UserRole.ADMIN.value, UserRole.TEACHER.value, UserRole.STUDENT.value])