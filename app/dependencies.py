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

def resolve_user_roles(user: User, db: Session) -> List[str]:
    """
    Menyelesaikan seluruh role pengguna secara dinamis:
    1. Siswa / Orang Tua -> Murni ['student'] atau ['parent'] tanpa perlu position
    2. Admin -> ['admin', 'staff', 'teacher', 'employee'] (Hak akses superuser)
    3. Pegawai / Guru -> ['employee', 'staff', <user.role>] + semua active position code
    """
    roles = set()
    
    # 1. Base role
    if user.role:
        roles.add(user.role.lower())

    # 2. Siswa / Orang Tua: tidak terpengaruh oleh tabel position
    if user.role in [UserRole.STUDENT.value, UserRole.PARENT.value]:
        return list(roles)

    # 3. Admin: Superuser otomatis memiliki hak akses staff & employee
    if user.role == UserRole.ADMIN.value:
        roles.update(["admin", "staff", "teacher", "employee"])
        return list(roles)

    # 4. Pegawai: Tambahkan role umum pegawai
    roles.update(["employee", "staff"])

    # 5. Ambil jabatan aktif dari tabel employee_positions
    if user.employee:
        from app.models.employee import EmployeePosition
        from app.models.master import Position, HomeroomAssignment

        active_positions = (
            db.query(Position)
            .join(EmployeePosition, EmployeePosition.position_id == Position.id)
            .filter(
                EmployeePosition.employee_id == user.employee.id,
                EmployeePosition.is_active == True
            )
            .all()
        )
        for pos in active_positions:
            if pos.code:
                roles.add(pos.code.lower())
            if pos.name:
                roles.add(pos.name.lower().replace(" ", "_"))

        # Cek apakah terdaftar sebagai wali kelas aktif
        has_homeroom = db.query(HomeroomAssignment).filter(
            HomeroomAssignment.employee_id == user.employee.id
        ).first()
        if has_homeroom:
            roles.update(["homeroom_teacher", "wali_kelas"])

        # Cek ptk_type jika guru
        if user.employee.ptk_type and "guru" in user.employee.ptk_type.lower():
            roles.add("teacher")

    return list(roles)


# ==========================================================
# SATPAM RBAC (ROLE-BASED ACCESS CONTROL)
# ==========================================================
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = [r.lower() for r in allowed_roles]

    def __call__(self, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        user_roles = resolve_user_roles(current_user, db)
        # Izinkan jika salah satu role user cocok dengan allowed_roles
        if not any(role in self.allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak. Endpoint ini hanya untuk role: {', '.join(self.allowed_roles)}"
            )
        return current_user


# --- SATPAM INSTAN YANG SIAP PAKAI DI SEMUA ROUTER ---
# 1. Khusus Admin
require_admin = RoleChecker([UserRole.ADMIN.value])

# 2. Staff (Admin, Pegawai, Guru, TU, Wakasek, dll)
require_staff = RoleChecker([
    UserRole.ADMIN.value, 
    UserRole.TEACHER.value, 
    UserRole.EMPLOYEE.value, 
    UserRole.STAFF.value,
    "staff", 
    "teacher", 
    "employee"
])

# 3. Khusus Guru
require_teacher = RoleChecker([UserRole.ADMIN.value, UserRole.TEACHER.value, "teacher"])

# 4. Semua Pengguna Login (Admin, Pegawai, Guru, Siswa, Orang Tua)
require_all = RoleChecker([
    UserRole.ADMIN.value, 
    UserRole.TEACHER.value, 
    UserRole.EMPLOYEE.value, 
    UserRole.STAFF.value,
    UserRole.STUDENT.value, 
    UserRole.PARENT.value,
    "admin", "teacher", "student", "parent", "employee", "staff"
])