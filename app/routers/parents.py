from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.student import Student
from app.models.parent import Parent, StudentParentRelation
from app.schemas.parent import ParentCreateWithRelation, StudentParentRelationResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/parents",
    tags=["Student Parents"]
)


# =========================================================================
# 1. TAMBAH ORANG TUA / WALI UNTUK SISWA (Khusus Admin)
# =========================================================================
@router.post(
    "/{student_id}",
    response_model=StudentParentRelationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
def add_parent_to_student(
    student_id: UUID,
    data: ParentCreateWithRelation,
    db: Session = Depends(get_db)
):
    # 1. Pastikan siswa ada
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Pisahkan data relationship_type dari biodata parent
    parent_data = data.model_dump()
    rel_type = parent_data.pop("relationship_type")

    # 3. Cek apakah parent dengan NIK ini sudah ada di database (misal orang tua dari kakak/adik)
    parent_obj = None
    if parent_data.get("nik"):
        parent_obj = db.query(Parent).filter(Parent.nik == parent_data["nik"]).first()

    if parent_obj:
        # Cek apakah relasi sudah ada untuk siswa ini
        existing_rel = db.query(StudentParentRelation).filter(
            StudentParentRelation.student_id == student_id,
            StudentParentRelation.parent_id == parent_obj.id
        ).first()
        if existing_rel:
            raise HTTPException(status_code=400, detail="Parent relation already exists for this student")
        # Update biodata jika ada perubahan
        for k, v in parent_data.items():
            if v is not None:
                setattr(parent_obj, k, v)
    else:
        parent_obj = Parent(**parent_data)
        db.add(parent_obj)
        db.flush()  # flush agar parent_obj.id langsung tersedia

    # 4. Simpan ke tabel pivot 'student_parent_relations'
    new_relation = StudentParentRelation(
        student_id=student_id,
        parent_id=parent_obj.id,
        relationship_type=rel_type
    )
    db.add(new_relation)
    
    # 5. Commit sekaligus untuk kedua tabel
    db.commit()
    db.refresh(new_relation)
    
    return new_relation


# =========================================================================
# 2. LIHAT SEMUA ORANG TUA / WALI DARI SISWA TERTENTU (Admin & Guru)
# =========================================================================
@router.get(
    "/{student_id}",
    response_model=List[StudentParentRelationResponse],
    dependencies=[Depends(require_staff)]
)
def get_student_parents(student_id: UUID, db: Session = Depends(get_db)):
    # Ambil semua relasi milik siswa, sekaligus load data parent-nya
    relations = (
        db.query(StudentParentRelation)
        .options(joinedload(StudentParentRelation.parent))
        .filter(StudentParentRelation.student_id == student_id)
        .all()
    )
    return relations


# =========================================================================
# 3. HAPUS RELASI ORANG TUA DARI SISWA (Khusus Admin)
# =========================================================================
@router.delete(
    "/relation/{relation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
def delete_parent_relation(relation_id: UUID, db: Session = Depends(get_db)):
    relation = db.query(StudentParentRelation).filter(StudentParentRelation.id == relation_id).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
        
    db.delete(relation)
    db.commit()
    return None