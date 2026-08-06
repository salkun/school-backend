from fastapi import APIRouter, FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import engine, Base, get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.routers import students, auth  # <--- PASTIKAN AUTH ADA DI SINI
from app.core.security import get_password_hash

# Generate tabel otomatis ke database PostgreSQL di Laragon
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Master Data API",
    description="Backend API untuk Sistem Master Data Sekolah (FastAPI + PostgreSQL)",
    version="1.0.0"
)

# Daftarkan Semua Router
app.include_router(auth.router)      # <--- PASTIKAN BARIS INI ADA
app.include_router(students.router)


# ==========================================
# --- Endpoints untuk Users (Helper CRUD) ---
# ==========================================

@app.post("/api/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users (Helper)"])
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    # Hash password sebelum disimpan ke DB
    hashed_pwd = get_password_hash(data.password)
    
    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_pwd,
        role=data.role,
        is_active=data.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/api/users/", response_model=List[UserResponse], tags=["Users (Helper)"])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users (Helper)"])
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to School Master Data API",
        "docs_url": "http://127.0.0.1:8000/docs"
    }