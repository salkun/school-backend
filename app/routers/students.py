from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentDetailResponse
from app.dependencies import require_admin, require_staff
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)

# 1. HANYA ADMIN: Boleh membuat siswa baru
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    # 1. Validasi / Penentuan user_id
    user_id = data.user_id
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found with provided user_id")
    else:
        # Otomatis buat akun user baru untuk siswa jika user_id tidak dikirim
        uname = data.username or data.nisn
        if not uname:
            raise HTTPException(status_code=400, detail="Username, NISN, atau user_id wajib diisi untuk akun siswa")
            
        existing_user = db.query(User).filter(User.username == uname).first()
        if existing_user:
            user_id = existing_user.id
        else:
            hashed_pwd = get_password_hash(data.password or "siswa123")
            new_user = User(
                username=uname,
                email=data.email,
                password=hashed_pwd,
                role="student",
                school_id=data.school_id,
                is_active=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_id = new_user.id

    # 2. Validasi duplikasi NIK / NISN
    existing_student = db.query(Student).filter(
        (Student.nik == data.nik) | (Student.nisn == data.nisn)
    ).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="NIK or NISN is already registered")

    # 3. Pisahkan first_name dan last_name jika belum terisi
    full_name = data.full_name.strip()
    first_name = data.first_name
    last_name = data.last_name
    if not first_name:
        parts = full_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else None

    # 4. Simpan data Student
    new_student = Student(
        user_id=user_id,
        school_id=data.school_id,
        nik=data.nik,
        nisn=data.nisn,
        full_name=full_name,
        first_name=first_name,
        last_name=last_name
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# 2. ADMIN & GURU: Boleh melihat daftar semua siswa
@router.get(
    "/",
    response_model=List[StudentResponse],
    dependencies=[Depends(require_staff)]
)
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).order_by(Student.full_name.asc()).all()


# 3. ADMIN & GURU: Boleh melihat detail biodata siswa
@router.get(
    "/{student_id}",
    response_model=StudentDetailResponse,
    dependencies=[Depends(require_staff)]
)
def get_student_detail(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# 4. HANYA ADMIN: Boleh memperbarui data pokok siswa
@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    dependencies=[Depends(require_admin)]
)
def update_student(student_id: UUID, data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_dict = data.model_dump(exclude_unset=True)

    # Validasi duplikasi NIK jika diubah
    if "nik" in update_dict and update_dict["nik"]:
        dup_nik = db.query(Student).filter(Student.nik == update_dict["nik"], Student.id != student_id).first()
        if dup_nik:
            raise HTTPException(status_code=400, detail="NIK already registered by another student")

    # Validasi duplikasi NISN jika diubah
    if "nisn" in update_dict and update_dict["nisn"]:
        dup_nisn = db.query(Student).filter(Student.nisn == update_dict["nisn"], Student.id != student_id).first()
        if dup_nisn:
            raise HTTPException(status_code=400, detail="NISN already registered by another student")

    # Update nama otomatis
    if "full_name" in update_dict and update_dict["full_name"]:
        fn = update_dict["full_name"].strip()
        student.full_name = fn
        if not update_dict.get("first_name"):
            parts = fn.split(maxsplit=1)
            student.first_name = parts[0]
            student.last_name = parts[1] if len(parts) > 1 else None

    for key, value in update_dict.items():
        if key not in ["full_name"]:
            setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


# 5. HANYA ADMIN: Boleh menghapus data siswa
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None
