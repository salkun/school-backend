from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse  # Sesuaikan dengan nama schema user kamu
from app.dependencies import require_admin  # <--- IMPORT SATPAM ADMIN

# PASANG DI SINI: Semua endpoint di bawah router ini OTOMATIS HANYA BISA DIAKSES ADMIN!
router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(require_admin)]  # <--- KUNCI TOTAL KHUSUS ADMIN
)


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