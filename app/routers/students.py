from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse, StudentDetailResponse
from app.dependencies import require_admin, require_staff  # <-- Satpam RBAC di-import

router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)

# 1. HANYA ADMIN: Boleh membuat siswa baru
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]  # <-- Pasang satpam admin
)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    # 1. Validasi user_id
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 2. Validasi duplikasi NIK / NISN
    existing_student = db.query(Student).filter(
        (Student.nik == data.nik) | (Student.nisn == data.nisn)
    ).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="NIK or NISN is already registered")

    # 3. Simpan data Student saja
    new_student = Student(**data.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# 2. ADMIN & GURU: Boleh melihat daftar semua siswa
@router.get(
    "/",
    response_model=List[StudentResponse],
    dependencies=[Depends(require_staff)]  # <-- Pasang satpam staff (admin & teacher)
)
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# 3. ADMIN & GURU: Boleh melihat detail biodata siswa
@router.get(
    "/{student_id}",
    response_model=StudentDetailResponse,
    dependencies=[Depends(require_staff)]  # <-- Pasang satpam staff (admin & teacher)
)
def get_student_detail(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# 4. HANYA ADMIN: Boleh menghapus data siswa
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]  # <-- Pasang satpam admin
)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None