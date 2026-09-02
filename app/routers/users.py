from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.dependencies import require_admin
from app.core.security import get_password_hash  

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(require_admin)]  # Semua endpoint di bawah ini otomatis KUNCI KHUSUS ADMIN
)

# ==========================================
# 1. CREATE USER (POST /api/users/)
# ==========================================
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """
    Hanya Admin yang bisa membuat user baru (termasuk mengaitkan school_id).
    """
    # 1. Cek apakah username atau email sudah ada di database
    existing_user = db.query(User).filter(User.username == data.username).first()
    if not existing_user and data.email:
        existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # 2. Hash password sebelum disimpan
    hashed_pwd = get_password_hash(data.password)

    # 3. Simpan ke database (termasuk school_id jika ada)
    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_pwd, 
        role=data.role,
        school_id=getattr(data, "school_id", None),  
        is_active=getattr(data, "is_active", True)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Hanya Admin yang bisa melihat daftar seluruh pengguna sistem.
    """
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_detail(user_id: UUID, db: Session = Depends(get_db)):
    """
    Hanya Admin yang bisa melihat detail akun pengguna tertentu.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)):
    """
    Hanya Admin yang bisa memperbarui data user (termasuk memasukkan school_id / ganti role).
    """
    # 1. Cari user di database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Ambil data yang dikirim saja (exclude yang None / tidak dikirim)
    update_data = data.model_dump(exclude_unset=True)

    # Validasi duplikasi username atau email jika diubah
    if "username" in update_data and update_data["username"]:
        dup_username = db.query(User).filter(User.username == update_data["username"], User.id != user_id).first()
        if dup_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")

    if "email" in update_data and update_data["email"]:
        dup_email = db.query(User).filter(User.email == update_data["email"], User.id != user_id).first()
        if dup_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    # 3. Jika password ikut diganti, hash terlebih dahulu
    if "password" in update_data and update_data["password"]:
        update_data["password"] = get_password_hash(update_data.pop("password"))
    elif "password" in update_data:
        update_data.pop("password")

    # 4. Update kolom yang ada di database
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Hanya Admin yang bisa menghapus akun pengguna.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return None