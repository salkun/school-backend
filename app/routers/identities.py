from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.student import Student, StudentIdentity
from app.schemas.student import StudentIdentityCreate, StudentIdentityResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/identities",
    tags=["Student Identities"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/{student_id}", response_model=StudentIdentityResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_identity(student_id: UUID, data: StudentIdentityCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_identity = db.query(StudentIdentity).filter(StudentIdentity.student_id == student_id).first()
    if existing_identity:
        for key, value in data.model_dump().items():
            setattr(existing_identity, key, value)
        db.commit()
        db.refresh(existing_identity)
        return existing_identity

    new_identity = StudentIdentity(student_id=student_id, **data.model_dump())
    db.add(new_identity)
    db.commit()
    db.refresh(new_identity)
    return new_identity

@router.get("/{student_id}", response_model=StudentIdentityResponse)
def get_identity(student_id: UUID, db: Session = Depends(get_db)):
    identity = db.query(StudentIdentity).filter(StudentIdentity.student_id == student_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found for this student")
    return identity