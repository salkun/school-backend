from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.student import Student, StudentIdentity, StudentAddress
from app.schemas.student import StudentCreate, StudentResponse, StudentDetailResponse
from app.dependencies import get_current_user  # <--- 1. IMPORT DEPENDENCY SATPAM

# 2. PASANG DEPENDENCY DI LEVEL ROUTER (Otomatis mengunci semua endpoint di file ini!)
router = APIRouter(
    prefix="/api/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)]  # <--- SEMUA ENDPOINT DI SINI WAJIB TOKEN
)


# --- Semua fungsi di bawah ini sekarang OTOMATIS TERKUNCI ---

@router.post("/", response_model=StudentDetailResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    # 1. Validasi apakah user_id ada di tabel users
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 2. Validasi duplikasi NIK atau NISN
    existing_student = db.query(Student).filter(
        (Student.nik == data.nik) | (Student.nisn == data.nisn)
    ).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="NIK or NISN is already registered")

    # 3. Simpan data Student utama
    new_student = Student(
        user_id=data.user_id,
        nik=data.nik,
        nisn=data.nisn,
        full_name=data.full_name,
        first_name=data.first_name,
        last_name=data.last_name
    )
    db.add(new_student)
    db.flush()

    # 4. Simpan data Identity siswa
    new_identity = StudentIdentity(
        student_id=new_student.id,
        **data.identity.model_dump()
    )
    db.add(new_identity)

    # 5. Simpan data Address siswa
    new_address = StudentAddress(
        student_id=new_student.id,
        **data.address.model_dump()
    )
    db.add(new_address)

    # 6. Commit transaksi ke PostgreSQL
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentDetailResponse)
def get_student_detail(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return None